import pytz

timezone = pytz.timezone(pytz.country_timezones['ID'][0])  # Ubah 'ID' dengan kode negara yang sesuai
print(f"Waktu saat ini: {timezone.zone}")