import re
import os
import json


def clean_text(text):
    text = "".join(char for char in text if ord(char)<128) # make sure text all standard ascii
    text = re.sub(r"(\${1,2})(?:(?!\1)[\s\S])*\1", "", text) # get rid of latex math eqs
    text = re.sub(" +", " ", text) # remove extra spaces
    text = text.replace("\n", " ") # don't split lines
    return "<|title|>" + text.strip() + "<|endoftext|>" # idk a GPT2 thing supposedly

def load_corpus(config = None):
    if config is None:
        config = get_config()

    train_sentences, test_sentences = [], []
    with open(config["corpus_train_file"]) as file:
        train_sentences = file.read.splitlines()

    with open(config["corpus_test_file"]) as file:
        test_sentences = file.read.splitlines()

    return train_sentences, test_sentences

def get_config(config_path):
    cwd = os.path.dirname(__file__)

    with open(os.path.join(cwd, config_path)) as f:
        config = json.load(f)

    config.update({"corpus_train_file": os.path.join(cwd, "../", config["corpus_train_file"])})
    config.update({"corpus_test_file": os.path.join(cwd, "../", config["corpus_test_file"])})
    if config.get("corpus_queries_file"):
        config.update({"corpus_queries_file": os.path.join(cwd, "../", config["corpus_queries_file"])})
    if config.get("song_file_name"):
        config.update({"song_file_name": os.path.join(cwd, "../", config["song_file_name"])})
    return config

# python run_clm.py \
# --model_type gpt2 \
# --model_name_or_path gpt2 \
# --train_file "C:\MyRepos\arxiv_asto_bot\data\train_corpus.txt" \
# --do_train \
# --validation_file "C:\MyRepos\arxiv_asto_bot\data\test_corpus.txt" \
# --do_eval \
# --save_steps -1 \
# --num_train_epochs 2 \
# --output_dir="output"
