# Tornado Air Conditioner Enhanced for Home Assistant

A feature-rich Home Assistant integration for Tornado and AUX Wi-Fi air conditioners.

This project is based on the excellent work of @romfreiman and extends the original integration with additional controls, improved synchronization and better stability.

---

## Features

### Climate
- Power
- HVAC mode
- Target temperature
- Fan mode
- Swing mode

### Additional switches
- Clean
- Anti Fungus
- Health
- Display
- Eco Mode
- Comfort Wind
- Auxiliary Heat
- Sleep
- Sleep DIY
- Child Lock
- Power Limit Enable

### Additional entities
- Power Limit slider (30–100%)
- Current temperature
- Target temperature
- Raw operating mode
- Raw fan mode

### Improvements
- Coordinator-based architecture
- Live synchronization with the Tornado app
- Automatic state refresh after changes
- Reduced cloud requests
- Improved timeout handling
- Better Home Assistant responsiveness

---

# Installation

## HACS (recommended)

1. Open HACS.
2. Open **Custom repositories**.
3. Add:

```
https://github.com/MarcDev01/tornado-aircon-enhanced
```

Category:

```
Integration
```

Install the integration and restart Home Assistant.

---

## Manual

Copy

```
custom_components/tornado
```

to

```
config/custom_components/
```

Restart Home Assistant.

---

# Configuration

Settings → Devices & Services → Add Integration

Fill in:

- Email
- Password
- Region

Done.

---

# Roadmap

Planned features:

- Native diagnostics
- Better error recovery
- Automatic cloud reconnect
- Horizontal swing support (where available)
- More device parameters
- Reduced cloud polling

---

# Credits

Original integration:
- @romfreiman

Based on:
- @maeek (ha-aux-cloud)
- @thewh1teagle (tornado-control)

Enhanced version:
- MarcDev01

---

# License

MIT License
