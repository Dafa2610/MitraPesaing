import random
import csv
from datetime import datetime, timedelta
import os
import math

def generate_random_timestamp_within_last_30_days():
    # Menghitung tanggal sekarang
    end_date = datetime.now()
    
    # Mendapatkan tanggal 30 hari yang lalu
    start_date = end_date - timedelta(days=60)
    
    # Mengonversi tanggal menjadi detik
    start_timestamp = int(start_date.timestamp())
    end_timestamp = int(end_date.timestamp())

    # Menghasilkan timestamp secara acak dalam rentang waktu
    random_timestamp = random.randint(start_timestamp, end_timestamp)
    
    return random_timestamp

def generate_random_points_within_radius(lat_ref, lng_ref, radius, num_points):
    points = []
    for _ in range(num_points):
        # Generate random distance and angle
        r = radius * math.sqrt(random.random())
        theta = random.uniform(0, 2*math.pi)
        # Convert to coordinates offset from reference point
        lat_offset = r * math.cos(theta) / 111111
        lng_offset = r * math.sin(theta) / (111111 * math.cos(lat_ref))
        # Calculate new coordinates
        lat = lat_ref + lat_offset
        lng = lng_ref + lng_offset
        points.append((lat, lng))
    return points

# Titik referensi
lat_ref = -0.044673831123607885
lng_ref = 109.3315755956118
# Buat file CSV jika belum ada
file_path = 'data.csv'
if not os.path.exists(file_path):
    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = ['jmlh', 'lat', 'lng', 'timestamp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

# Buka file CSV dalam mode append
with open(file_path, 'a', newline='') as csvfile:
    fieldnames = ['jmlh', 'lat', 'lng', 'timestamp']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Buat 1000 data acak dalam format yang diinginkan
    # for _ in range(100):
    #     jmlh = random.randint(10000, 150000)
    #     lat = round(random.uniform(-0.07, 0.02), 6)
    #     lng = round(random.uniform(109.23, 109.4), 6)
    #     timestamp = round(generate_random_timestamp_within_last_30_days())

    #     row = {'jmlh': jmlh, 'lat': lat, 'lng': lng, 'timestamp': timestamp}
    #     writer.writerow(row)
    
    # Buat 10 data acak di dalam radius 500m dari titik referensi
    radius_meters = 500
    num_points = 10
    random_points = generate_random_points_within_radius(lat_ref, lng_ref, radius_meters, num_points)

    for i, point in enumerate(random_points, 1):
        lat, lng = point
        timestamp = round(generate_random_timestamp_within_last_30_days())
        jmlh = random.randint(10, 150) * 1000

        row = {'jmlh': jmlh, 'lat': lat, 'lng': lng, 'timestamp': timestamp}
        writer.writerow(row)