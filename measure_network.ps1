# Windows PowerShell examples. Run against permitted destinations only.
# Replace <receiver-ip> with the IP of a machine you own/control.

ping -n 20 1.1.1.1
tracert -d 1.1.1.1
ping -n 20 8.8.8.8
tracert -d 8.8.8.8

# Start iperf3 server on the receiver:
# iperf3.exe -s
# TCP test from sender:
# iperf3.exe -c <receiver-ip> -t 30
# UDP test from sender:
# iperf3.exe -c <receiver-ip> -u -b 10M -t 30
