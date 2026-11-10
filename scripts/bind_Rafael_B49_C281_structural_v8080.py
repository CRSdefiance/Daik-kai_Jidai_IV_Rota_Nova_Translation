"""Bind the exactB49 C281 structural boundary;preserve the failed wrong-handler probe andrequire actual transition checks."""
import inspect,struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.research_wedding_command_v676 import walk
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B49_C281_structural_v8080')
SOURCE=Path('work/analysis/Rafael_next_clean_v8073/complete_clean_SC0_B49_EV0_andcoverage_before_current_English.json')
if __name__=='__main__':
    assert not ROOT.exists();source=read(SOURCE);commands=source['groups'][0]['commands'];inp=read('work/analysis/current_V8066_Rafael_native_v8069/current_native_input.json');source=dict(source,current_ROM=inp['current_ROM'],current_ROM_sha256=inp['current_ROM_sha256']);assert sha(Path(inp['current_ROM']).read_bytes())==inp['current_ROM_sha256'];images=[NdsImage.open(p) for p in ['work/clean.nds',source['current_ROM']]];selected=[c for c in commands if c['word'] in [0xC281]];assert len(selected)==1;rows=[]
    for c in selected:
        raw=bytes.fromhex(c['whole_command_hex']);synthetic=b'CS\0\1'+struct.pack('<H',len(raw))+bytes(2)+raw;versions=[]
        for label,image in zip(['clean','current'],images,strict=True):
            result=walk(image.read_file('/__arm9__.bin'),synthetic);assert result['error'] is None and result['stopped_offset']==result['logical_end']==len(synthetic) and len(result['rows'])==1 and result['rows'][0]['word']==c['word'] and result['rows'][0]['native_extent']==c['native_extent'];versions.append(dict(version=label,**result))
        assert versions[0]['rows']==versions[1]['rows'] and versions[0]['opaque_effect_bridges']==versions[1]['opaque_effect_bridges'];rows.append(dict(source_offset=c['offset'],source_word=c['word'],whole_source_command_hex=raw.hex(),source_extent=c['native_extent'],versions=versions,isolated_synthetic_offset8_not_original_block_cursor=True,all_nondecode_callees_bridged_with_zero_return=True,not_full_body_current_context_or_actual_UI_execution=True))
    ROOT.mkdir(parents=True);save(ROOT/'exact_C281_source_original_structural_boundary.json',dict(failed_wrong_predicate_handler_probe='scripts/prove_Rafael_B49_C281_v8079.py',failed_wrong_predicate_handler_probe_sha256=sha(Path('scripts/prove_Rafael_B49_C281_v8079.py').read_bytes()),source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),current_ROM=source['current_ROM'],current_ROM_sha256=source['current_ROM_sha256'],cases=rows,source_owned_structural_adapter=inspect.getsource(walk),source_C281_full_owned_effects_and_actual_transition_still_pending=True,no_prose_ROM_registry_ledger_orcredit_change=True,new_emulator_runs=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    for r in rows:print(dict(word=format(r['source_word'],'04X'),source_offset=r['source_offset'],extent=r['source_extent'],structural_bridges=r['versions'][1]['opaque_effect_bridges']))
