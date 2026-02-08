# Frozen Baseline --- AMOS22 nnU-Net (Dataset701, 3d_fullres)

## Purpose

This document formally freezes the nnU-Net baseline experiment for the
AMOS22 multi-organ abdominal CT segmentation project.\
The objective is to ensure **full reproducibility**, provide a **stable
control arm** for future architectural experiments (e.g., MONAI
pipelines), and document the exact training configuration used to
generate the baseline results.

------------------------------------------------------------------------

## Experiment Overview

**Framework:** nnU-Net v2\
**Dataset:** AMOS22\
**Dataset ID:** Dataset701_AMOS22\
**Configuration:** 3d_fullres\
**Cross-validation:** 5-fold (folds 0--4)\
**Training Schedule:** 1000 epochs per fold

This baseline represents the institutional reference model for all
future segmentation experiments.

------------------------------------------------------------------------

## Data Integrity

The following artifacts were preserved to guarantee dataset
reproducibility:

-   `manifests/dataset.json`
-   `manifests/splits_final.json`

These files define:

-   label schema\
-   modality\
-   training/validation partitions\
-   case allocation per fold

⚠️ **Do not modify these files.**\
Any dataset modification must create a new experiment lineage.

------------------------------------------------------------------------

## Metrics and Reports

Stored under:

    metrics/
    reports/

Contents include:

-   Fold-level `summary.json` files\
-   Aggregated cross-validation metrics\
-   Publication-grade cross-validation report

These constitute the authoritative performance record for this baseline.

------------------------------------------------------------------------

## Environment Snapshot

Saved under:

    env/

Includes:

-   `conda_env_medimg.yaml`
-   `pip_freeze.txt`
-   `system_torch_cuda_gpu.txt`

These files ensure that the software stack can be reconstructed
precisely.

------------------------------------------------------------------------

## nnU-Net Path Configuration

Reusable path script:

    nnunet_paths/set_nnunet_paths_windows.bat

Before running inference or retraining:

``` bat
conda activate medimg
call nnunet_paths\set_nnunet_paths_windows.bat
```

This guarantees consistent linkage to:

-   nnUNet_raw\
-   nnUNet_preprocessed\
-   nnUNet_results

------------------------------------------------------------------------

## Frozen Model Definition

The "frozen baseline" refers to:

-   the trained weights from folds 0--4\
-   the preprocessing plans\
-   dataset fingerprint\
-   environment configuration\
-   validation metrics

No additional tuning or retraining should occur within this directory.

All new experiments must branch into a separate folder.

Example:

    experiments/
        monai_dynunet_v1/
        transformer_unet_v1/

------------------------------------------------------------------------

## Recommended Inference Strategy

For production-style inference, use the **5-fold ensemble**:

    nnUNetv2_predict -d 701 -c 3d_fullres -f 0 1 2 3 4

Ensembling typically improves robustness and reduces variance compared
to single-fold models.

------------------------------------------------------------------------

## Reproducibility Statement

This baseline satisfies the core pillars of reproducible medical AI
research:

-   Fixed dataset partition\
-   Archived preprocessing pipeline\
-   Environment capture\
-   Deterministic configuration\
-   Formal performance report

Future model improvements must be evaluated against this baseline.

------------------------------------------------------------------------

## Governance Rule

> **Do not alter this directory.**\
> Treat it as a read-only scientific artifact.

If retraining is required:

1.  Create a new experiment directory.
2.  Document changes explicitly.
3.  Compare results against this frozen baseline.

------------------------------------------------------------------------

## Suggested Citation (Internal / Manuscript Drafting)

> "A five-fold cross-validation nnU-Net baseline was established on the
> AMOS22 dataset using a 3D full-resolution configuration.\
> The experiment was frozen with complete environment capture and
> dataset manifests to ensure long-term reproducibility and serve as the
> institutional reference model for subsequent architectural
> investigations."

------------------------------------------------------------------------

## Created By

Lab-style pipeline developed for reproducible academic medical imaging
research.

- Frozen on: 02/08/2026
- Operator: Hyeon Yu, MD

------------------------------------------------------------------------

## Notes for Future You

If you are reading this months or years later:

You already did the hard part correctly.

This baseline is your scientific anchor.
