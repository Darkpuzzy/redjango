import logging
import os
import sys
import psutil
import datetime, time

from loguru import logger

LOG_LEVEL = logging.getLevelName(os.environ.get("LOG_LEVEL", "DEBUG"))
JSON_LOGS = True if os.environ.get("JSON_LOGS", "0") == "1" else False


class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logging():
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(LOG_LEVEL)

    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    logger.configure(handlers=[{"sink": sys.stdout, "serialize": JSON_LOGS}])


def check_ram():
    while True:
        pid = os.getpid()
        python_process = psutil.Process(pid)
        date = str(datetime.datetime.now())
        json_response = {
            'date': date,
            'system info': {
                'cpu %': psutil.cpu_percent(),
                'total memory:': psutil.virtual_memory()[0],
                'memory GB used:': round(psutil.virtual_memory()[3] / 2 ** 30, 4),
                'memory % used:': psutil.virtual_memory()[2],
                'free memory': psutil.virtual_memory()[4]
            },
            'process system info': {
                'Process ID': pid,
                'Process name': python_process.name(),
                'status': python_process.status(),
                'Memory in percent': python_process.memory_percent(),
                'Memory': python_process.memory_info(),

            }
        }

        logger.info("Check system")
        logger.info(json_response)
        time.sleep(30)


