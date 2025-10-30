import pandas as pd
import matplotlib.pyplot as plt

#riders = pd.read_csv("https://raw.githubusercontent.com/RutgersDataScienceClub/Fall-2025-Datathon/refs/heads/main/rutgers_bus_data/ridership.csv")
riders = pd.read_csv("ridership_2025-10-20.csv")
bus = pd.read_csv("https://raw.githubusercontent.com/RutgersDataScienceClub/Fall-2025-Datathon/refs/heads/main/rutgers_bus_data/vehicles.csv")


merged = riders.merge(bus[['id', 'routeName']], left_on='bus_id', right_on='id', how='left')
ridership_summary = merged.groupby('routeName')['ridership_count'].agg(total_boarded='sum',total_trips='count',avg_boarded='mean').reset_index()
result = merged.merge(ridership_summary, on='routeName', how='left')



plt.figure(figsize=(10, 6))
plt.barh(ridership_summary['routeName'], ridership_summary['avg_boarded'], color='blue')
plt.xlabel('Average Ridership Count')
plt.ylabel('Bus Route')
plt.title('Average Ridership per Bus Route')
plt.tight_layout()
plt.show()
