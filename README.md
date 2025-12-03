--Zoopocalypse-- 

This program generates an escape room guideline in the form of HTML pages.
These HTML pages contain 4 challenges with randomly sampled animals from our dataset. 

The HTML pages are the demos for the challenges, with the challenge and hints to solve them whereas the markdown files contain both the randomly selected animals, hints and the correct answers. 

Some challenges (Challenge 3 and 4) contain AI generated hints using the google gemini generative model.

To run this program on NCC using slurm, first the project folder must be uploaded to the NCC. Then the slurm script should be ran through a jupyter notebook running on a kernel with the
requirements in "requirements.txt" installed. 

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

cd ~/Zoopocalypse

python3 game.py

--------------------------

Save as "enter_job_name.slurm"
and run with "!sbatch enter_job_name.slurm" 


After the program finishes running (Takes from 10 to 45 seconds because of the image hint generations), double click the game.html file. The entire challenge can be navigated from the html page that pops up.

