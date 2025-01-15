import os
import datetime
import logging
from apscheduler.schedulers.background import BackgroundScheduler


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("cleanup.log"), logging.StreamHandler()]
)


def remove_old_files():
    """Удаляет файлы старше 30 дней из директории 'file_storage'."""
    dir_path = "file_storage/"
    now = datetime.datetime.now()

    # Проверяем, существует ли директория
    if not os.path.exists(dir_path):
        logging.warning(f"Директория {dir_path} не существует.")
        return

    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        if os.path.isfile(file_path):
            try:
                # Вычисляем возраст файла
                file_age = now - datetime.datetime.fromtimestamp(
                    os.path.getctime(file_path)
                )

                # Удаляем файл, если его возраст превышает 30 дней
                if file_age.days > 30:
                    os.remove(file_path)
                    logging.info(f"Файл удален: {filename}")
            except Exception as e:
                logging.error(f"Ошибка при удалении {file_path}: {e}")


def start_scheduler():
    """
    Настраивает и запускает планировщик для выполнения задачи
    удаления старых файлов ежедневно.
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(remove_old_files, 'interval', days=1)
    scheduler.start()
    logging.info("Планировщик запущен.")
