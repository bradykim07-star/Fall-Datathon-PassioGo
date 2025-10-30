import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# --- File extraction ---
riders_files1 = ["ridership_2025-2-5.csv", "ridership_2025-2-12.csv", "ridership_2025-2-19.csv", "ridership_2025-2-26.csv", "ridership_2025-3-5.csv"]
riders_files2 = ["ridership_2025-9-3.csv", "ridership_2025-9-10.csv", "ridership_2025-9-17.csv", "ridership_2025-9-24.csv", "ridership_2025-10-1.csv"]

bus = pd.read_csv("https://raw.githubusercontent.com/RutgersDataScienceClub/Fall-2025-Datathon/refs/heads/main/rutgers_bus_data/vehicles.csv")

# --- Bus ID key ---
lx_ids = [17624, 4882, 7149, 7179, 4850, 13216, 18020, 19394, 18619]

# --- Load, merge, and clean both semesters ---
def load_and_process(files):
    riders = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
    riders = riders.merge(bus[['id', 'routeName']], left_on='bus_id', right_on='id', how='left')
    riders = riders[riders['bus_id'].isin(lx_ids)]
    riders = riders.drop(columns=['bus_id', 'id', 'routeName'])
    return riders

LX_spring = load_and_process(riders_files1)
LX_fall = load_and_process(riders_files2)

# --- Convert 'time' to datetime for plotting ---
start_time = pd.Timestamp("2025-10-15 00:00:00")
LX_spring['timestamp'] = start_time + pd.to_timedelta(LX_spring['time'], unit='m')
LX_fall['timestamp'] = start_time + pd.to_timedelta(LX_fall['time'], unit='m')

LX_spring = LX_spring.set_index('timestamp').sort_index()
LX_fall = LX_fall.set_index('timestamp').sort_index()

# --- Align both time series on timestamp ---
combined = pd.merge(
    LX_spring[['ridership_count']],
    LX_fall[['ridership_count']],
    left_index=True,
    right_index=True,
    suffixes=('_spring', '_fall'),
    how='inner'
)

# --- Compute difference (Fall - Spring) ---
combined['difference'] = (combined['ridership_count_fall'] - combined['ridership_count_spring'])


# --- Plot the difference ---
plt.figure(figsize=(12, 6))
plt.plot(combined.index, combined['difference'], color='purple', linewidth=2)

# --- Formatting ---
plt.title("Ridership Difference (Fall 2025 − Spring 2025) — LX Buses")
plt.xlabel("Time of Day")
plt.ylabel("Ridership Difference")
plt.axhline(0, color='black', linestyle='--', linewidth=1)  # baseline
plt.grid(True)

ax = plt.gca()
ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%I:%M %p'))
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
