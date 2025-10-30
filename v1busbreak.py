import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

times = pd.read_csv("https://raw.githubusercontent.com/RutgersDataScienceClub/Fall-2025-Datathon/6e17076c548dee460e94ecdf540c991bb2d0f56b/rutgers_bus_data/bus_breaks.csv")
stops = pd.read_csv("https://raw.githubusercontent.com/RutgersDataScienceClub/Fall-2025-Datathon/refs/heads/main/rutgers_bus_data/stops.csv")
bus = pd.read_csv("https://raw.githubusercontent.com/RutgersDataScienceClub/Fall-2025-Datathon/refs/heads/main/rutgers_bus_data/vehicles.csv")

x = times[['id', 'stop_id', 'break_duration']]
y = bus[['id', 'routeName']]

merged = x.merge(y, on='id', how='left')


break_summary = merged.groupby('stop_id')['break_duration'].agg(sum='sum', count='count', avg='mean').reset_index() #calculates the mean breaks
result = stops.merge(break_summary, on='stop_id', how='left') #merges the stops to get a final array

result_nonzero = result[result['avg'] > 0] #get rid of stops with no breaks/don't exist anymore

plt.figure(figsize=(10, 12))
labels = result_nonzero['shortname'].astype(str)
plt.barh(labels, result_nonzero['avg'], color='skyblue')
plt.xlabel('Average Break Time (minutes)')
plt.ylabel('Bus Stop')
plt.title('Average Break Duration per Bus Stop')
plt.tight_layout()
plt.show()




