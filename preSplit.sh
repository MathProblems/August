#!/bin/bash
python3 parseSdata.py $1
python3 ILPFormat.py $1
