import argparse
import subprocess

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--train_file", required=True)
    parser.add_argument("--test_file", required=True)
    parser.add_argument("--output_dir", default="output_model")

    args = parser.parse_args()

    subprocess.run([
        "python", "../../lib/run_clm.py",
        "--model_name_or_path", "gpt2",
        "--train_file", args.train_file,
        "--do_train",
        "--validation_file", args.test_file,
        "--do_eval",
        "--save_steps", "-1",
        "--per_device_train_batch_size", "1",
        "--block_size", "256",
        "--num_train_epochs", "2",
        "--output_dir", args.output_dir
    ], check=True)

if __name__ == "__main__":
    main()
