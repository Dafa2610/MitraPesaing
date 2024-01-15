from django.test import TestCase
from django_cron import models
from cron import PanggilData  # Sesuaikan dengan nama cron job Anda

class CronJobTest(TestCase):

    def test_cron_job_execution(self):
        cron_job = PanggilData()
        cron_job.do()  # Panggil metode do() untuk mengeksekusi cron job
        # Tambahkan asser atau pemeriksaan lain untuk memastikan tugas terjadwal berjalan sesuai yang diharapkan
