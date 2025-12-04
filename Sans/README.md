
🐾 **Zoopocalypse — Challenge 1 Implementation**

A JSON-Driven, Dataset-Conditioned Image-Inference Puzzle**


1. Introduction

This document describes the implementation of Challenge 1 for the Advanced Programming module.
The challenge presents a blurred animal image inference task, where the user is required to identify the species through a combination of:
	•	Controlled hint revelation
	•	Progressive blur reduction
	•	Multiple-choice decision making

The entire challenge is generated programmatically through a Python–JSON–HTML pipeline, ensuring reproducibility, transparency, and full alignment with the coursework specification.

Minimal inline JavaScript is used exclusively within the HTML renderer to enable small UI transitions; no standalone JavaScript files are employed, thereby meeting module constraints.


2. System Overview

Challenge 1 comprises three principal components:
	1.	Dataset-Driven JSON Generator
(generator.py)
Constructs a challenge instance by sampling from a curated zoological dataset and producing a structured JSON specification.
	2.	Pipeline Controller
(animal_challenge_pipeline.py)
Executes dataset loading, challenge construction, JSON serialisation, and HTML rendering.
	3.	Interactive HTML Renderer
(animal_challenge_html_renderer.py)
Produces a functional, interactive web-based challenge that responds dynamically to user actions (e.g., unblurring, hint requests).

The pipeline ensures deterministic structure while maintaining stochastic variability in animal selection.


3. JSON Schema Specification

Each challenge instance is represented by a formally defined JSON object.
An example is presented below:
```
{
  "challenge_id": "animal_001",
  "image": "Dataset/Images/Seal.jpg",
  "question": "Which animal is shown in this picture?",
  "options": ["seal", "tortoise", "lion", "mole"],
  "answer": "seal",
  "hints": [
    "This animal is primarily a carnivore.",
    "It typically lives in cold coastal waters.",
    "Its predators include polar bears and orcas.",
    "It belongs to the Phocidae family."
  ]
}
```
Core Fields

Field	Description
challenge_id	Unique identifier following animal_XXX pattern.
image	Path to local dataset image used for rendering.
question	User-facing prompt.
options	Multiple-choice candidates (1 correct + distractors).
answer	Ground-truth species label.
hints	Ordered list of progressively informative biological hints.

The JSON format is intentionally modular, enabling straightforward extension to new datasets, difficulty levels, or rendering systems.

⸻

4. Gameplay and Pedagogical Logic

The interface is designed around controlled information release:
	1.	Initial State
The displayed image is fully blurred, preventing trivial identification.
	2.	User Actions
	•	Reveal Hint → decreases score by 1
	•	Reduce Blur → decreases score by 1
	•	Submit Guess → validated immediately
	3.	Terminal Conditions
	•	Correct answer → image revealed, challenge completed
	•	Score reaches zero → user fails the attempt

This mechanic reinforces incremental reasoning and mirrors typical inference processes in AI-augmented decision-making systems.

⸻

5. Hint Generation Methodology

Hints are inferred directly from dataset attributes, including:
	•	Dietary classification
	•	Habitat descriptors
	•	Predator relationships
	•	Taxonomic family
	•	Conservation status

Hints progress from general → specific to maintain graded difficulty.
In cases of missing metadata, robust fallback hints ensure continuity of gameplay.

⸻

6. Pipeline Execution Summary

Running:

python Sans/animal_challenge_pipeline.py

Performs:
	1.	Dataset loading (CSV via pandas)
	2.	Random animal selection
	3.	Challenge JSON construction
	4.	HTML rendering
	5.	Output artefact generation

Running the root orchestrator:

python game.py

executes all group members’ pipelines sequentially and generates:
	•	A combined playable HTML interface
	•	A merged Markdown artifact (all_challenges.md)

⸻

7. Local Execution Guide

7.1 Repository Setup

```
git clone https://github.com/Udayan-P/Zoopocalypse.git
cd Zoopocalypse
```
7.2 Environment Preparation

```
python3 -m venv venv
source venv/bin/activate
```
7.3 Install Dependencies

Challenge 1 requires:

```
pip install pandas
```
7.4 Run Challenge 1 Pipeline
```
cd Sans
python3 animal_challenge_pipeline.py
```
Outputs:
	•	generated_challenge.json
	•	animal_challenge.html

7.5 Run Group-Wide Launcher
```
cd ..
python3 game.py
```
This verifies end-to-end integration with all team components.

⸻

8. NCC Execution (SLURM Batch Job)

Although only Challenge 3 is formally required to run on NCC, Challenge 1 is fully compatible with HPC execution.

8.1 Upload to NCC

```
scp -r Zoopocalypse/ fctm02@ncc1.clients.dur.ac.uk:/home/fctm02/
```
8.2 Login
```
ssh fctm02@ncc1.clients.dur.ac.uk
```
8.3 Create Environment
```
cd Zoopocalypse
python3 -m venv venv
source venv/bin/activate
pip install pandas
```

⸻

8.4 SLURM Batch Script Example

sans_run.slurm :
```
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
```
Submit job:
```
sbatch Sans/sans_run.slurm 
```
must be in the right directory!! 

Inspect outputs:
```
ls | grep sans_gen
sans_gen_error.txt
sans_gen_output.txt

cat sans_gen_output.txt
cat sans_gen_error.txt
```

Expected behaviour:
```
Running Challenge 1 generator on NCC...
Saved challenge JSON to generated_challenge.json
Wrote HTML challenge to animal_challenge.html
Job complete.
```
•	Dataset parsed successfully
•	JSON generated correctly
•	HTML produced without warnings or errors

<img width="874" height="176" alt="Screenshot 2025-12-04 at 1 16 45 PM" src="https://github.com/user-attachments/assets/750880bd-c1e5-451d-885c-3e2e89d6469e" />


<img width="1353" height="163" alt="Screenshot 2025-12-04 at 1 26 41 PM" src="https://github.com/user-attachments/assets/98f57edf-e743-49a9-901e-73e73194330c" />

<img width="878" height="271" alt="Screenshot 2025-12-04 at 1 29 01 PM" src="https://github.com/user-attachments/assets/5b629b9e-1eb6-43d9-a8f1-0d83a104e667" />


⸻

9. Feature Summary
	•	Dynamic blur-reduction mechanic
	•	Structured hint-reveal system
	•	Dataset-conditioned difficulty
	•	Automated HTML generation
	•	Deterministic reproducibility
	•	Fully modular software design

⸻

10. Status and Compliance

Challenge 1 has been:
	•	Fully implemented and validated
	•	Tested in isolation and via the group orchestration script
	•	Confirmed to meet all JSON formatting and gameplay requirements
	•	Verified to run without modification on both local and HPC environments

This implementation adheres to the Advanced Programming assessment specification, with clear structure, documented pipeline logic, and reproducible outputs suitable for academic evaluation.



