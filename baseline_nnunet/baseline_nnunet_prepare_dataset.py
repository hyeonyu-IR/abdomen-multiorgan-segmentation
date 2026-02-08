"""
Prepare AMOS22 for nnU-Net v2 (Windows-friendly).

- Reads AMOS22 layout:
    amos_root/
      imagesTr/*.nii.gz
      labelsTr/*.nii.gz
      imagesVa/*.nii.gz
      labelsVa/*.nii.gz
      imagesTs/*.nii.gz
      dataset.json

- Writes nnU-Net raw dataset:
    nnunet_raw/Dataset{dataset_id}_{dataset_name}/
      imagesTr/{caseid}_0000.nii.gz
      labelsTr/{caseid}.nii.gz
      imagesTs/{caseid}_0000.nii.gz
      dataset.json (nnU-Net style)

Notes:
- Copies files (safe/easy). You can later extend to symlinks if desired.
- Skips non-NIfTI files (e.g., .DS_Store).
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Dict, List, Tuple


def list_niigz(folder: Path) -> List[Path]:
    if not folder.exists():
        return []
    return sorted([p for p in folder.iterdir() if p.is_file() and p.name.endswith(".nii.gz")])


def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def stem_niigz(p: Path) -> str:
    # "amos_0001.nii.gz" -> "amos_0001"
    name = p.name
    if name.endswith(".nii.gz"):
        return name[:-7]
    return p.stem


def load_amos_dataset_json(amos_root: Path) -> Dict:
    ds = amos_root / "dataset.json"
    if not ds.exists():
        raise FileNotFoundError(f"AMOS dataset.json not found: {ds}")
    return json.loads(ds.read_text(encoding="utf-8"))


def build_nnunet_dataset_json(amos_ds: Dict, dataset_name: str) -> Dict:
    # nnU-Net v2 expects keys: channel_names, labels, numTraining, file_ending
    labels = amos_ds.get("labels", {})
    # Ensure string keys; nnU-Net is fine with {"background":0,...} or {"0":"background"...}
    # We'll keep AMOS style (index->name) but ensure strings.
    labels = {str(k): v for k, v in labels.items()}

    out = {
        "channel_names": {"0": "CT"},  # AMOS22 metadata indicates CT modality in your scan
        "labels": labels,
        "numTraining": int(amos_ds.get("numTraining", 0)),
        "file_ending": ".nii.gz",
        "name": dataset_name,
        "description": amos_ds.get("description", ""),
        "reference": "",
        "release": "",
        "license": amos_ds.get("license", ""),
    }
    return out


def copy_as_channel0(src: Path, dst_images_dir: Path, case_id: str) -> None:
    dst = dst_images_dir / f"{case_id}_0000.nii.gz"
    shutil.copy2(src, dst)


def copy_label(src: Path, dst_labels_dir: Path, case_id: str) -> None:
    dst = dst_labels_dir / f"{case_id}.nii.gz"
    shutil.copy2(src, dst)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--amos_root", required=True, help="Path to AMOS22 root (contains imagesTr/, labelsTr/, etc.)")
    ap.add_argument("--nnunet_raw", required=True, help="Path to NNUNet_raw (env var NNUNet_raw)")
    ap.add_argument("--dataset_id", type=int, required=True, help="nnU-Net dataset ID (e.g., 701)")
    ap.add_argument("--dataset_name", required=True, help="nnU-Net dataset name suffix (e.g., AMOS22)")
    ap.add_argument("--prefix", default=None, help="Optional case prefix (default: dataset_name)")
    args = ap.parse_args()

    amos_root = Path(args.amos_root)
    nnunet_raw = Path(args.nnunet_raw)

    if not amos_root.exists():
        raise FileNotFoundError(f"AMOS root not found: {amos_root}")

    ds_dir = nnunet_raw / f"Dataset{args.dataset_id:03d}_{args.dataset_name}"
    imagesTr_out = ds_dir / "imagesTr"
    labelsTr_out = ds_dir / "labelsTr"
    imagesTs_out = ds_dir / "imagesTs"

    ensure_dir(imagesTr_out)
    ensure_dir(labelsTr_out)
    ensure_dir(imagesTs_out)

    prefix = args.prefix or args.dataset_name

    # Training pairs
    imagesTr = list_niigz(amos_root / "imagesTr")
    labelsTr = {stem_niigz(p): p for p in list_niigz(amos_root / "labelsTr")}

    missing_labels = []
    written = 0
    for img in imagesTr:
        sid = stem_niigz(img)
        if sid not in labelsTr:
            # skip .DS_Store etc already filtered; this catches genuine missing
            missing_labels.append(sid)
            continue
        case_id = f"{prefix}_{sid}"
        copy_as_channel0(img, imagesTr_out, case_id)
        copy_label(labelsTr[sid], labelsTr_out, case_id)
        written += 1

    # Test images (labels usually unavailable)
    imagesTs = list_niigz(amos_root / "imagesTs")
    for img in imagesTs:
        sid = stem_niigz(img)
        case_id = f"{prefix}_{sid}"
        copy_as_channel0(img, hooking := imagesTs_out, case_id)

    # dataset.json
    amos_ds = load_amos_dataset_json(amos_root)
    nn_ds = build_nnunet_dataset_json(amos_ds, dataset_name=args.dataset_name)
    (ds_dir / "dataset.json").write_text(json.dumps(nn_ds, indent=2), encoding="utf-8")

    print("Created nnU-Net dataset folder:", ds_dir)
    print("Training cases written:", written)
    if missing_labels:
        print("WARNING: imagesTr with missing labelsTr (showing up to 20):", missing_labels[:20])


if __name__ == "__main__":
    main()
