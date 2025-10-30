import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

riders_files = ["ridership_2025-2-5.csv", "ridership_2025-2-12.csv", "ridership_2025-2-19.csv", "ridership_2025-2-26.csv", "ridership_2025-3-5.csv"]
riders_list = [pd.read_csv(f) for f in riders_files]
riders = pd.concat(riders_list, ignore_index=True)
bus = pd.read_csv("https://raw.githubusercontent.com/RutgersDataScienceClub/Fall-2025-Datathon/refs/heads/main/rutgers_bus_data/vehicles.csv")

h_ids = [4866, 18016, 19399]

H = riders.merge(bus[['id', 'routeName']], left_on='bus_id', right_on='id', how='left')
H = H[H['bus_id'].isin(h_ids)]
H = H.drop(columns=['bus_id', 'id', 'routeName'])

#use this commented snippet below if time needs to be adjusted to 6am start
start_time = pd.Timestamp("2025-10-20 00:00:00")

H['timestamp'] = start_time + pd.to_timedelta(H['time'], unit='m')
H = H.set_index('timestamp')


plt.figure(figsize=(12, 6))
#plt.plot(H.index, H['ridership_count'], marker='o', color ='green')
H_resampled = H.resample('10min').mean()  # average every 10 minutes
plt.plot(H_resampled.index, H_resampled['ridership_count'], color='green', linewidth=2)
plt.title("Ridership Time Series for H Buses")
plt.xlabel("Time")
plt.ylabel("Ridership Count")
plt.grid(True)
ax = plt.gca()
ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%I:%M %p'))
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()