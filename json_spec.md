# JSON Specification for "Guess the Animal From Pic" Challenge

## Description
This challenge presents the user with an image of an animal and asks them to guess which animal it is. The challenge includes multiple-choice options, hints, and metadata required to render the puzzle.Further possible modifications of this challenge include reducing photo resolution to increase difficulty 

## JSON Structure

Each challenge is represented by a JSON object with the following fields:

- **challenge_id** (string): Unique ID for the challenge.
- **image** (string): File path to the animal image.
- **question** (string): The question to present to the user.
- **options** (array of strings): List of multiple-choice answers.
- **answer** (string): Correct answer.
- **hints** (array of strings): Hints to be revealed gradually.

## Example JSON

```json
{
  "challenge_id": "animal_001",
  "image": "images/tiger_01.jpg",
  "question": "Which animal is shown in this picture?",
  "options": ["Tiger", "Lion", "Leopard", "Cheetah"],
  "answer": "Tiger",
  "hints": [
    "This animal has stripes.",
    "It is the largest species of cat.",
    "It is native to Asia."
  ]
}