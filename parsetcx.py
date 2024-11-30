from bs4 import BeautifulSoup

with open('activity_17561885211.tcx', 'r') as f:
    data = f.read()

Bs_data = BeautifulSoup(data , "xml")

b_laps = Bs_data.find_all('Lap')

b_id = Bs_data.find_all('Id')

print((b_laps[0]))


b_lap = Bs_data.find("Lap")

trackpoints = Bs_data.find_all("Trackpoint")

