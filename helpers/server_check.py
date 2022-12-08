import logging
import os
import sys
import psutil
import datetime, time
import json
import socket

from loguru import logger

# Constant
LOG_LEVEL = logging.getLevelName(os.environ.get("LOG_LEVEL", "DEBUG"))
JSON_LOGS = True if os.environ.get("JSON_LOGS", "0") == "1" else False
HOST = 'localhost'  # Symbolic name meaning all available interfaces
PORT = 50007  # Arbitrary non-privileged port


def check_ram_tcp():
    flag = True
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    logger.info('Server started')
    logger.info(f'SERVER: {str(HOST)}:{str(PORT)}')
    while flag:
        s.listen(10)
        conn, addr = s.accept()
        logger.info(f'Connected by {addr}')
        while True:
            data = conn.recv(1024)
            if data == b'get':
                pid = os.getpid()
                python_process = psutil.Process(pid)
                date = str(datetime.datetime.now())
                system_info = {
                    'date': date,
                    'system_info': {
                        'cpu %': psutil.cpu_percent(),
                        'total memory:': psutil.virtual_memory()[0],
                        'memory GB used:': round(psutil.virtual_memory()[3] / 2 ** 30, 4),
                        'memory % used:': psutil.virtual_memory()[2],
                        'free memory': psutil.virtual_memory()[4]
                    },
                    'process_system_info': {
                        'Process ID': pid,
                        'Process name': python_process.name(),
                        'status': python_process.status(),
                        'Memory in percent': python_process.memory_percent(),
                        'Memory': python_process.memory_info(),
                    }
                }
                system_to_string = json.dumps(system_info)
                conn.sendall(system_to_string.encode())
                time.sleep(0.2)
                break
            if data == b'stop':
                logger.info('Stopped')
                flag = False
                break

