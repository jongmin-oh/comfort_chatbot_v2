#!/bin/sh
gunicorn manage:app --worker-class=uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000 --reload