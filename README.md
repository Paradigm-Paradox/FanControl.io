# SprinklerController-io

An intelligent sprinkler and irrigation management system designed as a Home Assistant Add-on.

## Overview

**SprinklerController-io** provides precision irrigation scheduling, multi-zone control, weather-adaptive watering, and seamless integration with Home Assistant.

## Key Goals & Features (In Design)

- **Home Assistant Native**: Full Ingress support, entity discovery, and integration with HA events and automations.
- **Smart Weather Adaptation**: Automatic watering adjustments based on local precipitation, temperature, solar radiation, and evapotranspiration (ET).
- **Multi-Zone & Safety Management**:
  - Independent zone scheduling (cycle & soak to avoid runoff).
  - Master valve and pump control.
  - Hardware interlock protection (preventing concurrent valve opening beyond water supply pressure).
  - Automatic freeze protection and rain delay.
- **Hardware Agnostic**: Direct GPIO / relay boards, MQTT, or wireless ESPHome / Tasmota controller nodes.
- **Intuitive Web UI**: Real-time zone status, manual override, timeline scheduling, and water consumption estimates.

## Repository Structure

```text
├── docs/
│   └── DESIGN.md          # Architecture & functional specifications
├── .gitignore
└── README.md
```
