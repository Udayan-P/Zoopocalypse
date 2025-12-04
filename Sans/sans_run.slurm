#!/bin/bash
#SBATCH --job-name=sans_animal_gen
#SBATCH --partition=cpu
#SBATCH --output=sans_gen_output.txt
#SBATCH --error=sans_gen_error.txt
#SBATCH --time=00:05:00
#SBATCH --mem=1G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --chdir=/home3/fctm02/advprog/zoopocalypse/Zoopocalypse
echo "Running Challenge 1 generator on NCC..."
source venv/bin/activate
python3 Sans/animal_challenge_pipeline.py
echo "Job complete."
