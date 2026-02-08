# MODEL CARD --- AMOS22 Multi‑Organ Segmentation (nnU‑Net v2)

## Model Overview

**Model name:** frozen_baseline_amos22_701_3d_fullres\
**Architecture:** nnU‑Net v2 (3D full‑resolution configuration)\
**Task:** Automated multi‑organ abdominal CT segmentation\
**Training strategy:** 5‑fold cross‑validation with automatic experiment
planning

This model represents a frozen baseline developed within a lab‑style,
reproducible pipeline intended for academic research and methodological
benchmarking rather than immediate clinical deployment.

------------------------------------------------------------------------

## Intended Use

### Primary Use

-   Academic research
-   Pipeline validation
-   Educational demonstration of reproducible medical imaging workflows
-   Baseline comparator for future MONAI‑based models

### Out‑of‑Scope Use

-   Direct clinical decision making\
-   Autonomous diagnosis\
-   Use without expert radiologic oversight

------------------------------------------------------------------------

## Dataset

**Dataset:** AMOS22 (Abdominal Multi‑Organ Segmentation Challenge 2022)

Characteristics:

-   Multi‑center abdominal CT
-   Expert manual annotations
-   Multiple abdominal organs
-   Public research dataset

Please cite the dataset appropriately when using this model.

------------------------------------------------------------------------

## Training Environment

  Component             Specification
  --------------------- -----------------------------------------
  Framework             nnU‑Net v2
  GPU                   NVIDIA RTX‑class GPU (user workstation)
  Training scheme       5‑fold cross‑validation
  Configuration         3D full resolution
  Experiment planning   Automatic (nnU‑Net)

Environment snapshots are stored inside:

    frozen_baseline_amos22_701_3d_fullres/env/

------------------------------------------------------------------------

## Quantitative Performance

### Cross‑Validation Dice Scores

  Fold   Mean Dice
  ------ -----------
  0      0.8658
  1      0.8664
  2      0.8741
  3      0.8823
  4      0.8741

**Overall Mean Dice:** **0.8726**\
**Standard Deviation:** **0.0060**

### Interpretation

-   Very low variance across folds suggests **stable optimization** and
    **robust training behavior**.
-   Dice ≈ 0.87 is consistent with a **strong baseline** for
    heterogeneous multi‑organ CT datasets.
-   Fold‑3 demonstrates the highest performance, but the small
    dispersion indicates no meaningful fold bias.

------------------------------------------------------------------------

## Qualitative Validation

Structured expert review was performed on representative validation
cases across multiple organs.

Key observations:

-   Accurate segmentation for liver, kidneys, spleen, and major
    abdominal structures.
-   Appropriate handling of anatomic variation, including **pelvic
    ectopic kidney** --- correctly identified as renal tissue rather
    than bladder.
-   Minor boundary smoothing observed in some organs, typical of
    convolutional architectures.

Representative images are provided in the repository under:

    baseline_nnunet/reports/

------------------------------------------------------------------------

## Strengths

-   Fully reproducible pipeline\
-   Automated configuration minimizes human bias\
-   Stable cross‑validation performance\
-   Suitable as a reference baseline for future architectures

------------------------------------------------------------------------

## Limitations

-   Trained exclusively on AMOS22 --- external generalization not yet
    validated\
-   No prospective clinical evaluation\
-   Performance on rare anatomy remains uncertain\
-   Ensemble inference recommended for optimal robustness

------------------------------------------------------------------------

## Ethical Considerations

This model is intended strictly for research purposes.

Medical AI systems require:

-   External validation\
-   Monitoring for dataset bias\
-   Clinical governance\
-   Regulatory oversight

before any clinical translation.

------------------------------------------------------------------------

## Reproducibility

To reproduce the model:

1.  Restore nnU‑Net paths\
2.  Load frozen manifests\
3.  Use the saved environment\
4.  Run ensemble inference

All artifacts are preserved inside the frozen baseline directory.

------------------------------------------------------------------------

## Citation

If this repository contributes to academic work, please cite:

**nnU‑Net:**\
Isensee F, et al. *nnU‑Net: a self‑configuring method for deep
learning‑based biomedical image segmentation.* Nature Methods, 2021.

**AMOS22 Dataset:**\
Ji Y. et al. *AMOS: A Large‑Scale Abdominal Multi‑Organ Benchmark for
Versatile Medical Image Segmentation.*

------------------------------------------------------------------------

## Version

**Model version:** 1.0 (Frozen Baseline)\
**Status:** Stable research baseline\
**Next planned evolution:** MONAI‑based modular pipeline
