#!/bin/sh
set -o errexit
set -o nounset

celery -A fabpricetracker worker -l info