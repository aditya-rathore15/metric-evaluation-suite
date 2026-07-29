import json
import pandas as pd

from metrics import (
    compute_bleu,
    compute_rouge_l,
    compute_bert_scores,
)

def load_samples(path: str):
    with open(path, "r") as f:
        return [json.loads(line) for line in f]

def repeated_sentence_flag(report: str) -> int:
    sentences = [
        s.strip().lower()
        for s in report.split(".")
        if s.strip()
    ]

    return int(
        len(sentences) != len(set(sentences))
    )

def evaluate_sample(sample: dict):
    reference = sample["reference_report"].strip()
    candidate = sample["candidate_report"].strip()

    reference_len = len(reference.split())
    candidate_len = len(candidate.split())

    return {
        "sample_id": sample["sample_id"],
        "image": sample["image"],
        "bleu": round(compute_bleu(reference, candidate), 4),
        "rouge_l": round(compute_rouge_l(reference, candidate), 4),
        "reference_len": reference_len,
        "candidate_len": candidate_len,
        "length_ratio": round(candidate_len / reference_len, 4),
        "empty_output": int(candidate_len == 0),
        "repeated_sentence_flag": repeated_sentence_flag(candidate),
    }


def main():
    samples = load_samples(
        "data/sample_pairs.jsonl"
    )

    results = [
        evaluate_sample(sample)
        for sample in samples
    ]

    df = pd.DataFrame(results)

    references = [
        sample["reference_report"].strip()
        for sample in samples
    ]

    candidates = [
        sample["candidate_report"].strip()
        for sample in samples
    ]

    df["bertscore_f1"] = [
        round(score, 4)
        for score in compute_bert_scores(
            references,
            candidates
        )
    ]

    df = df[
        [
            "sample_id",
            "image",
            "bleu",
            "rouge_l",
            "bertscore_f1",
            "reference_len",
            "candidate_len",
            "length_ratio",
            "empty_output",
            "repeated_sentence_flag",
        ]
    ]

    df.to_csv(
        "outputs/metric_table.csv",
        index=False
    )

    print(f"Processed {len(df)} samples")
    print(f"Mean BLEU: {df['bleu'].mean():.4f}")
    print(f"Mean ROUGE-L: {df['rouge_l'].mean():.4f}")
    print(f"Mean BERTScore: {df['bertscore_f1'].mean():.4f}")
    print("Saved outputs/metric_table.csv")


if __name__ == "__main__":
    main()