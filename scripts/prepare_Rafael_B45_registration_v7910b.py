"""Bind the existing positive proof and parent fields from their actual schemas."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Rafael_B45_registration_tools_v7910b');assert not root.exists()
    row=derive('scripts/register_Rafael_B45_v7910.py','scripts/register_Rafael_B45_v7910b.py',{
        "sha(PARENT.read_bytes())==result['parent_ROM_sha256']":"sha(PARENT.read_bytes())==conf['parent_ROM_sha256']\n    assert sha(Path(result['positive_proof']).read_bytes())==result['positive_proof_sha256']"})
    root.mkdir(parents=True);save(root/'provenance.json',row)
