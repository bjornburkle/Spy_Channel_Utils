#!/bin/bash

for i in {1..128..5}; do
    echo "346345 $i $(($i+4))"
done > cmdList.txt
