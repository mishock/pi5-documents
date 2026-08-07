#!/bin/bash
# Local BlueZ alias for ANT BMS (does not change advertised Name on the module).
# Serial suffix = last 4 hex digits of MAC AA:BB:CC:91:23:45 → 2345
set -euo pipefail
CLASSIC=AA:BB:CC:91:23:45
BLE=AA:BB:CC:92:23:45
SUFFIX=2345

classic_path="/org/bluez/hci0/dev_${CLASSIC//:/_}"
ble_path="/org/bluez/hci0/dev_${BLE//:/_}"

dbus-send --system --print-reply --dest=org.bluez \
  "$classic_path" org.freedesktop.DBus.Properties.Set \
  string:org.bluez.Device1 string:Alias variant:string:"BMS-ANT24C-${SUFFIX}" >/dev/null

dbus-send --system --print-reply --dest=org.bluez \
  "$ble_path" org.freedesktop.DBus.Properties.Set \
  string:org.bluez.Device1 string:Alias variant:string:"ANT-BLE24C-${SUFFIX}" >/dev/null

echo "Alias set:"
bluetoothctl info "$CLASSIC" | egrep 'Name|Alias|Address' || true
bluetoothctl info "$BLE" | egrep 'Name|Alias|Address' || true
