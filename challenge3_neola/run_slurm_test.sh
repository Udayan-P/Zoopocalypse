#!/bin/bash
#SBATCH --job-name=zoop_test
#SBATCH --output=slurm_zoop_test.out
#SBATCH --error=slurm_zoop_test.err
#SBATCH --time=00:10:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --partition=jupyter

echo "=== Python version ==="
python3 --version

echo "=== Running generator ==="
python3 challenge3_neola/feature_challenge_generator.py \
    challenge3_neola/animals.json \
    challenge3_neola/feature_challenge.json

echo "=== DONE ==="
