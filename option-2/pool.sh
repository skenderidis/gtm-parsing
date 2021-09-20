#!/bin/bash

cp /config/bigip_gtm.conf /config/temp.conf
python /config/pool.py
