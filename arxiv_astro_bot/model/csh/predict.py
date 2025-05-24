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
    tokenizer = AutoTokenizer.from_pretrained("gpt2", from_pt=True, eos_token = "<|endoftext|>")
    model = TFGPT2LMHeadModel.from_pretrained(model_dir)

    # tokenize inputs
    input_encode = tokenizer.encode(input_phrase, return_tensors="tf")

    decoded = []
    i = 0
    while (len(decoded) < 200 and i < 10):

        if model_dir == "csh_bot_gpt2":
            output = model.generate(
                input_encode,
                max_length=500,
                min_length=150,
                no_repeat_ngram_size=4,
                repitition_penalty=50,
                # top_p=0.90,
                # top_k=50,
                do_sample=True,
                temperature=0.95,
                early_stopping=True
            )
        else:
            output = model.generate(
                input_encode,
                max_length=400,
                min_length=150,
                no_repeat_ngram_size=4,
                repitition_penalty=50,
                top_p=0.85,
                top_k=50,
                do_sample=True,
                temperature=0.95,
                early_stopping=True
            )

        decoded = '.'.join((tokenizer.decode(output[0], skip_special_tokens=True) + ' ').split('.'))
        i += 1


    print("\n\n\nOutput:\n")
    print(f"{decoded.replace('<|title|>', '').replace('<|endoftext|>', '')}\n")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("input_phrase", help="The input phrase to initialize the model", type=str)
    p.add_argument("--bucket", help="The S3 bucket name", required=True)
    p.add_argument("--model_subpath", help="The S3 key prefix for the model (e.g. lyricsbots/bot_xx/date_xx)", required=True)

    args = p.parse_args()

    main(args.input_phrase, args.bucket, args.version)
