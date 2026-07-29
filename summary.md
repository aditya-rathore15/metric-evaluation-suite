# CT Report Generation Metric Evaluation Summary

## Key Takeaways from Related Work
Before conducting the evaluation, I reviewed the provided research papers related to chest CT report generation and report evaluation, including work on CT-RATE, CT-CHAT, CT-CLIP, CT2Rep, Merlin, RadGraph, GREEN, FineRadScore, CRIMSON, and RadFact.

The papers highlighted that high textual similarity does not necessarily imply clinical correctness. Traditional text generation metrics such as BLEU and ROUGE primarily measure lexical overlap, while embedding-based metrics such as BERTScore measure semantic similarity. However, radiology reports are clinically meaningful documents in which the presence, absence, severity, and location of findings are often more important than surface-level wording.

Recent evaluation approaches therefore focus on clinical entities, relations, factual consistency, and finding-level correctness. Across the papers reviewed, common failure modes include omission of important findings, hallucination of unsupported findings, incorrect negation, and contradictions between generated and reference reports.

These observations motivated the evaluation approach used in this analysis. In addition to computing automatic similarity metrics, I manually reviewed report pairs to identify clinically significant discrepancies that may not be adequately reflected by BLEU, ROUGE-L, or BERTScore scores.

## Metrics Run

- BLEU
- ROUGE-L F1
- BERTScore F1
- RadGraph
- Report statistics: reference length, candidate length, length ratio, empty-output flag, and repeated-sentence flag

All 100 report pairs were evaluated successfully. No empty outputs were observed, and 1 report (ctchat_valid_0079) contained repeated sentence content.

## Aggregate Results

| Metric | Mean | Min | Max |
|---|---:|---:|---:|
| BLEU | 0.155 | 0.023 | 0.649 |
| ROUGE-L | 0.312 | 0.142 | 0.745 |
| BERTScore F1 | 0.870 | 0.830 | 0.954 |
| RadGraph Simple | 0.192 | 0.052 | 0.690 |
| RadGraph Partial | 0.170 | 0.046 | 0.621 |
| RadGraph Complete | 0.117 | 0.013 | 0.590 |
| Length ratio (cand/ref) | 1.14 | 0.37 | 11.33 |

The aggregate values above are computed as means over the 100 per-report scores, not as corpus-level BLEU or corpus-level ROUGE.

Although the mean candidate/reference length ratio was 1.14, the median ratio was 0.85, indicating that most generated reports were shorter than their reference reports.  

## Examples Where Metric Scores Are Misleading

During manual review, the clinically significant errors fell into the following categories:

| Error Type | Example |
|------------|----------|
| Unsupported or Hallucinated findings | Example 1, 6 |
| Laterality errors | Example 1 |
| Major finding omission | Example 2, 3 |
| Direct contradiction | Example 4 |
| Diagnostic reversal | Example 5 |

These categories were selected because they can substantially alter clinical interpretation while having limited impact on traditional text-similarity metrics.

### Example 1: Hallucinated Finding and Laterality Change (ctchat_valid_0001)

**Metrics**
- BLEU: 0.6494
- ROUGE-L: 0.7299
- BERTScore: 0.9539
- RadGraph Complete: 0.5905

**Reference Report**
- A few millimetric nonspecific nodules and mild recessions observed in the upper and lower lobe of the **right lung** only.
- Aeration of both lung parenchyma is normal; no infiltrative lesion detected.
- Impression: nodules and slight recessions in the right lung.

**Candidate Report**
- Reports bronchial wall thickening, more prominent centrally in **both lungs**.
- Adds minimal mosaic density differences in the lower lobes.
- Changes nodules from right-only to **bilateral**.
- Impression: bronchial wall thickening in both lungs, mosaic density differences (airway disease?), bilateral nodules.

**Interpretation**  
The generated report introduces findings not present in the reference, including bronchial wall thickening and mosaic density changes. It also changes the laterality of the nodules from unilateral to bilateral. This is both a hallucination and a laterality error. The text-similarity metrics remain high because the surrounding normal-report boilerplate is nearly identical between the two reports. RadGraph Complete is lower than the text-similarity metrics, suggesting weaker finding-level agreement, but it remains moderate because many shared normal findings and report structures are still present.

