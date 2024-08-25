import os
import datetime

from apscheduler.schedulers.background import BackgroundScheduler


def remove_old_files():
    dir_path = "file_storage/"
    now = datetime.datetime.now()

    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        if os.path.isfile(file_path):
            file_age = now - datetime.datetime.fromtimestamp(
                os.path.getctime(file_path)
                )
            if file_age.seconds > 600:
                os.remove(file_path)
                print(f"Файл был удален: {filename}")


# Настройка и запуск крон задачи
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(remove_old_files, 'interval', days=1)
    scheduler.start()
