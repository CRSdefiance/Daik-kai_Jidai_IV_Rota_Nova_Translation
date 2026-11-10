"""Bind the approval receipt through the map to avoid a manuscript self-hash cycle."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B223_atomic_seal_hash_tools_v7115c')
if __name__=='__main__':
    assert not ROOT.exists()
    jobs=[('dk4tool/patch/lil_B223_atomic_support_v1.py','dk4tool/patch/lil_B223_atomic_support_v2.py',{"==doc[k+'_sha256'],'proof hash:'":"==(mapping['evidence'][doc[k]] if k=='native_approval' else doc[k+'_sha256']),'proof hash:'"}),
      ('dk4tool/patch/lil_B223_editorial_v2.py','dk4tool/patch/lil_B223_editorial_v3.py',{'lil_B223_atomic_support_v1':'lil_B223_atomic_support_v2'}),
      ('scripts/validate_lil_B223_atomic_v7115b.py','scripts/validate_lil_B223_atomic_v7115c.py',{'lil_B223_editorial_v2 as owned':'lil_B223_editorial_v3 as owned',"ROOT=Path('work/analysis/lil_B223_atomic_v7115b')":"ROOT=Path('work/analysis/lil_B223_atomic_v7115c')",'lil_B223_atomic_support_v1.py':'lil_B223_atomic_support_v2.py',"    deps.add('work/analysis/lil_B223_atomic_field_tools_v7115b/source_locked_schema_correction.json')":"    deps.add('work/analysis/lil_B223_atomic_field_tools_v7115b/source_locked_schema_correction.json')\n    deps.add('work/analysis/lil_B223_atomic_seal_hash_tools_v7115c/source_locked_approval_hash_binding.json')"})]
    for a,b,c in jobs:assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c)
    rows=[derive(a,b,c) for a,b,c in jobs];ROOT.mkdir(parents=True);save(ROOT/'source_locked_approval_hash_binding.json',dict(tools=rows,failed_v1_v2_and_positive_configs_preserved=True,approval_receipt_hash_required_from_sealed_map_evidence=True,no_self_hash_cycle_or_missing_hash_waiver=True,no_native_address_source_prose_or_glyph_requirement_change=True,new_credit=0,full_goal_complete=False))
