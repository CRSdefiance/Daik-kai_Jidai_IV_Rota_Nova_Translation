"""Accept immutable clean-first packets with explicit per-record unconsulted flags."""
from scripts import extract_editorial_current_v2 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    "assert meanings['meanings'] == len(meanings['records']) and meanings['earlier_English_unconsulted']":
        "assert meanings['meanings'] == len(meanings['records']) and all(r['earlier_English_unconsulted'] for r in meanings['records'])",
})
exec(compile(source,__file__+'::same-current-binding-per-record-clean-first-gate','exec'),globals())
