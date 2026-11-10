"""Bind the original preparation import in the simultaneous source-locked successor map."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/build_registered_maria328_v1.py').read_text(encoding='utf-8'),{
    "'prepare_maria328_registered_v2':'prepare_maria328_registered_v1'":
        "'prepare_maria303_registered_v2':'prepare_maria328_registered_v1'",
})
exec(compile(source,__file__+'::same-release-contract-correct-original-preparation-binding','exec'),globals())
