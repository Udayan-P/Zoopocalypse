#!/bin/bash

#SBATCH -N 1 #SBATCH -c 2

#SBATCH -p "cpu" #SBATCH --qos="short" #SBATCH -t 00:10:00

source /etc/profile


python3 GAME.py