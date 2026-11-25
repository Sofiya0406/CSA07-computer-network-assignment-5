# CSA07 – Computer Networks
# Assignment 5 – CO5: Measuring Network Performance and Securing Applications

**Student:** S. Sofiya  
**Register Number:** 192521248  
**Department:** Information Technology

> Part B asks for measurements from the student's own network and simulator. Any example or target value below is identified as an assumption; replace it with actual command output and evidence before submission.

---

# PART A – DESIGN

## TASK A1 – Where Does the Delay Come From?

### A1.1 Delay calculation

Given:
- Packet size = 1,500 bytes = 12,000 bits
- Link bandwidth = 100 Mbps
- Distance = 2,000 km = 2,000,000 m
- Propagation speed assumption = `2 × 10^8 m/s`
- Routers = 3
- Each router: queuing = 0.5 ms and processing = 0.1 ms

**1. Transmission delay**

`Dtrans = packet bits / bandwidth`

`= 12,000 / (100 × 10^6) seconds = 0.00012 s = 0.12 ms`

**2. Propagation delay**

`Dprop = distance / propagation speed`

`= 2,000,000 / (2 × 10^8) = 0.01 s = 10 ms`

**3. Queuing delay**

`Dqueue = 3 × 0.5 = 1.5 ms`

**4. Processing delay**

`Dproc = 3 × 0.1 = 0.3 ms`

**Total delay**

`Dtotal = 0.12 + 10 + 1.5 + 0.3 = 11.92 ms`

Propagation delay (10 ms) dominates. Increasing every link to 1 Gbps reduces transmission delay from 0.12 ms to 0.012 ms. New total = `11.812 ms`, only 0.108 ms improvement. Therefore, upgrading link rate alone does not significantly reduce the dominant propagation delay.

### A1.2 Bandwidth–delay product

Given bandwidth = 1 Gbps and RTT = 80 ms = 0.08 s.

`BDP = bandwidth × RTT`

`= 1,000,000,000 × 0.08 = 80,000,000 bits`

`= 10,000,000 bytes ≈ 10 MB`

A 64 KB TCP window can carry only 64 KB before an acknowledgement is needed. Maximum throughput:

`Throughput = window bits / RTT`

`= (64 × 1024 × 8) / 0.08 = 6,553,600 bps ≈ 6.55 Mbps`

Thus 64 KB is far too small to fill a 1 Gbps, 80 ms path. A much larger TCP window (and window scaling) is required.

### A1.3 Targets and measurement tools

