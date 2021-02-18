#!/bin/bash
export PYTHONPATH=$PYTHONPATH:`pwd`/cocotb_helper
python3 nmigen/tb.py
