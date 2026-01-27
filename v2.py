import time
from collections import defaultdict
import psutil  # For network statistics

# Configuration
CHECK_INTERVAL = 5  # seconds between checks
THRESHOLD_PACKETS_PER_SEC = 10000  # adjust to your environment
THRESHOLD_CONNECTIONS = 1000  # active connections limit for alarm

def get_network_activity():
    net_io = psutil.net_io_counters()
    return net_io.packets_recv, net_io.packets_sent

def get_connection_count():
    connections = psutil.net_connections()
    return len([c for c in connections if c.status == 'ESTABLISHED'])

def detect_ddos():
    print("🎯 Starting DDoS detection... Press Ctrl+C to stop.")
    
    prev_recv, prev_sent = get_network_activity()
    
    while True:
        time.sleep(CHECK_INTERVAL)
        recv, sent = get_network_activity()
        conn_count = get_connection_count()

        recv_rate = (recv - prev_recv) / CHECK_INTERVAL
        sent_rate = (sent - prev_sent) / CHECK_INTERVAL

        print(f"Packets/sec — In: {recv_rate:.0f}, Out: {sent_rate:.0f}, Connections: {conn_count}")

        if recv_rate > THRESHOLD_PACKETS_PER_SEC or conn_count > THRESHOLD_CONNECTIONS:
            print("🚨 Potential DDoS detected! Abnormal network activity.")
        else:
            print("✅ Normal traffic levels.")

        prev_recv, prev_sent = recv, sent

if __name__ == "__main__":
    detect_ddos()
