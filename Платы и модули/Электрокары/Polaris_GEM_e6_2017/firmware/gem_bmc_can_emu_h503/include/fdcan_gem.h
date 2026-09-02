#pragma once

#include <cstdint>

// FDCAN1 classic CAN 250 kbit/s, extended ID TX-only
bool fdcanGemInit();
bool fdcanGemSendExt(uint32_t id, const uint8_t *data, uint8_t len = 8);
