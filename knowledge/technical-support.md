# MyClover.Tech - Technical Support Knowledge
*For when things need fixing, optimizing, or explaining.*

---

## NetMon - Common Questions & Troubleshooting

### How does NetMon discover devices?
NetMon supports SNMP v1/v2c/v3 discovery, ICMP ping sweeps, and agent-based monitoring. Point it at a subnet, tell it your SNMP community strings, and let it go hunting. Most networks are fully mapped within minutes.

### My alerts are too noisy. How do I tune them?
Classic problem. Start by adjusting trigger thresholds -- a brief ping spike isn't an emergency. Use hysteresis: set the problem threshold at, say, 95% CPU for 5 minutes, and recovery at 80% for 5 minutes. That filters out the spikes and catches the real fires. Maintenance windows are your friend too -- suppress alerts during scheduled work.

*Pro tip: If everything is "critical," nothing is critical. Prioritize ruthlessly.*

### Can NetMon monitor cloud resources?
Yes. HTTP/HTTPS checks, API endpoint monitoring, SSL certificate expiration tracking, and cloud VM agent deployment. If it has an IP address or a URL, NetMon can keep an eye on it.

### What protocols does NetMon support?
SNMP v1/v2c/v3, ICMP, TCP/UDP port checks, HTTP/HTTPS, SSH, WMI (Windows), JMX (Java), IPMI, and custom script-based checks. If there's a way to query it, NetMon probably speaks the language.

---

## SentryLog - Common Questions & Troubleshooting

### How do I forward logs to SentryLog?
SentryLog accepts syslog (TCP/UDP 514), Beats protocol (for Filebeat/Winlogbeat), and direct API ingestion. For most setups:
- **Linux**: Configure rsyslog to forward to SentryLog's IP on port 514
- **Windows**: Install Winlogbeat, point it at SentryLog
- **Network gear**: Set the syslog server to SentryLog's IP in your device config
- **Docker**: Use the GELF or syslog logging driver

### My log storage is growing fast. What do I do?
Set up retention policies. Not every log needs to live forever. Typical setup: hot storage for 30 days, warm for 90, cold/archive for compliance. SentryLog handles index rotation automatically -- just tell it your policy.

*The logs will forgive you for deleting them after 90 days. Your storage budget will thank you.*

### Can SentryLog help with compliance?
Absolutely. Built-in report templates for common frameworks. Automated log collection and retention policies that satisfy auditors. Search and export capabilities for incident response. It won't make compliance fun, but it'll make it possible.

---

## Citadel Backup - Common Questions & Troubleshooting

### How does deduplication work?
Citadel Backup uses Restic's content-defined chunking. Files are split into variable-size chunks, hashed, and only unique chunks are stored. If you back up 100 VMs running the same OS, the shared OS files are stored once. Storage savings are typically 60-80% depending on data similarity.

### What's the 3-2-1 backup rule and does Citadel support it?
The 3-2-1 rule: 3 copies of your data, on 2 different types of media, with 1 copy offsite. Citadel Backup supports local NAS storage + cloud replication. Keep a local copy on the Citadel appliance (fast restores) and replicate to cloud S3-compatible storage (offsite). Rule followed.

*The 3-2-1 rule exists because "it's fine, the RAID will protect us" is a horror story, not a backup strategy.*

### My backup is slow. What gives?
Check these in order:
1. **Network bandwidth** -- is the source connected via gigabit? 100Mbps connections bottleneck quickly on large datasets.
2. **Source disk speed** -- spinning disks on the source can be the limiter, especially with lots of small files.
3. **First backup vs incremental** -- the initial backup is always the big one. Incrementals after that are fast because only changed chunks transfer.
4. **Encryption overhead** -- minimal on modern CPUs with AES-NI, but worth checking if you're on older hardware.

---

## AI Agent - Common Questions & Troubleshooting

### Which model should I pick?
Depends on your hardware and use case:
- **Puck (16GB)**: Phi-3 Mini or Llama 3.2 3B. Fast responses, good for basic Q&A and simple automation.
- **Edge (32GB)**: Llama 3.1 7B or Mistral 7B. Solid all-rounder. Handles most tasks well.
- **Edge Pro (64GB)**: Llama 3.1 13B or CodeLlama 13B. Better reasoning, longer context, code generation.
- **Citadel NAS / Rack**: Whatever fits your VRAM. GPU-accelerated inference makes larger models practical.

*When in doubt, start with the 7B model. It's the Honda Civic of AI models -- reliable, efficient, gets the job done.*

### The AI response is slow. How do I speed it up?
1. **Enable GPU inference** if your hardware supports it (toggle in AI settings)
2. **Use a smaller model** -- 7B is 2-3x faster than 13B
3. **Reduce context length** if you don't need long conversations
4. **Check system resources** -- if the CPU is pegged by monitoring or backups, the AI will feel it

### Can I fine-tune models for my specific use case?
Check out the Model Marketplace in the AI Engine settings. We offer specialized fine-tunes for security analysis, network troubleshooting, and helpdesk scenarios. Custom fine-tuning is available through our consulting services.

### Is my data safe with the AI Agent?
When running in local-only mode, your data never leaves the appliance. Queries are processed on-device, and the model runs entirely in local memory. No cloud calls, no telemetry, no "oops we accidentally trained on your data." Hybrid mode lets you use cloud LLMs for specific tasks, but that's opt-in and clearly labeled.

---

## Citadel Hardware - General Troubleshooting

### The appliance won't boot / no display output
1. Check power LED -- is it on?
2. Try a different monitor/cable (HDMI or DisplayPort depending on model)
3. Remove any USB devices except keyboard
4. If it was working before: hold power button for 10 seconds to force shutdown, wait 30 seconds, power on
5. Still stuck? Contact support -- we'll get you sorted fast.

### How do I access the web interface?
Connect the appliance to your network. It picks up a DHCP address automatically. Check your router/DHCP server for the assigned IP, then open `https://<ip-address>` in a browser. Default credentials are in the quick-start card that shipped with your unit.

*Lost the quick-start card? It happens. Contact support and we'll get you back in.*

### Can I expand storage on a Citadel NAS?
Yes. Hot-swap drive bays on the R4/R8/R16 models. Pop in a new drive, the system detects it, and you can expand your storage pool. For the AI NAS, NVMe slots can be upgraded. Check the hardware guide for your specific model's max capacity.

### What about firmware updates?
Updates are delivered through the MyClover.Tech management interface. One-click updates with automatic backup before applying. We don't do forced updates -- you control when and what gets updated.

---

## Network & Connectivity

### What ports does MyClover.Tech use?
Default ports (all configurable):
- **443** -- Web interface (HTTPS)
- **8400** -- API access
- **514** -- Syslog (TCP/UDP) for SentryLog
- **161/162** -- SNMP for NetMon
- **51820** -- WireGuard VPN
- **3000** -- Gitea (Dev Environment)
- **1935** -- RTMP ingest (StreamServer)

### Can I put the appliance behind a reverse proxy?
Absolutely. Works great with nginx, Traefik, Caddy, or whatever you prefer. The built-in Traefik handles internal routing, but if you have an existing reverse proxy infrastructure, CloverBot plays nice.

### VPN setup -- how do I connect remote sites?
MyClover.Tech includes WireGuard for site-to-site and remote access VPN. Generate configs through the management interface, distribute to clients. Simple, fast, and cryptographically solid. No Java applets from 2008 required.

*WireGuard is what VPN should have been from the start. We just made it easier to set up.*
