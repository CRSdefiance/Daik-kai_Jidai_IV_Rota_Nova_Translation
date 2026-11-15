"""Preserve the failed audit; distinguish binary English FE physical planes from indexed source planes."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Rafael_B45_actual_schema_v7895b');assert not root.exists()
    result=derive('scripts/audit_Rafael_B45_actual_v7895.py','scripts/audit_Rafael_B45_actual_v7895b.py',{
        'work/analysis/Rafael_B45_actual_v7895':'work/analysis/Rafael_B45_actual_v7895b',
        "physical[(y//12*16+y%12)*228+x]=logical[y*228+x]":
        "physical[(y//12*16+y%12)*228+x]=int(bool(logical[y*228+x]))",
        "black={(i%228,i//228) for i,b in enumerate(physical) if b==15}":
        "black={(i%228,i//228) for i,b in enumerate(physical) if b==(15 if version=='clean_Japanese' else 1)}",
        "ASCII_gray=set();CP_gray={(i%228,i//228) for i,b in enumerate(physical) if b==14}":
        "ASCII_gray=set();CP_gray={(i%228,i//228) for i,b in enumerate(physical) if b==14} if version=='clean_Japanese' else set()",
    })
    root.mkdir(parents=True);save(root/'provenance.json',dict(derivation=result,
        failure='English FE physical plane hash:original English oracle stores binary ink;source CP932 oracle stores native indexed foreground15/shadow14',
        all_original_full_plane_hashes_andactual_palette_masks_still_checked=True,
        original_failed_audit_andJapanese_partial_sheets_preserved=True,
        no_ROM_prose_orcapture_change_no_new_emulator_run=True,new_credit=0,full_goal_complete=False))
