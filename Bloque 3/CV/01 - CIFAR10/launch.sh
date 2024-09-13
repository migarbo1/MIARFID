#!/bin/bash

source ~/computer_vision_lab/venv/bin/activate

python ~/computer_vision_lab/CIFAR-10/main.py $1 $2 $3 $4

deactivate