---

### Example 2: Missed Multi-Finding Report (ctchat_valid_0015)

**Metrics**
- BLEU: 0.0274
- ROUGE-L: 0.1928
- BERTScore: 0.8463
- RadGraph Complete: 0.0335

**Reference Report**
- Four measured pulmonary nodules (5mm, 6x4mm, 5x2mm, 8x5mm) across both lungs.
- Ground-glass density increases and mosaic attenuation pattern, more prominent basally.
- Fatty liver, gallbladder calculus, possible cystic duct density.
- Impression: findings dubious for Covid-19 pneumonia; clinical/laboratory correlation recommended.

**Candidate Report**
- Reports only emphysematous changes and bilateral atelectasis.
- Mentions generic "millimetric nodules" with no measurements or locations.
- No mention of ground-glass pattern, liver findings, or gallbladder finding.
- Impression: emphysematous changes, atelectasis, nodules, atherosclerotic changes, hiatal hernia.

**Interpretation**  
The generated report omits nearly all of the clinically specific content in the reference: the measured nodules, the ground-glass/mosaic pattern, the suspected Covid-19 pneumonia, and the incidental liver and gallbladder findings. BLEU and ROUGE-L correctly reflect this as a low-similarity pair. BERTScore remains relatively high because both reports still use similar radiology language and mention some generic thoracic findings. RadGraph Complete is very low, which better reflects the poor finding-level agreement between the generated and reference reports.

---

### Example 3: Erased Follow-Up Finding (ctchat_valid_0038)

**Metrics**
- BLEU: 0.2720
- ROUGE-L: 0.5455
- BERTScore: 0.9141
- RadGraph Complete: 0.3188

**Reference Report**
- An 8.5x6.2mm finding in the right lung middle lobe, irregular contours, patchy density.
- Flagged as nodule versus early infectious process; clinical/laboratory correlation recommended.
- Impression: faint nodule/early infectious process, follow-up recommended after excluding infection.

**Candidate Report**
- States lung parenchyma aeration is normal with no nodular or infiltrative lesion.
- Impression: thoracic CT examination within normal limits.

**Interpretation**  
The reference describes a right middle-lobe finding that requires clinical/laboratory correlation and follow-up after excluding an infection. The generated report omits this finding and reports the study as normal. This is clinically significant, since a finding requiring monitoring is fully erased. ROUGE-L and BERTScore still suggest moderate-to-high agreement because the reports share normal-report language and structure. RadGraph Complete is lower, showing that the structured clinical overlap is weaker than the surface-level similarity suggests.  

---

### Example 4: Contradiction of Pleural Effusion (ctchat_valid_0068)

**Metrics**
- BLEU: 0.6022
- ROUGE-L: 0.7454
- BERTScore: 0.9431
- RadGraph Complete: 0.4138

**Reference Report**
- Several millimetric nonspecific pulmonary nodules are present.
- A 25 mm appearance is interpreted as a left loculated pleural effusion.
- Impression: findings favor a loculated pleural effusion on the left.

**Candidate Report**
- Reports minimal emphysematous changes.
- States that no pleural effusion is present.
- Impression: minimal emphysematous changes in both lungs.

**Interpretation**  
The generated report contradicts the key finding in the reference report. The reference explicitly identifies a left loculated pleural effusion, whereas the generated report states that no pleural effusion is present. This is a direct contradiction rather than a simple omission. BLEU, ROUGE-L, and BERTScore remain high because much of the surrounding report content is similar. RadGraph Complete is lower than the text-similarity metrics, but it remains moderate because other normal structures and report entities overlap even though the central pleural-effusion finding is wrong.

---

### Example 5: Diagnostic Reversal (ctchat_valid_0080)

**Metrics**
- BLEU: 0.0233
- ROUGE-L: 0.2418
- BERTScore: 0.8604
- RadGraph Complete: 0.0492

