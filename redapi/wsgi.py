import multiprocessing
import os
import logging

from django.core.wsgi import get_wsgi_application
import threading
from users.cashinfo import setup_logging, logger, check_ram


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'redapi.settings')

# LOGGIN INFO
setup_logging()
process_name = multiprocessing.current_process().name
logger.info(f'Process {process_name} started')
for k, v in os.environ.items():
    logger.info(f'{k}={v}')

logger.info("Server started")

thr = threading.Thread(target=check_ram, daemon=True).start()

application = get_wsgi_application()
