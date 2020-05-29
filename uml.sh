#!/bin/sh

pyreverse -a 0 -s 0 -f PUB_ONLY -o pdf ./factory.py \
          ./order.py \
          ./mes.py \
          ./interpreter.py \
           -p All