# SprinklerController-io: Design & Architecture Document

## 1. Overview
**SprinklerController-io** is an intelligent irrigation management system built as a Home Assistant Add-on. It connects Home Assistant's automation engine to distributed **ESP32** field microcontrollers (over Wi-Fi, Ethernet, and Bluetooth) to control 24VAC solenoid valves, pumps, flow meters, and environmental sensors with edge-level safety.

---

## 2. ESP32 Microcontroller Architecture

The ESP32 family (Espressif Systems) acts as the field execution hardware:

```
+-----------------------------------------------------------------------------------+
|                           Home Assistant Core / Supervisor                        |
|                                                                                   |
|    +-------------------------------------------------------------------------+    |
|    |                      SprinklerController-io Add-on                      |    |
|    |  - Scheduling Engine (ET weather model, rain delays, freeze lockout)   |    |
|    |  - Cycle & Soak Sequencer (pulse watering, runoff prevention)           |    |
|    |  - Hydraulic Management (Max concurrent zones, master valve interlock)  |    |
|    |  - Ingress Web UI & ESP32 Blueprint Generator                          |    |
|    +-----------------------------------+-------------------------------------+    |
+----------------------------------------|------------------------------------------+
                                         | (Native HA API / MQTT)
           +-----------------------------+-----------------------------+
           |                                                           |
+----------v-----------------------------+       +---------------------v--------------------+
|  ESP32 Edge Node: Ethernet / PoE       |       |  ESP32 Edge Node: Wi-Fi + BLE Gateway    |
|  (e.g., WT32-ETH01 / Olimex POE)       |       |  (e.g., ESP32-WROOM-32 / ESP32-S3)       |
|                                        |       |                                          |
|  Hardware Features:                    |       |  Hardware Features:                      |
|  - 10/100 Mbps RJ45 Wired Ethernet     |       |  - 2.4 GHz 802.11 b/g/n Wi-Fi            |
|  - 4 to 16 Relay Channels (24VAC)      |       |  - Bluetooth Low Energy (BLE) tracker    |
|  - Hardware turn-off watchdog timers   |       |  - Zone Relays + Pump Control            |
|  - Flow Meter Pulse Counter (GPIO)     |       |  - Wireless Soil Moisture Probes (BLE)   |
|  - NC Rain Sensor Hardware Cutoff      |       |  - Pressure Transducer (0-100 PSI)       |
+----------------------------------------+       +------------------------------------------+
```

### 2.1 Supported ESP32 Hardware Profiles
1. **Wired Ethernet & PoE Boards** *(Ideal for valve boxes & outdoor manifolds)*:
   - **WT32-ETH01**: Low-cost ESP32 with LAN8720 PHY Ethernet.
   - **Olimex ESP32-POE / ESP32-POE-ISO**: Power-over-Ethernet eliminates separate AC/DC power adapters.
   - **LilyGO T-ETH-Lite**: Modern Ethernet board with microSD and expansion pins.
2. **Wi-Fi Relay Boards**:
   - ESP32-WROOM-32 paired with optocoupled 4/8/16 relay boards or dedicated ESP32 relay modules (e.g. Kincony KC868, LilyGO T-Relay).
   - ESP32-S3 / C3 compact modules.
3. **Bluetooth Low Energy (BLE) Integration**:
   - Uses ESP32's onboard BLE radio as an active BLE listener.
   - Collects moisture, soil temperature, and battery telemetry from Xiaomi Mi Flora (HHCCJCY01HHCC), Tuya BLE, or Qingping garden probes directly without needing external BLE hubs.

### 2.2 Edge-Level Safety Watchdog
To prevent catastrophic water damage or pool flooding if network connection or Home Assistant fails:
- **Autonomous Max Runtime Interlock**: Every relay in the ESP32 firmware includes an internal hardware shut-off countdown (e.g., 30 minutes). If no command arrives, the ESP32 automatically de-energizes the solenoid.
- **Mutual Exclusion Interlock**: Hardware and firmware mutual exclusion ensures only one high-draw zone valve opens at a time if limited by water supply volume.
- **Physical Rain Sensor Interlock**: Digital input directly tied to a physical rain switch; when tripped, hardware shuts off all irrigation relays instantly.

---

## 3. Core Software Modules (Add-on Engine)

### 3.1 Zone Scheduler & "Cycle and Soak"
- **Cycle & Soak**: Instead of watering a single zone for 30 consecutive minutes, the engine splits watering into cycles (e.g., three 10-minute cycles separated by 20-minute soak intervals), allowing water to absorb into hard or sloped ground.
- **Master Valve & Pump Staging**: Configurable lead time (open master valve 5 seconds before zone valve) and lag time to prevent hydraulic water hammer and dry pump operation.

### 3.2 Dynamic Weather Adaptation
- **Evapotranspiration (ET)**: Uses FAO-56 Penman-Monteith methodology or solar radiation + temperature heuristics to calculate daily water loss.
- **Rain Delay**: Pauses irrigation if rainfall in the past 24-48 hours exceeds threshold, or if future precipitation probability is high.
- **Freeze Lockout**: Automatically inhibits watering when ambient temperature drops below 3°C (37°F).

### 3.3 Hydraulic Diagnostics & Leak Detection
- **Pulse-Counter Flow Monitoring**: Measures real-time Gallons/Liters Per Minute (GPM/LPM).
- **Leak Alarms**: Triggers instant notification and shuts master valve if flow is detected while all zones are idle.
- **Pipe Burst / Clog Alerts**: Compares actual GPM against zone baselines.

---

## 4. Ingress Dashboard & Blueprint Generator
- Embedded Web UI accessible from Home Assistant sidebar.
- One-click ESPHome YAML generator for flashing ESP32 Wi-Fi and Ethernet boards.
- Interactive timeline, manual valve test buttons, and historical water consumption graphs.
