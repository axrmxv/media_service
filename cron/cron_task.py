import os
import datetime

from apscheduler.schedulers.background import BackgroundScheduler


def remove_old_files():
    """Удаляет файлы старше 30 дней из директории 'file_storage'."""
    dir_path = "file_storage/"
    now = datetime.datetime.now()

    # Проверяем, существует ли директория
    if not os.path.exists(dir_path):
        print(f"Директория {dir_path} не существует.")
        return

    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        if os.path.isfile(file_path):
            # Вычисляем возраст файла
            file_age = now - datetime.datetime.fromtimestamp(
                os.path.getctime(file_path)
                )

            # Удаляем файл, если его возраст превышает 10 минут
            if file_age.seconds > 600:
                os.remove(file_path)
                print(f"Файл был удален: {filename}")


def start_scheduler():
    """
    Настраивает и запускает планировщик для выполнения задачи
    удаления старых файлов ежедневно.
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(remove_old_files, 'interval', days=1)
    scheduler.start()
