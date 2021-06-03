#!/bin/bash

if [ "$1" == "-d" ]; then
	docker run -v `pwd`:/workdir nm bash -c "cd workdir; bash sim.bash"
else
	python3 nmigen/tb.py
fi
