# from django_cron import CronJobBase, Schedule
# import geopandas as gpd
# import pandas as pd
# import firebase_admin
# from firebase_admin import credentials, db
# from sklearn.cluster import DBSCAN
# import matplotlib.pyplot as plt

# # Initialize Firebase only once
# if not firebase_admin._apps:
#     cred = credentials.Certificate("pesaing-bornewtech-firebase-adminsdk-b7jjc-f0515b7c83.json")
#     firebase_admin.initialize_app(cred, {
#         'databaseURL': 'https://pesaing-bornewtech-default-rtdb.firebaseio.com/'
#     })

# class GetFirebaseDataCronJob(CronJobBase):
#     RUN_EVERY_MIDNIGHT = Schedule(run_at_times=['00:00'])

#     schedule = RUN_EVERY_MIDNIGHT
#     code = 'pesaing.get_firebase_data_cron_job'  # Unique code for this cron job

#     def do(self):
#         ref = db.reference('data')

#         # Import data from Firebase
#         firebase_data = ref.get()

#         print(firebase_data)

#         # Inisialisasi data
#         data_trsk = pd.DataFrame.from_records(firebase_data)

#         def olahdata(data):
#             data_fix = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data['lng'], data['lat']))
#             return data_fix 

#         x = olahdata(data_trsk)

#         # Pilih parameter DBSCAN
#         eps = 0.004  # Sesuaikan nilai ini sesuai kebutuhan Anda
#         min_samples = 4  # Sesuaikan nilai ini sesuai kebutuhan Anda

#         dbscan = DBSCAN(eps=eps, min_samples=min_samples)
#         x['cluster'] = dbscan.fit_predict(x[['lng', 'lat']])

#         # Hapus Data
#         ref.delete()

#         # Menghapus kolom geometry
#         x = x.drop(columns=['geometry'])

#         df = pd.DataFrame(x)

#         # Menghitung total jmlh berdasarkan nilai cluster yang lebih dari 1
#         total_jmlh_per_cluster = df[df['cluster'] > 1].groupby('cluster')['jmlh'].sum().reset_index()

#         # Menggabungkan total_jmlh_per_cluster dengan DataFrame asli
#         result_df = pd.merge(df, total_jmlh_per_cluster, how='left', on='cluster', suffixes=('', '_total'))

#         # Mengisi nilai NaN pada kolom jmlh_total dengan 0
#         result_df['jmlh_total'] = result_df['jmlh_total'].fillna(0)

#         # Membuat fungsi untuk normalisasi berdasarkan rentang nilai
#         def custom_normalize(value):
#             if value <= 0:
#                 return 0.2
#             elif value <= 100000:
#                 return 0.4
#             elif value <= 500000:
#                 return 0.6
#             else:
#                 return 1.0

#         # Mengaplikasikan fungsi normalisasi pada kolom jmlh_total
#         result_df['jmlh_total_normalized'] = result_df['jmlh_total'].apply(custom_normalize)

#         # Menampilkan DataFrame hasil
#         print(result_df)

#         # Visualisasi hasil clustering
#         plt.scatter(result_df['lng'], result_df['lat'], c=result_df['cluster'], cmap='viridis', s=5)
#         plt.title('DBSCAN Clustering')
#         plt.xlabel('Longitude')
#         plt.ylabel('Latitude')
#         plt.savefig('Datamining.png')

#         result_df.to_csv("data_selected.csv", index=False)

#         print(result_df)

#         for index, row in result_df.iterrows():
#             data = {
#                 'jmlh': int(row['jmlh']),
#                 'lat': float(row['lat']),
#                 'lng': float(row['lng']),
#                 'timestamp': int(row['timestamp']),
#                 'cluster': int(row['cluster']),
#                 'weight': float(row['jmlh_total_normalized'])
#             }

#             # Mengirim data ke Firebase
#             ref.push().set(data)

#         print("Tugas harian berjalan pada jam 00.00")

