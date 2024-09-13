#!/bin/bash

# transformations; batch size; epochs; imbalance treatment; network; size of Densenet; crop size

sbatch launch.sh '03' 512 150 2 3 'p' 32

sbatch launch.sh '13' 512 150 2 3 'p' 32

sbatch launch.sh '23' 512 150 2 3 'p' 32

