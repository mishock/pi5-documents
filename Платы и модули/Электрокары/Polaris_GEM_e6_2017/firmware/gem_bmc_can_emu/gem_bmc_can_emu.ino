/*
 * GEM e6 — эмулятор BMC (A2): CAN v4 + дискрет X3 (K5/K12/VCM/K7, interlock p11).
 * Плата: Arduino Nano + MCP2515/TJA1050 + 4× реле.
 */
#include <SPI.h>
#include <mcp2515.h>
#include "bmc_can_gen.h"
#include "hw_pins.h"

#define MCP2515_CS_PIN  10
#define MCP2515_CLOCK   MCP_8MHZ  // 16 МГц → MCP_16MHZ

#define CAN_BITRATE     CAN_250KBPS
#define LED_PIN          LED_BUILTIN

static const uint32_t CAN_ID_EF3  = 0x0CFF0EF3UL;
static const uint32_t CAN_ID_0FF3 = 0x0CFF0FF3UL;
static const uint32_t CAN_ID_10  = 0x0CFF10F3UL;
static const uint32_t CAN_ID_11  = 0x0CFF11F3UL;
static const uint32_t CAN_ID_12  = 0x0CFF12F3UL;
static const uint32_t CAN_ID_DM1  = 0x18FECAF3UL;

MCP2515 mcp2515(MCP2515_CS_PIN);
struct can_frame txFrame;
BmcGenerator gen;

unsigned long nextEf3 = 0;
unsigned long next0ff3 = 0;
unsigned long next10 = 0;
unsigned long next11 = 0;
unsigned long next12 = 0;
unsigned long nextDm1 = 0;

unsigned long lastLed = 0;
unsigned long lastInterlockMs = 0;
bool interlockPrev = false;

static inline bool due(unsigned long now, unsigned long target) {
  return (long)(now - target) >= 0;
}

bool sendExt(uint32_t id, const uint8_t *data) {
  txFrame.can_id = id | CAN_EFF_FLAG;
  txFrame.can_dlc = 8;
  memcpy(txFrame.data, data, 8);
  return mcp2515.sendMessage(&txFrame) == MCP2515::ERROR_OK;
}

void pollInterlock() {
  const unsigned long now = millis();
  if (now - lastInterlockMs < 100) {
    return;
  }
  lastInterlockMs = now;
  const bool active = interlockActive();
  updateDiscreteOutputs();
  if (active != interlockPrev) {
    interlockPrev = active;
    Serial.print(F("Interlock p11: "));
    Serial.println(active ? F("ON → K7 ON") : F("OFF → K7 OFF"));
  }
}

void setup() {
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);

  relaysInit();
  interlockInit();
  interlockPrev = interlockActive();

  Serial.begin(115200);
  while (!Serial && millis() < 3000) {
  }

  Serial.println(F("GEM BMC emu v4.2 — CAN + K5/K12/VCM ON, K7 по interlock"));
  Serial.print(F("Interlock D6: "));
  Serial.println(interlockPrev ? F("active") : F("idle"));

  mcp2515.reset();
  if (mcp2515.setBitrate(CAN_BITRATE, MCP2515_CLOCK) != MCP2515::ERROR_OK) {
    Serial.println(F("ERR: setBitrate"));
  }
  if (mcp2515.setNormalMode() != MCP2515::ERROR_OK) {
    Serial.println(F("ERR: setNormalMode"));
  }

  const unsigned long t = millis() + 3000UL;
  nextEf3 = t;
  next0ff3 = t;
  next10 = t + 2;
  next11 = t + 4;
  next12 = t + 6;
  nextDm1 = t;

  Serial.println(F("CAN TX через 3 с…"));
}

void loop() {
  const unsigned long now = millis();

  pollInterlock();

  if (due(now, nextEf3)) {
    uint8_t buf[8];
    gen.nextEf3(buf);
    sendExt(CAN_ID_EF3, buf);
    nextEf3 += 10;
  }

  if (due(now, next0ff3)) {
    uint8_t buf[8];
    gen.next0ff3(buf);
    sendExt(CAN_ID_0FF3, buf);
    next0ff3 += 100;
  }

  if (due(now, next10)) {
    uint8_t buf[8];
    gen.next10(buf);
    sendExt(CAN_ID_10, buf);
    next10 += 100;
  }

  if (due(now, next11)) {
    uint8_t buf[8];
    gen.next11(buf);
    sendExt(CAN_ID_11, buf);
    next11 += 100;
  }

  if (due(now, next12)) {
    uint8_t buf[8];
    gen.next12(buf);
    sendExt(CAN_ID_12, buf);
    next12 += 100;
  }

  if (due(now, nextDm1)) {
    uint8_t buf[8];
    gen.nextDm1(buf);
    sendExt(CAN_ID_DM1, buf);
    nextDm1 += 1000;
  }

  if (due(now, lastLed + 1000)) {
    lastLed = now;
    digitalWrite(LED_PIN, !digitalRead(LED_PIN));
  }
}
