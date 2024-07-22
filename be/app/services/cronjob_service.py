from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app.services.certificate_service import CertificateService
from config.config import Config
from bson.objectid import ObjectId
from apscheduler.jobstores.base import JobLookupError

class CronjobService:
    def __init__(self, client, scheduler: BackgroundScheduler):
        db = client['it']
        self.collection = db['cronjobs']
        self.client = client
        self.scheduler = scheduler

    def add_cronjob(self, cronjob_data):
        result = self.collection.insert_one(cronjob_data)
        self.schedule_job(cronjob_data, scheduler=self.scheduler)
        return str(result.inserted_id)

    def update_cronjob(self, cronjob_id, cronjob_data):
        cronjob_data = {k: v for k, v in cronjob_data.items() if k != '_id'}
        self.collection.update_one(
            {"_id": ObjectId(cronjob_id)},
            {"$set": cronjob_data}
        )
        self.schedule_job(cronjob_data, cronjob_id, scheduler=self.scheduler)
        return cronjob_id

    def delete_cronjob(self, cronjob_id):
        self.collection.delete_one({"_id": ObjectId(cronjob_id)})
        try:
            self.scheduler.remove_job(str(cronjob_id))
        except JobLookupError:
            print(f"No job by the id of {cronjob_id} was found in the scheduler.")


    def get_cronjobs(self):
        cronjobs = list(self.collection.find())
        for cronjob in cronjobs:
            cronjob['_id'] = str(cronjob['_id'])
        return cronjobs 

    def load_jobs(self, scheduler: BackgroundScheduler = None):
        if not scheduler:
            scheduler = BackgroundScheduler()
        jobs = list(self.collection.find())
        for job in jobs:
            self.schedule_job(job, str(job['_id']), scheduler)

    def schedule_job(self, job_data, job_id=None, scheduler: BackgroundScheduler = None):
        if not scheduler:
            scheduler = BackgroundScheduler()

        job_id = job_id or str(job_data['_id'])
        if not job_id:
            raise ValueError("job_id must be a nonempty string")

        trigger = CronTrigger.from_crontab(job_data['expression'])
        task_function = self.get_task_function(job_data['task'])
        scheduler.add_job(
            func=task_function,
            trigger=trigger,
            id=job_id,
            replace_existing=True
        )

    def get_task_function(self, task_name):
        if task_name == 'sync_cloudflare':
            return self.run_sync_cloudflare
        elif task_name == 'check_subdomains':
            return self.run_check_subdomains
        # 添加更多任务对应的函数
        raise ValueError(f"未知任务: {task_name}")

    def run_sync_cloudflare(self):
        Config.refresh_settings_cache()
        certificate_service = CertificateService(self.client)
        certificate_service.sync_cloudflare_records()

    def run_check_subdomains(self):
        Config.refresh_settings_cache()
        certificate_service = CertificateService(self.client)
        domain_list = certificate_service.get_domain_list()
        filtered_domain_list = certificate_service.filter_valid_domains(domain_list)
        if filtered_domain_list:
            certificate_service.check_subdomains(filtered_domain_list)
