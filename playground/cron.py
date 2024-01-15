from django_cron import CronJobBase, Schedule
from .views import GetFirebaseDataCronJob  # Sesuaikan dengan path dan nama fungsi views Anda

class PanggilData(CronJobBase):
    RUN_AT_TIMES = Schedule(run_at_times=['00:00'])

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'playground.cron.PanggilData'

    def do(self):
        # Panggil fungsi dari views Anda
        GetFirebaseDataCronJob()
        pass
