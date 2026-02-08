# baseline_nnunet (AMOS22)

This folder documents a **reproducible nnU-Net v2 baseline** for the AMOS22 dataset stored locally at:

`C:\Users\hyeon\Documents\miniconda_medimg_env\data\amos22`

Your AMOS22 folder structure (as scanned) is:
- `imagesTr/` (241 files; includes a `.DS_Store`)
- `labelsTr/` (240 files)
- `imagesVa/` (120 files)
- `labelsVa/` (120 files)
- `imagesTs/` (240 files)
- `labelsTs/` (empty)
- `dataset.json` defines labels `0..15` (15 organs + background)

**Important:** Do **not** commit imaging volumes (`*.nii.gz`) into GitHub. Keep data in `.../data/amos22` and only commit code/config/docs.

---

## 0) Prerequisites

### A. Activate your environment
In **Anaconda Prompt**:

```bat
conda activate medimg
```

### B. Install nnU-Net v2 (if not installed)
```bat
pip install nnunetv2
```

### C. Set nnU-Net paths (Windows)
Pick a root folder for nnU-Net outputs (recommended under your `miniconda_medimg_env\data`). Example:

- `NNUNET_BASE = C:\Users\hyeon\Documents\miniconda_medimg_env\data\nnunet_amos22`

Create the folders:
```bat
mkdir C:\Users\hyeon\Documents\miniconda_medimg_env\data\nnunet_amos22
mkdir C:\Users\hyeon\Documents\miniconda_medimg_env\data\nnunet_amos22\nnunet_raw
mkdir C:\Users\hyeon\Documents\miniconda_medimg_env\data\nnunet_amos22\nnunet_preprocessed
mkdir C:\Users\hyeon\Documents\miniconda_medimg_env\data\nnunet_amos22\nnunet_results
```

Set environment variables for current terminal session:
```bat
set NNUNet_raw=C:\Users\hyeon\Documents\miniconda_medimg_env\data\nnunet_amos22\nnunet_raw
set NNUNet_preprocessed=C:\Users\hyeon\Documents\miniconda_medimg_env\data\nnunet_amos22\nnunet_preprocessed
set NNUNet_results=C:\Users\hyeon\Documents\miniconda_medimg_env\data\nnunet_amos22\nnunet_results
```

(Optional) Persist them:
```bat
setx NNUNet_raw "C:\Users\hyeon\Documents\miniconda_medimg_env\data\nnunet_amos22\nnunet_raw"
setx NNUNet_preprocessed "C:\Users\hyeon\Documents\miniconda_medimg_env\data\nnunet_amos22\nnunet_preprocessed"
setx NNUNet_results "C:\Users\hyeon\Documents\miniconda_medimg_env\data\nnunet_amos22\nnunet_results"
```

Close and re-open the terminal if you used `setx`.

---

## 1) Create an nnU-Net dataset folder from your AMOS22 layout

nnU-Net v2 expects a dataset folder like:
`%NNUNet_raw%\DatasetXXX_AMOS22\imagesTr\case_0000.nii.gz`

Because AMOS22 currently uses names like `amos_0001.nii.gz` and doesn't have the `_0000` channel suffix, we create a **lightweight copy** (or symlink) that matches nnU-Net naming.

### Option A (recommended first): copy into nnU-Net raw structure
From your repo root:

```bat
python baseline_nnunet_prepare_dataset.py ^
  --amos_root "C:\Users\hyeon\Documents\miniconda_medimg_env\data\amos22" ^
  --nnunet_raw "%NNUNet_raw%" ^
  --dataset_id 701 ^
  --dataset_name AMOS22
```

This creates:
- `%NNUNet_raw%\Dataset701_AMOS22\imagesTr\AMOS22_XXXX_0000.nii.gz`
- `%NNUNet_raw%\Dataset701_AMOS22\labelsTr\AMOS22_XXXX.nii.gz`
- `%NNUNet_raw%\Dataset701_AMOS22\imagesTs\...` (from `imagesTs/`)
- It also writes `dataset.json` in nnU-Net format.

**Note:** Dataset IDs just need to be unique on your machine. `701` is an arbitrary suggestion.

---

## 2) Plan & preprocess

```bat
nnUNetv2_plan_and_preprocess -d 701 --verify_dataset_integrity
```

---

## 3) Train (baseline)

Start with `3d_fullres` (most common baseline):

```bat
nnUNetv2_train 701 3d_fullres 0
```

This trains fold 0. For a full baseline across all folds:

```bat
nnUNetv2_train 701 3d_fullres 0
nnUNetv2_train 701 3d_fullres 1
nnUNetv2_train 701 3d_fullres 2
nnUNetv2_train 701 3d_fullres 3
nnUNetv2_train 701 3d_fullres 4
```

---

## 4) Inference

### A) Predict on the official test set (labels unavailable)
```bat
nnUNetv2_predict ^
  -i "%NNUNet_raw%\Dataset701_AMOS22\imagesTs" ^
  -o outputs\nnunet_pred_imagesTs ^
  -d 701 -c 3d_fullres -f 0 1 2 3 4
```

### B) Predict on the provided validation set (has labels)
Your AMOS22 has `imagesVa/` and `labelsVa/`. nnU-Net does not use a separate `imagesVa` folder by default, so we treat this as an **external evaluation set**.

First, convert `imagesVa` into nnU-Net-style *input* folder (we can add this later in the same prepare script), then:

```bat
nnUNetv2_predict -i outputs\nnunet_input_imagesVa -o outputs\nnunet_pred_imagesVa -d 701 -c 3d_fullres -f 0 1 2 3 4
```

Then evaluate with your own script (recommended, consistent with MONAI later), or with nnU-Net utilities if you prefer.

---

## 5) What we will do next (recommended)

1) Run **sanity audit** (label range, pairing, shape/affine checks) on:
   - `imagesTr/labelsTr` (training)
   - `imagesVa/labelsVa` (external validation)
2) Create a small parser that collects nnU-Net metrics into a single CSV that your future `pipeline.ipynb` can read.

---
