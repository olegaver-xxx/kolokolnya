#!/bin/bash

export DJANGO_SETTINGS_MODULE=main.settings
dramatiq tasks -p "${WORKER_COUNT:-2}" -t 1
