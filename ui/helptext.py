HELP_TEXT ="""TRAFFIC LIGHT SIMULATOR - USER GUIDE

OVERVIEW:
This simulator models a 4-way traffic intersection with intelligent traffic light control.
You can test different algorithms, traffic conditions, and emergency scenarios.

CONTROL ALGORITHMS:
• Fixed Time: Traditional timer-based system (30-60 second cycles)
• Priority Based: Gives priority to lanes with more vehicles
• Adaptive: AI-like system considering multiple factors
• Round Robin: Equal time allocation for fairness

TRAFFIC DENSITY:
• Low: Light traffic (10% spawn rate)
• Medium: Moderate traffic (25% spawn rate)  
• High: Heavy traffic (45% spawn rate)

EMERGENCY FREQUENCY:
• None: No emergency vehicles
• Rare: Emergency every ~200 cycles
• Occasional: Emergency every ~67 cycles
• Frequent: Emergency every ~25 cycles

SIMULATION CONTROLS:
▶ Start/Stop: Begin or end the simulation
⏸ Pause: Temporarily halt the simulation
🚗 Add Vehicle: Manually add a random vehicle to a random lane
🚨 Emergency: Trigger an emergency vehicle immediately
🔄 Reset: Clear all data and return to initial state

VEHICLE TYPES:
🚙 Regular Car (Blue): Standard passenger vehicle - 75% of traffic
🚌 Bus (Orange): Higher capacity, gets priority - 20% of traffic
🏍 Motorcycle (Purple): Smaller, faster vehicle - 5% of traffic
🚨 Emergency (Red): Highest priority, triggers emergency mode

HOW TO USE:
1. Choose your preferred control algorithm
2. Set traffic density level and emergency frequency
3. Click "Start" to begin simulation
4. Watch vehicles accumulate and lights change
5. Use manual controls to test scenarios
6. Check Statistics tab for performance metrics

TIPS:
• Run simulations for at least 5-10 minutes for meaningful data
• Test each algorithm multiple times for consistency
• Use manual controls to create interesting scenarios
• Export statistics to compare different runs
        """
