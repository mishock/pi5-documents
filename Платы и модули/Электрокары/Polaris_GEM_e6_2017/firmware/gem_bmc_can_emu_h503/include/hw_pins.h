#pragma once

#include <Arduino.h>

// PB MCU01 H503A — см. PINOUT.md (проверить по вашей ревизии платы)

// Реле: HIGH = вкл (модули с опто, active-high IN)
#define RELAY_ACTIVE_LOW  0

#define RELAY_K5_PIN      PA0   // BMC X3 p4 → K5 DC/DC Relay #1
#define RELAY_K12_PIN     PA1   // BMC X3 p5 → K12 DC/DC Relay #2
#define RELAY_VCM_PIN     PA2   // BMC X3 p12 → A1 VCM +12 V
#define RELAY_K7_PIN      PA4   // BMC X3 p3 → K7 Delta-Q Charger Relay GND
#define PIN_INTERLOCK_IN  PA3   // BMC X3 p11 interlock (+12 V через оптопару)
#define LED_PIN           PC13

#if RELAY_ACTIVE_LOW
#define RELAY_ON   LOW
#define RELAY_OFF  HIGH
#else
#define RELAY_ON   HIGH
#define RELAY_OFF  LOW
#endif

inline void interlockInit() { pinMode(PIN_INTERLOCK_IN, INPUT); }

inline bool interlockActive() { return digitalRead(PIN_INTERLOCK_IN) == HIGH; }

// SM §8.28–8.30: K5/K12/V-Out ON при ключе или зарядке; K7 (p3) ON при зарядке
inline void updateDiscreteOutputs() {
  digitalWrite(RELAY_K5_PIN, RELAY_ON);
  digitalWrite(RELAY_K12_PIN, RELAY_ON);
  digitalWrite(RELAY_VCM_PIN, RELAY_ON);
  digitalWrite(RELAY_K7_PIN, interlockActive() ? RELAY_ON : RELAY_OFF);
}

inline void relaysInit() {
  pinMode(RELAY_K5_PIN, OUTPUT);
  pinMode(RELAY_K12_PIN, OUTPUT);
  pinMode(RELAY_VCM_PIN, OUTPUT);
  pinMode(RELAY_K7_PIN, OUTPUT);
  digitalWrite(RELAY_K5_PIN, RELAY_OFF);
  digitalWrite(RELAY_K12_PIN, RELAY_OFF);
  digitalWrite(RELAY_VCM_PIN, RELAY_OFF);
  digitalWrite(RELAY_K7_PIN, RELAY_OFF);
  delay(20);
  updateDiscreteOutputs();
}
