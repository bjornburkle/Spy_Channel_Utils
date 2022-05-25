#!/bin/bash

RUNNUMBER=$1
PARTITIONS=( "TI_27-JAN-2010_2" "TM_09-JUN-2009_1" "TO_30-JUN-2009_1" "TP_09-JUN-2009_1" )
for PARTITION in "${PARTITIONS[@]}"; do
    cp sourcefromedm_TEMPLATE_cfg.py sourcefromedm_${PARTITION}_${RUNNUMBER}_cfg.py
    sed -i "s/RUNNUMBER/${RUNNUMBER}/g" sourcefromedm_${PARTITION}_${RUNNUMBER}_cfg.py
    sed -i "s/PARTITION/${PARTITION}/g" sourcefromedm_${PARTITION}_${RUNNUMBER}_cfg.py
done
