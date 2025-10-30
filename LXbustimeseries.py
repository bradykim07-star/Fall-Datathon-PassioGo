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
LX = LX.drop(columns=['bus_id', 'id', 'routeName'])

# Average across all days — “stacking” them into one representative day
LX = (
    LX.groupby('time')['ridership_count']
    .mean()
    .reset_index()
)


#start time adjuster
start_time = pd.Timestamp("2025-10-15 00:00:00")
LX['timestamp'] = start_time + pd.to_timedelta(LX['time'], unit='m')
LX = LX.set_index('timestamp')
LX = LX.sort_index()

#Standard deviation calculation of data
riders_all = pd.concat([pd.read_csv(f) for f in riders_files2], ignore_index=True)
riders_all = riders_all.merge(bus[['id', 'routeName']], left_on='bus_id', right_on='id', how='left')
riders_all = riders_all[riders_all['bus_id'].isin(lx_ids)]
riders_all['time_of_day'] = pd.to_timedelta(riders_all['time'], unit='m')

# compute mean and std per time across all days
stats = riders_all.groupby('time')['ridership_count'].agg(['mean', 'std']).reset_index()

# convert to timestamps for plotting
stats['timestamp'] = start_time + pd.to_timedelta(stats['time'], unit='m')
stats = stats.set_index('timestamp')
stats_resampled = stats.resample('5min').mean()


plt.figure(figsize=(12, 6))
#these are differing plotting methods
#plt.plot(LX.index, LX['ridership_count'], marker='o', color ='green')
LX_resampled = LX.resample('5min').mean()  # average every x minutes
plt.plot(LX_resampled.index, LX_resampled['ridership_count'], color='blue', linewidth=2)

plt.fill_between(stats_resampled.index, stats_resampled['mean'] - stats_resampled['std'], stats_resampled['mean'] + stats_resampled['std'], color='#9ecae1', alpha=0.4, label='±1 Std Dev')

#final plot formatting
plt.title("Ridership Time Series for LX Buses")
plt.xlabel("Time")
plt.ylabel("Ridership Count")
plt.grid(True)
ax = plt.gca()
ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%I:%M %p'))
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

