"""Bind Rafael's next crew rumors, letters, and Havana scenes to the latest build."""

from pathlib import Path

from scripts import pair_rafael_B221_B240_20261122 as prior
from scripts import register_rafael_B221_B240_20261122 as parent
from scripts.source_locked_derivation_v5118 import checked_text


base, native = parent.base, parent.native
ROOT = Path("work/analysis/rafael_B241_B260_followup_20261122")
PAIRED = ROOT / "paired_source_registered_candidate.json"
EARLIER = Path("translations/rafael_B241_B260_integrated_final_review_v1.json")
B246 = Path("releases/all_routes_editorial_20261118_papal_states_titis_candidate/verification/registered_review.json")
source = checked_text(prior.source, {
    '    references = {(r["block"], r["source_reference"]["offset"]): r for r in prior["records"]}':
        '''    restored = [r | {"source_Japanese": r["Japanese"]} for r in base.load(B246)["records"]
                if r["file_path"] == ARCHIVE and r["block"] == 246]
    assert len(restored) == 18 and not any(r["block"] == 246 for r in prior["records"])
    references = {(r["block"], r["source_reference"]["offset"]): r for r in prior["records"] + restored}''',
    '    print("270 exact source and current records bound across Rafael B221–240, including seven choice labels and 29 actor-style variants.")':
        '''    packet = base.load(PAIRED)
    packet["additional_B246_review"] = {"path": str(B246), "sha256": base.digest(B246), "records": len(restored)}
    base.save(PAIRED, packet)
    print("310 exact source and current records bound across Rafael B241–260, including the 18 earlier B246 records.")''',
    'range(221, 241)': 'range(241, 261)',
    'len(ready) == 270': 'len(ready) == 310',
    'for r in ready) == 7': 'for r in ready) == 6',
    'for r in ready) == 29': 'for r in ready) == 14',
    'for g in groups) == 4': 'for g in groups) == 2',
})
scope = prior.scope | globals()
exec(compile(source, __file__ + "::exact-source-current-binding", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
