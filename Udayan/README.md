# Udayan Challenge  
## Hangman Style Animal Guessing Game  
### Advanced Programming Individual Component  

**Author** Udayan Purandare  
**Course** MSc Advanced Computer Science at Durham University  
**Module** Advanced Programming  

-----------------------------------------------------------------------------------------------------------------------------------

## Introduction

This document presents my full individual contribution to the group project for the Advanced Programming module.  
My component is a complete Hangman style animal guessing experience.

The work includes a formal JSON challenge description, a dataset driven generator, rendering pipelines for both Markdown and HTML, a fully automated execution sequence, and optional HPC integration through NCC SLURM.

The goal is to construct a reproducible workflow that creates Hangman style challenges from zoological data. The challenge begins with a completely hidden animal name and progressively reveals characters and structured hints derived from metadata.  
Outputs include JSON, Markdown, and HTML demonstration files.

-----------------------------------------------------------------------------------------------------------------------------------

## Challenge Objective

The Hangman challenge enables a player to identify an animal selected from a zoological dataset.  
The system reveals progressive hints and partial character visibility until the player identifies the correct species.

The challenge incorporates

**A complete JSON representation**  
**A Markdown file rendered from JSON**  
**An HTML representation of the Markdown version**  
**Automated hint generation using structured features**  
**A repeatable workflow allowing full regeneration on demand**

-----------------------------------------------------------------------------------------------------------------------------------

## Folder Structure Overview

    Udayan
        assets
            monkey.png
            zombie.png

        datasets
            __pycache__
                dataset_loader.cpython-313.pyc
                dataset_loader.cpython-314.pyc
            dataset_loader.py
            Zoo_Animals_Dataset.csv

        docs
            hangman_json_spec.md

        generators
            __pycache__
                hangman_generator.cpython-314.pyc
            hangman_generator.py

        json_examples
            generated_hangman.json
            hangman_example.json

        misc
            challenges
                hangman.py
            prototypes
                hangman_renderer.py
                hangman.py

        output
            hangman_example.html
            hangman_example.md
            hangman_generated.html
            hangman_generated.md

        renderers
            __pycache__
            hangman_json_renderer.py
            hangman_markdown_to_html.py

        run_hangman_pipeline.py
        run_udayan.slurm


This structure ensures clear separation of functions

**Datasets** contain zoological information and loading utilities  
**Generators** construct JSON challenge instances  
**Renderers** translate JSON into Markdown and HTML  
**Output** stores produced artefacts  
**Misc** retains prototypes and tests  
**SLURM file** demonstrates HPC integration  

-----------------------------------------------------------------------------------------------------------------------------------

## JSON Specification Summary

The JSON specification located in the docs folder defines the format of a Hangman challenge.  
Fields include the challenge identifier, target species, obscured representation, hint list, and further metadata needed by the rendering tools.  

-----------------------------------------------------------------------------------------------------------------------------------

## Pipeline Description

The Python script run_hangman_pipeline.py executes the full workflow.  
Its behaviour includes

**Loading the zoological dataset**  
**Selecting one species**  
**Producing a complete JSON challenge**  
**Writing JSON into the json_examples directory**  
**Rendering Markdown output**  
**Converting Markdown into HTML**  
**Saving all outputs into the output directory**

This pipeline requires no manual steps and provides fully reproducible results.

-----------------------------------------------------------------------------------------------------------------------------------

## HPC Integration

The file run_udayan.slurm demonstrates how the full workflow can be executed on NCC systems.  
It configures job requirements, allocates compute resources, loads Python environments, and executes the pipeline script.

-----------------------------------------------------------------------------------------------------------------------------------

## How to Run

Execute the pipeline directly from the project root.
All JSON, Markdown, and HTML outputs will regenerate inside the output directory.

-----------------------------------------------------------------------------------------------------------------------------------

## Conclusion

This component provides a complete data driven Hangman style challenge.  
It includes structured JSON modelling, dataset processing, rendering tools, automated pipelines, and optional HPC execution.  

