import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#file extraction
riders_files1 = ["ridership_2025-2-5.csv", "ridership_2025-2-12.csv", "ridership_2025-2-19.csv", "ridership_2025-2-26.csv", "ridership_2025-3-5.csv"]
riders_files2 = ["ridership_2025-9-3.csv", "ridership_2025-9-10.csv", "ridership_2025-9-17.csv", "ridership_2025-9-24.csv", "ridership_2025-10-1.csv"]
riders_list = [pd.read_csv(f) for f in riders_files1]
riders = pd.concat(riders_list, ignore_index=True)

bus = pd.read_csv("https://raw.githubusercontent.com/RutgersDataScienceClub/Fall-2025-Datathon/refs/heads/main/rutgers_bus_data/vehicles.csv")

#bus ids to match
ee_ids = [4896, 13208, 4862, 15188, 15185, 18015, 20284]

#file merging and cleaning
EE = riders.merge(bus[['id', 'routeName']], left_on='bus_id', right_on='id', how='left')
EE = EE[EE['bus_id'].isin(ee_ids)]
EE = EE.drop(columns=['bus_id', 'id', 'routeName'])


EE = (
    EE.groupby('time')['ridership_count']
    .mean()
    .reset_index()
)


#setting up time series
start_time = pd.Timestamp("2025-10-15 00:00:00")
EE['timestamp'] = start_time + pd.to_timedelta(EE['time'], unit='m')
EE = EE.set_index('timestamp')

#Standard deviation calculation of data
riders_all = pd.concat([pd.read_csv(f) for f in riders_files1], ignore_index=True)
riders_all = riders_all.merge(bus[['id', 'routeName']], left_on='bus_id', right_on='id', how='left')
riders_all = riders_all[riders_all['bus_id'].isin(ee_ids)]
riders_all['time_of_day'] = pd.to_timedelta(riders_all['time'], unit='m')


# compute mean and std per time across all days
stats = riders_all.groupby('time')['ridership_count'].agg(['mean', 'std']).reset_index()


# convert to timestamps for plotting
stats['timestamp'] = start_time + pd.to_timedelta(stats['time'], unit='m')
stats = stats.set_index('timestamp')
stats_resampled = stats.resample('5min').mean()

#plotting
plt.figure(figsize=(12, 6))

#these are differing plotting methods
#plt.plot(EE.index, EE['ridership_count'], marker='o', color ='green')
#plt.plot(EE.index, EE['ridership_count'], color='green', linewidth=2)
EE_resampled = EE.resample('5min').mean()  # average every x minutes
plt.plot(EE_resampled.index, EE_resampled['ridership_count'], color='blue', linewidth=2)

plt.fill_between(stats_resampled.index, stats_resampled['mean'] - stats_resampled['std'], stats_resampled['mean'] + stats_resampled['std'],color='#9ecae1', alpha=0.4, label='±1 Std Dev')


#standard plot formatting
plt.title("Ridership Time Series for EE Buses")
plt.xlabel("Time")
plt.ylabel("Ridership Count")
plt.grid(True)
ax = plt.gca()
ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%I:%M %p'))
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()