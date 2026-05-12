# CloverDrone — UAV Control & FPV Module

## What Is CloverDrone?

CloverDrone is MyClover.Tech's UAV (drone) control and FPV video module. It brings drone flight control, mission planning, live video, and AI-powered video analysis into the CloverStack platform.

Think of it as mission control for drones, built by people who actually understand IT infrastructure. Not a toy — this is built on production-grade open-source projects used by commercial drone operators worldwide.

## Core Capabilities

### Flight Control & Ground Station
- **MAVLink + MAVProxy** — the universal drone communication protocol. Works with ArduPilot, PX4, and most commercial flight controllers
- **QGroundControl** — full ground station UI with mission planning, telemetry, waypoints, geofencing, and parameter tuning
- **DroneKit-Python** — Python SDK for scripting autonomous missions, custom flight logic, and CloverStack automation integration

### FPV & Video
- **OpenHD** — low-latency HD video over Wi-Fi, designed for long-range FPV
- **WFB-ng (WiFi Broadcast next gen)** — raw Wi-Fi packet injection for ultra-low latency video
- **StreamServer integration** — pipe FPV feeds directly into StreamServer for recording, multi-viewer, and remote observation
- **WebRTC bridge** — browser-based FPV viewing from any device, anywhere

### AI Integration
- **YOLO/object detection** on Edge Pro or Citadel hardware for real-time video analysis
- **Automated survey, inspection, and mapping missions** via DroneKit scripts
- **Chappie AI** can analyze drone telemetry for anomaly detection and preventive maintenance

## How It Fits the Stack

CloverDrone isn't standalone — it's deeply integrated with CloverStack:

- **Puck/Edge** → Ground station controller (runs QGroundControl + MAVProxy + video receiver)
- **Edge Pro/Citadel** → Mission control server (DroneKit automation, AI video analysis, StreamServer recording)
- **Field Laptop** → Mobile ground station for field operations
- **CloverMesh** → Multi-drone fleet management across distributed nodes
- **StreamServer** → Record and live-stream all FPV feeds
- **NetMon** → Monitor drone network links and telemetry health

## Pricing

### Software Tiers
- **CloverDrone Pilot — $29/month** — 1 drone, ground station, FPV video, basic mission planning
- **CloverDrone Fleet — $79/month** — unlimited drones, AI video analysis, automation scripting, StreamServer integration
- **CloverDrone Enterprise — $149/month** — fleet + BVLOS operations, compliance logging, multi-site mesh

### Hardware Bundles
- **Drone Ground Station Kit — $1,299** — Edge Pro + gamepad controller + FPV screen + antennas. QGroundControl and CloverDrone pre-installed. Includes 1-year Pilot license.
- **Field Drone Pack — $3,999** — Citadel Field Laptop pre-loaded with QGroundControl + CloverDrone + long-range antenna kit. The ultimate mobile ground station.

## Use Cases

1. **Site surveys** — Automated flyover and mapping for construction, agriculture, or infrastructure inspection
2. **Security patrol** — Scheduled drone patrols with AI object detection, integrated with Wazuh alerts
3. **Infrastructure inspection** — Inspect towers, roofs, solar panels without climbing. AI spots damage automatically
4. **Search & rescue** — Real-time video feed to multiple viewers via StreamServer
5. **Agriculture** — Crop monitoring, NDVI mapping, precision agriculture integration

## Technical Details

- **Supported protocols**: MAVLink v1/v2, MAVLink over TCP/UDP/Serial
- **Compatible flight controllers**: ArduPilot (Pixhawk, Cube, etc.), PX4, any MAVLink-compatible FC
- **Video codecs**: H.264, H.265 (hardware decode on Edge Pro/Citadel)
- **Latency**: <100ms with OpenHD/WFB-ng, <200ms with WebRTC bridge
- **Range**: Depends on radio hardware — OpenHD supports multi-kilometer range with proper antennas

## Open-Source Credits

CloverDrone is built on these outstanding projects. We appreciate every contributor:
- **QGroundControl** (Apache 2.0) — Dronecode Foundation
- **ArduPilot / MAVLink** (LGPL/MIT) — ArduPilot community
- **DroneKit-Python** (Apache 2.0) — 3D Robotics / community
- **OpenHD** (GPL) — OpenHD project
- **WFB-ng** (GPL) — Vasily Evseenko

> Fun fact: The same MAVLink protocol CloverDrone uses also flies on Mars. NASA's Ingenuity helicopter uses a MAVLink-compatible system. So technically, CloverStack is Mars-tested technology. Kind of.
