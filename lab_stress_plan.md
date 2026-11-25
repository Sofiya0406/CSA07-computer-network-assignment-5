# Task B3 – Safe isolated-lab plan

Only test systems you own/control in an isolated lab or simulator.

- Apply `tc netem` delay/loss to a lab interface only.
- Run iperf3 between the two lab hosts and record TCP throughput.
- Generate bounded normal HTTP requests to a local test server; do not create a denial-of-service flood.
- Compare response times with and without rate limiting.
- Save firewall counters and permitted/denied connection test outputs.
- Remove netem settings after testing: `sudo tc qdisc del dev eth0 root`.
