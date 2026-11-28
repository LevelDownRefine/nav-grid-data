"""Verify the published navigation package references exact checked-out bytes."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1] / "navigation"
package = json.loads((root / "prepared-package.json").read_text(encoding="utf-8"))
files = {
    "dataset_sha256": root / "dataset.json",
    "localization_manifest_sha256": root / "localization" / "manifest.json",
    "prepared_manifest_sha256": root / "localization" / "prepared" / "manifest.json",
}
errors = []
for key, path in files.items():
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    expected = package.get(key)
    if actual != expected:
        errors.append(f"{path}: {key} expected {expected}, got {actual}")
    else:
        print(f"OK {path}: {actual}")
if errors:
    raise SystemExit("\n".join(errors))
