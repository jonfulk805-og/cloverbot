# CloverMesh Radio — LoRa Mesh Networking

## What Is It?
CloverMesh Radio brings Meshtastic-powered LoRa mesh networking to the CloverStack. Off-grid encrypted text messaging, GPS tracking, and sensor telemetry — no cell towers, no internet, no monthly carrier fees. Just radio waves and math.

Each node is a relay. The mesh builds and heals itself. Drop nodes across a site, and they automatically find the best multi-hop path. Range? We're talking 10+ miles per hop, 100+ miles line of sight with good antennas. LoRa is basically radio magic — spread-spectrum modulation below the noise floor.

## Key Features

### AES-256 Encryption
Every message encrypted end-to-end by default. Private channels with pre-shared keys. Your mesh traffic stays private.

### GPS Tracking
Every node broadcasts position. Real-time map of all devices, people, and assets. Set geofencing alerts when something wanders where it shouldn't.

### Self-Healing Mesh
Multi-hop routing finds the best path automatically. Nodes join and leave without breaking anything. The network adapts in seconds, not minutes.

### Ultra-Low Power
LoRa nodes run for days on small batteries, weeks on solar panels. Perfect for remote deployments where the nearest power outlet is miles away.

### MQTT Bridge
Bridge LoRa mesh traffic to IP networks via MQTT. Pipe telemetry straight into NetMon dashboards, SentryLog for audit logging, or any monitoring system.

### Python API
Full `meshtastic` Python package for scripting. Automate node management, send messages programmatically, integrate with CloverBot and Chappie AI.

### Linux Native Daemon
`meshtasticd` runs on any CloverStack appliance. Turn your Puck, Edge, or Citadel into a Meshtastic gateway node bridging LoRa ↔ IP networks.

## How It Fits the Stack

- **NetMon** — Monitor node health, signal quality, hop count, battery levels via MQTT bridge
- **SentryLog** — Log all mesh traffic for compliance/audit: message routing, node joins/leaves, signal analytics
- **CloverDrone** — LoRa telemetry link for long-range drone ops where Wi-Fi dies. GPS position relay, mission status, emergency RTH commands
- **Chappie AI** — Anomaly detection on mesh telemetry, predict node failures, optimize relay placement
- **Edge Devices (Puck/Edge/Edge Pro)** — Run `meshtasticd` directly; any CloverStack appliance becomes a LoRa gateway
- **Field Laptop** — Mobile mesh gateway + map display for field ops in zero-infrastructure zones

## Pricing

| Plan | Price | What You Get |
|------|-------|--------------|
| **Radio** | $19/mo | Up to 10 LoRa nodes, MQTT bridge, NetMon integration, GPS tracking, encrypted channels |
| **Field** | $49/mo | Unlimited nodes, CloverDrone telemetry relay, SentryLog compliance logging, geofencing, Python API |
| **Enterprise** | $99/mo | Multi-site mesh federation, compliance audit, custom private channels, full REST API, priority support |

## Hardware Kits

### Meshtastic Node Kit (5-pack) — $199
- 5× Heltec V3 or RAK WisBlock nodes
- Pre-flashed Meshtastic firmware
- Antennas + weatherproof cases
- Quick-start guide + channel config
- 1-year Radio license included

### Long-Range Relay Node — $149
- Solar-powered outdoor enclosure
- High-gain antenna (10+ mile range)
- Pre-configured as relay/router
- Mount-anywhere bracket kit
- Rated for -40°F to 140°F

## Use Cases

1. **Construction & Mining** — Crew comms + asset tracking with zero infrastructure
2. **Forestry & Agriculture** — Sensor mesh across thousands of acres at $35/node
3. **Emergency & Disaster** — Self-healing comms when cell towers are down
4. **Campus & Warehouse** — Extend monitoring into RF-dead zones
5. **Drone Fleet Ops** — LoRa command & telemetry for BVLOS operations
6. **Utility & SCADA** — Remote monitoring where running cable is impractical

## Supported Hardware
- Heltec V3 (ESP32-S3 + SX1262 LoRa)
- RAK WisBlock (nRF52840 + LoRa)
- T-Beam (ESP32 + GPS + LoRa)
- LilyGO T-Deck (ESP32-S3 + keyboard + screen)
- Any Meshtastic-compatible device
- CloverStack appliances via `meshtasticd` Linux daemon

## Open Source Credits
- **Meshtastic Firmware** — GPL 3.0, by the Meshtastic community
- **Meshtastic Python API** — Apache 2.0, by the Meshtastic project
- **LoRa** — modulation technology by Semtech
- **Heltec Automation** — ESP32 + LoRa hardware
- **RAKwireless** — WisBlock modular IoT hardware

## Fun Facts
The Meshtastic community world record for a single LoRa hop is over 254 km (158 miles). That's farther than most cell towers can dream of. Done with a $30 radio and a good antenna. The physics of LoRa are genuinely wild.

*CloverMesh Radio — because sometimes the best network is one that doesn't need infrastructure at all.* 📡
