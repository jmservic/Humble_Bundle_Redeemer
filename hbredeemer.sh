#!/bin/bash
TOP_DIR=$(dirname $0)
cd $TOP_DIR
source venv/bin/activate
python src/main.py $@

