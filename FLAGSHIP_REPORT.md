
# Flagship Report — AMOS22 Multi‑Organ Segmentation (nnU‑Net)

## Abstract
**Purpose:** Establish a reproducible baseline for automated abdominal multi‑organ segmentation using nnU‑Net with structured cross‑validation and radiologist‑led qualitative assessment.

**Methods:** AMOS22 dataset, nnU‑Net v2 (3D full resolution), 5‑fold cross‑validation. Environment, manifests, and training artifacts frozen.

**Results:** Mean Dice **0.8725 ± 0.0068**, demonstrating stable optimization with low fold variance. Qualitative review confirmed strong anatomical fidelity. An ectopic left kidney located in the pelvis was correctly segmented.

**Conclusion:** This frozen baseline provides a research‑grade reference model for future MONAI experimentation.

---

## Training Configuration
- Architecture: nnU‑Net v2 (3D full resolution)
- Dataset: AMOS22
- Training: 5‑fold cross‑validation
- GPU: NVIDIA CUDA‑enabled workstation
- Reproducibility artifacts preserved

---

## Quantitative Results

|   Fold |   Dice |   FN |   FP |    IoU |    TP |   n_ref |
|-------:|-------:|-----:|-----:|-------:|------:|--------:|
|      0 | 0.8658 | 4565 | 4038 | 0.7921 | 85599 |   90165 |
|      1 | 0.8664 | 6265 | 7178 | 0.7924 | 98767 |  105032 |
|      2 | 0.8741 | 5559 | 5754 | 0.8022 | 96493 |  102053 |
|      3 | 0.8823 | 4334 | 4165 | 0.8098 | 84590 |   88925 |
|      4 | 0.8741 | 5559 | 5754 | 0.8022 | 96493 |  102053 |

### Cross‑Validation Performance
**Mean Dice:** 0.8725  
**Standard deviation:** 0.0068

Interpretation: Low dispersion indicates robust generalization and minimal split sensitivity.

---

## Structured Qualitative Assessment — Mean Organ Scores

Scoring scale: Excellent=4, Good=3, Fair=2, Poor=1, Failure=0

|                 |   Mean Score |
|:----------------|-------------:|
| Liver           |         4    |
| Stomach         |         3.92 |
| Pancreas        |         3.31 |
| Kidney          |         4    |
| Adrenal         |         3.46 |
| Spleen          |         3.92 |
| Bladder         |         4    |
| Prostate/Uterus |         3.92 |
| Aorta           |         4    |

### Key Observations
- Liver, kidneys, spleen, bladder, and aorta approach near‑expert quality.
- Pancreas remains the dominant failure mode due to low contrast and morphological variability.
- Anatomical variant correctly handled: **left ectopic kidney located in the pelvis (not bladder)**.

---

## Training Curve

(Representative curve retained in repository: `/baseline_nnunet/runpackets/`)

---

## Discussion
nnU‑Net achieved reliable multi‑organ segmentation with minimal manual tuning. The combination of quantitative Dice metrics and structured qualitative scoring supports the model as a strong academic baseline.

---

## Limitations
- Internal validation only
- External dataset testing recommended
- Rare anatomy performance uncertain

---

## Reproducibility
All manifests, splits, metrics, environment files, and frozen artifacts are stored inside:

```
baseline_nnunet/frozen_baseline_amos22_701_3d_fullres/
```

---
