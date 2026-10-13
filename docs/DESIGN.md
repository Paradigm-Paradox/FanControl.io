# SprinklerController-io Design Specification

## 1. System Vision & Scope
SprinklerController-io is designed to bridge local hardware (relays, valves, flow meters) and Home Assistant intelligence, offering autonomous scheduling and weather-reactive irrigation control.

---

## 2. Core Architecture Options

### A. Add-on Architecture
- **Ingress Web App**: A lightweight frontend (e.g., Vue/React or Svelte + FastAPI/Go/Node backend) embedded within the Home Assistant sidebar.
- **HA Integration Layer**:
  - Integration via Home Assistant WebSocket API / Long-Lived Access Token or Ingress token.
  - MQTT integration (publishing state entities, switches, sensors, timers).
- **Core Engine**:
  - Scheduler (Cron / rule-based / solar-event based).
  - Safety Supervisor (Max run duration, conflict locks, rain sensor interrupts).
  - Weather Evaluator (ET calculation, Open-Meteo / local weather station integration).

---

## 3. Key Subsystems & Design Questions

### 3.1 Hardware Interfacing
- **Target Hardware**:
  - [ ] ESPHome / Tasmota microcontrollers (relays over MQTT/Native API)
  - [ ] Local Raspberry Pi / SBC GPIO relays
  - [ ] Commercial controller bridges (Rain Bird, Rachio, Hunter, B-hyve)
  - [ ] Standard USB / Serial / I2C relay modules

### 3.2 Zone Management & Safety
- **Zones & Valves**:
  - Multi-zone sequential vs concurrent watering restrictions.
  - Master valve / Booster pump delay and lead times.
  - Cycle and Soak: Pulse watering for heavy soil / sloped areas to prevent runoff.
- **Safety Interlocks**:
  - Maximum runtime watchdog per zone.
  - Rain sensor hard-wired digital input or HA binary sensor.
  - Freeze lockout (e.g. ambient temp < 37°F / 3°C).

### 3.3 Weather & Water Budgeting
- **Calculations**:
  - Fixed duration vs. Evapotranspiration (ET) / Solar radiation / Soil moisture feedback.
  - Dynamic scaling factor (e.g. % adjustment based on season or 7-day rolling rain forecast).

### 3.4 Data & Persistence
- SQLite or lightweight JSON/YAML store inside the container volume (`/data`).
- History logging: runtime per zone, estimated water volume (flow meter integration).

---

## 4. Proposed Milestone Roadmap
1. **Phase 1: Architecture & Requirements Definition**
2. **Phase 2: HA Add-on Skeleton (`config.yaml`, `Dockerfile`, Web UI stub)**
3. **Phase 3: Core Controller Engine & State Machine**
4. **Phase 4: Scheduler & Weather Logic**
5. **Phase 5: Ingress UI & Testing**
