import argparse
import os
import json
import pandas as pd
import arxiv
import re

from arxiv_astro_bot.lib import ARXIV_CONFIG_PATH, ARXIV_TRAIN_PROP
from arxiv_astro_bot.utils.corpus import clean_text, get_config

def main(query, max_results, config_path):

    # configurations via config.json
    config = get_config(config_path)

    query_file = config["corpus_queries_file"]
    train_file, test_file = config["corpus_train_file"], config["corpus_test_file"]

    # get the previous queries to only update corpus with new papers, or create an empty DF
    if all([os.path.exists(f) for f in [query_file, train_file, test_file]]):
        prev_queries = pd.read_csv(query_file)
    else:
        prev_queries = pd.DataFrame(columns = config["query_keys"])
        # create files
        for file in [train_file, test_file]:
            with open(file, "w") as f:
                pass

    search = arxiv.Search(
        query = query,
        max_results = max_results,
        sort_by = arxiv.SortCriterion.SubmittedDate
    )

    abstracts, query_dicts = [], []
    for result in search.results():
        # check that result not already in corpus
        if prev_queries.entry_id.str.contains(result.entry_id).any():
            continue
        query_dicts.append({ key: result.__dict__[key] for key in config["query_keys"]})
        abstracts.append(clean_text(result.summary))

    # write abstracts as new line in one of train/test split
    train_n = int(len(abstracts) * ARXIV_TRAIN_PROP)
    for i, abstract in enumerate(abstracts):
        corpus_file = train_file if i < train_n else test_file
        with open(corpus_file, "a") as f:
            f.write(abstract)

    new_queries = pd.DataFrame.from_dict(query_dicts)
    pd.concat([prev_queries, new_queries], ignore_index = True).to_csv(query_file)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--config", "-q", help="Path to the config for the arvix corpus files", default=ARXIV_CONFIG_PATH, type=str)
    p.add_argument("--query", "-q", help="Defines the keywork/subject to query from the Arxiv", default="cat:astro-ph", type=str)
    p.add_argument("--max_results", "-n", help="Sets the maximum results to query and add to the corpus", default=500, type=int)

    args = p.parse_args()

    main(args.query, args.max_results, args.config)
