/*
 * Генератор CAN-кадров BMC (SA=0xF3) — алгоритм v4 (GEM e6).
 * Порт с Pi: Платы и модули/Электрокары/Polaris_GEM_e6_2017/scripts/can-bmc-emulate.py
 */
#pragma once

#include <Arduino.h>

static const uint8_t CHARGER_HOLD = 10;

static const uint8_t EF3_HEARTBEAT[][8] PROGMEM = {
  {0xFA, 0x7C, 0x8E, 0x04, 0xD2, 0xA4, 0x0E, 0x74},
  {0xFA, 0x7C, 0x8F, 0x04, 0xD2, 0xA4, 0x0E, 0x75},
  {0xFA, 0x7C, 0x8E, 0x04, 0xD2, 0xA4, 0x0E, 0x74},
  {0xFA, 0x7C, 0x8F, 0x04, 0xD2, 0xA4, 0x0E, 0x75},
  {0xFA, 0x7C, 0x8E, 0x04, 0xD2, 0xA4, 0x0E, 0x74},
  {0xFA, 0x7C, 0x8F, 0x04, 0xD2, 0xA4, 0x0E, 0x75},
  {0xFA, 0x7C, 0x8E, 0x04, 0xD2, 0xA4, 0x0E, 0x74},
  {0xFB, 0x7C, 0x8E, 0x04, 0xD2, 0xA4, 0x0E, 0x75},
  {0xFA, 0x7C, 0x8E, 0x04, 0xD2, 0xA4, 0x0E, 0x74},
};
static const uint8_t EF3_COUNT = 9;

static const uint8_t PAYLOAD_10[8] PROGMEM = {
  0xC8, 0x2F, 0x8F, 0xFF, 0xFF, 0x00, 0xC7, 0xAE};

static const uint8_t PAYLOAD_DM1[8] PROGMEM = {
  0x00, 0xFF, 0x00, 0x00, 0x00, 0x00, 0xFF, 0xFF};

static const uint8_t BASE_11[6] PROGMEM = {
  0x42, 0xC0, 0x52, 0xFD, 0xFF, 0x46};

static inline uint8_t xorChecksum(const uint8_t *data, uint8_t len) {
  uint8_t c = data[0];
  for (uint8_t i = 1; i < len; i++) {
    c ^= data[i];
  }
  return c;
}

struct BmcGenerator {
  uint8_t iEf3 = 0;

  uint8_t ctr11 = 0x1F;
  uint8_t ctr12 = 0x8F;

  uint8_t ctr3 = 0xE7;
  uint8_t ctr4 = 0xF8;
  uint8_t ctr3Step = 0;
  uint8_t hold0ff3 = CHARGER_HOLD;
  uint8_t cur0ff3[8];

  BmcGenerator() { buildCharger(); }

  void buildCharger() {
    cur0ff3[0] = 0xC6;
    cur0ff3[1] = 0xB0;
    cur0ff3[2] = 0x06;
    cur0ff3[3] = ctr3;
    cur0ff3[4] = ctr4;
    cur0ff3[5] = 0xFF;
    cur0ff3[6] = 0x7F;
    cur0ff3[7] = xorChecksum(cur0ff3, 7);
  }

  void advanceCharger() {
    ctr3Step++;
    uint8_t delta = ((ctr3Step & 7) == 1) ? 0xAF : 0xB0;
    ctr3 = (uint8_t)(ctr3 + delta);
    if (ctr3Step % 3 == 0) {
      ctr4--;
    }
    buildCharger();
  }

  void nextEf3(uint8_t *out) {
    memcpy_P(out, EF3_HEARTBEAT[iEf3 % EF3_COUNT], 8);
    iEf3++;
  }

  void next0ff3(uint8_t *out) {
    if (hold0ff3 == 0) {
      advanceCharger();
      hold0ff3 = CHARGER_HOLD;
    }
    hold0ff3--;
    memcpy(out, cur0ff3, 8);
  }

  void next10(uint8_t *out) { memcpy_P(out, PAYLOAD_10, 8); }

  void next11(uint8_t *out) {
    memcpy_P(out, BASE_11, 6);
    out[6] = ctr11;
    out[7] = xorChecksum(out, 7);
    ctr11 = (uint8_t)(ctr11 + 0x10);
  }

  void next12(uint8_t *out) {
    out[0] = out[1] = out[2] = out[3] = out[4] = 0xFF;
    out[5] = 0x00;
    out[6] = ctr12;
    out[7] = (uint8_t)(0xFF - ctr12);
    ctr12 = (uint8_t)(ctr12 + 0x10);
  }

  void nextDm1(uint8_t *out) { memcpy_P(out, PAYLOAD_DM1, 8); }
};
