#!/bin/bash
until ./tweets.py; do
    echo "'tweets.py' crashed with exit code $?. Restarting..." >&2
    sleep 2
done