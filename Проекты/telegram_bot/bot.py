import asyncio
import sqlite3
import os
import json
import random
import csv
import io
import re
import base64
import tempfile
import urllib.request
from datetime import datetime
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from dotenv import load_dotenv
from openai import OpenAI
import anthropic

# Загружаем переменные окружения
load_dotenv()

# ============================================
# НАСТРОЙКИ
# ============================================

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
# Прямой доступ к api.telegram.org с Pi5 часто таймаутится — HTTP-прокси xray (10809→10808)
TELEGRAM_PROXY = (
    os.getenv("TELEGRAM_PROXY")
    or os.getenv("HTTPS_PROXY")
    or os.getenv("HTTP_PROXY")
    or "http://127.0.0.1:10809"
).strip()

if not TOKEN:
    print("❌ ОШИБКА: BOT_TOKEN не найден в файле .env")
    exit(1)

if not DEEPSEEK_API_KEY:
    print("⚠️ ПРЕДУПРЕЖДЕНИЕ: DEEPSEEK_API_KEY не найден, бот будет работать в режиме локальной базы знаний")

# Папка для логов
LOGS_DIR = "user_logs"
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

# Папка для экспортов
EXPORTS_DIR = "exports"
if not os.path.exists(EXPORTS_DIR):
    os.makedirs(EXPORTS_DIR)

# Файл с базой знаний ответов (резерв)
KNOWLEDGE_FILE = "knowledge_base.json"

# Файл со списком ID для рассылки
BROADCAST_IDS_FILE = "broadcast_ids.txt"

# Файл с system_prompt для DeepSeek
SYSTEM_PROMPT_FILE = "system_prompt.txt"

# Файлы инструкций и сервиса для отправки пользователю
SERVICE_DOC_FILES = [
    "knowledge/service/diligence_service_book_2026.pdf",
    "knowledge/service/yak_service_book.pdf",
    "knowledge/service/yak_washer_service_book.pdf",
]

INSTRUCTION_DOC_FILES = {
    "Як": "knowledge/instructions/yak_manual_2025.pdf",
    "Дилижанс": "knowledge/instructions/diligence_manual_2025.pdf",
    "Поливомоечная машина": "knowledge/instructions/washer_operation_manual.pdf",
}

SHEET_CSV_URL = (
    "https://docs.google.com/spreadsheets/d/"
    "1c9__Xbrq8RAfEjphu-Sb4iS3WnHMLDYc4SIcVhVqNzU/export?format=csv&gid=0"
)
MAINTENANCE_SHEET_CSV_URL = (
    "https://docs.google.com/spreadsheets/d/"
    "1II4KEQZHzkfzabq9wgCuIOyVaOhl-9nNgUYLQky328s/export?format=csv&gid=1469311667"
)

# Файл для постоянного экспорта пользователей
USERS_EXPORT_FILE = os.path.join(EXPORTS_DIR, "users_export.csv")

# Состояния для ConversationHandler
PHONE_REQUEST = 1

# Создаём файл broadcast_ids.txt если его нет
if not os.path.exists(BROADCAST_IDS_FILE):
    with open(BROADCAST_IDS_FILE, "w", encoding="utf-8") as f:
        f.write("")
    print(f"✅ Создан файл {BROADCAST_IDS_FILE}")

# Настройка DeepSeek клиента
if DEEPSEEK_API_KEY:
    client = OpenAI(
        api_key=DEEPSEEK_API_KEY,
        base_url="https://api.deepseek.com/v1"
    )
    AI_MODE = "deepseek"
    print("✅ DeepSeek AI подключен")
else:
    AI_MODE = "local"
    print("✅ Режим локальной базы знаний")

# Настройка Anthropic клиента для распознавания изображений
def _load_anthropic_token() -> str:
    creds_path = os.path.expanduser("~/.claude/.credentials.json")
    try:
        with open(creds_path) as f:
            return json.load(f)["claudeAiOauth"]["accessToken"]
    except Exception:
        return os.getenv("ANTHROPIC_API_KEY", "")

_anthropic_token = _load_anthropic_token()
anthropic_client = anthropic.Anthropic(api_key=_anthropic_token) if _anthropic_token else None
if anthropic_client:
    print("✅ Anthropic Vision подключен")
else:
    print("⚠️ Anthropic Vision недоступен (нет токена)")

# ============================================
# ЗАГРУЗКА SYSTEM_PROMPT ИЗ ФАЙЛА
# ============================================

