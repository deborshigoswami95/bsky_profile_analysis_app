#!/bin/bash

echo "Installing packages from requirements.txt..."
pip install -r requirements.txt

echo "Downloading the spaCy model 'en_core_web_sm'..."
python -m spacy download en_core_web_sm
