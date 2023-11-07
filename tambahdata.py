import random
import csv

# Buat file CSV untuk menyimpan data
with open('data.csv', 'w', newline='') as csvfile:
    fieldnames = ['jmlh', 'lat', 'lng']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Buat 1000 data acak dalam format yang diinginkan
    for _ in range(500):
        jmlh = random.randint(10000, 100000)
        lat = round(random.uniform(-0.06, -0.01), 6)
        lng = round(random.uniform(109.3, 109.4), 6)

        row = {'jmlh': jmlh, 'lat': lat, 'lng': lng}
        writer.writerow(row)