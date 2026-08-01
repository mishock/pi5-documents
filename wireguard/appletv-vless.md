# Apple TV — клиент VLESS (vpn1)

Дата: 2026-08-01

## Клиент в 3x-ui

| Параметр | Значение |
|----------|----------|
| Email / имя | `appletv` |
| Inbound | `vless-reality` |
| Flow | пусто (без `xtls-rprx-vision` — на tvOS иначе часто TLS-ошибка) |
| Подписка | `https://89.127.199.6:2096/sub/5101960c-1fb4-4c31-b125-fff1e6e29a6b` |
| Адрес в ссылке | `89.127.199.6:443` (через `externalProxy` в inbound) |

Полная методичка сервера (панель, SSH, остальные устройства): `vpn-guide.md` (локально, не в git).

## Клиент на ТВ

1. Установить **Happ — Proxy Utility for TV** (tvOS 17.6+).
2. Импортировать URL подписки выше.
3. При ошибке TLS: обновить подписку в Happ (или удалить профиль и импортировать снова), затем подключить.

RAGE и штатный VPN Apple TV для этого профиля не подходят.

## Если снова «ошибка TLS»

1. Обновить подписку на ТВ (чтобы подтянулись IP и отсутствие flow).
2. Проверить время/дату на Apple TV (автоматически).
3. SNI должен быть `www.yahoo.com`, security — Reality (не обычный TLS).

## Ручной импорт (если подписка на ТВ «залипла»)

1. В Happ на ТВ: **+** → **Web Import** → код на [tv.happ.su](https://tv.happ.su).
2. Вставить **не URL подписки**, а ключ:

```
vless://b48909b4-93c3-4fd0-8001-d35f97be1738@89.127.199.6:443?flow=xtls-rprx-vision&fp=safari&pbk=eLJWF7Vceo4G2_0HqtutZZxnwS8rs71pGAgFLkCfQGo&security=reality&sid=1af21aa5234990ad&sni=www.yahoo.com&spx=%2F&type=tcp#appletv
```

3. Старый профиль с ошибкой TLS — удалить.
4. На Apple TV: Настройки → Основные → Дата и время → **автоматически**.

Проверено с Pi 5 (xray): туннель `appletv` поднимается, выходной IP `89.127.199.6`.

