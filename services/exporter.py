import csv
from datetime import datetime

def export_csv(path, model, avg_wait=None, throughput=None, conf=None):
    rows = [
        ["Traffic Light Simulation Statistics"],
        ["Exported on:", datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        [], ["Configuration"],
    ]
    if conf:
        rows += [["Algorithm:", conf.get("algo","")],
                 ["Traffic Density:", conf.get("density","")],
                 ["Emergency Frequency:", conf.get("emfreq","")],
                 ["Green Light Duration:", f"{conf.get('green',0)}s"]]
    rows += [[], ["Performance Metrics"],
             ["Total Vehicles Processed:", model.total_vehicles_processed],
             ["Simulation Time:", f"{model.simulation_time}s"]]
    if avg_wait is not None:
        rows.append(["Average Wait Time:", f"{avg_wait:.2f} cycles"])
    if throughput is not None:
        rows.append(["Throughput:", f"{throughput:.2f} vehicles/min"])
    rows.append(["Emergency Vehicles Processed:", model.emergency_processed])
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); [w.writerow(r) for r in rows]
