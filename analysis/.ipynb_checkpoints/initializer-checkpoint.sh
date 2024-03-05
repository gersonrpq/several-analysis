#!/bin/bash

virtualenv_folder="./venv"

if [ -e "$file_path" ]; then
    echo "Found Virtualenv Folder"
    source venv/bin/activate
    pip install -r requirements.txt
else
    echo "Creating Virtualenv"
    pip3 install -r virtualenv
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt
fi

dataset_file='./las_vegas_airbnb_data.csv'

if [-e "$dataset_file"]; then
    echo "Dataset Found"
else
    kaggle datasets download kanchana1990/airbnb-las-vegas-listings --unzip
fi

echo "Installing Sentiment Models"
python -m textblob.download_corpora
python -m spacy download en_core_web_sm
python -m nltk.downloader punkt
