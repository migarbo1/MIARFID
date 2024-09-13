#!/bin/bash

# layer; dropout; batch size; epochs; unfreeze epoch; initial LR; unfreeze LR; network 

sbatch launch.sh -2 '0.3' 64 300 150 '1e-1' '1e-4' 'res'

sbatch launch.sh -2 '0.3' 64 200 100 '1e-1' '1e-4' 'res'

sbatch launch.sh -1 '0.3' 64 300 150 '1e-1' '1e-4' 'res'

sbatch launch.sh -1 '0.3' 64 200 150 '1e-1' '1e-4' 'res'

sbatch launch.sh -1 '0.3' 64 200 100 '1e-1' '1e-4' 'res'

sbatch launch.sh 40 '0.3' 64 100 75 '1e-1' '1e-4' 'vgg'

sbatch launch.sh 37 '0.3' 64 100 75 '1e-1' '1e-4' 'vgg'

sbatch launch.sh 33 '0.3' 64 100 75 '1e-1' '1e-4' 'vgg'

sbatch launch.sh 30 '0.3' 64 100 75 '1e-1' '1e-4' 'vgg'

sbatch launch.sh -1 '0.3' 64 300 150 '1e-1' '1e-4' 'den'

sbatch launch.sh -1 '0.3' 64 200 100 '1e-1' '1e-4' 'den'

sbatch launch.sh -1 '0.3' 64 300 150 '1e-1' '1e-4' 'den'

sbatch launch.sh -1 '0.3' 64 200 150 '1e-1' '1e-4' 'den'

sbatch launch.sh -1 '0.3' 64 200 100 '1e-1' '1e-4' 'den'
