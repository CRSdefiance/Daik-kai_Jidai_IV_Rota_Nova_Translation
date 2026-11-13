"""Preserve the rejected stage and correct only the canonical Maria32 scope key."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha

root=Path('work/analysis/lil_B176_checkpoint_successor_v4573c')
assert not root.exists()
source=Path('scripts/checkpoint_lil_B176_v4573.py')
target=Path('scripts/checkpoint_lil_B176_v4573b.py')
derive(source,target,{
    "ROOT = Path('work/analysis/lil_B176_checkpoint_v4573')":"ROOT = Path('work/analysis/lil_B176_checkpoint_v4573b')",
    'canonical_Maria10_pending_uncredited':'canonical_Maria32_pending_uncredited',
})
old_audit=Path('scripts/verify_editorial_handoff_v4574b.py')
new_audit=Path('scripts/verify_editorial_handoff_v4574c.py')
derive(old_audit,new_audit,{
    'from scripts.checkpoint_lil_B176_v4573 import':'from scripts.checkpoint_lil_B176_v4573b import',
    "ROOT=Path('work/analysis/editorial_handoff_verification_v4574')":"ROOT=Path('work/analysis/editorial_handoff_verification_v4574c')",
})
root.mkdir(parents=True)
save(root/'source_derivation.json',dict(rejected_stage=str(source),rejected_stage_sha256=sha(source.read_bytes()),
    successor_stage=str(target),successor_stage_sha256=sha(target.read_bytes()),
    rejected_audit=str(old_audit),rejected_audit_sha256=sha(old_audit.read_bytes()),
    successor_audit=str(new_audit),successor_audit_sha256=sha(new_audit.read_bytes()),
    reason='The independent audit rejected the accidental Maria10 scope key before any current metadata write. Restore exact canonical Maria32 key; preserve initial stage, both rejected audits and every proof.',
    no_completion_credit=True,full_goal_complete=False))
