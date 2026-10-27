"""Derive a source-owned successor with explicit pause and double-end ownership."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
SOURCE=Path('scripts/research_lil_B142_B145_relocation_v3593.py')
TARGET=Path('scripts/research_lil_B152_B154_relocation_v3638.py')
if __name__=='__main__':
    assert not TARGET.exists();text=SOURCE.read_text(encoding='utf-8')
    pairs=[('lil_B142_B145_relocation_v3593','lil_B152_B154_relocation_v3638'),('lil_B142_B145_editorial_manuscript_v4','lil_B152_B154_editorial_manuscript_v6'),('all_routes_combined_v3561','all_routes_combined_v3607'),('len(results)==4','len(results)==3'),("for r in results)==38","for r in results)==59"),("for r in results)==25","for r in results)==8"),("for r in results)==125","for r in results)==40"),("for r in results)==91","for r in results)==104"),("for r in results)==0\n    target_blocks","for r in results)==1\n    target_blocks"),('[142,143,144,145]','[152,153,154]'),('all38speech_and25_relative_operands_preserved','all59speech_and8_relative_operands_preserved'),('all125_relocated_native_skip_cases_match_original_target_mapping','all40_relocated_native_skip_cases_match_original_target_mapping'),('all332_other_SC2_blocks_exact','all333_other_SC2_blocks_exact'),('no_source2000_commands=True,source_FE_system_objects=1','no_source2000_commands=False,source_FE_system_objects=0'),("91commands/38speech/25spans/125targetskipcases,inversebytes and332otherblocks exact.","104commands/59speech/8spans/40targetskipcases,pause andfourendwords,inversebytes and333otherblocks exact.")]
    for a,b in pairs:assert a in text,a;text=text.replace(a,b)
    needle="        restored=bytearray(target[:len(logical)]);struct.pack_into('<H',restored,4,old_end-8)"
    addition="""        end_maps=[]
        for oldcmd in spec['all_current_native_commands']:
            if oldcmd['word']!=0:continue
            at=oldcmd['offset'];new=mapped(at)
            assert oldcmd['native_extent']==4 and source[at:at+4]==target[new:new+4]==bytes(4)
            end_maps.append(dict(source_offset=at,target_offset=new,extent=4,source_four_zero_bytes_exact=True))
        assert len(end_maps)==(2 if number==154 else 1)
        assert end_maps[-1]['source_offset']+4==old_end and end_maps[-1]['target_offset']+4==len(logical)
        if number==154:assert end_maps[0]['target_offset']+4==end_maps[1]['target_offset']
"""
    assert needle in text;text=text.replace(needle,addition+needle)
    needle='            text_records=texts,actor_style_commands=styles,choice_commands=choices,relative_skip_fixups=fixups,'
    assert needle in text;text=text.replace(needle,'            original_declared_end_word_maps=end_maps,\n'+needle)
    text=text.replace('        external_references_complete=False,not_a_release_relocation_map=True,','        four_declared_end_words_and_B154_two_word_suffix_exact=True,\n        external_references_complete=False,not_a_release_relocation_map=True,')
    TARGET.write_text(text,encoding='utf-8',newline='\n');proof=Path('work/analysis/lil_B152_B154_relocation_derivation_v3638');assert not proof.exists();proof.mkdir(parents=True);save(proof/'source_derivation.json',dict(source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),successor=str(TARGET),successor_sha256=sha(TARGET.read_bytes()),explicit_pause_and_two_end_word_source_ownership=True,no_executed_predecessor_modified=True))
