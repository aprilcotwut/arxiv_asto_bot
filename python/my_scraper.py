#!/usr/bin/env python
# encoding: utf-8

import arxiv
import rpy2
import rpy2.robjects as robjects
import pandas as pd
r = robjects.r
r['source']('../R/scrape.R')

def get_query_data(queries, num_results):
    if not isinstance(queries, list):
        queries = [queries]
    for query in queries:
        files = arxiv.query(query=query,
                            max_results=num_results,
                            sort_by="submittedDate",
                            sort_order="descending",
                            prune=True,
                            iterative=False,
                            max_chunk_results=1000
        )
    keep_cols = ['affiliation', 'arxiv_url', 'author', 'guidislink', 'id','pdf_url', 'published', 'title', 'updated']
    return pd.DataFrame(files)[keep_cols]

def get_content(pdf_urls):
    content = r.scrape_pdf_urls(pdf_urls)
    return content
