from core.constants import LANES

def snapshot(m):
    waiting = sum(len(q) for q in m.queues.values())
    avg = (sum(m.wait_times)/len(m.wait_times)) if m.wait_times else 0.0
    thr = (m.total_vehicles_processed/m.simulation_time*60) if m.simulation_time else 0.0
    eff = (m.total_vehicles_processed/max(m.total_vehicles_processed+waiting, 1))*100
    emc = sum(1 for q in m.queues.values() for v in q if v == "Emergency")
    best = max(m.green_duration, key=m.green_duration.get) if sum(m.green_duration.values()) else "None"
    return dict(waiting=waiting, avg=avg, thr=thr, eff=eff, emc=emc, best=best)

def long_report(m, algo, density, emfreq, green, speed):
    lines = []
    lines += ["="*60, "TRAFFIC LIGHT SYSTEM - ANALYTICS REPORT", "="*60, ""]
    lines += [f"Simulation Runtime: {m.simulation_time} seconds ({m.cycle_count} cycles)", ""]
    lines += ["SYSTEM CONFIGURATION:",
              f"   Control Algorithm: {algo}",
              f"   Traffic Density: {density}",
              f"   Emergency Frequency: {emfreq}",
              f"   Green Light Duration: {green} seconds",
              f"   Simulation Speed: {speed}%", "",
              "CURRENT SYSTEM STATUS:",
              f"   Active Green Light: {m.current_green or 'None'}",
              f"   Emergency Mode: {'ACTIVE' if m.emergency_mode else 'Inactive'}",
              f"   Time Since Last Change: {m.cycle_count - m.last_green_change} cycles", "",
              "TRAFFIC QUEUE ANALYSIS:"]
    tot = 0
    for lane in LANES:
        q = m.queues[lane]; L = len(q); tot += L
        comp = {"Car":0,"Bus":0,"Motorcycle":0,"Emergency":0}
        for v in q: comp[v] = comp.get(v,0)+1
        icon = "OK" if L==0 else "LOW" if L<=3 else "MED" if L<=6 else "HIGH"
        parts = ", ".join([f"{cnt} {vt}" for vt, cnt in comp.items() if cnt])
        lines.append(f"   {icon} {lane:8}: {L:2} vehicles" + (f" ({parts})" if parts else ""))
    lines += [f"   Total Vehicles Waiting: {tot}", f"   Average Queue Length: {tot/4:.1f} vehicles per lane", "",
              "PERFORMANCE METRICS:"]
    snap = snapshot(m)
    lines += [f"   Total Vehicles Processed: {m.total_vehicles_processed}",
              f"   Emergency Vehicles Processed: {m.emergency_processed}",
              f"   System Throughput: {snap['thr']:.2f} vehicles/minute",
              f"   Average Wait Time: {snap['avg']:.2f} cycles", "",
              "TRAFFIC LIGHT ANALYSIS:"]
    tg = sum(m.green_duration.values())
    if tg:
        for lane in LANES:
            d = m.green_duration[lane]; pct = d/tg*100; diff = abs(pct-25.0)
            icon = "FAIR" if diff<=5 else "OK" if diff<=10 else "UNFAIR"
            lines.append(f"   {icon} {lane:8}: {d:4} cycles ({pct:5.1f}% of total)")
    lines += ["", "="*60, f"Report End - Cycle {m.cycle_count} | Runtime: {m.simulation_time}s", "="*60, ""]
    return "\n".join(lines)
