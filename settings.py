#!/usr/bin/env python3
import os

port = str(os.getenv("REDIS_PORT", 6379))
db = str(os.getenv("REDIS_DB", 0))
host = str(os.getenv("REDIS_HOST", 'redis'))

REDIS_URL = f"redis://{host}:{port}/{db}"
RQ_DASHBOARD_REDIS_URL = REDIS_URL
QUEUES = ['default']