def load_system_prompt():
    """Загружает system_prompt из файла system_prompt.txt"""
    if os.path.exists(SYSTEM_PROMPT_FILE):
        with open(SYSTEM_PROMPT_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    else:
        default_prompt = """Ты — официальный AI-консультант компании ЭЛЬТАВР, российского производителя коммерческого электротранспорта.

Твоя задача — не просто отвечать на вопросы, а помогать клиенту подобрать решение под конкретную задачу.

Правила ответов:
- Отвечай вежливо, полезно и по делу
- Будь краток и конкретен (2-3 предложения)
- Используй эмодзи где уместно
- Отвечай на том же языке, что и пользователь

Будь полезным помощником компании ЭЛЬТАВР!"""
        
        with open(SYSTEM_PROMPT_FILE, "w", encoding="utf-8") as f:
            f.write(default_prompt)
        print(f"✅ Создан файл {SYSTEM_PROMPT_FILE}")
        return default_prompt

SYSTEM_PROMPT = load_system_prompt()
print(f"📝 Загружен system_prompt из {SYSTEM_PROMPT_FILE}")

# ============================================
# АВТОМАТИЧЕСКОЕ ДОБАВЛЕНИЕ ID
# ============================================

def sync_ids_from_logs():
    """Синхронизирует ID из папки user_logs с файлом broadcast_ids.txt"""
    log_ids = set()
    if os.path.exists(LOGS_DIR):
        for filename in os.listdir(LOGS_DIR):
            if filename.endswith('.txt'):
                try:
                    user_id = int(filename.replace('.txt', ''))
                    log_ids.add(user_id)
                except ValueError:
                    pass
    
    current_ids = set(load_broadcast_ids())
    new_ids = log_ids - current_ids
    
    if new_ids:
        all_ids = list(current_ids | log_ids)
        save_broadcast_ids(all_ids)
        print(f"🆕 Добавлены новые ID: {len(new_ids)} шт.")
        return True, new_ids
    return False, set()

# ============================================
# РАБОТА СО СПИСКОМ ID
# ============================================

def load_broadcast_ids():
    """Загружает список ID из файла для рассылки"""
    if os.path.exists(BROADCAST_IDS_FILE):
        with open(BROADCAST_IDS_FILE, "r", encoding="utf-8") as f:
            ids = [line.strip() for line in f if line.strip()]
            return [int(id_str) for id_str in ids if id_str.isdigit()]
    return []

def save_broadcast_ids(ids_list):
    """Сохраняет список ID в файл"""
    with open(BROADCAST_IDS_FILE, "w", encoding="utf-8") as f:
        for user_id in ids_list:
            f.write(f"{user_id}\n")

def add_broadcast_id(user_id):
    """Добавляет ID в список для рассылки"""
    ids = load_broadcast_ids()
    if user_id not in ids:
        ids.append(user_id)
        save_broadcast_ids(ids)
        return True
    return False

def remove_broadcast_id(user_id):
    """Удаляет ID из списка для рассылки"""
    ids = load_broadcast_ids()
    if user_id in ids:
        ids.remove(user_id)
        save_broadcast_ids(ids)
        return True
    return False

def get_broadcast_stats():
    """Получает статистику по списку рассылки"""
    ids = load_broadcast_ids()
    return len(ids), ids

# ============================================
# ЭКСПОРТ ПОЛЬЗОВАТЕЛЕЙ В CSV
# ============================================

def export_users_to_csv():
    """Экспортирует всех пользователей в CSV файл на сервере"""
    cursor.execute("SELECT user_id, username, first_name, last_name, phone, email, registered_at FROM users")
    users = cursor.fetchall()
    
    if not users:
        return False, 0
    
    try:
        with open(USERS_EXPORT_FILE, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(["ID", "Username", "Имя", "Фамилия", "Телефон", "Email", "Дата регистрации"])
            for user in users:
                writer.writerow([
                    user[0],
                    user[1] or "",
                    user[2] or "",
                    user[3] or "",
                    user[4] or "",
                    user[5] or "",
                    user[6] or ""
                ])
        
        print(f"✅ Экспорт сохранён на сервере: {USERS_EXPORT_FILE} ({len(users)} пользователей)")
        return True, len(users)
    except Exception as e:
        print(f"❌ Ошибка сохранения экспорта: {e}")
        return False, 0

# ============================================
# ЛОКАЛЬНАЯ БАЗА ЗНАНИЙ (РЕЗЕРВ)
# ============================================

def load_knowledge_base():
    """Загружает базу знаний из файла knowledge_base.json"""
    if os.path.exists(KNOWLEDGE_FILE):
        with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        default_kb = {
            "responses": [
                {
                    "keywords": ["компания", "о вас", "кто вы", "эльтавр"],
                    "response": "🏢 ЭЛЬТАВР - производитель коммерческого электротранспорта. Основана в 2014 году в Симферополе."
                },
                {
                    "keywords": ["мощность", "характеристики"],
                    "response": "⚡ Технические характеристики уточняйте на сайте eltavr.ru"
                },
                {
                    "keywords": ["цена", "стоимость"],
                    "response": "💰 Стоимость зависит от комплектации. Оставьте заявку на сайте eltavr.ru"
                }
            ],
            "default_response": "📝 Уточните вопрос на сайте eltavr.ru",
            "fallback_responses": ["🤔 Не совсем понял. Уточните вопрос."]
        }
        with open(KNOWLEDGE_FILE, "w", encoding="utf-8") as f:
            json.dump(default_kb, f, ensure_ascii=False, indent=2)
        print("✅ Создан файл knowledge_base.json")
        return default_kb

def get_local_response(user_message):
    """Находит ответ в локальной базе знаний"""
    kb = load_knowledge_base()
    user_msg = user_message.lower()
    
    for rule in kb.get("responses", []):
        for keyword in rule.get("keywords", []):
            if keyword.lower() in user_msg:
                return rule.get("response")
    
    fallbacks = kb.get("fallback_responses", [])
    return random.choice(fallbacks) if fallbacks else kb.get("default_response")

# ============================================
# ПОЛУЧЕНИЕ КОНТЕКСТА ИЗ ИСТОРИИ ДИАЛОГА
# ============================================

def get_chat_context(user_id: int, last_n: int = 20, max_chars: int = 6000) -> str:
    """Получает расширенный контекст переписки пользователя из лога."""
    log_file = os.path.join(LOGS_DIR, f"{user_id}.txt")
    
    if not os.path.exists(log_file):
        return ""
    
    try:
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        recent = lines[-last_n * 2:] if len(lines) > last_n * 2 else lines

        entries = []
        for line in recent:
            if "👤" in line:
                parts = line.split(":", 2)
                if len(parts) >= 3:
                    entries.append(f"👤 Пользователь: {parts[2].strip()}")
            elif "🤖" in line and "РАССЫЛКА" not in line:
                parts = line.split(":", 2)
                if len(parts) >= 3:
                    entries.append(f"🤖 Бот: {parts[2].strip()}")

        if not entries:
            return ""

        # Ограничиваем размер, но стараемся сохранить как можно больше последних реплик.
        selected = []
        current_len = 0
        for item in reversed(entries):
            item_len = len(item) + 1
            if current_len + item_len > max_chars:
                break
            selected.append(item)
            current_len += item_len

        selected.reverse()
        context = "📜 История диалога:\n" + "\n".join(selected)
        return context + "\n---\n"
    except Exception as e:
        print(f"Ошибка чтения истории: {e}")
        return ""


def should_include_history(user_message: str) -> bool:
    """
    Подключаем историю только по явному запросу пользователя,
    чтобы не расходовать лишние токены в обычном диалоге.
    """
    text = (user_message or "").lower()
    triggers = (
        "перечитай историю",
        "прочитай историю",
        "прочитай выше",
        "посмотри выше",
        "подними историю",
        "что я писал выше",
    )
    return any(trigger in text for trigger in triggers)

# ============================================
# AI ФУНКЦИЯ DEEPSEEK
# ============================================

async def get_ai_response(user_message: str, user_id: int, username: str = None) -> str:
    """Получает ответ от DeepSeek AI с учётом истории диалога"""
    
    if AI_MODE != "deepseek":
        return get_local_response(user_message)
    
    try:
        current_system_prompt = load_system_prompt()
        
        chat_history = ""
        if should_include_history(user_message):
            chat_history = get_chat_context(user_id, last_n=20, max_chars=6000)

        if chat_history:
            full_prompt = f"{chat_history}\n👉 Текущий вопрос пользователя: {user_message}"
            print(f"📜 История диалога для {user_id} передана в AI")
        else:
            full_prompt = user_message
        
        # Модели DeepSeek
        models_to_try = [
            "deepseek-chat",
            "deepseek-coder",
        ]
        
        last_error = None
        
        for model_name in models_to_try:
            try:
                print(f"🔄 Пробуем модель DeepSeek: {model_name}")
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": current_system_prompt},
                        {"role": "user", "content": full_prompt}
                    ],
                    temperature=0.7,
                    max_tokens=500
                )
                print(f"✅ Успешно с моделью: {model_name}")
                return response.choices[0].message.content
            except Exception as e:
                last_error = e
                print(f"❌ Модель {model_name} не работает: {e}")
                continue
        
        print(f"❌ Все модели DeepSeek недоступны: {last_error}")
        return get_local_response(user_message)
        
    except Exception as e:
        print(f"❌ Ошибка DeepSeek: {e}")
        return get_local_response(user_message)

# ============================================
# БАЗА ДАННЫХ ПОЛЬЗОВАТЕЛЕЙ
# ============================================

def init_db():
    """Инициализирует базу данных"""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            phone TEXT,
            email TEXT,
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("PRAGMA table_info(users)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'last_name' not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN last_name TEXT")
    if 'phone' not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN phone TEXT")
    if 'email' not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN email TEXT")
    
    conn.commit()
    return conn, cursor

db, cursor = init_db()

# При запуске создаём начальный экспорт
export_users_to_csv()

# ============================================
# ЛОГИРОВАНИЕ ПЕРЕПИСКИ
# ============================================

def log_message(user_id, direction, text, username=None):
    """Сохраняет сообщение в файл пользователя"""
    filename = os.path.join(LOGS_DIR, f"{user_id}.txt")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if direction == "USER":
        log_entry = f"[{timestamp}] 👤 {username or 'user'}: {text}\n"
    else:
        log_entry = f"[{timestamp}] 🤖 БОТ: {text}\n"
    
    with open(filename, "a", encoding="utf-8") as f:
        f.write(log_entry)
    
    if direction == "USER":
        if add_broadcast_id(user_id):
            print(f"🆕 Добавлен ID {user_id} в список рассылки")

def is_admin(user_id):
    return user_id == ADMIN_ID

# ============================================
# ФУНКЦИИ ДЛЯ РАБОТЫ С ТЕЛЕФОНОМ
# ============================================

async def request_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запрашивает номер телефона у пользователя"""
    user_id = update.effective_user.id
    
    cursor.execute("SELECT phone FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    
    if result and result[0]:
        await update.message.reply_text("✅ Ваш номер телефона уже сохранён в системе.")
        return ConversationHandler.END
    
    button = KeyboardButton("📱 Отправить номер телефона", request_contact=True)
    reply_markup = ReplyKeyboardMarkup([[button]], resize_keyboard=True, one_time_keyboard=True)
    
    await update.message.reply_text(
        "📞 Для более качественной поддержки, пожалуйста, поделитесь своим номером телефона.\n\n"
        "Это поможет нашему менеджеру связаться с вами при необходимости.\n\n"
        "Нажмите на кнопку ниже:",
        reply_markup=reply_markup
    )
    return PHONE_REQUEST

async def save_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Сохраняет номер телефона пользователя"""
    contact = update.message.contact
    user_id = update.effective_user.id
    
    if contact and contact.user_id == user_id:
        phone = contact.phone_number
        
        cursor.execute(
            "UPDATE users SET phone = ? WHERE user_id = ?",
            (phone, user_id)
        )
        db.commit()
        
        export_users_to_csv()
        
        reply_markup = ReplyKeyboardRemove()
        
        await update.message.reply_text(
            "✅ Спасибо! Ваш номер телефона сохранён.\n\n"
            "Теперь я смогу лучше помочь вам с подбором транспорта.\n\n"
            "Задавайте любые вопросы!",
            reply_markup=reply_markup
        )
    
    return ConversationHandler.END

