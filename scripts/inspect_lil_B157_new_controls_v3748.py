"""Map new source command boundaries without claiming effect-body or UI execution."""
import inspect,struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.research_wedding_command_v676 import walk
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B157_new_control_boundaries_v3748')
SOURCE=Path('work/analysis/lil_B157_source_v3746/all75_clean_current_complete_context.json')
if __name__=='__main__':
    assert not ROOT.exists();source=read(SOURCE);commands=source['blocks'][0]['all_clean_native_commands'];images=[NdsImage.open(p) for p in ['work/clean.nds',source['current_ROM']]];selected=[c for c in commands if c['word'] in [0xC281,0x4885]];assert len(selected)==2;rows=[]
    for c in selected:
        raw=bytes.fromhex(c['whole_command_hex']);synthetic=b'CS\0\1'+struct.pack('<H',len(raw))+bytes(2)+raw;versions=[]
        for label,image in zip(['clean','current'],images,strict=True):
            result=walk(image.read_file('/__arm9__.bin'),synthetic);assert result['error'] is None and result['stopped_offset']==result['logical_end']==len(synthetic) and len(result['rows'])==1 and result['rows'][0]['word']==c['word'] and result['rows'][0]['native_extent']==c['native_extent'];versions.append(dict(version=label,**result))
        assert versions[0]['rows']==versions[1]['rows'] and versions[0]['opaque_effect_bridges']==versions[1]['opaque_effect_bridges'];rows.append(dict(source_offset=c['offset'],source_word=c['word'],whole_source_command_hex=raw.hex(),source_extent=c['native_extent'],versions=versions,isolated_synthetic_offset8_not_original_block_cursor=True,all_nondecode_callees_bridged_with_zero_return=True,not_full_body_current_context_or_actual_UI_execution=True))
    ROOT.mkdir(parents=True);save(ROOT/'C281_and4885_source_original_structural_boundaries.json',dict(source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),current_ROM=source['current_ROM'],current_ROM_sha256=source['current_ROM_sha256'],cases=rows,source_owned_structural_adapter=inspect.getsource(walk),source_C281_and4885_full_owned_effects_and_actual_transitions_still_pending=True,no_prose_ROM_registry_ledger_orcredit_change=True,new_emulator_runs=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    for r in rows:print(dict(word=format(r['source_word'],'04X'),source_offset=r['source_offset'],extent=r['source_extent'],structural_bridges=r['versions'][1]['opaque_effect_bridges']))
