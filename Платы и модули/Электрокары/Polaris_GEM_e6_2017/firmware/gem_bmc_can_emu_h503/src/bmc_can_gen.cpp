#include "bmc_can_gen.h"

static const uint8_t EF3_HEARTBEAT[9][8] = {
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

static const uint8_t PAYLOAD_10[8] = {0xC8, 0x2F, 0x8F, 0xFF, 0xFF, 0x00, 0xC7, 0xAE};
static const uint8_t PAYLOAD_DM1[8] = {0x00, 0xFF, 0x00, 0x00, 0x00, 0x00, 0xFF, 0xFF};
static const uint8_t BASE_11[6] = {0x42, 0xC0, 0x52, 0xFD, 0xFF, 0x46};

uint8_t xorChecksum(const uint8_t *data, uint8_t len) {
  uint8_t c = data[0];
  for (uint8_t i = 1; i < len; i++) {
    c ^= data[i];
  }
  return c;
}

BmcGenerator::BmcGenerator() { buildCharger(); }

void BmcGenerator::buildCharger() {
  cur0ff3_[0] = 0xC6;
  cur0ff3_[1] = 0xB0;
  cur0ff3_[2] = 0x06;
  cur0ff3_[3] = ctr3_;
  cur0ff3_[4] = ctr4_;
  cur0ff3_[5] = 0xFF;
  cur0ff3_[6] = 0x7F;
  cur0ff3_[7] = xorChecksum(cur0ff3_, 7);
}

void BmcGenerator::advanceCharger() {
  ctr3Step_++;
  uint8_t delta = ((ctr3Step_ & 7) == 1) ? 0xAF : 0xB0;
  ctr3_ = static_cast<uint8_t>(ctr3_ + delta);
  if (ctr3Step_ % 3 == 0) {
    ctr4_--;
  }
  buildCharger();
}

void BmcGenerator::nextEf3(uint8_t *out) {
  memcpy(out, EF3_HEARTBEAT[iEf3_ % 9], 8);
  iEf3_++;
}

void BmcGenerator::next0ff3(uint8_t *out) {
  if (hold0ff3_ == 0) {
    advanceCharger();
    hold0ff3_ = CHARGER_HOLD;
  }
  hold0ff3_--;
  memcpy(out, cur0ff3_, 8);
}

void BmcGenerator::next10(uint8_t *out) { memcpy(out, PAYLOAD_10, 8); }

void BmcGenerator::next11(uint8_t *out) {
  memcpy(out, BASE_11, 6);
  out[6] = ctr11_;
  out[7] = xorChecksum(out, 7);
  ctr11_ = static_cast<uint8_t>(ctr11_ + 0x10);
}

void BmcGenerator::next12(uint8_t *out) {
  out[0] = out[1] = out[2] = out[3] = out[4] = 0xFF;
  out[5] = 0x00;
  out[6] = ctr12_;
  out[7] = static_cast<uint8_t>(0xFF - ctr12_);
  ctr12_ = static_cast<uint8_t>(ctr12_ + 0x10);
}

void BmcGenerator::nextDm1(uint8_t *out) { memcpy(out, PAYLOAD_DM1, 8); }
