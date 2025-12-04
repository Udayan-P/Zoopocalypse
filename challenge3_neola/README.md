## **Zoopocalypse – Challenge 3 Implementation**

This repository contains my implementation for **Challenge 3 (Feature Challenge)** for the *Advanced Programming* module. The challenge generates an animal-identification puzzle using a structured JSON specification, auto-renders Markdown and HTML pages.


# 1. Project File Overview

### **1.1 Core Challenge 3 Scripts**

#### **feature_challenge_generator.py**

Generates a **random Feature Challenge JSON** from *animals.json*.
Responsible for:

* Selecting an animal from the dataset
* Building 6 categories of attributes
* Selecting **5 initial hints** 
* Generating an **AI Hint** using the **Google Gemini Model**
* Saving the final JSON as `feature_challenge.json`
* Producing the attribute distribution plot (Matplotlib + Seaborn)

This script is what gets executed on NCC via SLURM.

#### **feature_challenge_pipeline.py**

A full pipeline wrapper that:

1. Calls the generator
2. Produces plots
3. Creates all Markdown pages
4. Converts Markdown → HTML

Running this file locally reproduces the final challenge pages.

#### **feature_challenge_renderer.py**

Converts the JSON challenge into:

* Stage 0 → 3 hint pages
* Answer page
* Wrong-attempt pages

Creates structured Markdown under `/pages`.

#### **markdown_to_html.py**

Converts any Markdown page into the final styled HTML output used for assessment.
Includes the updated page formatting, custom CSS, and card-based layout.

### **1.2 Dataset + JSON Files**

#### **animals.json**

The cleaned dataset of 39 animals used to generate attributes, diet, physical traits, biological traits, and habitat/environmental flags.

#### **example_feature_challenge.json**

A **hand-coded example challenge JSON** used for demonstration and to meet the coursework requirement for manually structured JSON.

#### **feature_challenge.json**

The **generated** JSON created by the pipeline or SLURM execution.
This file includes:

* `initial_hints` (5 indices)
* `max_additional_hints`
* `ai_hint_seed`
* rarity score
* 31 attribute entries
* auto-generated plot references

This file proves the generator script and AI pipeline ran successfully.

### **1.3 Output Folders**

#### **example_pages/**

Hand-rendered Markdown + HTML pages from the hand-coded JSON.

#### **pages/**

Auto-generated pages created when running the pipeline or SLURM job.

#### **plots/**

Contains the Seaborn/Matplotlib generated plot:

* `attribute_count_distribution.png`
  Used to visualise the number of attributes per animal.

### **1.4 NCC / SLURM Files**

#### **run_slurm_test.sh**

Batch script used to run the generator on NCC.
Loads Python, executes the generator, and stores `.out` + `.err` logs.

#### **slurm_zoop_test.out**

Successful execution log:

* Correct Python version
* Dataset loaded
* Random animal generated
* AI hint produced
* JSON written
* Plot created

#### **slurm_zoop_test.err**

Warning logs (e.g., Google API version deprecation) — present to demonstrate authentic execution.

### **2.5 requirements.txt**

Contains all Python dependencies required for both local and NCC execution:

* google-generativeai
* matplotlib
* seaborn
* pillow
* markdown

The NCC environment successfully installed and executed these requirements.

# **2. How to Run Locally (Pipeline Execution)**

### **Step 1 — Install requirements**

```bash
pip install -r requirements.txt
```

### **Step 2 — Run the full Challenge 3 pipeline**

Inside the repository root:

```bash
cd challenge3_neola
python3 feature_challenge_pipeline.py
```

### **Expected local output**

* `feature_challenge.json` generated
* Plot created under `/plots`
* Markdown pages generated under `/pages`
* HTML pages created from Markdown

To open the challenge manually:

```
challenge3_neola/pages/stage_0/example_feature_challenge_hint0_a0.html
```

# **3. Running on NCC using SLURM (Coursework Requirement)**

### **Step 1 — Upload project to NCC**

Copy `Zoopocalypse/` to your NCC home directory.

### **Step 2 — Make the SLURM script executable**

```bash
chmod +x run_slurm_test.sh
```

### **Step 3 — Submit the batch job**

```bash
sbatch run_slurm_test.sh
```

### **Step 4 — Check the job logs**

```bash
cat slurm_zoop_test.out
cat slurm_zoop_test.err
```

### **Expected SLURM output (already included in repo)**

* Dataset successfully loaded
* Random animal selected (“Spectacled Bear”)
* Plot created via Matplotlib/Seaborn
* AI hint successfully generated using Gemini
* JSON written to `challenge3_neola/feature_challenge.json`
* Job completed without errors

These logs are included as proof that the system works on NCC as required.

# **5. AI Integration (Gemini API)**

The challenge uses the **Google Gemini Generative AI API** to produce a natural-language AI hint.

Inside the generator:

```python
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
```

A **temporary token** was used during NCC execution.
Even if external access is restricted for the marker, **the presence of the generated `ai_hint_seed` inside feature_challenge.json serves as proof that the AI call executed successfully on NCC**.

---

# **6. Plotting: Seaborn + Matplotlib**

The generator uses:

* **Matplotlib** for figure rendering
* **Seaborn** for stylistic plotting

Output file:

```
challenge3_neola/plots/attribute_count_distribution.png
```

# Preview of Challenge 3

<img width="766" height="1638" alt="image" src="https://github.com/user-attachments/assets/c7a43064-9b32-494c-b1bd-b63fdc3dc576" />



