from django.shortcuts import render
from django.http import HttpResponse
from playground.script import olahdata
import pandas as pd
import firebase_admin
from firebase_admin import credentials, db
from io import BytesIO
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
import csv
import base64



 

# Create your views here.
cred = credentials.Certificate("pesaing-bornewtech-firebase-adminsdk-b7jjc-f0515b7c83.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://pesaing-bornewtech-default-rtdb.firebaseio.com/'
})

def get_data_from_firebase(request):
    # Referensi Firebase
    ref = db.reference('data')  # Ganti dengan path data di Firebase

    # Ambil data dari Firebase
    firebase_data = ref.get()
    # Inisialisasi list Django
    data_list = []

    # with open('data.csv', 'w', newline='') as csvfile:
    #     fieldnames = ['jmlh', 'lat', 'lng']
    #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #     writer.writeheader()

    #     # Looping melalui anak-anak (trsk1, trsk2, trsk3) dan menulis data ke dalam file CSV
    #     for key, value in firebase_data.items():
    #         row = {
    #             'jmlh': value.get('jmlh', ''),
    #             'lat': value.get('lat', ''),
    #             'lng': value.get('lng', '')
    #         }
    #         writer.writerow(row)
    
    data_trsk = pd.read_csv('data.csv', sep=',')

    x = olahdata(data_trsk)
    # Pilih parameter DBSCAN
    eps = 0.003  # Sesuaikan nilai ini sesuai kebutuhan Anda
    min_samples = 5  # Sesuaikan nilai ini sesuai kebutuhan Anda

    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    x['cluster'] = dbscan.fit_predict(x[['lat', 'lng']])

    # Visualisasi hasil clustering
    plt.figure(figsize=(8, 6))
    plt.scatter(x['lng'], x['lat'], c=x['cluster'], cmap='viridis', s=5)
    plt.title('DBSCAN Clustering')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Hasil Clustering dengan DBSCAN')
    plt.colorbar()
    plt.grid(True)

    plt.savefig('Datamining.png')

    print(x)
    # Ubah data dari Firebase ke dalam list Django

    return render(request, 'hello.html', {'data_list': firebase_data})