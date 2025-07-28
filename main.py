import psutil
import time
import csv
from datetime import datetime

def bytes_to_mb(bytes_val):
    return round(bytes_val / (1024 * 1024), 2)


