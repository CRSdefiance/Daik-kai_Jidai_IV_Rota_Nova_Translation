"""Prepare complete B177 execution/native-plane auditing using the corrected observer schema."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

root=Path('work/analysis/lil_B177_actual_tools_v4638')
assert not root.exists()
tool=derive('scripts/audit_lil_B176_actual_v4588b.py','scripts/audit_lil_B177_actual_v4638.py',{
    'B176':'B177','lil_B176':'lil_B177',
    'actual_v4588':'actual_v4638','display_fixture_v4585':'display_fixture_v4635',
    'native_approval_v4572':'native_approval_v4622',
    'display_run_v4587':'display_run_v4637','display_v4587':'display_v4637',
    'source_event176_not_selected':'source_event177_not_selected',
    "source['block']!=176":"source['block']!=177",'original_source_block=176':'original_source_block=177',
    "selected[-1]['original_source_offset']==386":"selected[-1]['original_source_offset']==482",
    "r.get('original_source_block')==176":"r.get('original_source_block')==177",
    "ui[0]['original_source_offset']==384":"ui[0]['original_source_offset']==480",
    'single_source_end386_actually_reached':'single_source_end482_actually_reached',
    'actual_source_event176_not_selected':'actual_source_event177_not_selected',
})
root.mkdir(parents=True)
save(root/'source_derivation.json',dict(tool=tool,source_speeches=10,source_commands=13,fixture_commands=22,
    source_A000=1,original_prelude_A000=4,impersonal_FE=1,single_end=482,frames=9001,
    long_R12_complete216x64_plane_required=True,pending_entry_row_references_resolved_by_original_schema=True,
    no_new_editorial_credit=True,full_goal_complete=False))
