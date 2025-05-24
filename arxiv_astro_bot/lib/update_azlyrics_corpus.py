import argparse
import logging
import os
import json
import pandas as pd
import random
from tqdm import tqdm

from azlyrics import azlyrics

from arxiv_astro_bot.lib import CSH_CONFIG_PATH, CSH_TRAIN_PROP
from arxiv_astro_bot.lib.utils import clean_text, get_config
import time

def main(config_path):
    # configurations via config.json
    config = get_config(config_path)

    song_file, query_file = config["song_name_file"], config["corpus_queries_file"]
    train_file, test_file = config["corpus_train_file"], config["corpus_test_file"]

    # get the previous queries to only update corpus with new papers, or create an empty DF
    queries = []
    if not os.path.exists(query_file):
        logging.warning("No query file -- assuming corpus contains none of the provided songs")
    else:
        with open(query_file, "r") as f:
            queries = f.read().splitlines()

    for file in [train_file, test_file]:
        if not os.path.exists(file):
            with open(file, "w") as f:
                pass

    if not os.path.exists(song_file):
        logging.warning(f"No song file at location, will not update corpus: {song_file}")
        return

    songs = []
    with open(song_file, "r") as f:
        songs = f.read().splitlines()
    songs = [s for s in songs if s not in queries]

    train_n = int(len(songs) * CSH_TRAIN_PROP)
    train_songs = random.sample(songs, train_n)

    pbar = tqdm(train_songs)
    for song in pbar:
        pbar.set_description(f"Adding: {song}")
        try:
            lyrics = azlyrics.lyrics(config["artist"], song)[0]
            # lyrics = "".join(char for char in lyrics if ord(char)<128) # make sure text all standard ascii
            lyrics = "<|title|>" + lyrics + "<|endoftext|>"
            with open(train_file, "a") as f:
                f.write(lyrics)
            with open(query_file, "a") as f:
                f.write(song + "\n")
        except Exception:
            logging.warning(f"Could not download: {song}")
        time.sleep(10)

    if train_n == len(songs):
        return

    test_songs = [s for s in songs if s not in train_songs]

    pbar = tqdm(test_songs)
    for song in pbar:
        pbar.set_description(f"Adding: {song}")
        try:
            lyrics = azlyrics.lyrics(config["artist"], song)[0]
            # lyrics = "".join(char for char in lyrics if ord(char)<128) # make sure text all standard ascii
            lyrics = "<|title|>" + lyrics + "<|endoftext|>"
            with open(test_file, "a") as f:
                f.write(lyrics)
            with open(query_file, "a") as f:
                f.write(song + "\n")
        except Exception:
            logging.warning(f"Could not download: {song}")
        time.sleep(10)

    if train_n == len(songs):
        return




if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--config", "-q", help="Path to the config for the azlyrics corpus files", default=CSH_CONFIG_PATH, type=str)

    args = p.parse_args()

    main(args.config)
