"""Derive complete B50 source/current/final and whole-image inverses plus loader/caller binding."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B50_references_production_tools_v8527');assert not root.exists()
    path=Path('dk4tool/patch/hodram_B49_references_v1.py');source=path.read_text(encoding='utf-8')
    a=source.index("    refs={r['id']:r for r in group['text_records']};choice=");b=source.index('    blocks=list(current);',a)
    refs="""    refs={r['id']:r for r in group['text_records']};rows=doc['records']
    require(len(refs)==len(rows)==len({r['id'] for r in rows})==3,'three disjoint canonical speech identities')
    for row in rows:
        ref=refs[row['id']];sr,cr,fr=row['source_reference'],row['current_reference'],row['final_reference']
        raw=bytes.fromhex(row['source_hex']);before=bytes.fromhex(row['current_hex']);value=bytes.fromhex(ref['target_hex'])
        for block,reference_,expected in [(japanese,sr,raw),(old,cr,before),(target,fr,value)]:
            at=reference_['offset'];require(reference_['block']==50 and reference_['bytes']==len(expected) and block[at:at+len(expected)+1]==expected+b'\\0' and block[:at].count(b'\\0')==reference_['record_index'],'complete source/current/final reference:'+row['id'])
        expected=dict(file_path=PATH,block=50,offset=ref['new_offset'],bytes=ref['new_length'],header_offset=ref['new_offset']-5,record_index=ref['new_record_index'],target_block_sha256=sha(target))
        require(fr==expected and row['final_hex']==row['stored_hex']==ref['target_hex'],'exact reviewed final reference/body/parity:'+row['id'])
"""
    tools=[derive(str(path),'dk4tool/patch/hodram_B50_references_v1.py',{
        'hodram_B49_reconstruction_v2':'hodram_B50_reconstruction_v1',
        'from dk4tool.dialogue.hodram_B49_choices_v2 import compile_choices\n':'',
        "source['operands_requiring_adjustment_when_resizing'],doc['typed_choice_records'],compile_choices(doc['typed_choice_records'])":"[]",
        "source['all_original_source_commands']":"source['groups'][0]['all_original_source_commands']",
        'len(group[\'command_map\'])==36 and len(cleantexts)==len(oldtexts)==len(texts)==14':"len(group['command_map'])==12 and len(cleantexts)==len(oldtexts)==len(texts)==3",
        'all36 commands and14 speech identities':'all12 commands and3 speech identities',
        "        elif c['word']==0x2100:require([a['whole_command_hex'],b['whole_command_hex'],c['whole_command_hex']]==[group['choice_commands'][0][k] for k in ['clean_hex','old_hex','target_hex']],'complete typed menu command')\n":'',
        "len(group['relative_fixups'])==8 and sum(len(r['cases']) for r in group['relocated_skip_cases'])==40":"not group['relative_fixups'] and not group['relocated_skip_cases']",
        'all eight native relative sites':'zero relative sites andno query ormenu',
        source[a:b]:refs,
        '==[49]':'==[50]','==49':'==50','[49]':'[50]',
        'editorial_references=16,speeches=14,typed_choices=2,commands=36,relative_sites=8':'editorial_references=3,speeches=3,typed_choices=0,commands=12,relative_sites=0',
        'B49':'B50',
    })]
    tools.append(derive('dk4tool/patch/hodram_B49_loaders_v1.py','dk4tool/patch/hodram_B50_loaders_v1.py',{
        "caller['block']==49":"caller['block']==50",
        "caller['all14_text_records']":"caller['all3_text_records']",
        "caller['typed_choice_records']==declared['choice_commands']":"caller['typed_choice_records']==[]",
        "a.get('native_selected_block')==49":"a.get('native_selected_block')==50",
        '[(49,49,[48])]':'[(50,50,[49])]',
        'event49 original prerequisite48':'event50 original prerequisite49',
        'all36 caller-selected source/current/final command maps and16record references':'all12 caller-selected source/current/final command maps and3record references',
        'B49':'B50',
    }))
    tools.append(derive('scripts/validate_Hodram_B49_references_v8443.py','scripts/validate_Hodram_B50_references_v8528.py',{
        'hodram_B49_references_v1':'hodram_B50_references_v1','hodram_B49_loaders_v1':'hodram_B50_loaders_v1',
        'validate_Hodram_B49_native_v8433':'validate_Hodram_B50_native_v8520',
        'Hodram_B49_independent_refs_v8443':'Hodram_B50_independent_refs_v8528',
        'work/analysis/Hodram_B49_relocation_v8398/reconstruction.json':'work/analysis/Hodram_B50_references_v8503/source_current_final_map.json',
        'work/analysis/Hodram_B49_choice_binding_v8387b/current_with_choices.json':'work/analysis/Hodram_B50_current_v8488/current_effective.json',
        'Hodram_B49_source_controls_v8384':'Hodram_B50_source_controls_v8486',
        'Hodram_B49_loaders_v8404':'Hodram_B50_loaders_v8503',
        'Hodram_B49_references_v8405b':'Hodram_B50_references_v8503',
        'translations/hodram_B49_editorial_manuscript_v4.json':'translations/hodram_B50_editorial_manuscript_v5.json',
        'Independent B49:16source/current/final references':'Independent B50:3source/current/final references',
        'complete B49':'complete B50',
    }))
    root.mkdir(parents=True);save(root/'derivations.json',dict(tools=tools,all_native_high_integer_constants_andmultiplicity_preserved=True,all_whole_clean_current_research_archive_andROM_inverse_guards_preserved=True,all325_payloads650_parent_modes326_actions_andsource_EV1_census_guards_preserved=True,canonical_source_plusfull_current_ROM_lifecycle_remains_required=True,no_emulator_replay_ROM_orcredit_change=True,new_credit=0,full_goal_complete=False))
