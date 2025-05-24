import os
import argparse
import logging

from transformers import AutoTokenizer, TFGPT2LMHeadModel
from arxiv_astro_bot.utils.s3 import resolve_s3_path, download_model_from_s3

s3 = boto3.client("s3")

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
logging.disable(logging.WARNING)


def main(input_phrase, bucket, version):
    s3_key = resolve_s3_path(version)
    model_path = download_model_from_s3(bucket, s3_key)

    # load gpt-2 tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained("gpt2", from_pt=True)
    model = TFGPT2LMHeadModel.from_pretrained(model_path)

    # tokenize inputs
    input_encode = tokenizer.encode(input_phrase, return_tensors="tf")

    output = model.generate(
        input_encode,
        max_length=70,
        min_length=30,
        num_return_sequences=3,
        no_repeat_ngram_size=1,
        repitition_penalty=75,
        # top_p=0.90,
        # top_k=50,
        do_sample=True,
        temperature=0.95,
        early_stopping=False
    )

    print("\n\n\nOutput:\n")
    for i, sequence in enumerate(output):
        print(f"{i}: {'.'.join((tokenizer.decode(sequence, skip_special_tokens=True) + ' ').split('.')[:-1])}.\n")
        print(f"{len('.'.join((tokenizer.decode(sequence, skip_special_tokens=True) + ' ').split('.')[:-1]))}")


    output = model.generate(
        input_encode,
        max_length=70,
        min_length=50,
        no_repeat_ngram_size=2,
        repitition_penalty=75,
        top_p=0.80,
        top_k=0,
        do_sample=True,
        temperature=.95,
        early_stopping=True
    )

    print("\n\n\nOutput:\n")
    print(f"{i}: {'.'.join((tokenizer.decode(output[0], skip_special_tokens=True) + ' ').split('.')[:-1])}.\n")
    print(f"{len('.'.join((tokenizer.decode(sequence, skip_special_tokens=True) + ' ').split('.')[:-1]))}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("input_phrase", help="The input phrase to initialize the model", type=str)
    p.add_argument("--bucket", help="The S3 bucket name", required=True)
    p.add_argument("--model_subpath", help="The S3 key prefix for the model (e.g. lyricsbots/bot_xx/date_xx)", required=True)

    args = p.parse_args()

    main(args.input_phrase, args.bucket, args.version)