**Reference Report**
- Ground-glass density increases in round-oval configuration, diffuse peripheral distribution, both lungs.
- Multiple measured nodules (8mm, two 3mm, 6x3mm) across both lungs.
- Impression: findings compatible with Covid-19 pneumonia in the first place; other viral pneumonias in differential diagnosis.

**Candidate Report**
- States no suspicious nodule, mass, or infiltration detected in either lung.
- Impression: no signs of infection detected in the lungs.

**Interpretation**  
The generated report reverses the diagnostic impression of the reference. Where the reference describes findings consistent with Covid-19 pneumonia and lists multiple measured nodules, the candidate reports a normal study with no signs of infection. BLEU and ROUGE-L correctly score this pair very low. BERTScore remains high enough to suggest meaningful similarity because both reports use similar radiology phrasing. RadGraph Complete is also very low, which aligns with the manual review and better reflects the diagnostic reversal.

---

### Example 6: Unsupported Findings (ctchat_valid_0044)  

**Metrics**
- BLEU: 0.0722
- ROUGE-L: 0.2756
- BERTScore: 0.8637
- RadGraph Complete: 0.0563

**Reference Report**
- No pathological lymph nodes are observed.
- No pneumonic infiltration, consolidation, suspicious mass, or nodular lesion is detected.
- Impression: examination within normal limits.

**Candidate Report**
- Reports emphysematous changes in both lungs.
- Reports atelectasis in the right middle lobe and left upper lobe lingular segment.
- Reports millimetric nodules in both lungs.
- Adds atherosclerotic changes and hiatal hernia.
- Impression: emphysematous changes, atelectasis, nodules, atherosclerotic changes, and hiatal hernia.

**Interpretation**  
This example shows false-positive overgeneration. The reference report is essentially normal, but the generated report adds multiple abnormalities, including emphysematous changes, atelectasis, nodules, atherosclerotic changes, and hiatal hernia. BLEU and ROUGE-L are low, reflecting poor lexical overlap, but BERTScore remains relatively high because the reports share radiology style and normal-structure wording. RadGraph Complete is very low, which better reflects that the candidate introduces unsupported clinical findings.

## Interpretation: Why Report-Level Metrics Miss Finding-Level Errors

BLEU and ROUGE-L mainly check if the same words and phrases appear in both reports. In this dataset, many reports share boilerplate descriptions of normal structures such as the trachea, mediastinum, heart, aorta, esophagus, lymph nodes, liver, adrenals, and bones. Since this part takes up most of the report, two reports can match closely on all these normal sections while completely disagreeing on the one line that actually matters. This is why Examples 1 and 4 still get high BLEU and ROUGE-L scores even though one report invents a new finding and the other contradicts the reference.

BERTScore captures broader semantic similarity, but it can still remain high when reports use similar radiology language and structure. In Examples 3 and 5, BERTScore stayed above 0.85 even though one report dropped a finding that needed follow-up and the other reversed the diagnosis completely. This shows that even high BERTScore values can occur when clinically important findings are omitted or contradicted. Therefore, semantic similarity alone does not guarantee clinical correctness.

RadGraph provides a more clinically oriented signal because it compares extracted findings and their relations rather than only comparing surface wording. This helped in examples with severe omissions, hallucinated findings, or diagnostic reversal, where RadGraph Complete was much lower than BERTScore. However, RadGraph is still not a complete substitute for manual review. In examples where the candidate and reference share many normal structures, RadGraph can remain moderate even when an important finding is wrong or contradicted.

Overall, this evaluation shows that report-level text similarity is useful for broad comparison, but it is not sufficient for evaluating clinical correctness. A more reliable evaluation should combine text-similarity metrics, clinically structured metrics such as RadGraph, and manual review.  

## Additional Radiology-Specific Metrics  

RadGraph was included as a radiology-specific metric to compare clinical entities and relations between the generated and reference reports. It produced simple, partial, and complete F1-style scores for each report pair.

GREEN, RadFact, CRIMSON, and FineRadScore were not run in this submission because the focus was on core automatic metrics and RadGraph. From reviewing these methods, I learned that they are useful next steps for deeper clinical factuality evaluation, but they require additional model/API setup and careful validation before use.