async def skip_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Пропускает запрос телефона"""
    await update.message.reply_text(
        "Хорошо, продолжим без номера телефона.\n\n"
        "Вы всегда можете поделиться им позже командой /phone"
    )
    return ConversationHandler.END

async def show_my_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает пользователю его сохранённый номер телефона"""
    user_id = update.effective_user.id
    cursor.execute("SELECT phone FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    
    if result and result[0]:
        await update.message.reply_text(f"📞 Ваш номер телефона: `{result[0]}`", parse_mode="Markdown")
    else:
        await update.message.reply_text(
            "❌ У вас ещё не сохранён номер телефона.\n\n"
            "Отправьте /phone чтобы добавить его."
        )

# ============================================
# АДМИН КОМАНДЫ
# ============================================

async def set_user_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Админ команда: /setphone 123456789 +71234567890"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⛔ Доступно только администратору.")
        return
    
    args = context.args
    if len(args) != 2:
        await update.message.reply_text("❌ Пример: /setphone 123456789 +71234567890")
        return
    
    try:
        user_id = int(args[0])
        phone = args[1]
        
        cursor.execute(
            "UPDATE users SET phone = ? WHERE user_id = ?",
            (phone, user_id)
        )
        db.commit()
        
        export_users_to_csv()
        
        if cursor.rowcount > 0:
            await update.message.reply_text(f"✅ Телефон {phone} сохранён для пользователя {user_id}")
        else:
            await update.message.reply_text(f"⚠️ Пользователь {user_id} не найден")
    except ValueError:
        await update.message.reply_text("❌ ID должен быть числом")

async def set_user_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Админ команда: /setemail 123456789 user@example.com"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⛔ Доступно только администратору.")
        return
    
    args = context.args
    if len(args) != 2:
        await update.message.reply_text("❌ Пример: /setemail 123456789 user@example.com")
        return
    
    try:
        user_id = int(args[0])
        email = args[1]
        
        cursor.execute(
            "UPDATE users SET email = ? WHERE user_id = ?",
            (email, user_id)
        )
        db.commit()
        
        export_users_to_csv()
        
        if cursor.rowcount > 0:
            await update.message.reply_text(f"✅ Email {email} сохранён для пользователя {user_id}")
        else:
            await update.message.reply_text(f"⚠️ Пользователь {user_id} не найден")
    except ValueError:
        await update.message.reply_text("❌ ID должен быть числом")

async def export_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Экспортирует пользователей в CSV"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⛔ Доступно только администратору.")
        return
    
    success, count = export_users_to_csv()
    
    if not success:
        await update.message.reply_text("❌ Нет пользователей для экспорта")
        return
    
    try:
        with open(USERS_EXPORT_FILE, 'rb') as f:
            await update.message.reply_document(
                document=f,
                filename=f"users_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                caption=f"📊 Экспорт пользователей\n\n👥 Всего: {count}\n📅 {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}"
            )
        
        print(f"✅ Экспорт отправлен в Telegram")
        
    except Exception as e:
        print(f"❌ Ошибка отправки экспорта: {e}")
        await update.message.reply_text(f"❌ Ошибка: {e}")

async def get_user_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Админ команда: /userinfo 123456789"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⛔ Доступно только администратору.")
        return
    
    if not context.args:
        await update.message.reply_text("❌ Пример: /userinfo 123456789")
        return
    
    try:
        user_id = int(context.args[0])
        cursor.execute("SELECT user_id, username, first_name, last_name, phone, email, registered_at FROM users WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()
        
        if user:
            info = f"📋 **Информация о пользователе**\n\n"
            info += f"🆔 ID: `{user[0]}`\n"
            info += f"👤 Username: @{user[1] if user[1] else 'Нет'}\n"
            info += f"📛 Имя: {user[2] if user[2] else 'Не указано'}\n"
            info += f"📛 Фамилия: {user[3] if user[3] else 'Не указана'}\n"
            info += f"📞 Телефон: {user[4] if user[4] else 'Не указан'}\n"
            info += f"📧 Email: {user[5] if user[5] else 'Не указан'}\n"
            info += f"📅 Зарегистрирован: {user[6] if user[6] else 'Неизвестно'}"
            
            await update.message.reply_text(info, parse_mode="Markdown")
        else:
            await update.message.reply_text(f"❌ Пользователь {user_id} не найден")
    except ValueError:
        await update.message.reply_text("❌ ID должен быть числом")

# ============================================
# КОМАНДЫ БОТА
# ============================================

SERVICE_BUTTON_TEXT = "Сервис"
INSTRUCTIONS_BUTTON_TEXT = "Инструкции"
YAK_INSTRUCTION_TEXT = "Як"
DILIGENCE_INSTRUCTION_TEXT = "Дилижанс"
WASHER_INSTRUCTION_TEXT = "Поливомоечная машина"
SERVICE_BOOKS_BUTTON_TEXT = "Сервисные книжки"
SERVICE_VIN_BUTTON_TEXT = "Поиск по VIN"
SERVICE_MAINTENANCE_BUTTON_TEXT = "Плановое ТО"
SERVICE_CURTIS_BUTTON_TEXT = "Ошибки Curtis"
CURTIS_ALL_CODES_BUTTON_TEXT = "Все коды Curtis"
CURTIS_PDF_BUTTON_TEXT = "PDF кодов Curtis"
CURTIS_HOW_BUTTON_TEXT = "Как читать LED"
BACK_TO_SERVICE_MENU_TEXT = "В раздел сервиса"
BACK_TO_MAIN_MENU_TEXT = "Назад"
AWAITING_INSTRUCTION_KEY = "awaiting_instruction_vehicle"
AWAITING_FRAME_LOOKUP_KEY = "awaiting_frame_lookup"
AWAITING_MAINTENANCE_LOOKUP_KEY = "awaiting_maintenance_lookup"
AWAITING_CURTIS_CODE_KEY = "awaiting_curtis_code"
SERVICE_SUBMENU_KEY = "service_submenu_active"
CURTIS_SUBMENU_KEY = "curtis_submenu_active"
CURTIS_FAULT_CODES_FILE = "knowledge/service/curtis_fault_codes.json"
CURTIS_FAULT_PDF_FILE = "knowledge/service/curtis_fault_codes_ru.pdf"
TELEGRAM_MESSAGE_LIMIT = 3900

def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [[SERVICE_BUTTON_TEXT]],
        resize_keyboard=True
    )

def get_service_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [
            [SERVICE_MAINTENANCE_BUTTON_TEXT, SERVICE_VIN_BUTTON_TEXT],
            [INSTRUCTIONS_BUTTON_TEXT, SERVICE_BOOKS_BUTTON_TEXT],
            [SERVICE_CURTIS_BUTTON_TEXT],
            [BACK_TO_MAIN_MENU_TEXT],
        ],
        resize_keyboard=True,
    )

def get_curtis_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [
            [CURTIS_HOW_BUTTON_TEXT, CURTIS_ALL_CODES_BUTTON_TEXT],
            [CURTIS_PDF_BUTTON_TEXT],
            [BACK_TO_SERVICE_MENU_TEXT],
            [BACK_TO_MAIN_MENU_TEXT],
        ],
        resize_keyboard=True,
    )

def get_instruction_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [
            [YAK_INSTRUCTION_TEXT, DILIGENCE_INSTRUCTION_TEXT],
            [WASHER_INSTRUCTION_TEXT],
            [SERVICE_BUTTON_TEXT],
            [BACK_TO_MAIN_MENU_TEXT],
        ],
        resize_keyboard=True,
    )

async def send_doc_if_exists(update: Update, file_path: str) -> bool:
    """Отправляет документ, если файл существует."""
    if not os.path.exists(file_path):
        return False
    try:
        with open(file_path, "rb") as doc_file:
            await update.message.reply_document(document=doc_file)
        return True
    except Exception as e:
        print(f"⚠️ Ошибка отправки файла {file_path}: {e}")
        return False


