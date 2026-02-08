# Abdomen Multi-Organ Segmentation (AMOS22) — Lab-Style Template

This repository is a **reusable, lab-style codebase** for abdominal multi-organ CT segmentation on **AMOS22**, with an emphasis on:

- **reproducible baselines** (nnU-Net first; MONAI experiments later)
- **traceable artifacts** (manifests, environment snapshots, fold metrics, reports)
- **practical workflows** (CLI for long runs; notebooks for “cockpit” checks)

> **No imaging data are stored in this repository.** Raw/preprocessed nnU-Net data and any `*.nii.gz` volumes live outside Git.

---

## Current repository structure (matches the live repo)

```
abdomen-multiorgan-segmentation/
  README.md
  .gitignore
  CITATION.cff
  nnunet_baseline_environment.yaml

  docs/
    DATASET_ACKNOWLEDGEMENT.md

  notebooks/
    AMOS22_dataset_explorer.ipynb

  outputs_dataset_scan/
    scan_manifest.json
    *.csv

  baseline_nnunet/
    prepare_dataset.py
    baseline_nnunet_prepare_dataset.py
    fix_dataset_json.py
    set_nnunet_paths.bat
    AMOS22_sanity_audit.ipynb
    baseline_nnunet_README.md

    outputs_audit/
      amos22_audit_table.csv

    reports/
      AMOS22_nnunet_cross_validation_report.pdf

    runpackets/              # provenance bundle (logs, debug json, progress figs)
      fold_0/ ...
      fold_1/ ...
      fold_2/ ...
      fold_3/ ...
      fold_4/ ...

    frozen_baseline_amos22_701_3d_fullres/
      README_freeze.md
      env/
      manifests/
      metrics/
      nnunet_paths/
      reports/
```

### Design rules (practical)
- **`baseline_nnunet/frozen_baseline_*` is immutable** (“frozen baseline”). Treat as read-only.
- **Notebooks are cockpit tools** (sanity checks / quick audits), while **long training runs stay headless** via CLI.
- Any new research ideas should go into a new folder (e.g., `experiments/monai_*`) rather than changing the frozen baseline.

---

## Frozen baseline (reference model)

A formally frozen nnU-Net baseline is included:

- **Dataset:** AMOS22 (CT), 15 organs + background  
- **nnU-Net dataset ID:** Dataset701_AMOS22  
- **Configuration:** 3d_fullres  
- **Protocol:** 5-fold cross-validation (folds 0–4)  
- **Artifacts captured:** dataset manifests, environment snapshot, fold summaries, training logs, and a publication-grade CV report  

Start here:
- `baseline_nnunet/frozen_baseline_amos22_701_3d_fullres/README_freeze.md`
- `baseline_nnunet/reports/AMOS22_nnunet_cross_validation_report.pdf`

---

## Data location & nnU-Net paths (outside Git)

nnU-Net expects three environment variables (Windows):

- `nnUNet_raw`
- `nnUNet_preprocessed`
- `nnUNet_results`

This repo provides helper scripts:

- **Local script (repo-level):** `baseline_nnunet/set_nnunet_paths.bat`
- **Frozen baseline script:** `baseline_nnunet/frozen_baseline_amos22_701_3d_fullres/nnunet_paths/set_nnunet_paths_windows.bat`

Usage:
```bat
conda activate medimg
call baseline_nnunet\set_nnunet_paths.bat
```

---

## Workflow overview

### 1) Dataset sanity checks (cockpit)
- `notebooks/AMOS22_dataset_explorer.ipynb` (directory audit)
- `baseline_nnunet/AMOS22_sanity_audit.ipynb` (shape/label/spacings audit)

### 2) Prepare nnU-Net dataset structure (CLI)
- `baseline_nnunet/prepare_dataset.py`

### 3) Train nnU-Net 5-fold CV (CLI)
Example (3d_fullres):
```bat
nnUNetv2_train 701 3d_fullres 0
nnUNetv2_train 701 3d_fullres 1
...
nnUNetv2_train 701 3d_fullres 4
```

### 4) Validate (if interrupted)
```bat
nnUNetv2_train 701 3d_fullres 3 --val
nnUNetv2_train 701 3d_fullres 4 --val
```

### 5) Reporting
- Publication-grade CV report (PDF): `baseline_nnunet/reports/AMOS22_nnunet_cross_validation_report.pdf`
- Fold runpackets (logs/progress/debug): `baseline_nnunet/runpackets/fold_*`

---

## Inference on your own CT (recommended: 5-fold ensemble)

1) Convert DICOM → NIfTI (outside scope here).
2) Put the case into an input folder with nnU-Net naming:
   - `case_001_0000.nii.gz`

Then run (example):
```bat
conda activate medimg
call baseline_nnunet\set_nnunet_paths.bat

nnUNetv2_predict ^
  -i "PATH\TO\inputs" ^
  -o "PATH\TO\outputs" ^
  -d 701 ^
  -c 3d_fullres ^
  -f 0 1 2 3 4
```

Visualize with **3D Slicer** or **ITK-SNAP** by overlaying the predicted labelmap onto the CT.

---

## How to cite

### AMOS22 dataset
- AMOS22 challenge portal: https://amos22.grand-challenge.org/
- AMOS paper (arXiv): https://arxiv.org/abs/2206.08023

**Ji Y, Bai H, Yang J, et al.** *AMOS: A Large-Scale Abdominal Multi-Organ Benchmark for Versatile Medical Image Segmentation.* NeurIPS Datasets and Benchmarks (2022).

### nnU-Net
- Nature Methods: https://www.nature.com/articles/s41592-020-01008-z
- PubMed: https://pubmed.ncbi.nlm.nih.gov/33288961/

**Isensee F, Jaeger PF, Kohl SAA, Petersen J, Maier-Hein KH.** *nnU-Net: a self-configuring method for deep learning-based biomedical image segmentation.* **Nature Methods**. 2021;18:203–211. doi:10.1038/s41592-020-01008-z.

### nnU-Net code repository
- https://github.com/MIC-DKFZ/nnUNet

---

## Repository governance

- Do **not** modify frozen baselines.
- Create new experiment folders for any changes (architecture, augmentation, loss, preprocessing, etc.).
- Do **not** commit medical images or derived NIfTI volumes (`*.nii.gz`).

---

## Disclaimer
Research/educational use only. Users are responsible for compliance with dataset licenses and institutional policies.
