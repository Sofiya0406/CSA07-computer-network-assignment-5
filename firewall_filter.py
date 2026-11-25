"""A stateless packet filter: the first matching rule decides."""
RULES = [
    ("allow", "tcp", 443, None),
    ("allow", "tcp", 22, "10.1."),
    ("deny", "tcp", 22, None),
    ("allow", "udp", 53, None),
]
DEFAULT = "deny"


def decide(proto, port, src):
    for action, rule_proto, dport, prefix in RULES:
        protocol_matches = rule_proto == proto
        port_matches = dport is None or dport == port
        source_matches = prefix is None or src.startswith(prefix)
        if protocol_matches and port_matches and source_matches:
            return action
    return DEFAULT


if __name__ == "__main__":
    packets = [
        ("tcp", 443, "49.37.2.8"),
        ("tcp", 22, "10.1.4.20"),
        ("tcp", 22, "49.37.2.8"),
        ("udp", 53, "10.1.4.20"),
        ("tcp", 80, "49.37.2.8"),
        ("icmp", None, "49.37.2.8"),
    ]
    for packet in packets:
        print(f"{packet[0]:<5} {str(packet[1]):<5} from {packet[2]:<10} -> {decide(*packet)}")