def load_curtis_fault_data() -> dict | None:
    """Загружает таблицу LED-кодов Curtis из knowledge/service."""
    if not os.path.exists(CURTIS_FAULT_CODES_FILE):
        return None
    try:
        with open(CURTIS_FAULT_CODES_FILE, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception as e:
        print(f"⚠️ Ошибка чтения {CURTIS_FAULT_CODES_FILE}: {e}")
        return None


def split_telegram_chunks(text: str, limit: int = TELEGRAM_MESSAGE_LIMIT) -> list[str]:
    """Режет длинный текст на сообщения Telegram по абзацам."""
    text = (text or "").strip()
    if not text:
        return []
    if len(text) <= limit:
        return [text]

    chunks: list[str] = []
    current = ""
    for block in text.split("\n\n"):
        piece = block if not current else current + "\n\n" + block
        if len(piece) <= limit:
            current = piece
            continue
        if current:
            chunks.append(current)
            current = ""
        if len(block) <= limit:
            current = block
            continue
        start = 0
        while start < len(block):
            chunks.append(block[start:start + limit])
            start += limit
    if current:
        chunks.append(current)
    return chunks


def format_curtis_code_entry(entry: dict) -> str:
    code = entry.get("code", "?")
    name = entry.get("name", "")
    meaning = entry.get("meaning", "")
    fix = entry.get("fix", "")
    return (
        f"Код {code}\n"
        f"{name}\n"
        f"Что это: {meaning}\n"
        f"Как устранить: {fix}"
    )


def build_curtis_how_to_text(data: dict) -> str:
    lines = data.get("how_to_read") or []
    body = "\n".join(lines)
    family = data.get("family") or "Curtis AC"
    return f"Ошибки LED контроллеров Curtis\nСемейство: {family}\n\n{body}"


def build_curtis_all_codes_text(data: dict) -> str:
    parts = [
        "Полная расшифровка LED-кодов Curtis.",
        "Для каждого кода: суть и как устранять.",
        "",
    ]
    for entry in data.get("codes") or []:
        parts.append(format_curtis_code_entry(entry))
        parts.append("")
    unused = data.get("unused_codes") or []
    if unused:
        parts.append(
            "Незанятые номера (на LED не используются): "
            + ", ".join(str(n) for n in unused)
            + "."
        )
    return "\n".join(parts).strip()


def lookup_curtis_codes(data: dict, code_raw: str) -> list[dict]:
    """Ищет код(ы) по номеру: 47, код 47, 51-67 и т.п."""
    normalized = (code_raw or "").strip().upper()
    normalized = normalized.replace("КОД", " ").replace("CODE", " ")
    normalized = re.sub(r"[^0-9\-]", " ", normalized)
    normalized = " ".join(normalized.split())
    if not normalized:
        return []

    codes = data.get("codes") or []
    matches: list[dict] = []

    # Диапазон OEM 51-67
    if normalized in {"51-67", "51—67", "51–67"} or normalized.replace(" ", "") in {
        "51-67", "51—67", "51–67"
    }:
        return [e for e in codes if str(e.get("code", "")).startswith("51")]

    # Одно или несколько чисел
    numbers = re.findall(r"\d{1,3}", normalized)
    if not numbers:
        return []

    wanted = {n.zfill(2) if len(n) == 1 else n for n in numbers}
    # также без ведущего нуля
    wanted |= {str(int(n)) for n in numbers}

    for entry in codes:
        code = str(entry.get("code", ""))
        if code in wanted:
            matches.append(entry)
            continue
        # OEM-блок
        if code.startswith("51") and any(
            51 <= int(n) <= 67 for n in numbers if n.isdigit()
        ):
            if entry not in matches:
                matches.append(entry)
    return matches


async def send_curtis_text_chunks(
    update: Update,
    text: str,
    reply_markup: ReplyKeyboardMarkup | None = None,
) -> None:
    chunks = split_telegram_chunks(text)
    if not chunks:
        await update.message.reply_text(
            "Таблица кодов Curtis сейчас недоступна.",
            reply_markup=reply_markup or get_curtis_keyboard(),
        )
        return
    for idx, chunk in enumerate(chunks):
        markup = reply_markup if idx == len(chunks) - 1 else None
        await update.message.reply_text(chunk, reply_markup=markup)

def normalize_frame_number(value: str) -> str:
    """Нормализует номер рамы для строгого сравнения."""
    normalized = (value or "").upper().strip()
    normalized = normalized.replace("*", "").replace("'", "").replace('"', "")
    normalized = "".join(normalized.split())
    # Приводим похожие кириллические символы к латинице.
    cyr_to_lat = str.maketrans({
        "А": "A", "В": "B", "С": "C", "Е": "E", "Н": "H",
        "К": "K", "М": "M", "О": "O", "Р": "P", "Т": "T",
        "Х": "X", "У": "Y",
    })
    normalized = normalized.translate(cyr_to_lat)
    # Убираем все символы, кроме латиницы и цифр.
    return re.sub(r"[^A-Z0-9]", "", normalized)


def looks_like_frame_candidate(value: str) -> bool:
    """Проверяет, похожа ли строка на номер рамы/VIN."""
    if not value or len(value) < 8:
        return False
    has_digit = any(ch.isdigit() for ch in value)
    has_alpha = any("A" <= ch <= "Z" for ch in value)
    return has_digit and has_alpha


def extract_frame_candidates(*values: str) -> set[str]:
    """
    Возвращает набор нормализованных кандидатов номера рамы из свободного текста.
    Нужен как fallback, если в таблице сдвинулись колонки.
    """
    raw = " ".join((v or "") for v in values if v)
    if not raw:
        return set()

    # Берем как отдельные токены, так и цельную строку.
    parts = re.split(r"[\s,;|/]+", raw)
    parts.append(raw)

    candidates: set[str] = set()
    for part in parts:
        candidate = normalize_frame_number(part)
        if looks_like_frame_candidate(candidate):
            candidates.add(candidate)
    return candidates

def normalize_header(value: str) -> str:
    """Нормализует заголовок колонки для поиска по имени."""
    return " ".join((value or "").strip().lower().replace("ё", "е").split())


def to_excel_column_name(index_zero_based: int) -> str:
    """Преобразует индекс колонки (0-based) в Excel-имя."""
    n = index_zero_based + 1
    name = []
    while n > 0:
        n, rem = divmod(n - 1, 26)
        name.append(chr(ord("A") + rem))
    return "".join(reversed(name))


def parse_date_safe(value: str):
    """Пробует распарсить дату из строки в популярных форматах."""
    raw = (value or "").strip()
    if not raw:
        return None
    for fmt in ("%d.%m.%Y", "%d.%m.%y", "%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(raw, fmt)
        except ValueError:
            continue
    return None


def get_frame_data_from_sheet(frame_number: str):
    """
    Возвращает данные по номеру рамы из публичного CSV Google Sheets.
    Ищет колонки по их названиям в строке заголовков.
    """
    try:
        with urllib.request.urlopen(SHEET_CSV_URL, timeout=15) as response:
            content = response.read().decode("utf-8-sig", errors="replace")
    except Exception as e:
        return None, f"Ошибка доступа к таблице: {e}"

    rows = list(csv.reader(io.StringIO(content)))
    if not rows:
        return None, "Таблица пуста."

    header_aliases = {
        "frame": {
            "№ рамы", "номер рамы", "рама", "vin", "vin номер", "vin-код", "vin код",
            # В таблице Эльтавр VIN часто лежит в колонке «Машина».
            "машина",
        },
        "config": {"комплектация"},
        "customer": {"заказчик", "клиент"},
        "ship_date": {"дата отгрузки заказчику", "дата отгрузки", "отгрузка"},
        "service_date": {"дата планового то", "плановое то", "дата то"},
    }

    normalized_aliases = {
        key: {normalize_header(alias) for alias in aliases}
        for key, aliases in header_aliases.items()
    }

    header_row_index = None
    header_map = {}
    for idx, row in enumerate(rows[:30]):
        current_map = {}
        for col_idx, cell in enumerate(row):
            cell_norm = normalize_header(cell)
            if not cell_norm:
                continue
            for key, aliases in normalized_aliases.items():
                if key not in current_map and cell_norm in aliases:
                    current_map[key] = col_idx
        if "frame" in current_map:
            header_row_index = idx
            header_map = current_map
            break

    if header_row_index is None:
        return None, "Не удалось найти заголовки в таблице."

    target = normalize_frame_number(frame_number)
    for row in rows[header_row_index + 1:]:
        frame_idx = header_map.get("frame")
        row_candidates: set[str] = set()

        if frame_idx is not None and len(row) > frame_idx:
            row_frame = normalize_frame_number(row[frame_idx])
            if looks_like_frame_candidate(row_frame):
                row_candidates.add(row_frame)

        # Fallback: иногда колонка "№ рамы" сдвигается, поэтому ищем VIN-подобные значения
        # в первых колонках строки.
        for cell in row[:8]:
            row_candidates.update(extract_frame_candidates(cell))

        if target in row_candidates:
            # По требованию: поле "Машина" выдаём строго из колонки B.
            machine_from_col_b = row[1].strip() if len(row) > 1 else ""
            data = {
                "machine": machine_from_col_b,
                "config": row[header_map["config"]].strip()
                if "config" in header_map and len(row) > header_map["config"] else "",
                "customer": row[header_map["customer"]].strip()
                if "customer" in header_map and len(row) > header_map["customer"] else "",
                "ship_date": row[header_map["ship_date"]].strip()
                if "ship_date" in header_map and len(row) > header_map["ship_date"] else "",
                "service_date": row[header_map["service_date"]].strip()
                if "service_date" in header_map and len(row) > header_map["service_date"] else "",
            }
            return data, None

    return None, None


def get_maintenance_data_from_sheet(frame_number: str):
    """
    Ищет VIN в колонке "Шасси" и возвращает:
    - дату продажи
    - заполненные поля планового ТО из диапазона G..DA
    """
    try:
        with urllib.request.urlopen(MAINTENANCE_SHEET_CSV_URL, timeout=15) as response:
            content = response.read().decode("utf-8-sig", errors="replace")
    except Exception as e:
        return None, f"Ошибка доступа к таблице ТО: {e}"

    rows = list(csv.reader(io.StringIO(content)))
    if not rows:
        return None, "Таблица ТО пуста."

    chassis_aliases = {"шасси"}
    sale_aliases = {"дата продажи"}
    fallback_chassis_idx = 4  # Колонка E
    fallback_contacts_idx = 2  # Колонка C
    fallback_machine_name_idx = 3  # Колонка D

    header_row_index = None
    chassis_idx = None
    sale_idx = None
    for idx, row in enumerate(rows[:30]):
        normalized = [normalize_header(cell) for cell in row]
        for col_idx, col_name in enumerate(normalized):
            if chassis_idx is None and col_name in chassis_aliases:
                chassis_idx = col_idx
            if sale_idx is None and col_name in sale_aliases:
                sale_idx = col_idx
        if chassis_idx is not None:
            header_row_index = idx
            break
        # reset for next potential header row
        chassis_idx = None
        sale_idx = None

    # Если заголовок "Шасси" не найден, используем фиксированную колонку E.
    if header_row_index is None:
        header_row_index = 0
    if chassis_idx is None:
        chassis_idx = fallback_chassis_idx

    target = normalize_frame_number(frame_number)
    header_row = rows[header_row_index] if len(rows) > header_row_index else []
    maintenance_start_idx = 6    # G
    maintenance_end_idx = 104    # DA

    for row in rows[header_row_index + 1:]:
        row_candidates: set[str] = set()

        if len(row) > chassis_idx:
            row_frame = normalize_frame_number(row[chassis_idx])
            if looks_like_frame_candidate(row_frame):
                row_candidates.add(row_frame)

        # Fallback на случай сдвинутых колонок в исходном листе.
        for cell in row[:8]:
            row_candidates.update(extract_frame_candidates(cell))

        if target not in row_candidates:
            continue

        sale_date = row[sale_idx].strip() if sale_idx is not None and len(row) > sale_idx else ""
        contacts = row[fallback_contacts_idx].strip() if len(row) > fallback_contacts_idx else ""
        machine_name = row[fallback_machine_name_idx].strip() if len(row) > fallback_machine_name_idx else ""

        maintenance_entries = []
        max_idx = min(maintenance_end_idx, len(row) - 1)
        for col_idx in range(maintenance_start_idx, max_idx + 1):
            value = row[col_idx].strip() if len(row) > col_idx else ""
            if not value:
                continue

            header_name = ""
            if len(header_row) > col_idx:
                header_name = (header_row[col_idx] or "").strip()
            label = header_name or f"ТО ({to_excel_column_name(col_idx)})"
            maintenance_entries.append((label, value))

        return {
            "sale_date": sale_date,
            "contacts": contacts,
            "machine_name": machine_name,
            "maintenance_entries": maintenance_entries,
        }, None

    return None, None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    username = user.username or ""
    first_name = user.first_name or ""
    last_name = user.last_name or ""
    
    cursor.execute(
        "INSERT OR IGNORE INTO users (user_id, username, first_name, last_name) VALUES (?, ?, ?, ?)",
        (user_id, username, first_name, last_name)
    )
    db.commit()
    
    export_users_to_csv()
    add_broadcast_id(user_id)
    log_message(user_id, "USER", "/start", username)
    
    welcome = f"""🏢 Здравствуйте, {first_name}!

Я бот поддержки компании ЭЛЬТАВР с AI от DeepSeek.

🚗 Мы производим коммерческий электротранспорт:
• Электробусы «Дилижанс»
• Электрогрузовики «Як»
• Спецтехника

💬 Напишите ваш вопрос, и я помогу!

Для связи с менеджером: /phone"""
    
    log_message(user_id, "BOT", welcome, username)
    await update.message.reply_text(welcome, reply_markup=get_main_menu_keyboard())

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда help"""
    user_id = update.effective_user.id

    if user_id != ADMIN_ID:
        await update.message.reply_text("⛔ Команда /help доступна только администратору.")
        return

    help_text = """🔐 **АДМИН ПАНЕЛЬ**

📚 **Команды рассылки:**
/broadcast текст - рассылка всем
/broadcastfile - рассылка из файла message.txt
/broadcastids 123,456 | текст - рассылка по ID
/broadcastlist - список ID
/addid ID - добавить ID
/removeid ID - удалить ID
/clearids - очистить список

📊 **Статистика и логи:**
/stats - статистика
/getlog ID - лог пользователя
/listlogs - список логов
/synclogs - синхронизация ID

👥 **Управление:**
/userinfo ID - информация о пользователе
/setphone ID телефон - установить телефон
/setemail ID email - установить email
/exportusers - экспорт в CSV

📞 **Телефон:**
/phone - запросить номер
/myphone - показать свой номер

🤖 **AI:** DeepSeek"""

    await update.message.reply_text(help_text, parse_mode="Markdown")

# === КОМАНДЫ РАССЫЛКИ ===

async def broadcast_to_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⛔ Доступно только администратору.")
        return
    
    text = " ".join(context.args)
    if not text:
        await update.message.reply_text("Пример: /broadcast Всем привет!")
        return
    
    cursor.execute("SELECT user_id FROM users")
    users = cursor.fetchall()
    
    if not users:
        await update.message.reply_text("Нет пользователей")
        return
    
    sent = 0
    await update.message.reply_text(f"📢 Рассылка для {len(users)} пользователей...")
    
    for user in users:
        try:
            await context.bot.send_message(chat_id=user[0], text=f"📢 {text}")
            sent += 1
            await asyncio.sleep(0.05)
        except:
            pass
    
    await update.message.reply_text(f"✅ Отправлено: {sent}")

async def broadcast_from_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⛔ Доступно только администратору.")
        return
    
    message_file = "message.txt"
    
    if not os.path.exists(message_file):
        await update.message.reply_text(f"❌ Файл {message_file} не найден!")
        return
    
    ids = load_broadcast_ids()
    if not ids:
        await update.message.reply_text(f"❌ Список ID пуст!")
        return
    
    with open(message_file, "r", encoding="utf-8") as f:
        message_text = f.read().strip()
    
    await update.message.reply_text(f"📢 Рассылка для {len(ids)} пользователей...")
    
    sent = 0
    for user_id in ids:
        try:
            await context.bot.send_message(chat_id=user_id, text=message_text)
            sent += 1
            await asyncio.sleep(0.05)
        except:
            pass
    
    await update.message.reply_text(f"✅ Отправлено: {sent}")

async def broadcast_by_ids(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⛔ Доступно только администратору.")
        return
    
    args = " ".join(context.args)
    parts = args.split("|")
    
    if len(parts) < 2:
        await update.message.reply_text("❌ Формат: /broadcastids 123,456 | Текст")
        return
    
    ids_str = parts[0].strip()
    message_text = parts[1].strip()
    
    try:
        ids_list = [int(id_str.strip()) for id_str in ids_str.split(",")]
    except ValueError:
        await update.message.reply_text("❌ ID должны быть числами")
        return
    
    sent = 0
    for user_id in ids_list:
        try:
            await context.bot.send_message(chat_id=user_id, text=message_text)
            sent += 1
            await asyncio.sleep(0.05)
        except:
            pass
    
    await update.message.reply_text(f"✅ Отправлено: {sent}")

async def show_broadcast_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⛔ Доступно только администратору.")
        return
    
    count, ids = get_broadcast_stats()
    
    if not ids:
        await update.message.reply_text("📭 Список ID пуст.")
        return
    
    text = f"📋 СПИСОК ID (всего: {count})\n\n"
    for i, user_id in enumerate(ids[:30], 1):
        text += f"{i}. {user_id}\n"
    
    if len(ids) > 30:
        text += f"\n... и еще {len(ids) - 30}"
    
    await update.message.reply_text(text)

async def add_broadcast_id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⛔ Доступно только администратору.")
        return
    
    if not context.args:
        await update.message.reply_text("❌ Пример: /addid 123456789")
        return
    
    try:
        user_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("❌ ID должен быть числом")
        return
    
    if add_broadcast_id(user_id):
        await update.message.reply_text(f"✅ ID {user_id} добавлен")
    else:
        await update.message.reply_text(f"⚠️ ID {user_id} уже есть")

async def remove_broadcast_id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⛔ Доступно только администратору.")
        return
    
    if not context.args:
        await update.message.reply_text("❌ Пример: /removeid 123456789")
        return
    
    try:
        user_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("❌ ID должен быть числом")
        return
    
    if remove_broadcast_id(user_id):
        await update.message.reply_text(f"✅ ID {user_id} удален")
    else:
        await update.message.reply_text(f"⚠️ ID {user_id} не найден")

async def clear_broadcast_ids(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⛔ Доступно только администратору.")
        return
    
    save_broadcast_ids([])
    await update.message.reply_text("✅ Список очищен")

async def sync_logs_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⛔ Доступно только администратору.")
        return
    
    added, new_ids = sync_ids_from_logs()
    
    if added:
        await update.message.reply_text(f"✅ Добавлено ID: {len(new_ids)}")
    else:
        await update.message.reply_text("✅ Новых ID не найдено")

# === СТАТИСТИКА ===

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⛔ Доступно только администратору.")
        return
    
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM users WHERE phone IS NOT NULL AND phone != ''")
    users_with_phone = cursor.fetchone()[0]
    
    logs_count = len([f for f in os.listdir(LOGS_DIR) if f.endswith('.txt')])
    broadcast_count, _ = get_broadcast_stats()
    
    await update.message.reply_text(
        f"📊 СТАТИСТИКА\n\n"
        f"👥 Пользователей: {total_users}\n"
        f"📞 С телефоном: {users_with_phone}\n"
        f"💬 Диалогов: {logs_count}\n"
        f"📋 ID в рассылке: {broadcast_count}\n"
        f"🤖 AI: DeepSeek"
    )

async def getlog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⛔ Доступно только администратору.")
        return
    
    if not context.args:
        await update.message.reply_text("❌ Пример: /getlog 123456789")
        return
    
    try:
        user_id = int(context.args[0])
        log_file = os.path.join(LOGS_DIR, f"{user_id}.txt")
        
        if not os.path.exists(log_file):
            await update.message.reply_text(f"❌ Нет логов для {user_id}")
            return
        
        with open(log_file, "rb") as f:
            await update.message.reply_document(
                document=f,
                filename=f"user_{user_id}_log.txt",
                caption=f"📋 Лог пользователя {user_id}"
            )
    except ValueError:
        await update.message.reply_text("❌ ID должен быть числом")

async def listlogs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⛔ Доступно только администратору.")
        return
    
    logs = [f.replace('.txt', '') for f in os.listdir(LOGS_DIR) if f.endswith('.txt')]
    
    if not logs:
        await update.message.reply_text("📭 Нет логов")
        return
    
    text = f"📁 ПОЛЬЗОВАТЕЛИ (всего: {len(logs)})\n\n"
    for user_id in logs[:30]:
        cursor.execute("SELECT username, first_name FROM users WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()
        if user and user[0]:
            text += f"• `{user_id}` - @{user[0]}\n"
        elif user and user[1]:
            text += f"• `{user_id}` - {user[1]}\n"
        else:
            text += f"• `{user_id}`\n"
    
    if len(logs) > 30:
        text += f"\n... и еще {len(logs) - 30}"
    
    await update.message.reply_text(text, parse_mode="Markdown")

# === ОБРАБОТЧИК ФОТО ===

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    username = user.username or ""

    if not anthropic_client:
        await update.message.reply_text("❌ Распознавание изображений недоступно.")
        return

    await update.message.reply_text("🔍 Анализирую изображение...")

    photo = update.message.photo[-1]
    caption = update.message.caption or "Опиши, что изображено на этом фото."

    try:
        tg_file = await context.bot.get_file(photo.file_id)
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            tmp_path = tmp.name
        await tg_file.download_to_drive(tmp_path)

        with open(tmp_path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode()
        os.unlink(tmp_path)

        msg = anthropic_client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": img_b64}},
                    {"type": "text", "text": caption}
                ]
            }]
        )
        response = msg.content[0].text
    except Exception as e:
        response = f"❌ Ошибка при анализе изображения: {e}"

    log_message(user_id, "USER", f"[фото] {caption}", username)
    log_message(user_id, "BOT", response, username)
    await update.message.reply_text(response)


# === ОБРАБОТЧИК СООБЩЕНИЙ ===

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    username = user.username or ""
    text = update.message.text
    
    if text.startswith('/'):
        return

    if text == BACK_TO_MAIN_MENU_TEXT:
        context.user_data.pop(AWAITING_FRAME_LOOKUP_KEY, None)
        context.user_data.pop(AWAITING_MAINTENANCE_LOOKUP_KEY, None)
        context.user_data.pop(AWAITING_INSTRUCTION_KEY, None)
        context.user_data.pop(AWAITING_CURTIS_CODE_KEY, None)
        context.user_data.pop(SERVICE_SUBMENU_KEY, None)
        context.user_data.pop(CURTIS_SUBMENU_KEY, None)
        response = "Главное меню."
        log_message(user_id, "USER", text, username)
        log_message(user_id, "BOT", response, username)
        await update.message.reply_text(response, reply_markup=get_main_menu_keyboard())
        return

    if text == BACK_TO_SERVICE_MENU_TEXT:
        context.user_data.pop(AWAITING_CURTIS_CODE_KEY, None)
        context.user_data.pop(CURTIS_SUBMENU_KEY, None)
        context.user_data.pop(AWAITING_FRAME_LOOKUP_KEY, None)
        context.user_data.pop(AWAITING_MAINTENANCE_LOOKUP_KEY, None)
        context.user_data[SERVICE_SUBMENU_KEY] = True
        response = (
            "Раздел сервиса.\n"
            "Плановое ТО — даты обслуживания по VIN/шасси.\n"
            "Поиск по VIN — данные по отгрузке и комплектации.\n"
            "Инструкции и сервисные книжки — отправка PDF.\n"
            "Ошибки Curtis — расшифровка светодиодных кодов контроллера."
        )
        log_message(user_id, "USER", text, username)
        log_message(user_id, "BOT", response, username)
        await update.message.reply_text(response, reply_markup=get_service_keyboard())
        return

    if text == SERVICE_BUTTON_TEXT:
        context.user_data.pop(AWAITING_INSTRUCTION_KEY, None)
        context.user_data.pop(AWAITING_CURTIS_CODE_KEY, None)
        context.user_data.pop(CURTIS_SUBMENU_KEY, None)
        context.user_data[AWAITING_FRAME_LOOKUP_KEY] = False
        context.user_data[AWAITING_MAINTENANCE_LOOKUP_KEY] = False
        context.user_data[SERVICE_SUBMENU_KEY] = True
        response = (
            "Раздел сервиса.\n"
            "Плановое ТО — даты обслуживания по VIN/шасси.\n"
            "Поиск по VIN — данные по отгрузке и комплектации.\n"
            "Инструкции и сервисные книжки — отправка PDF.\n"
            "Ошибки Curtis — расшифровка светодиодных кодов контроллера."
        )
        log_message(user_id, "USER", text, username)
        log_message(user_id, "BOT", response, username)
        await update.message.reply_text(
            response,
            reply_markup=get_service_keyboard(),
        )
        return

    if text == SERVICE_BOOKS_BUTTON_TEXT:
        context.user_data[SERVICE_SUBMENU_KEY] = True
        context.user_data.pop(AWAITING_FRAME_LOOKUP_KEY, None)
        context.user_data.pop(AWAITING_MAINTENANCE_LOOKUP_KEY, None)
        context.user_data.pop(AWAITING_CURTIS_CODE_KEY, None)
        context.user_data.pop(CURTIS_SUBMENU_KEY, None)
        log_message(user_id, "USER", text, username)
        intro = "Отправляю сервисные книжки файлами."
        log_message(user_id, "BOT", intro, username)
        await update.message.reply_text(intro, reply_markup=get_service_keyboard())
        for path in SERVICE_DOC_FILES:
            await send_doc_if_exists(update, path)
        return

    if text == SERVICE_VIN_BUTTON_TEXT:
        context.user_data[SERVICE_SUBMENU_KEY] = True
        context.user_data.pop(AWAITING_CURTIS_CODE_KEY, None)
        context.user_data.pop(CURTIS_SUBMENU_KEY, None)
        context.user_data[AWAITING_FRAME_LOOKUP_KEY] = True
        context.user_data[AWAITING_MAINTENANCE_LOOKUP_KEY] = False
        response = "Введите номер рамы — покажу машину, комплектацию, дату отгрузки и дату планового ТО."
        log_message(user_id, "USER", text, username)
        log_message(user_id, "BOT", response, username)
        await update.message.reply_text(
            response,
            reply_markup=get_service_keyboard(),
        )
        return

    if text == SERVICE_MAINTENANCE_BUTTON_TEXT:
        context.user_data[SERVICE_SUBMENU_KEY] = True
        context.user_data.pop(CURTIS_SUBMENU_KEY, None)
        context.user_data.pop(AWAITING_CURTIS_CODE_KEY, None)
        context.user_data[AWAITING_FRAME_LOOKUP_KEY] = False
        context.user_data[AWAITING_MAINTENANCE_LOOKUP_KEY] = True
        response = "Введите VIN (Шасси) — покажу дату продажи и все плановые ТО (1-5)."
        log_message(user_id, "USER", text, username)
        log_message(user_id, "BOT", response, username)
        await update.message.reply_text(
            response,
            reply_markup=get_service_keyboard(),
        )
        return

    if text == SERVICE_CURTIS_BUTTON_TEXT:
        context.user_data[SERVICE_SUBMENU_KEY] = True
        context.user_data[CURTIS_SUBMENU_KEY] = True
        context.user_data[AWAITING_CURTIS_CODE_KEY] = True
        context.user_data.pop(AWAITING_FRAME_LOOKUP_KEY, None)
        context.user_data.pop(AWAITING_MAINTENANCE_LOOKUP_KEY, None)
        data = load_curtis_fault_data()
        if data is None:
            response = (
                "Раздел ошибок Curtis временно недоступен. "
                "Попробуйте позже или обратитесь в сервис ЭЛЬТАВР."
            )
            log_message(user_id, "USER", text, username)
            log_message(user_id, "BOT", response, username)
            await update.message.reply_text(response, reply_markup=get_service_keyboard())
            return
        intro = (
            "Раздел ошибок LED контроллеров Curtis.\n"
            "Как читать LED — правила мигания красный/жёлтый.\n"
            "Все коды Curtis — полная таблица: что за ошибка и как устранить.\n"
            "PDF кодов Curtis — файл для печати/поля.\n"
            "Или просто пришлите номер кода (например 47)."
        )
        how_to = build_curtis_how_to_text(data)
        log_message(user_id, "USER", text, username)
        log_message(user_id, "BOT", intro, username)
        await update.message.reply_text(intro, reply_markup=get_curtis_keyboard())
        await send_curtis_text_chunks(update, how_to, reply_markup=get_curtis_keyboard())
        return

    if text == CURTIS_HOW_BUTTON_TEXT:
        context.user_data[CURTIS_SUBMENU_KEY] = True
        context.user_data[AWAITING_CURTIS_CODE_KEY] = True
        data = load_curtis_fault_data()
        log_message(user_id, "USER", text, username)
        if data is None:
            response = "Таблица кодов Curtis сейчас недоступна."
            log_message(user_id, "BOT", response, username)
            await update.message.reply_text(response, reply_markup=get_curtis_keyboard())
            return
        how_to = build_curtis_how_to_text(data)
        log_message(user_id, "BOT", how_to[:200], username)
        await send_curtis_text_chunks(update, how_to, reply_markup=get_curtis_keyboard())
        return

    if text == CURTIS_ALL_CODES_BUTTON_TEXT:
        context.user_data[CURTIS_SUBMENU_KEY] = True
        context.user_data[AWAITING_CURTIS_CODE_KEY] = True
        data = load_curtis_fault_data()
        log_message(user_id, "USER", text, username)
        if data is None:
            response = "Таблица кодов Curtis сейчас недоступна."
            log_message(user_id, "BOT", response, username)
            await update.message.reply_text(response, reply_markup=get_curtis_keyboard())
            return
        all_codes = build_curtis_all_codes_text(data)
        log_message(user_id, "BOT", f"Curtis all codes ({len(all_codes)} chars)", username)
        await send_curtis_text_chunks(update, all_codes, reply_markup=get_curtis_keyboard())
        return

    if text == CURTIS_PDF_BUTTON_TEXT:
        context.user_data[CURTIS_SUBMENU_KEY] = True
        context.user_data[AWAITING_CURTIS_CODE_KEY] = True
        log_message(user_id, "USER", text, username)
        intro = "Отправляю PDF полной таблицы кодов Curtis (RU)."
        log_message(user_id, "BOT", intro, username)
        await update.message.reply_text(intro, reply_markup=get_curtis_keyboard())
        sent = await send_doc_if_exists(update, CURTIS_FAULT_PDF_FILE)
        if not sent:
            await update.message.reply_text(
                "PDF сейчас недоступен. Используйте «Все коды Curtis» текстом.",
                reply_markup=get_curtis_keyboard(),
            )
        return

    if context.user_data.get(AWAITING_CURTIS_CODE_KEY) and text not in {
        SERVICE_CURTIS_BUTTON_TEXT,
        CURTIS_HOW_BUTTON_TEXT,
        CURTIS_ALL_CODES_BUTTON_TEXT,
        CURTIS_PDF_BUTTON_TEXT,
        BACK_TO_SERVICE_MENU_TEXT,
        BACK_TO_MAIN_MENU_TEXT,
        SERVICE_BUTTON_TEXT,
    }:
        data = load_curtis_fault_data()
        log_message(user_id, "USER", text, username)
        if data is None:
            response = "Таблица кодов Curtis сейчас недоступна."
            log_message(user_id, "BOT", response, username)
            await update.message.reply_text(response, reply_markup=get_curtis_keyboard())
            return
        matches = lookup_curtis_codes(data, text)
        unused = {str(n) for n in (data.get("unused_codes") or [])}
        numbers = re.findall(r"\d{1,3}", text)
        if matches:
            response = "\n\n".join(format_curtis_code_entry(e) for e in matches)
            response += "\n\nМожно прислать другой номер кода или открыть «Все коды Curtis»."
        elif numbers and any(n in unused or n.zfill(2) in unused for n in numbers):
            response = (
                f"Код {numbers[0]} на LED не используется (свободный номер).\n"
                "Проверьте счёт вспышек: это один двузначный код, не два отдельных."
            )
        else:
            response = (
                "Код не распознан. Пришлите номер вроде 47 или 23.\n"
                "Или нажмите «Все коды Curtis» / «Как читать LED»."
            )
        log_message(user_id, "BOT", response[:300], username)
        await send_curtis_text_chunks(update, response, reply_markup=get_curtis_keyboard())
        return

    if context.user_data.get(SERVICE_SUBMENU_KEY) and text not in {
        INSTRUCTIONS_BUTTON_TEXT,
        SERVICE_BOOKS_BUTTON_TEXT,
        SERVICE_VIN_BUTTON_TEXT,
        SERVICE_MAINTENANCE_BUTTON_TEXT,
        SERVICE_CURTIS_BUTTON_TEXT,
        CURTIS_HOW_BUTTON_TEXT,
        CURTIS_ALL_CODES_BUTTON_TEXT,
        CURTIS_PDF_BUTTON_TEXT,
        BACK_TO_SERVICE_MENU_TEXT,
    } and not context.user_data.get(
        AWAITING_FRAME_LOOKUP_KEY
    ) and not context.user_data.get(AWAITING_MAINTENANCE_LOOKUP_KEY) and not context.user_data.get(
        AWAITING_CURTIS_CODE_KEY
    ):
        response = (
            "Выберите: «Плановое ТО», «Поиск по VIN», «Инструкции», "
            "«Сервисные книжки» или «Ошибки Curtis»."
        )
        log_message(user_id, "USER", text, username)
        log_message(user_id, "BOT", response, username)
        await update.message.reply_text(
            response,
            reply_markup=get_service_keyboard(),
        )
        return

    if context.user_data.get(AWAITING_FRAME_LOOKUP_KEY):
        frame_number = text.strip()
        frame_data, error = get_frame_data_from_sheet(frame_number)

        if error:
            response = f"Не удалось получить данные. {error}"
        elif frame_data is None:
            response = f"Номер рамы {frame_number} не найден."
        else:
            response = (
                f"Номер рамы: {frame_number}\n"
                f"Машина: {frame_data.get('machine') or 'не указана'}\n"
                f"Комплектация: {frame_data.get('config') or 'не указана'}"
            )

        context.user_data[AWAITING_FRAME_LOOKUP_KEY] = False
        context.user_data[SERVICE_SUBMENU_KEY] = True
        log_message(user_id, "USER", frame_number, username)
        log_message(user_id, "BOT", response, username)
        await update.message.reply_text(response, reply_markup=get_service_keyboard())
        return

    if context.user_data.get(AWAITING_MAINTENANCE_LOOKUP_KEY):
        frame_number = text.strip()
        maintenance_data, error = get_maintenance_data_from_sheet(frame_number)

        if error:
            response = f"Не удалось получить данные. {error}"
        elif maintenance_data is None:
            response = f"VIN/Шасси {frame_number} не найден."
        else:
            maintenance_entries = maintenance_data.get("maintenance_entries", [])
            maintenance_block = ""
            if maintenance_entries:
                maintenance_lines = [f"{label}: {value}" for label, value in maintenance_entries]
                maintenance_block = "\n" + "\n".join(maintenance_lines)
            response = (
                f"VIN/Шасси: {frame_number}\n"
                f"Машина: {maintenance_data.get('machine_name') or 'не указана'}\n"
                f"Контакты: {maintenance_data.get('contacts') or 'не указаны'}\n"
                f"Дата продажи: {maintenance_data.get('sale_date') or 'не указана'}"
                f"{maintenance_block}"
            )

        context.user_data[AWAITING_MAINTENANCE_LOOKUP_KEY] = False
        context.user_data[SERVICE_SUBMENU_KEY] = True
        log_message(user_id, "USER", frame_number, username)
        log_message(user_id, "BOT", response, username)
        await update.message.reply_text(response, reply_markup=get_service_keyboard())
        return

    if text == INSTRUCTIONS_BUTTON_TEXT:
        context.user_data[SERVICE_SUBMENU_KEY] = True
        context.user_data.pop(AWAITING_FRAME_LOOKUP_KEY, None)
        context.user_data.pop(AWAITING_MAINTENANCE_LOOKUP_KEY, None)
        context.user_data.pop(AWAITING_CURTIS_CODE_KEY, None)
        context.user_data.pop(CURTIS_SUBMENU_KEY, None)
        context.user_data[AWAITING_INSTRUCTION_KEY] = False
        response = "Отправляю все инструкции файлами: Дилижанс, Поливомоечная машина и Як."
        log_message(user_id, "USER", text, username)
        log_message(user_id, "BOT", response, username)
        await update.message.reply_text(response, reply_markup=get_service_keyboard())
        for path in INSTRUCTION_DOC_FILES.values():
            await send_doc_if_exists(update, path)
        return

    if context.user_data.get(AWAITING_INSTRUCTION_KEY):
        # Совместимость со старыми сессиями: если флаг остался в user_data,
        # завершаем этот режим и просим нажать кнопку Инструкции заново.
        context.user_data[AWAITING_INSTRUCTION_KEY] = False
        response = "Нажмите «Инструкции» — отправлю сразу все PDF."
        log_message(user_id, "USER", text, username)
        log_message(user_id, "BOT", response, username)
        await update.message.reply_text(response, reply_markup=get_service_keyboard())
        return
    
    # Защита от грубостей
    rude_words = ["гандон", "дурак", "идиот", "козел", "сволочь", "тварь", "сука"]
    if any(word in text.lower() for word in rude_words):
        response = "🙏 Пожалуйста, общайтесь вежливо. Я здесь, чтобы помочь вам."
        await update.message.reply_text(response)
        return

    # VIN/рама без кнопки (если polling оборвался и флаг awaiting потерян)
    frame_guess = normalize_frame_number(text)
    if looks_like_frame_candidate(frame_guess) and len(frame_guess) >= 10:
        frame_data, error = get_frame_data_from_sheet(text.strip())
        if error:
            response = f"Не удалось получить данные. {error}"
        elif frame_data is None:
            response = f"Номер рамы {text.strip()} не найден."
        else:
            response = (
                f"Номер рамы: {text.strip()}\n"
                f"Машина: {frame_data.get('machine') or 'не указана'}\n"
                f"Комплектация: {frame_data.get('config') or 'не указана'}"
            )
        context.user_data[SERVICE_SUBMENU_KEY] = True
        log_message(user_id, "USER", text, username)
        log_message(user_id, "BOT", response, username)
        await update.message.reply_text(response, reply_markup=get_service_keyboard())
        return
    
    log_message(user_id, "USER", text, username)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {user_id}: {text[:50]}")
    
    await update.message.chat.send_action(action="typing")
    await asyncio.sleep(0.3)
    
    response = await get_ai_response(text, user_id, username)
    
    log_message(user_id, "BOT", response, username)
    await update.message.reply_text(response, reply_markup=get_main_menu_keyboard())

# ============================================
# ЗАПУСК БОТА
# ============================================

def main():
    print("=" * 50)
    print("🏢 БОТ ПОДДЕРЖКИ ЭЛЬТАВР (DeepSeek AI)")
    print("=" * 50)
    print(f"Администратор: {ADMIN_ID}")
    print(f"Логи: {LOGS_DIR}/")
    print(f"Режим: {'DeepSeek AI' if AI_MODE == 'deepseek' else 'Локальная база'}")
    print(f"Файл ID: {BROADCAST_IDS_FILE}")
    print("=" * 50)
    
    sync_ids_from_logs()
    print("✅ Бот готов!")
    
    # Больший пул + таймауты: иначе после 502 прокси сокеты залипают в CLOSE-WAIT
    # и getUpdates перестаёт забирать сообщения (бот «молчит»).
    builder = (
        Application.builder()
        .token(TOKEN)
        .connection_pool_size(16)
        .pool_timeout(30.0)
        .connect_timeout(20.0)
        .read_timeout(30.0)
        .write_timeout(30.0)
        .get_updates_connection_pool_size(4)
        .get_updates_pool_timeout(30.0)
        .get_updates_connect_timeout(20.0)
        .get_updates_read_timeout(50.0)
    )
    if TELEGRAM_PROXY:
        builder = builder.proxy(TELEGRAM_PROXY).get_updates_proxy(TELEGRAM_PROXY)
        print(f"🌐 Telegram proxy: {TELEGRAM_PROXY}")
    application = builder.build()

    async def on_error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        err = context.error
        print(f"⚠️ Handler error: {type(err).__name__}: {err}")

    application.add_error_handler(on_error)
    
    # ConversationHandler для телефона
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("phone", request_phone)],
        states={
            PHONE_REQUEST: [
                MessageHandler(filters.CONTACT, save_phone),
                CommandHandler("skip", skip_phone),
                MessageHandler(filters.TEXT & ~filters.COMMAND, skip_phone)
            ]
        },
        fallbacks=[CommandHandler("skip", skip_phone)]
    )
    
    # Команды
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("myphone", show_my_phone))
    application.add_handler(conv_handler)
    
    # Админ команды
    application.add_handler(CommandHandler("broadcast", broadcast_to_all))
    application.add_handler(CommandHandler("broadcastfile", broadcast_from_file))
    application.add_handler(CommandHandler("broadcastids", broadcast_by_ids))
    application.add_handler(CommandHandler("broadcastlist", show_broadcast_list))
    application.add_handler(CommandHandler("addid", add_broadcast_id_command))
    application.add_handler(CommandHandler("removeid", remove_broadcast_id_command))
    application.add_handler(CommandHandler("clearids", clear_broadcast_ids))
    application.add_handler(CommandHandler("synclogs", sync_logs_command))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("getlog", getlog))
    application.add_handler(CommandHandler("listlogs", listlogs))
    application.add_handler(CommandHandler("userinfo", get_user_info))
    application.add_handler(CommandHandler("setphone", set_user_phone))
    application.add_handler(CommandHandler("setemail", set_user_email))
    application.add_handler(CommandHandler("exportusers", export_users))
    
    # Обработчик фото
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    # Обработчик сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    application.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=False)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Бот остановлен")