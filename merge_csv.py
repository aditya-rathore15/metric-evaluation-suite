import pandas as pd

metric_df = pd.read_csv("outputs/metric_table.csv")
radgraph_df = pd.read_csv("outputs/radgraph_scores.csv")

merged = metric_df.merge(
    radgraph_df,
    on=["sample_id", "image"],
    how="left"
)

print(merged.shape)
print(merged[["radgraph_simple", "radgraph_partial", "radgraph_complete"]].isna().sum())

merged.to_csv("outputs/metric_table.csv", index=False)