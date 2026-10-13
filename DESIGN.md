# GreenhouseControl-io: Design & Architecture Document

## Overview
GreenhouseControl-io is an edge-native Home Assistant Add-on providing automated climate, vapor pressure deficit (VPD) regulation, smart irrigation, and supplemental lighting management for hobbyist and commercial greenhouses.

## Core Features
1. **Precision Climate & VPD Regulation**:
   - Continuous calculation of saturation vapor pressure, air vapor pressure, and vapor pressure deficit (kPa).
   - Canopy temperature leaf offset calculation or direct thermal sensor input.
   - Dynamic stage targeting: Seedling (0.4-0.8 kPa), Vegetative (0.8-1.1 kPa), Flowering (1.1-1.5 kPa).
   - Coordinated ventilation (ridge/side louvers), exhaust fans, misting/humidifiers, and heating.
2. **Smart Irrigation & Fertigation**:
   - VWC (Volumetric Water Content) soil moisture threshold triggers.
   - Integrated safety run-time watchdogs preventing catastrophic overwatering.
   - Low-reservoir lockouts and flood sensors.
3. **Lighting & Photoperiod Control**:
   - Daily Light Integral (DLI) tracking from PAR / Lux sensors.
   - Supplemental light dimming and photoperiod schedule automation.
4. **Home Assistant Ecosystem Integration**:
   - Built-in Ingress UI accessible directly inside the Home Assistant sidebar.
   - Real-time entity reading and service calls via the Home Assistant Supervisor Core API.
   - MQTT auto-discovery for standalone ESPHome / Tasmota greenhouse microcontrollers.

## Project Structure
- `repository.yaml` — Repository manifest for adding to Home Assistant Add-on Store.
- `greenhouse_control/` — The complete add-on distribution.
  - `config.yaml` — Add-on definition, options schema, and ingress settings.
  - `Dockerfile` — Production multi-arch container definition.
  - `app/` — Core Python FastAPI backend and responsive Ingress web dashboard.
