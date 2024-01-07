import random
import csv
from datetime import datetime, timedelta

def generate_random_timestamp_within_last_30_days():
    # Menghitung tanggal sekarang
    end_date = datetime.now()
    
    # Mendapatkan tanggal 30 hari yang lalu
    start_date = end_date - timedelta(days=30)
    
    # Mengonversi tanggal menjadi detik
    start_timestamp = int(start_date.timestamp())
    end_timestamp = int(end_date.timestamp())

    # Menghasilkan timestamp secara acak dalam rentang waktu
    random_timestamp = random.randint(start_timestamp, end_timestamp)
    
    return random_timestamp

# Buat file CSV untuk menyimpan data
with open('data.csv', 'w', newline='') as csvfile:
    fieldnames = ['jmlh', 'lat', 'lng','timestamp']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Buat 1000 data acak dalam format yang diinginkan
    for _ in range(1000):
        jmlh = random.randint(10000, 100000)
        lat = round(random.uniform(-0.06, -0.01), 6)
        lng = round(random.uniform(109.3, 109.4), 6)
        timestamp = round(generate_random_timestamp_within_last_30_days())

        row = {'jmlh': jmlh, 'lat': lat, 'lng': lng, 'timestamp': timestamp}
        writer.writerow(row)