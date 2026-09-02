#include "fdcan_gem.h"

#include <Arduino.h>
extern "C" {
#include "stm32h5xx_hal.h"
}

// PB MCU01: FDCAN1 PB7=TX, PB8=RX → внешний TJA1050/SNP65 (обязателен!)
static FDCAN_HandleTypeDef hfdcan1;

static void fdcanClockEnable() {
  __HAL_RCC_FDCAN_CLK_ENABLE();
  __HAL_RCC_GPIOB_CLK_ENABLE();
}

static void fdcanGpioInit() {
  GPIO_InitTypeDef gpio = {};
  gpio.Mode = GPIO_MODE_AF_PP;
  gpio.Pull = GPIO_NOPULL;
  gpio.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
  gpio.Alternate = GPIO_AF9_FDCAN1;
  gpio.Pin = GPIO_PIN_7 | GPIO_PIN_8;
  HAL_GPIO_Init(GPIOB, &gpio);
}

bool fdcanGemInit() {
  fdcanClockEnable();
  fdcanGpioInit();

  hfdcan1.Instance = FDCAN1;
  hfdcan1.Init.ClockDivider = FDCAN_CLOCK_DIV1;
  hfdcan1.Init.FrameFormat = FDCAN_FRAME_CLASSIC;
  hfdcan1.Init.Mode = FDCAN_MODE_NORMAL;
  hfdcan1.Init.AutoRetransmission = ENABLE;
  hfdcan1.Init.TransmitPause = DISABLE;
  hfdcan1.Init.ProtocolException = DISABLE;
  // ~250 kbit/s при типичном FDCAN kernel clock H503 (подстроить при ошибках на шине)
  hfdcan1.Init.NominalPrescaler = 10;
  hfdcan1.Init.NominalSyncJumpWidth = 1;
  hfdcan1.Init.NominalTimeSeg1 = 13;
  hfdcan1.Init.NominalTimeSeg2 = 2;
  hfdcan1.Init.DataPrescaler = 1;
  hfdcan1.Init.DataSyncJumpWidth = 1;
  hfdcan1.Init.DataTimeSeg1 = 1;
  hfdcan1.Init.DataTimeSeg2 = 1;
  hfdcan1.Init.StdFiltersNbr = 0;
  hfdcan1.Init.ExtFiltersNbr = 0;
  hfdcan1.Init.TxFifoQueueMode = FDCAN_TX_FIFO_OPERATION;

  if (HAL_FDCAN_Init(&hfdcan1) != HAL_OK) {
    return false;
  }
  if (HAL_FDCAN_Start(&hfdcan1) != HAL_OK) {
    return false;
  }
  if (HAL_FDCAN_ActivateNotification(&hfdcan1, FDCAN_IT_BUS_OFF, 0) != HAL_OK) {
    return false;
  }
  return true;
}

bool fdcanGemSendExt(uint32_t id, const uint8_t *data, uint8_t len) {
  if (len > 8) {
    return false;
  }

  FDCAN_TxHeaderTypeDef hdr = {};
  hdr.Identifier = id & 0x1FFFFFFFU;
  hdr.IdType = FDCAN_EXTENDED_ID;
  hdr.TxFrameType = FDCAN_DATA_FRAME;
  static const uint32_t dlcMap[9] = {
      FDCAN_DLC_BYTES_0, FDCAN_DLC_BYTES_1, FDCAN_DLC_BYTES_2, FDCAN_DLC_BYTES_3,
      FDCAN_DLC_BYTES_4, FDCAN_DLC_BYTES_5, FDCAN_DLC_BYTES_6, FDCAN_DLC_BYTES_7,
      FDCAN_DLC_BYTES_8,
  };
  hdr.DataLength = dlcMap[len];
  hdr.ErrorStateIndicator = FDCAN_ESI_ACTIVE;
  hdr.BitRateSwitch = FDCAN_BRS_OFF;
  hdr.FDFormat = FDCAN_CLASSIC_CAN;
  hdr.TxEventFifoControl = FDCAN_NO_TX_EVENTS;
  hdr.MessageMarker = 0;

  return HAL_FDCAN_AddMessageToTxFifoQ(&hfdcan1, &hdr, const_cast<uint8_t *>(data)) == HAL_OK;
}

extern "C" void FDCAN1_IT0_IRQHandler(void) { HAL_FDCAN_IRQHandler(&hfdcan1); }

extern "C" void HAL_FDCAN_MspInit(FDCAN_HandleTypeDef *hfdcan) {
  if (hfdcan->Instance != FDCAN1) {
    return;
  }
  fdcanClockEnable();
  fdcanGpioInit();
  HAL_NVIC_SetPriority(FDCAN1_IT0_IRQn, 3, 0);
  HAL_NVIC_EnableIRQ(FDCAN1_IT0_IRQn);
}
