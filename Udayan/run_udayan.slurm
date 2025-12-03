#!/bin/bash
#SBATCH --job-name=udayan_hangman_gen
#SBATCH --output=hangman_gen_output.txt
#SBATCH --error=hangman_gen_error.txt
#SBATCH --time=00:05:00
#SBATCH --mem=2G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --chdir=/home3/rbfn02/advprog/Zoopocalypse

echo "Running hangman generator with Python 3..."
python3 Udayan/generators/hangman_generator.py

echo "Job complete."