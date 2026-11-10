"""Correct whole-container comparison while preserving every native control byte."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B212_nested_comparison_v6594b')
if __name__=='__main__':
    assert not ROOT.exists()
    old="nontext=lambda cs:[(c['offset'],c['whole_command_hex']) for c in cs if c['word'] not in [0x4000,0x2100,0x2200]];assert nontext(old)==nontext(now)"
    new="nontext=lambda cs:[(c['offset'],c['whole_command_hex'][:8] if c['word']==0x100 else c['whole_command_hex']) for c in cs if c['word'] not in [0x4000,0x2100,0x2200]];assert nontext(old)==nontext(now)\n    inverse=bytearray(target);inverse_regions=[]\n    for a,b in zip(old,now,strict=True):\n        if a['word'] in [0x4000,0x2100,0x2200]:\n            at,end=a['offset'],a['offset']+a['native_extent'];assert a['native_extent']==b['native_extent'];inverse[at:end]=source[at:end];inverse_regions.append(dict(offset=at,bytes=end-at,source_command_sha256=sha(source[at:end]),current_command_sha256=sha(target[at:end])))\n    assert len(inverse_regions)==11 and bytes(inverse)==source"
    proof=derive('scripts/map_lil_B212_source_v6594.py','scripts/map_lil_B212_source_v6594b.py',{'lil_B212_source_v6594':'lil_B212_source_v6594b',old:new,'source_current_command_shape_exact=True,records=rows':'source_current_command_shape_exact=True,all_control_headers_operands_ends_and_complete884_byte_inverse_exact=True,source_current_prose_container_regions=inverse_regions,records=rows'})
    ROOT.mkdir(parents=True);save(ROOT/'nested_container_comparison_correction.json',dict(proof=proof,predecessor_preserved='scripts/map_lil_B212_source_v6594.py',reason='0100 whole-command extents contain nested speech bytes. Compare each exact four-byte 0100 control header and every independently mapped nested command, then restore all11 speech/choice containers and require every884 byte to recover. No source control or operand mismatch was waived.',no_ROM_ledger_or_credit_change=True,full_goal_complete=False))
