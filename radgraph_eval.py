import json
import pandas as pd
from radgraph import F1RadGraph

INPUT_FILE = "data/sample_pairs.jsonl"
OUTPUT_FILE = "outputs/radgraph_scores.csv"


def load_samples(path):
    with open(path, "r") as f:
        return [json.loads(line) for line in f]


def main():
    print("Loading samples...")
    samples = load_samples(INPUT_FILE)

    refs = [
        sample["reference_report"].strip()
        for sample in samples
    ]

    hyps = [
        sample["candidate_report"].strip()
        for sample in samples
    ]

    print("Loading RadGraph model...")

    radgraph = F1RadGraph(
        reward_level="all",
        model_type="radgraph-xl"
    )

    print(f"Scoring {len(samples)} report pairs...")

    result = radgraph(
        refs=refs,
        hyps=hyps
    )

    # Returned structure:
    # (
    #   mean_reward,
    #   reward_list,
    #   hypothesis_annotations,
    #   reference_annotations
    # )

    mean_reward = result[0]
    reward_list = result[1]

    simple_scores = reward_list[0]
    partial_scores = reward_list[1]
    complete_scores = reward_list[2]

    rows = []

    for i, sample in enumerate(samples):
        rows.append({
            "sample_id": sample["sample_id"],
            "image": sample["image"],
            "radgraph_simple": round(float(simple_scores[i]), 4),
            "radgraph_partial": round(float(partial_scores[i]), 4),
            "radgraph_complete": round(float(complete_scores[i]), 4),
        })

    df = pd.DataFrame(rows)

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(f"\nSaved: {OUTPUT_FILE}")

    print("\nAggregate Statistics")
    print("-" * 40)

    print(
        f"Mean RadGraph Simple   : "
        f"{df['radgraph_simple'].mean():.4f}"
    )

    print(
        f"Mean RadGraph Partial  : "
        f"{df['radgraph_partial'].mean():.4f}"
    )

    print(
        f"Mean RadGraph Complete : "
        f"{df['radgraph_complete'].mean():.4f}"
    )

    print("\nBatch Means Reported By RadGraph")
    print("-" * 40)
    print(mean_reward)


if __name__ == "__main__":
    main()