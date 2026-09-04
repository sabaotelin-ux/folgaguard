import os
import shutil

def get_system_telemetry():
    total, used, free = shutil.disk_usage(".")
    
    mem_info = {}
    try:
        with open("/proc/meminfo", "r") as f:
            for line in f:
                parts = line.split(":")
                if len(parts) == 2:
                    mem_info[parts[0].strip()] = parts[1].strip()
    except Exception:
        pass

    load_avg = os.getloadavg() if hasattr(os, "getloadavg") else (0.0, 0.0, 0.0)

    print("=== Aegis Telemetria de Borda ===")
    print(f"[Armazenamento] Total: {total // (2**20)} MB | Usado: {used // (2**20)} MB | Livre: {free // (2**20)} MB")
    print(f"[Carga do Sistema (Load Avg)] 1m, 5m, 15m: {load_avg}")
    if "MemTotal" in mem_info and "MemAvailable" in mem_info:
        print(f"[Memória RAM] Total: {mem_info['MemTotal']} | Disponível: {mem_info['MemAvailable']}")
    print("================================")

if __name__ == "__main__":
    get_system_telemetry()
