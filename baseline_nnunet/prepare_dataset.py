# prepare_dataset.py — Prepare AMOS22 for nnU-Net v2 (Windows-friendly)

# Input (your AMOS22):
#   amos_root/
#     imagesTr/*.nii.gz
#     labelsTr/*.nii.gz
#     imagesVa/*.nii.gz
#     labelsVa/*.nii.gz
#     imagesTs/*.nii.gz
#     dataset.json

# Output (nnU-Net raw):
#   NNUNet_raw/Dataset{ID}_{NAME}/
#     imagesTr/{CASE}_0000.nii.gz
#     labelsTr/{CASE}.nii.gz
#     imagesTs/{CASE}_0000.nii.gz
#     (optional) imagesVaExt/{CASE}_0000.nii.gz
#     (optional) labelsVaExt/{CASE}.nii.gz
#     dataset.json

# Run example:
#   python baseline_nnunet\prepare_dataset.py ^
#     --amos_root "C:\Users\hyeon\Documents\miniconda_medimg_env\data\amos22" ^
#     --nnunet_raw "%NNUNet_raw%" ^
#     --dataset_id 701 ^
#     --dataset_name AMOS22 ^
#     --include_val


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
    return name[:-7] if name.endswith(".nii.gz") else p.stem


def load_amos_dataset_json(amos_root: Path) -> Dict:
    ds = amos_root / "dataset.json"
    if not ds.exists():
        raise FileNotFoundError(f"AMOS dataset.json not found: {ds}")
    return json.loads(ds.read_text(encoding="utf-8"))


def build_nnunet_dataset_json(amos_ds: Dict, dataset_name: str) -> Dict:
    """
    nnU-Net v2 expects labels as: {"background": 0, "organ": 1, ...}
    """
    labels_in = amos_ds.get("labels", {})
    # AMOS labels_in is typically {"0":"background", "1":"spleen", ...}
    # Convert to nnU-Net format: name -> int
    labels_out = {v: int(k) for k, v in labels_in.items()}

    out = {
        "channel_names": {"0": "CT"},
        "labels": labels_out,
        "numTraining": int(amos_ds.get("numTraining", 0)),
        "file_ending": ".nii.gz",
        "name": dataset_name,
        "description": amos_ds.get("description", ""),
        "reference": "",
        "release": "",
        "license": amos_ds.get("license", ""),
    }
    return out


def copy_image_as_channel0(src: Path, dst_images_dir: Path, case_id: str) -> None:
    dst = dst_images_dir / f"{case_id}_0000.nii.gz"
    shutil.copy2(src, dst)


def copy_label(src: Path, dst_labels_dir: Path, case_id: str) -> None:
    dst = dst_labels_dir / f"{case_id}.nii.gz"
    shutil.copy2(src, dst)


def convert_split(
    images_dir: Path,
    labels_dir: Path | None,
    out_images_dir: Path,
    out_labels_dir: Path | None,
    case_prefix: str,
) -> Tuple[int, List[str]]:
    """
    Convert one split. Returns (written_pairs, missing_labels_ids).
    """
    ensure_dir(out_images_dir)
    if labels_dir is not None and out_labels_dir is not None:
        ensure_dir(out_labels_dir)

    images = list_niigz(images_dir)
    labels_map = {stem_niigz(p): p for p in list_niigz(labels_dir)} if labels_dir else {}

    missing = []
    written = 0

    for img in images:
        sid = stem_niigz(img)
        case_id = f"{case_prefix}_{sid}"

        if labels_dir is not None:
            lbl = labels_map.get(sid)
            if lbl is None:
                missing.append(sid)
                continue
            copy_image_as_channel0(img, out_images_dir, case_id)
            copy_label(lbl, out_labels_dir, case_id)  # type: ignore[arg-type]
            written += 1
        else:
            copy_image_as_channel0(img, out_images_dir, case_id)

    return written, missing


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--amos_root", required=True, help="AMOS22 root containing imagesTr/, labelsTr/, etc.")
    ap.add_argument("--nnunet_raw", required=True, help="NNUNet_raw folder (env var NNUNet_raw)")
    ap.add_argument("--dataset_id", type=int, required=True, help="nnU-Net dataset ID (e.g., 701)")
    ap.add_argument("--dataset_name", required=True, help="Dataset name (e.g., AMOS22)")
    ap.add_argument("--prefix", default=None, help="Case prefix (default: dataset_name)")
    ap.add_argument("--include_val", action="store_true", help="Also convert imagesVa/labelsVa into imagesVaExt/labelsVaExt")
    args = ap.parse_args()

    amos_root = Path(args.amos_root)
    nnunet_raw = Path(args.nnunet_raw)

    if not amos_root.exists():
        raise FileNotFoundError(f"AMOS root not found: {amos_root}")

    ds_dir = nnunet_raw / f"Dataset{args.dataset_id:03d}_{args.dataset_name}"
    imagesTr_out = ds_dir / "imagesTr"
    labelsTr_out = ds_dir / "labelsTr"
    imagesTs_out = ds_dir / "imagesTs"

    prefix = args.prefix or args.dataset_name

    # Train
    train_written, train_missing = convert_split(
        images_dir=amos_root / "imagesTr",
        labels_dir=amos_root / "labelsTr",
        out_images_dir=imagesTr_out,
        out_labels_dir=labelsTr_out,
        case_prefix=prefix,
    )

    # Test (no labels expected)
    _test_written, _ = convert_split(
        images_dir=amos_root / "imagesTs",
        labels_dir=None,
        out_images_dir=imagesTs_out,
        out_labels_dir=None,
        case_prefix=prefix,
    )

    # Optional external validation (kept separate from nnU-Net internal CV)
    val_written = 0
    val_missing: List[str] = []
    if args.include_val:
        imagesVa_out = ds_dir / "imagesVaExt"
        labelsVa_out = ds_dir / "labelsVaExt"
        val_written, val_missing = convert_split(
            images_dir=amos_root / "imagesVa",
            labels_dir=amos_root / "labelsVa",
            out_images_dir=imagesVa_out,
            out_labels_dir=labelsVa_out,
            case_prefix=prefix,
        )

    # dataset.json
    amos_ds = load_amos_dataset_json(amos_root)
    nn_ds = build_nnunet_dataset_json(amos_ds, dataset_name=args.dataset_name)
    (ds_dir / "dataset.json").write_text(json.dumps(nn_ds, indent=2), encoding="utf-8")

    print("Created nnU-Net dataset folder:", ds_dir)
    print("Training pairs written:", train_written)
    if train_missing:
        print("WARNING: Missing TRAIN labels for (showing up to 20):", train_missing[:20])

    if args.include_val:
        print("Validation pairs written (external):", val_written)
        if val_missing:
            print("WARNING: Missing VAL labels for (showing up to 20):", val_missing[:20])

    print("Done.")


if __name__ == "__main__":
    main()
