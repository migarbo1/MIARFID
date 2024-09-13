#!/bin/bash

sbatch launch.sh '0' 512 1 'S'

sbatch launch.sh '01' 512 1 'S'

sbatch launch.sh '0' 512 2 'S'

sbatch launch.sh '01' 512 2 'S'
