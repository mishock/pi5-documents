/**
 * GEM e6 BMC CAN эмулятор v4.2 — PB MCU01 H503A (STM32H503CB)
 * FDCAN1 250 kbit/s + реле K5/K12/VCM/K7 + interlock (SM §8.28)
 */
#include <Arduino.h>

#include "bmc_can_gen.h"
#include "fdcan_gem.h"
#include "hw_pins.h"

static constexpr uint32_t ID_EF3 = 0x0CFF0EF3U;
static constexpr uint32_t ID_0FF3 = 0x0CFF0FF3U;
static constexpr uint32_t ID_10 = 0x0CFF10F3U;
static constexpr uint32_t ID_11 = 0x0CFF11F3U;
static constexpr uint32_t ID_12 = 0x0CFF12F3U;
static constexpr uint32_t ID_DM1 = 0x18FECAF3U;

static BmcGenerator gen;
static uint8_t payload[8];

static uint32_t last10ms = 0;
static uint32_t last100ms = 0;
static uint32_t last1s = 0;
static uint32_t lastInterlockMs = 0;
static bool interlockPrev = false;

static void pollInterlock() {
  const uint32_t now = millis();
  if (now - lastInterlockMs < 100) {
    return;
  }
  lastInterlockMs = now;
  updateDiscreteOutputs();
  const bool active = interlockActive();
  if (active != interlockPrev) {
    interlockPrev = active;
    Serial.print("Interlock p11: ");
    Serial.println(active ? "ON → K7 ON" : "OFF → K7 OFF");
  }
}

static void sendExt(uint32_t id, void (BmcGenerator::*fn)(uint8_t *)) {
  (gen.*fn)(payload);
  if (!fdcanGemSendExt(id, payload, 8)) {
    digitalWrite(LED_PIN, !digitalRead(LED_PIN));
  }
}

void setup() {
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, HIGH);

  Serial.begin(115200);
  delay(500);

  relaysInit();
  interlockInit();
  interlockPrev = interlockActive();

  if (!fdcanGemInit()) {
    Serial.println("FDCAN init FAIL");
    while (true) {
      digitalWrite(LED_PIN, !digitalRead(LED_PIN));
      delay(100);
    }
  }

  Serial.println("GEM BMC emu H503 v4.2 OK");
  Serial.println("CAN 250k ext, SA=0xF3");
  Serial.print("Interlock PA3: ");
  Serial.println(interlockPrev ? "active" : "idle");

  last10ms = last100ms = last1s = millis();
  digitalWrite(LED_PIN, LOW);
}

void loop() {
  const uint32_t now = millis();

  pollInterlock();

  if (now - last10ms >= 10) {
    last10ms = now;
    sendExt(ID_EF3, &BmcGenerator::nextEf3);
  }

  if (now - last100ms >= 100) {
    last100ms = now;
    sendExt(ID_0FF3, &BmcGenerator::next0ff3);
    sendExt(ID_10, &BmcGenerator::next10);
    sendExt(ID_11, &BmcGenerator::next11);
    sendExt(ID_12, &BmcGenerator::next12);
  }

  if (now - last1s >= 1000) {
    last1s = now;
    sendExt(ID_DM1, &BmcGenerator::nextDm1);
    digitalWrite(LED_PIN, !digitalRead(LED_PIN));
  }
}
