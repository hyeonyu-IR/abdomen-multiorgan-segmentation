# Abdomen Multi-Organ Segmentation (AMOS22) — Lab-Style Template

This repository is a **reusable, lab-style codebase** for abdominal multi-organ segmentation, built to support:
- reproducible baselines (nnU-Net, MONAI)
- standardized experiment tracking (configs, manifests, metrics, reports)
- manuscript- and GitHub-ready artifacts

> **Data are not included in this repository.** See **Data & Access** below.

---

## Repository architecture

Recommended top-level layout (you can reuse this for future datasets/projects):

```
abdomen-multiorgan-segmentation/
  README.md
  .gitignore
  CITATION.cff

  docs/
    DATASET_ACKNOWLEDGEMENT.md
    USAGE.md
    METHODS.md
    CHANGELOG.md

  baseline_nnunet/
    frozen_baseline_amos22_701_3d_fullres/
      README_freeze.md
      env/
      manifests/
      metrics/
      reports/
      nnunet_paths/

    scripts/
      prepare_dataset.py
      10_collect_nnunet_cv_metrics.py
      11_make_nnunet_cv_report.py
    notebooks/
      AMOS22_sanity_audit.ipynb
      pipeline.ipynb   # cockpit only (no long overnight runs)

  experiments/
    monai_dynunet_v1/
      configs/
      src/
      scripts/
      outputs/
      reports/
    transformer_unet_v1/
      ...

  inference/
    inputs/           # local-only (ignored by git)
    outputs/          # local-only (ignored by git)

  outputs/            # local-only (ignored by git)
```

### Design rules (practical)
- **Baselines are immutable**: anything inside `baseline_nnunet/frozen_*` is treated as read-only.
- **New ideas live in `experiments/`** with their own configs/outputs.
- **Notebooks are cockpit tools**, not the engine (overnight runs remain headless via CLI).

---

## Frozen baseline (reference model)

This repository contains a formally frozen nnU-Net baseline:

- **Dataset:** AMOS22 (CT), label set with 15 organs + background  
- **nnU-Net dataset ID:** Dataset701_AMOS22  
- **Configuration:** 3d_fullres  
- **Protocol:** 5-fold cross-validation (folds 0–4)  
- **Artifacts:** environment snapshot, dataset manifests, fold metrics, and a publication-grade CV report  

See:
- `baseline_nnunet/frozen_baseline_amos22_701_3d_fullres/README_freeze.md`
- `baseline_nnunet/frozen_baseline_amos22_701_3d_fullres/reports/AMOS22_nnunet_cross_validation_report.pdf`

---

## Data & access (AMOS22)

AMOS22 is distributed via the AMOS22 Grand Challenge platform. Please follow the dataset terms and access instructions there.

- AMOS22 Grand Challenge portal: https://amos22.grand-challenge.org/

This repository intentionally excludes:
- imaging volumes (e.g., `*.nii.gz`)
- nnU-Net raw/preprocessed/results directories
- any model checkpoints unless explicitly released

---

## How to cite

### Dataset
If you use AMOS/AMOS22, please cite the dataset paper:

- https://arxiv.org/abs/2206.08023
- NeurIPS Datasets and Benchmarks paper PDF: https://proceedings.neurips.cc/paper_files/paper/2022/file/ee604e1bedbd069d9fc9328b7b9584be-Paper-Datasets_and_Benchmarks.pdf

**Ji Y, Bai H, Yang J, et al.** *AMOS: A Large-Scale Abdominal Multi-Organ Benchmark for Versatile Medical Image Segmentation.* NeurIPS Datasets and Benchmarks (2022).

### Framework
If you use nnU-Net, please cite:

- Nature Methods: https://www.nature.com/articles/s41592-020-01008-z
- PubMed: https://pubmed.ncbi.nlm.nih.gov/33288961/

**Isensee F, Jaeger PF, Kohl SAA, Petersen J, Maier-Hein KH.** *nnU-Net: a self-configuring method for deep learning-based biomedical image segmentation.* **Nature Methods**. 2021;18:203–211. doi:10.1038/s41592-020-01008-z.

### Code repository
nnU-Net implementation repository:
- https://github.com/MIC-DKFZ/nnUNet

---

## Notes on reproducibility & governance

- Do not modify frozen baselines; create a new experiment directory under `experiments/` instead.
- Keep dataset and nnU-Net runtime folders outside Git, and configure paths with helper scripts.

---

## Disclaimer

This repository is intended for research and educational use. Users are responsible for compliance with all dataset licenses, institutional policies, and regulations.
