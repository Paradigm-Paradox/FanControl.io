# Home Assistant Add-on: SprinklerController-io

An intelligent irrigation and sprinkler management system built to operate seamlessly with Home Assistant and distributed **ESP32** field microcontrollers.

---

## Features

- **ESP32 Edge Microcontroller Support**: Native compatibility with Wi-Fi, wired Ethernet (WT32-ETH01, Olimex PoE), and Bluetooth Low Energy (BLE) soil sensor bridges.
- **Fail-Safe Edge Protection**: Built-in ESP32 auto-off safety timers prevent yard flooding even if Wi-Fi or Home Assistant disconnects.
- **Cycle & Soak Scheduling**: Splits runtimes into brief watering pulses interspersed with soak periods to eliminate runoff on slopes or dense clay soil.
- **Smart Weather Adjustments**: Evapotranspiration (ET) calculations and automatic rain/freeze delays.
- **Hydraulic Pressure Watchdog**: Limits concurrent active valves to protect domestic water pressure and flow rates.
- **Ingress Web Dashboard**: Modern control panel embedded directly into the Home Assistant interface.

---

## ESP32 Hardware Options

### 1. Wired Ethernet & PoE (Recommended for Outdoor Valve Manifolds)
- **WT32-ETH01**: Compact ESP32 board with 10/100 Mbps RJ45 Ethernet port.
- **Olimex ESP32-POE / ESP32-POE-ISO**: Power-over-Ethernet (PoE) board providing single-cable power and data.

### 2. Standard Wi-Fi ESP32
- **NodeMCU-32S / ESP32-WROOM-32 / D1 Mini ESP32**: Inexpensive Wi-Fi boards paired with 4-, 8-, or 16-channel 24VAC relay modules.

### 3. Bluetooth Low Energy (BLE)
- Integrated BLE scanning for battery-powered wireless soil moisture sensors (e.g. Xiaomi MiFlora / Qingping).

---

## Installation & Setup

1. Add this repository URL to your Home Assistant Add-on Store:
   `https://github.com/Paradigm-Paradox/SprinklerController-io`
2. Locate **SprinklerController-io** and click **Install**.
3. Configure your zones, switches, and weather sensors in the **Configuration** tab.
4. Flash your ESP32 boards using the included templates in the `templates/esphome/` directory.
5. Click **Start** and open the **Web UI**!
