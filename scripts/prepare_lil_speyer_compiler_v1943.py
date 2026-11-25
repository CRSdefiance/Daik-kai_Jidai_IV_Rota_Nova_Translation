"""Generate an inspectable guarded Speyer compiler from the frozen typed compiler."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

SOURCE=Path('dk4tool/patch/lil_lessons_editorial.py')
SOURCE_SHA='a268bfae5ab46ae845e09d91b66c0817683fbfa98f2021451b77666b24b75e19'
OUT=Path('dk4tool/patch/lil_speyer_editorial.py')
ROOT=Path('work/analysis/lil_Speyer_compiler_v1943')

if __name__=='__main__':
    assert not OUT.exists() and not ROOT.exists() and sha(SOURCE.read_bytes())==SOURCE_SHA
    text=SOURCE.read_text(encoding='utf-8')
    changes={
        'Source/runtime-bound B120/B23 prose and typed-choice relocation layer.':'Source/runtime-bound B25/B128 Speyer prose and typed-choice relocation layer.',
        'from dataclasses import replace\n':'',
        'from dk4tool.dialogue.profiles import get_dialogue_profile':'from dk4tool.dialogue.lil_speyer_profile import profile_for',
        'translations/lil_lessons_editorial_release_v1.json':'translations/lil_speyer_editorial_release_v1.json',
        'Lil lessons ':'Lil Speyer ',
        'dk4-lil-lessons-editorial-release-v1':'dk4-lil-speyer-editorial-release-v1',
        'dk4-lil-lessons-source-relocation-map-v1':'dk4-lil-speyer-source-relocation-map-v1',
        'all124_nested_command_boundaries_and36_relative_sites_verified':'all137_nested_command_boundaries_and48_relative_sites_verified',
        'all180_relocated_relative_skip_cases_preserve_original_targets':'all240_relocated_relative_skip_cases_preserve_original_targets',
        'len(refs)==60':'len(refs)==57',
        'exhaustive60 speech coverage differs':'exhaustive57 speech coverage differs',
        "==4,'exhaustive four choice labels required'":"==2,'exhaustive two choice labels required'",
        '[23,120]':'[25,128]',
        "    profile=get_dialogue_profile(doc['dialogue_profile'])\n    fe_profile=replace(profile,name='lil-lessons-FE-runtime-bound-v1',leading_speaker_bytes=profile.leading_speaker_bytes|{254})\n":'',
        "number=spec['block'];block=container.blocks[number];original=jp.blocks[number]":
            "number=spec['block'];block=container.blocks[number];original=jp.blocks[number]\n        profile=profile_for(arm,block)",
        "fe_profile if raw[:1]==b'\\xfe' else profile":'profile',
        'len(changes)==64':'len(changes)==59',
        'only_SC2_blocks23_and120_changed':'only_SC2_blocks25_and128_changed',
        'all60_speeches_four_choices_and36_relative_operands_verified':'all57_speeches_two_choices_and48_relative_operands_verified',
    }
    for old,new in changes.items():
        expected=2 if old=='[23,120]'else 1
        assert text.count(old)==expected,(old,text.count(old))
        text=text.replace(old,new)
    anchor="    fonts={r['id']:r for r in load(doc['native_font_proof'])['cases']}"
    addition="""    actual=load(doc['actual_visual_review'])
    _require(actual.get('all51_activated_revised_speeches102_holds_complete_native_independent_actual_glyphs') is True
        and actual.get('both_revised_choice_labels_two_actual_holds_complete_native_ink_and_bounds') is True
        and actual.get('same107_original_B128_commands_results_and_event_transitions') is True
        and actual.get('normal_docking_Port_action_B128_entry_and_Hamburg_return_not_overridden') is True
        and actual.get('all_readonly_observer_boundaries_and_host_restoration_pass') is True,
        'complete representative actual proof required')
    _require(mapping.get('representative51_speech102_holds_and_two_choice_labels_approved') is True
        and mapping.get('target_SC2_sha256')==config['target_SC2_sha256'], 'approved actual/map target required')
"""
    assert text.count(anchor)==1
    text=text.replace(anchor,addition+anchor)
    anchor="            compiled=encode_relocatable_dialogue(raw,row['english'],profile)"
    addition="""            _require(row.get('native_display_consumer')=='original_progressive_54020'
                and (HEADER+raw[:1]).hex()==row['source_complete_preamble_hex'], 'complete original progressive preamble differs:'+ident)
            _require(all(raw.count(k.encode('ascii'))==row['english'].count('{MACRO:'+k+'}') for k in ('FI','FA','FO')),
                'source runtime substitution count differs:'+ident)
"""
    assert text.count(anchor)==1
    text=text.replace(anchor,addition+anchor)
    anchor="        boundaries={r['new_offset']for r in spec['mapped_native_commands']}|{len(logical)}"
    addition="""        mapped_commands=spec['mapped_native_commands']
        _require(len(mapped_commands)==(15 if number==25 else 122)
            and len({r['old_offset']for r in mapped_commands})==len(mapped_commands), 'complete typed command census required')
        for command in mapped_commands:
            old_at,new_at=command['old_offset'],command['new_offset']
            _require(new_at==_mapped(patches,old_at)
                and command['new_native_extent']==_mapped(patches,old_at+command['old_native_extent'])-new_at
                and struct.unpack_from('<H',block,old_at)[0]==command['word']
                and struct.unpack_from('<H',logical,new_at)[0]==command['word']
                and command['target_0100_ancestors']==[_mapped(patches,a)for a in command['source_0100_ancestors']],
                'complete mapped command/extent/ancestor differs')
            if command['word']==0x4000:
                _require(block[old_at:old_at+6]==logical[new_at:new_at+6], 'original complete speech preamble changed')
            elif command['word']not in(0x100,0x200,0x300,0x2100):
                _require(block[old_at:old_at+command['old_native_extent']]==logical[new_at:new_at+command['new_native_extent']],
                    'unowned opaque command changed')
        _require(len(spec['relative_skip_fixups'])==(8 if number==25 else 40), 'complete relative span census required')
"""
    assert text.count(anchor)==1
    text=text.replace(anchor,addition+anchor)
    compile(text,str(OUT),'exec')
    ROOT.mkdir(parents=True)
    OUT.write_text(text,encoding='utf-8')
    save(ROOT/'compiler_provenance.json',dict(source=str(SOURCE),source_sha256=SOURCE_SHA,
        compiler=str(OUT),compiler_sha256=sha(OUT.read_bytes()),exact_scope='SC2 B25/B128;57 speeches,two labels,48 relative spans',
        source_bound_private_profile_and_all137_command_mappings_checked=True,
        all_guards_before_sole_image_mutation=True,registered_config_not_yet_created=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(compiler=str(OUT),sha256=sha(OUT.read_bytes()),registered_config_pending=True))
