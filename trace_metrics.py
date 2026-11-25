"""Network performance metrics from the assignment's sample packet trace."""

TRACE = [
    (1, 0, 42, 1200), (2, 20, 61, 1200), (3, 40, 85, 1200),
    (4, 60, None, 1200), (5, 80, 119, 1200), (6, 100, 146, 1200),
    (7, 120, 158, 1200), (8, 140, 190, 1200), (9, 160, None, 1200),
    (10, 180, 222, 1200),
]


def metrics(trace):
    received = [(seq, tx, rx, size) for seq, tx, rx, size in trace if rx is not None]
    if not trace or not received:
        raise ValueError("Trace must contain at least one received packet")

    loss = (len(trace) - len(received)) / len(trace) * 100
    delays = [rx - tx for _, tx, rx, _ in received]
    avg_delay = sum(delays) / len(delays)

    consecutive_differences = [
        abs(delays[i] - delays[i - 1]) for i in range(1, len(delays))
    ]
    jitter = (
        sum(consecutive_differences) / len(consecutive_differences)
        if consecutive_differences else 0.0
    )

    received_bits = sum(size * 8 for _, _, _, size in received)
    duration_ms = received[-1][2] - received[0][1]
    throughput = received_bits / duration_ms  # bits/ms numerically equals kbps
    return loss, avg_delay, jitter, throughput


if __name__ == "__main__":
    loss, delay, jitter, throughput = metrics(TRACE)
    print(f"packet loss {loss:.1f} %")
    print(f"average delay {delay:.1f} ms, jitter {jitter:.1f} ms")
    print(f"throughput {throughput:.1f} kbps")
    print("VoIP quality:", "acceptable" if delay < 150 and jitter < 30 and loss < 1 else "poor")
