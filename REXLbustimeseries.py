import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#riders_files = ["ridership_2025-2-5.csv", "ridership_2025-2-12.csv", "ridership_2025-2-19.csv", "ridership_2025-2-26.csv", "ridership_2025-3-5.csv"]
riders_files = ["ridership_2025-9-3.csv", "ridership_2025-9-10.csv", "ridership_2025-9-17.csv", "ridership_2025-9-24.csv", "ridership_2025-10-1.csv"]
riders_list = [pd.read_csv(f) for f in riders_files]
riders = pd.concat(riders_list, ignore_index=True)
bus = pd.read_csv("https://raw.githubusercontent.com/RutgersDataScienceClub/Fall-2025-Datathon/refs/heads/main/rutgers_bus_data/vehicles.csv")

rexl_ids = [4855, 4874, 19050, 19051, 20282]



REXL = riders.merge(bus[['id', 'routeName']], left_on='bus_id', right_on='id', how='left')
REXL = REXL[REXL['bus_id'].isin(rexl_ids)]
REXL = REXL.drop(columns=['bus_id', 'id', 'routeName'])

start_time = pd.Timestamp("2025-10-20 00:00:00")

REXL['timestamp'] = start_time + pd.to_timedelta(REXL['time'], unit='m')
REXL = REXL.set_index('timestamp')

plt.figure(figsize=(12, 6))
#plt.plot(EE.index, EE['ridership_count'], marker='o', color ='green')
#plt.plot(EE.index, EE['ridership_count'], color='green', linewidth=2)
REXL_resampled = REXL.resample('5min').mean()  # average every 10 minutes
plt.plot(REXL_resampled.index, REXL_resampled['ridership_count'], color='green', linewidth=2)
plt.title("Ridership Time Series for REXL Buses")
plt.xlabel("Time")
plt.ylabel("Ridership Count")
plt.grid(True)
ax = plt.gca()
ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%I:%M %p'))
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()