import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#file extraction
#1 is for spring '24 semester, 2 is for fall '25 semester
riders_files1 = ["ridership_2025-2-5.csv", "ridership_2025-2-12.csv", "ridership_2025-2-19.csv", "ridership_2025-2-26.csv", "ridership_2025-3-5.csv"]
riders_files2 = ["ridership_2025-9-3.csv", "ridership_2025-9-10.csv", "ridership_2025-9-17.csv", "ridership_2025-9-24.csv", "ridership_2025-10-1.csv"]
riders_list = [pd.read_csv(f) for f in riders_files2]
riders = pd.concat(riders_list, ignore_index=True)
bus = pd.read_csv("https://raw.githubusercontent.com/RutgersDataScienceClub/Fall-2025-Datathon/refs/heads/main/rutgers_bus_data/vehicles.csv")

#bus id key
lx_ids = [17624, 4882, 7149, 7179, 4850, 13216, 18020, 19394, 18619]

#file merging and cleaning
LX = riders.merge(bus[['id', 'routeName']], left_on='bus_id', right_on='id', how='left')
print(sorted(LX['routeName'].dropna().unique()))
LX = LX[LX['bus_id'].isin(lx_ids)]
LX = LX.drop(columns=[ 'id', 'routeName'])


#start time adjuster
start_time = pd.Timestamp("2025-10-15 00:00:00")
LX['timestamp'] = start_time + pd.to_timedelta(LX['time'], unit='m')
LX = LX.set_index('timestamp')
LX = LX.sort_index()


# Compute average ridership across all buses at each timestamp
avg_ridership = LX.groupby('timestamp')['ridership_count'].mean()

plt.figure(figsize=(12, 6))
for bus_id, data in LX.groupby('bus_id'):
    diff = data['ridership_count'] - avg_ridership.reindex(data.index)
    plt.plot(data.index, diff, label=f'Bus {bus_id}', alpha=0.8)

plt.title("Difference from Average Ridership (Each LX Bus)")
plt.xlabel("Time")
plt.ylabel("Ridership Difference")
plt.grid(True)
ax = plt.gca()
ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%I:%M %p'))
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

"""
plt.figure(figsize=(12, 6))
for bus_id, data in LX.groupby('bus_id'):
    plt.plot(data.index, data['ridership_count'], label=f'Bus {bus_id}', alpha=0.8)

plt.title("Ridership Time Series for Each LX Bus")
plt.xlabel("Time")
plt.ylabel("Ridership Count")
plt.grid(True)
ax = plt.gca()
ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%I:%M %p'))
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()
"""