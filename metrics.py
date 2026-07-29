import torch
from nltk.translate.bleu_score import sentence_bleu
from nltk.translate.bleu_score import SmoothingFunction
from rouge_score import rouge_scorer
from bert_score import score as bert_score

device = "mps" if torch.backends.mps.is_available() else "cpu"

_smooth = SmoothingFunction().method1


def compute_bleu(reference: str, candidate: str) -> float:
    return sentence_bleu(
        [reference.split()],
        candidate.split(),
        smoothing_function=_smooth,
    )


# ROUGE-L SCORE
_rouge = rouge_scorer.RougeScorer(
    ["rougeL"],
    use_stemmer=True
)

def compute_rouge_l(reference: str, candidate: str) -> float:
    score = _rouge.score(reference, candidate)
    return score["rougeL"].fmeasure


# BERT SCORE
def compute_bert_scores(
    references: list[str],
    candidates: list[str]
):
    _, _, f1 = bert_score(
        candidates,
        references,
        lang="en",
        device=device,
        verbose=True
    )

    return [float(x) for x in f1]