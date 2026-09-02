/*
 * Пины эмулятора BMC (A2) — Arduino Nano.
 * См. PINOUT.md и WIRING_REFERENCE.md (X3 p3/p4/p5/p11/p12).
 */
#pragma once

#include <Arduino.h>

// --- Реле (модули с оптоизоляцией) ---
// true = типовой модуль «LOW включает реле»; false = HIGH включает
#define RELAY_ACTIVE_LOW  1

#define RELAY_K5_PIN      3   // → BMC X3:p4 → K5 DC/DC Converter Relay #1 (GND coil)
#define RELAY_K12_PIN     4   // → BMC X3:p5 → K12 Fuse Box DC/DC Relay #2 (GND coil)
#define RELAY_VCM_PIN     5   // → BMC X3:p12 → A1 VCM +12 V (V-Out, через силовое реле +12V)
#define RELAY_K7_PIN      7   // → BMC X3:p3 → K7 Delta-Q Charger Relay GND

// --- Вход interlock (BMC X3:p11 Aux NO, +12 V от зарядника) ---
#define PIN_INTERLOCK_IN  6

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
