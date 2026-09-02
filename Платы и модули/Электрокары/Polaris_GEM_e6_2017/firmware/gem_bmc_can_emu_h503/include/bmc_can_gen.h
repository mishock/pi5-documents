#pragma once

#include <cstdint>
#include <cstring>

constexpr uint8_t CHARGER_HOLD = 10;

uint8_t xorChecksum(const uint8_t *data, uint8_t len);

class BmcGenerator {
 public:
  BmcGenerator();

  void nextEf3(uint8_t *out);
  void next0ff3(uint8_t *out);
  void next10(uint8_t *out);
  void next11(uint8_t *out);
  void next12(uint8_t *out);
  void nextDm1(uint8_t *out);

 private:
  void buildCharger();
  void advanceCharger();

  uint8_t iEf3_ = 0;
  uint8_t ctr11_ = 0x1F;
  uint8_t ctr12_ = 0x8F;
  uint8_t ctr3_ = 0xE7;
  uint8_t ctr4_ = 0xF8;
  uint8_t ctr3Step_ = 0;
  uint8_t hold0ff3_ = CHARGER_HOLD;
  uint8_t cur0ff3_[8];
};
