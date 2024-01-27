from django_cron import CronJobBase, Schedule
from django.shortcuts import render
from django.http import HttpResponse
from playground.script import olahdata
import pandas as pd
import firebase_admin
from firebase_admin import credentials, db
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

class GetFirebaseDataCronJob(CronJobBase):
    ref = db.reference('data')  # Ganti dengan path data di Firebase


    # Ambil data dari Firebase
    firebase_data = ref.get()

    print(firebase_data)
    # Inisialisasi list Django
    data_trsk = pd.read_csv('data.csv', sep=',')

    x = olahdata(data_trsk)
    # Pilih parameter DBSCAN
    eps = 0.002  # Sesuaikan nilai ini sesuai kebutuhan Anda
    min_samples = 5  # Sesuaikan nilai ini sesuai kebutuhan Anda

    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    x['cluster'] = dbscan.fit_predict(x[['lat', 'lng']])

    #Hapus Data
    ref.delete()

    berat_cluster = x['cluster'].value_counts()
    print(berat_cluster)

    # Visualisasi hasil clustering
    # Pilih parameter DBSCAN
    eps = 0.003  # Sesuaikan nilai ini sesuai kebutuhan Anda
    min_samples = 5  # Sesuaikan nilai ini sesuai kebutuhan Anda

    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    x['cluster'] = dbscan.fit_predict(x[['lat', 'lng']])

    #menghapus kolom geometry
    x = x.drop(columns=['geometry'])

    df = pd.DataFrame(x)

    # Menghitung total jmlh berdasarkan nilai cluster yang lebih dari 1
    total_jmlh_per_cluster = df[df['cluster'] > 1].groupby('cluster')['jmlh'].sum().reset_index()

    # Menggabungkan total_jmlh_per_cluster dengan DataFrame asli
    result_df = pd.merge(df, total_jmlh_per_cluster, how='left', on='cluster', suffixes=('', '_total'))

    # Mengisi nilai NaN pada kolom jmlh_total dengan 0
    result_df['jmlh_total'] = result_df['jmlh_total'].fillna(0)

    # Membuat fungsi untuk normalisasi berdasarkan rentang nilai
    def custom_normalize(value):
        if value <= 100000:
            return 1
        elif value <= 500000:
            return 2
        elif value <= 700000:
            return 3
        elif value <= 1000000:
            return 4
        else:
            return 5

    # Mengaplikasikan fungsi normalisasi pada kolom jmlh_total
    result_df['jmlh_total_normalized'] = result_df['jmlh_total'].apply(custom_normalize)

    # Menampilkan DataFrame hasil
    print(result_df)

    # Visualisasi hasil clustering
    # plt.figure(figsize=(8, 6))

    plt.scatter(result_df['lng'], result_df['lat'], c=result_df['cluster'], cmap='viridis', s=5)
    plt.title('DBSCAN Clustering')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    # plt.show()

    plt.savefig('Datamining.png')

    selected_columns = result_df[["jmlh", "lat", "lng", "timestamp", "cluster"]]
    selected_columns.to_csv("data_selected.csv", index=False)

    print(result_df)
    
    for index, row in result_df.iterrows():
        data = {
            'jmlh': int(row['jmlh']),
            'lat': float(row['lat']),
            'lng': float(row['lng']),
            'timestamp': int(row['timestamp']),
            'cluster': int(row['cluster']),
            'weight': float(row['jmlh_total_normalized'])
        }
        
    
        # Mengirim data ke Firebase
        ref.push().set(data)
    
    # return render(request, 'hello.html', {'data_list': x})
    # RUN_EVERY_MIDNIGHT = Schedule(run_at_times=['00:00'])
    # # Referensi Firebase 
    # def do(self):