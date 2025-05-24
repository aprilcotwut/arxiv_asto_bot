import os
import argparse
import logging

from transformers import AutoTokenizer, TFGPT2LMHeadModel
from arxiv_astro_bot.utils.s3 import resolve_s3_path, download_model_from_s3

s3 = boto3.client("s3")

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
logging.disable(logging.WARNING)

def main(input_phrase, model_dir):
    # load gpt-2 tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained("gpt2", from_pt=True, bos_token = "<|title|>", eos_token = "<|endoftext|>")
    model = TFGPT2LMHeadModel.from_pretrained(model_dir)

    # tokenize inputs
    input_encode = tokenizer.encode(input_phrase, return_tensors="tf")

    decoded = []
    i = 0
    while (len(decoded) < 200 and i < 10):
        output = model.generate(
            input_encode,
            max_length=500,
            min_length=200,
            # so this one is a bit awkward, because in song you want some repitition
            # but if you set it too high you might just get repitition
            no_repeat_ngram_size=10,
            repitition_penalty=75,
            # top_p and top_k can be used together instead of temprature
            # top_p=0.93,
            # top_k=75,
            do_sample=True,
            # temperature is entropy based so ^ temp ^ ...creativity
            temperature=0.95,
            early_stopping=True
        )

        decoded = '.'.join((tokenizer.decode(output[0], skip_special_tokens=True) + ' ').split('.'))
        i += 1

    print("\n\n\nOutput:\n")
    print(f"{decoded.replace('<|title|>', '').replace('<|endoftext|>', '')}\n")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    # I actually get great results leaving the input phrase empty
    p.add_argument("--input_phrase", help="The input phrase to initialize the model", default=" ", type=str)
    p.add_argument("--model_dir", help="The directory containing the trained model", default="calle13_bot_gpt2", type=str)

    args = p.parse_args()

    main(args.input_phrase, args.model_dir)
