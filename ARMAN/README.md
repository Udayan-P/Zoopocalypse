--Zoopocalypse-- 

This program generate the challenge 4.

The challenge is to order the given animals in the correct order (Ascending) based on the given feature.

The user can also click on the animals' names to reveal AI generated images of the animals to get an idea.

--------------------------
Example SLURM batch script
--------------------------

#!/bin/bash

#SBATCH -N 1
#SBATCH -c 2

#SBATCH -p "cpu"
#SBATCH --qos="short"
#SBATCH -t 00:10:00

source /etc/profile

python3 GAME.py

--------------------------

Save as "enter_job_name.slurm"
and run with "!sbatch enter_job_name.slurm" 


After the program finishes running (Takes from 5 to 30 seconds because of the image hint generations), double click the challenge.html file in the html folder.

Due to the programs running in root on NCC the program sometimes can't find the proper path for some files such as images when the HTML file is opened through JupyterLab.

