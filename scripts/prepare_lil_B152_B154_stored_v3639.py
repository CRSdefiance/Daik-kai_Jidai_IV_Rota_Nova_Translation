"""Bind final stored targets using the unchanged original native font/macro probe."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
SOURCE=Path('scripts/prove_lil_B142_B145_stored_v3594.py')
TARGET=Path('scripts/prove_lil_B152_B154_stored_v3639.py')
if __name__=='__main__':
    assert not TARGET.exists();text=SOURCE.read_text(encoding='utf-8')
    pairs=[('all38','all59'),('All38','All59'),('all38_final_stored_targets152','all59_final_stored_targets236'),('lil_B142_B145_stored_v3594','lil_B152_B154_stored_v3639'),('lil_B142_B145_editorial_manuscript_v4','lil_B152_B154_editorial_manuscript_v6'),('lil_B142_B145_relocation_v3593','lil_B152_B154_relocation_v3638'),('lil_B142_B145_voices_v3572','lil_B152_B160_voices_v3616'),('len(cases)==38 and fresh==72 and reused==80','len(cases)==59 and fresh==144 and reused==92'),('in [2,4,9,13,16,20,23,109,171,254]','in [2,9,14,17,20,92,115,148]'),('current_final_stored_macro_alignment_cases=152','current_final_stored_macro_alignment_cases=236'),('new_parity_macro_alignment_cases=72','new_parity_macro_alignment_cases=144'),('exact_byte_identical_reused_macro_alignment_cases=80','exact_byte_identical_reused_macro_alignment_cases=92'),('new_parity_tail_planes=18','new_parity_tail_planes=36'),('exact_reused_compiled_planes=20','exact_reused_compiled_planes=23'),('152 alignment cases:72fresh on18parity tails plus80exact reuses','236 alignment cases:144fresh on36parity tails plus92exact reuses')]
    for a,b in pairs:assert a in text,a;text=text.replace(a,b)
    text=text.replace('"""Bind all59 final stored targets;repaint18 new parity tails and reuse20 byte-identical bodies."""','"""Bind59 stored targets;repaint36 parity tails,reuse23 exact compiled bodies."""')
    TARGET.write_text(text,encoding='utf-8',newline='\n');root=Path('work/analysis/lil_B152_B154_stored_derivation_v3639');assert not root.exists();root.mkdir(parents=True);save(root/'source_derivation.json',dict(source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),successor=str(TARGET),successor_sha256=sha(TARGET.read_bytes()),no_executed_predecessor_modified=True))
