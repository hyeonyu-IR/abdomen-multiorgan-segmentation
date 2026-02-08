from pathlib import Path
import json

p = Path(r"C:\Users\hyeon\Documents\miniconda_medimg_env\data\nnunet_amos22\nnunet_raw\Dataset701_AMOS22\dataset.json")
ds = json.loads(p.read_text(encoding="utf-8"))

labels = ds["labels"]  # currently id->name
# convert to name->id
ds["labels"] = {v: int(k) for k, v in labels.items()}

p.write_text(json.dumps(ds, indent=2), encoding="utf-8")
print("Rewrote labels to name->id in:", p)