Illustrative service targets (confirm with the company's application requirements):

| Application | One-way delay target | Jitter target | Packet loss target | Throughput target |
|---|---:|---:|---:|---:|
| Live video | <150 ms | <30 ms | <1% | 2–4 Mbps per HD stream |
| Voice | <150 ms | <30 ms | <1% | about 80 kbps per G.711 direction |
| Recorded video | buffering acceptable; low start delay | not critical | near-zero after recovery | 5–8 Mbps per HD stream |
| E-mail | seconds acceptable | not critical | reliable delivery | low; burst-based |
| Large downloads | depends on user experience | not critical | TCP recovery | as high as available link allows |

Tools:
- `ping`: RTT, loss and repeated-sample variation (jitter estimate).
- `traceroute` / `tracert`: path and per-hop RTT.
- `iperf3`: TCP/UDP throughput, UDP jitter and loss.
- Wireshark: packet timings, retransmissions, DNS/HTTP/TLS analysis and RTP stream analysis.
- SNMP: interface utilisation, errors, discards and device counters over time.
- Packet Tracer / NS-3: controlled simulation of topology, load, delay and queueing.

**Active measurement:** sends test packets/traffic (ping, traceroute, iperf3). It can test a chosen path and load but may consume bandwidth and may not represent every user.

**Passive measurement:** observes existing traffic and counters (Wireshark capture, SNMP). It shows actual user traffic without injecting test flows, but cannot directly measure an unused path or service that no user is currently using.

**Passive-only alternative:** It can estimate throughput/utilisation, packet loss where sequence information is visible, retransmissions, observed RTT where protocol exchanges permit, and application timing for captured flows. It may miss one-way delay without synchronised clocks, unused-path performance, and performance under a load that has not occurred. Problems may only be noticed after users experience them.

---

## TASK A2 – Follow the Application Protocols

### A2.1 E-mail SMTP sequence

Example SMTP dialogue (reply codes are typical):

```text
S: 220 mail.example.com ESMTP ready
C: EHLO student.example
S: 250-mail.example.com
S: 250 OK
C: MAIL FROM:<student@example.com>
S: 250 OK
C: RCPT TO:<teacher@example.com>
S: 250 OK
C: DATA
S: 354 End data with <CRLF>.<CRLF>
C: Subject: Assignment
C:
C: Please find my assignment attached.
C: .
S: 250 Message accepted for delivery
C: QUIT
S: 221 Bye
```

POP3 with “delete after download” removes messages from the server after one device downloads them. The phone may download and delete a message, so it may not appear on the laptop or lab PC. IMAP keeps mail on the server and synchronises folders, read/unread status and message state across devices.

### A2.2 FTP and monitoring

**Active FTP:** the client opens a control connection to server TCP port 21, then the server initiates the data connection back to the client's negotiated port. A firewall/NAT may block this inbound server-to-client connection.

**Passive FTP:** the client requests PASV/EPSV; the server provides a data port and the client initiates the data connection outbound. This is generally easier through client-side firewalls.

SFTP (over SSH) or HTTPS is preferred because the session and credentials/data are encrypted. Plain FTP does not protect credentials or file contents.

**SNMP GET:** An SNMP manager sends a GET request for an interface counter OID (for example, an interface's input octets) to the router's SNMP agent. The agent returns the current counter value in a response.

**SNMP TRAP:** When a link changes state, the router's agent can send an unsolicited linkDown/linkUp notification to the configured manager. Use SNMPv3 where possible for authentication and encryption.

### A2.3 DNS and HTTP timings

In browser Developer Tools → Network, inspect:
- DNS lookup: time to resolve the hostname.
- Initial connection: TCP connection establishment.
- SSL/TLS: secure handshake time.
- Waiting / TTFB: time until the first response byte.
- Content download: time to transfer response body.
- Queueing/stalled: browser scheduling or connection wait.

A long DNS phase suggests resolver/name-resolution delay; long connection/TLS phases suggest handshake or network delay; long TTFB suggests server processing or upstream delay; long download suggests low throughput or a large resource.

**Alternative: webmail versus IMAP for 50 messages**

Assume 50 messages average 20 KB each and all message bodies are opened:
- Approximate message content = `50 × 20 KB = 1,000 KB ≈ 1 MB`, excluding attachments and protocol overhead.
- Webmail over HTTPS transfers HTML/CSS/JavaScript, images and message content; cached assets may reduce repeated transfer. Exact volume depends on page design and whether all messages are opened.
- IMAP can fetch headers first and retrieve selected bodies/attachments on demand; if all 50 bodies are fetched, message-content volume is still about 1 MB plus protocol overhead.
- Both can be secured with TLS. Webmail is centrally managed through a browser; IMAP security depends on correctly configured TLS and client settings. No exact traffic total can be determined without actual message sizes and a capture.

---

## TASK A3 – Peer-to-Peer, VoIP and Overlays

### A3.1 Distribute a 4 GB package

Package size = `4 GB × 8 = 32 Gbit`.

**Client–server:**
- Server upload = 100 Mbps.
- Time to send one full package copy to all centres is limited by server's 100 Mbps upload.
- `32,000 Mbit / 100 Mbps = 320 s = 5 min 20 s` (ideal, ignoring protocol overhead and other traffic).

**Peer-to-peer:**
- Server upload = 100 Mbps.
- 20 centres each upload at 20 Mbps, giving a theoretical combined upload capacity of `100 + (20 × 20) = 500 Mbps` once peers have received pieces.
- Total delivered data to 20 centres = `20 × 32 Gbit = 640 Gbit`.
- Ideal aggregate-upload lower bound = `640,000 Mbit / 500 Mbps = 1,280 s`.
- Each centre can download at 50 Mbps; aggregate download capacity = 1,000 Mbps, so this is not the limiting bound in this simplified calculation.

**Important interpretation:** P2P reduces the load on the original server and scales better as peers contribute upload capacity, but the ideal lower-bound calculation above does not mean P2P must finish faster than the 320 s server-only result. With the stated 20 Mbps upload per centre, the aggregate upload available is still insufficient to deliver 20 complete copies faster than a continuously available 100 Mbps server. P2P wins when peer upload capacity is large enough, many peers are available, and the server is the bottleneck; it may not win with slow or unreliable peers, few peers, or high coordination/availability overhead.

### A3.2 Real cost of a G.711 voice call

- Speech rate = 64 kbps.
- Packetisation interval = 20 ms = 0.02 s.
- Packets per second = `1 / 0.02 = 50 packets/s`.
- Payload per packet = `64,000 × 0.02 / 8 = 160 bytes`.
- IP/UDP/RTP headers = 40 bytes.
- Total per packet = `160 + 40 = 200 bytes`.
- Bandwidth per direction = `200 × 8 × 50 = 80,000 bps = 80 kbps`.

On a 2 Mbps link, theoretical calls per direction = `2,000 / 80 = 25 calls`, before link-layer overhead, encryption, signalling and safety margin. Practical supported calls will be lower.

**SIP** establishes, modifies and terminates the call/session (signalling). **RTP** carries the real-time audio/video media packets.

### A3.3 Overlay networks

A CDN is an overlay of distributed edge caches/servers placed above the internet's underlying IP network. It serves recorded lectures and course packages from a nearby edge, reducing origin-server load and user latency.

A VPN creates encrypted logical tunnels over the internet between users/sites. It protects traffic between regional centres and company resources but does not by itself reduce physical propagation delay.

**Alternative: CDN with a 1 Gbps edge in each region**
- One 4 GB package = 32 Gbit.
- Per-region edge delivery time = `32 Gbit / 1 Gbps = 32 s` ideal.
- If all 20 regions have their own 1 Gbps edge and enough upstream content is pre-positioned, each can download at that edge rate concurrently; ideal delivery is about 32 s per centre.
- CDN costs more for edge/storage/traffic services but reduces origin load and improves regional availability. P2P uses clients' upload capacity and may be cheaper, but depends on peers being online and willing/able to upload.

---

## TASK A4 – Find the Hole in the Firewall

### A4.1 SSL/TLS

A TLS certificate binds a server identity (domain) to a public key and is signed by a trusted certificate authority. The client validates the certificate chain, hostname and validity. The handshake negotiates protocol version, cipher suite and shared session keys, and authenticates the server (and optionally the client).

An attacker on café Wi-Fi can generally see network metadata such as IP addresses, ports, packet sizes, timing and traffic volume. With correctly validated HTTPS, the attacker cannot read or modify the encrypted application contents or passwords. The attacker may still block traffic, observe metadata, or exploit a certificate warning/user mistake or compromised endpoint.

### A4.2 Rule analysis and corrected order

Rules are processed top to bottom; first match wins.

Given:
1. allow TCP any → 443
2. allow TCP any → 22
3. deny TCP any → 22
4. allow TCP 10.1.0.0/16 → 22
5. allow UDP any → 53
6. deny all any → any

- Rule 3 can never take effect because rule 2 already allows all TCP traffic to destination port 22.
- Rule 4 can never take effect because rule 2 also matches the trusted `10.1.0.0/16` sources.
- Security hole: SSH (TCP/22) is allowed from every source, not just the trusted management network.

**Corrected order:**
1. Allow TCP any → 443
2. Allow TCP source `10.1.0.0/16` → destination port 22
3. Deny TCP any → destination port 22
4. Allow UDP any → destination port 53 (only if this server must provide DNS; otherwise restrict to trusted resolvers)
5. Deny all any → any

**Firewall types**
- Stateless packet filter: checks each packet's header against rules; does not inherently know whether it belongs to an established connection.
- Stateful firewall: tracks connection state and permits packets belonging to valid established/related sessions.
- Application-layer proxy firewall: terminates/proxies application sessions and can inspect application commands/content, enabling more detailed controls but adding processing and latency.

The completed TODO Python program is in `TaskA4/firewall_filter.py`.

**Alternative: cloud WAF**
A WAF can detect/block application-layer attacks such as SQL injection and cross-site scripting (XSS), which a basic port/protocol packet filter cannot understand. It may add processing and routing delay; the actual added latency depends on provider, region, inspection mode and caching and must be measured. Because the company hosts a public learning website and has experienced an outage, a managed WAF/CDN security service is justified, with latency tested before rollout.

---

## TASK A5 – How Easy Is It to Take the Site Down?

### A5.1 Size the SYN attack

- Half-open connection queue = 1,024 entries.
- Each entry remains for 60 seconds.
- Required sustained arrival rate to fill the queue = `1,024 / 60 = 17.07 SYN packets/s` (assuming no successful handshakes, no early cleanup and a full queue).

**SYN cookies:** The server encodes connection state into the SYN-ACK sequence number rather than allocating a full queue entry immediately. It allocates state only after receiving a valid ACK, reducing half-open queue exhaustion.

**DNS amplification:** Attackers send small DNS queries with a spoofed victim source address to open resolvers. The much larger DNS responses go to the victim. Blocking at the victim is difficult because the traffic comes from many legitimate-looking DNS servers and consumes the victim's incoming link before local filtering can act.

### A5.2 Protection plan

| Attack | Protection |
|---|---|
| SYN flood | SYN cookies, SYN rate limits, connection limits and upstream DDoS scrubbing |
| DNS amplification | Upstream scrubbing/ISP filtering, ingress anti-spoofing (BCP 38) at source networks, rate limiting at open resolvers |
| HTTP request flood | CDN/WAF, bot detection, application rate limits and caching |
| Volumetric bandwidth flood | ISP/cloud DDoS scrubbing and CDN/anycast distribution |

**Alternative: four times server capacity**

If four servers each independently handle the same half-open queue capacity, total queue = `4 × 1,024 = 4,096`. With a 60-second timeout, the sustained fill rate is `4,096 / 60 = 68.27 SYN/s`. This is only four times the original threshold and does not protect the upstream link from volumetric attacks. Buying capacity alone is not a realistic DDoS defence.

---

# PART B – IMPLEMENTATION AND EXPERIMENTAL INVESTIGATION

## TASK B1 – Measure a Real Network

### B1.1 Delay and path

Run ping and traceroute to three destinations (for example, a nearby university/public DNS, a national server and an overseas server) at morning, afternoon and evening. Record at least 20 ping samples per run.

Windows commands:
```powershell
ping -n 20 1.1.1.1
tracert -d 1.1.1.1
ping -n 20 8.8.8.8
tracert -d 8.8.8.8
```

Use the same three destinations and time windows for fair comparison. Record min/average/max RTT and packet loss. Jitter can be estimated as the mean absolute difference between consecutive RTT samples.

Propagation lower bound = path distance / propagation speed. Actual RTT also includes router processing, queueing, transmission and return-path delay. Do not claim an exact propagation delay unless the path distance and route are known.

### B1.2 TCP and UDP throughput

Run `iperf3` on two machines you own/control:
- Receiver: `iperf3 -s`
- Sender TCP: `iperf3 -c <receiver-ip> -t 30`
- Sender UDP: `iperf3 -c <receiver-ip> -u -b 10M -t 30`

Repeat on wired and Wi-Fi. Record sender/receiver, link type, test duration, TCP throughput, UDP throughput, UDP jitter and loss. Do not run tests against a public server without permission.

### B1.3 Wireshark capture

Capture your own permitted voice/video test call or a generated RTP lab stream. Use Telephony → RTP → RTP Streams → Analyze where available. Record packet count, packet loss, jitter, payload/packet size and stream duration. If traffic is encrypted or the application does not use visible RTP, state that limitation rather than inventing RTP measurements.

### B1.4 Compare with targets

Compare each actual measurement with the A1.3 target table. Mark pass/fail and explain whether the issue is delay, jitter, loss, throughput or time-of-day congestion.

### Completed trace-analysis code

`TaskB1/trace_metrics.py` computes the assignment's supplied sample trace. The sample has 10 packets, 2 missing packets, so loss is 20%. This is a provided test trace, not a capture from the student's own network.

**Alternative: synchronised one-way delay versus half RTT**

Example: upload one-way delay = 80 ms and download one-way delay = 20 ms, so RTT = 100 ms. Half RTT = 50 ms, which is 30 ms lower than the actual 80 ms upload delay. Halving RTT assumes a symmetric path; an asymmetric path makes that estimate misleading. Synchronized endpoint clocks are needed for direct one-way delay measurement.

---

## TASK B2 – Simulate Under Varying Conditions

Build a small topology with a company server, one regional centre, a client PC, a voice endpoint and a router/link. Test at least:
1. Baseline bandwidth and delay.
2. Lower bandwidth.
3. Increased propagation/queueing delay.
4. Increased number of users/background downloads.
5. Voice with normal best-effort queue.
6. Voice with priority QoS queue.

Record throughput, delay and packet loss for every run. A background file download should increase queueing delay for voice under best effort. A correctly configured priority queue should reduce voice delay/jitter, but may reduce bandwidth available to lower-priority downloads.

Packet Tracer is easier for topology, routing and ACL demonstrations; NS-3 offers more detailed configurable traffic, queueing and performance models. Use the same topology/traffic assumptions for a fair comparison. Add actual screenshots and results.

---

## TASK B3 – Performance Under Stress and Attack

### B3.1 Delay and loss

In an isolated Linux lab, `tc netem` can add delay/loss to a test interface. Example (replace `eth0` with the lab interface):

```bash
sudo tc qdisc add dev eth0 root netem delay 50ms loss 1%
sudo tc qdisc change dev eth0 root netem delay 150ms loss 5%
sudo tc qdisc change dev eth0 root netem delay 300ms loss 10%
sudo tc qdisc del dev eth0 root
```

Run controlled iperf3 and voice-quality tests at each setting. Record the results. Do not apply these settings to a shared or production network.

### B3.2 Window size

Compare iperf3 with default TCP settings and a controlled socket/window setting on a long-delay lab path. Compare measured throughput with the A1.2 BDP (10 MB) and 64 KB window limit (about 6.55 Mbps). Record the exact command and negotiated window values.

### B3.3 Firewall and flood

Apply the corrected firewall policy in an isolated lab or Packet Tracer ACL. Test allowed HTTPS, allowed management SSH from the trusted subnet, denied SSH from other sources and denied unrelated traffic.

For load testing, use a bounded request-rate test against a local test server in an isolated lab only. Compare response time with and without rate limiting. Do not run denial-of-service tests against real websites, public IPs or shared networks.

### B3.4 Trade-off

Strict-priority (DiffServ EF) can keep voice delay low, but excessive priority traffic can starve downloads. Weighted fair queuing shares capacity among classes and protects other traffic, but may give voice slightly higher delay than strict priority. Select the policy based on measured voice delay/jitter and minimum acceptable download throughput.

---

## TASK B4 – Final Engineering Decision

### B4.1 Predict the effect

A student in another continent will generally experience higher propagation delay because of the longer physical path. Doubling users may increase queueing delay, jitter and packet loss if link, server or AP capacity is not increased. Exact values must be predicted from the student's B1 measurements and B2 simulation; they cannot be calculated from the assignment alone because no measured baseline or overseas path is supplied.

### B4.2 Security check

Repeat normal HTTPS, DNS, e-mail and authorised staff management tests at the doubled simulated load. Verify that rate limits block abnormal request rates while allowing normal user traffic. Save firewall counters, server response times and allowed/denied test results.

### B4.3 Recommendation

1. Deploy a CDN with regional edge caching for recorded lectures and course packages.
2. Use QoS (priority for voice/live-class media, fair scheduling for downloads).
3. Increase bottleneck uplink capacity based on measured busy-hour utilisation and BDP.
4. Add regional application/media servers for students on other continents.
5. Deploy a managed WAF and upstream DDoS scrubbing service.
6. Monitor delay, jitter, loss, throughput, interface utilisation and server load using SNMP and active probes.

Quote the actual B1/B2/B3 measurements in the final report before submitting.

**Alternative: regional servers**
Use measured RTTs: if India RTT is `RTT_india` and regional edge RTT is `RTT_edge`, approximate RTT improvement is `RTT_india − RTT_edge`. For example only, a reduction from 220 ms to 40 ms gives 180 ms lower RTT. Regional servers can substantially improve live-class responsiveness, but require content synchronisation, storage, security and operational cost. Use the measured route values to make the final cost decision.

---

## Conclusion

The calculations show that propagation delay can dominate long-distance communication, small TCP windows limit high-BDP links, application protocols need suitable transport/security, and firewalls must use correct rule order. CDN caching, QoS, regional servers, monitoring and upstream DDoS protection improve the company's ability to serve live classes and downloads. Part B must be completed with the student's own measurements, captures and simulation outputs.
