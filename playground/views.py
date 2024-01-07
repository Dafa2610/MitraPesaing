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
from rest_framework.views import APIView
from rest_framework.response import Response
from flask import Flask, jsonify
from django.core.management.base import BaseCommand
from firebase_admin import db


 

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
    data_trsk = pd.read_csv('data.csv', sep=',')

    x = olahdata(data_trsk)
    # Pilih parameter DBSCAN
    eps = 0.002  # Sesuaikan nilai ini sesuai kebutuhan Anda
    min_samples = 5  # Sesuaikan nilai ini sesuai kebutuhan Anda

    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    x['cluster'] = dbscan.fit_predict(x[['lat', 'lng']])


    # Visualisasi hasil clustering
    # Pilih parameter DBSCAN
    eps = 0.003  # Sesuaikan nilai ini sesuai kebutuhan Anda
    min_samples = 5  # Sesuaikan nilai ini sesuai kebutuhan Anda

    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    x['cluster'] = dbscan.fit_predict(x[['lat', 'lng']])

    #menghapus kolom geometry
    x = x.drop(columns=['geometry'])

    # Visualisasi hasil clustering
    # plt.figure(figsize=(8, 6))

    plt.scatter(x['lng'], x['lat'], c=x['cluster'], cmap='viridis', s=5)
    plt.title('DBSCAN Clustering')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    # plt.show()

    plt.savefig('Datamining.png')

    selected_columns = x[["jmlh", "lat", "lng", "timestamp", "cluster"]]
    selected_columns.to_csv("data_selected.csv", index=False)

    print(x)
    
    for index, row in x.iterrows():
        data = {
            'jmlh': int(row['jmlh']),
            'lat': float(row['lat']),
            'lng': float(row['lng']),
            'timestamp': int(row['timestamp']),
            'cluster': int(row['cluster'])
        }
        
    
        # Mengirim data ke Firebase
        # ref.push().set(data)

    # Baca file CSV dan masukkan data ke Firebase Realtime Database
    # with open('data_selected.csv', newline='') as csvfile:
    #     csv_reader = csv.DictReader(csvfile)
    #     for row in csv_reader:
    #         data = {
    #             'jmlh': int(row['jmlh']),
    #             'lat': float(row['lat']),
    #             'lng': float(row['lng']),
    #             'timestamp': int(row['timestamp']),
    #             'cluster': int(row['cluster'])
    #         }
    #         # ref.push().set(data)
    # # print(x)

    # Buka file CSV dalam mode append ('a') agar Anda dapat menambahkan data baru
    # with open('data_selected.csv', mode='a', newline='') as file:
    #     writer = csv.writer(file)
    #     # Tulis data baru ke dalam file CSV
    #     for row in x:
    #         writer.writerow(row)
    #         print(row)
    # Ubah data dari Firebase ke dalam list Django

    return render(request, 'hello.html', {'data_list': selected_columns})