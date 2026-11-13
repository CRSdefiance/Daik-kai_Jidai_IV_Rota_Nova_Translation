"""Bind seven original predicates,six pictures,two resources and14 opaque effects."""
import inspect,struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts.prove_lil_B139_B140_conditionals_v3461c import probe
from scripts.prove_lil_B145_picture_controls_v3587 import picture
from scripts import prove_lil_B141_controls_v3538b as resource_base
from scripts.research_wedding_command_v676 import walk
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B196_controls_v5596')
SOURCE=Path('work/analysis/lil_B196_source_v5590/all36_clean_current_complete_context_with_twelve_choice_labels.json')
INPUT=Path('work/analysis/lil_B196_voices_v5591/current_native_input.json')

if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);g=packet['blocks'][0]
    images=[NdsImage.open(p) for p in ['work/clean.nds',packet['current_ROM']]]
    blocks=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[196] for im in images]
    commands=g['all_current_native_commands'];words=[0x6302,0x632E]
    assert sorted({c['word'] for c in commands if c['word']&0xFF00==0x6300})==words
    adapter=inspect.getsource(resource_base.control630A)
    changes=[('previous,boundary_return):','previous,boundary_return,word):'),
        ("value=bytes.fromhex('0a63')","assert word in SOURCE_RESOURCE_WORDS;value=struct.pack('<H',word)"),
        ('[0x02386EFC,10,2,1]','[0x02386EFC,word&255,2,1]')]
    for a,b in changes:assert a in adapter;adapter=adapter.replace(a,b)
    namespace={**resource_base.__dict__,'SOURCE_RESOURCE_WORDS':words};exec(compile(adapter,__file__+'::source-two-resource-boundaries','exec'),namespace)
    ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,packet['historical_snapshot_ROM'],ROOT/'current_context')
    predicates=[];pictures=[];effects=[];resources=[]
    for c in commands:
        if c['word']==0x8000:
            result=ctx.execute(probe,blocks[1],c);ctx.machines.pop()
            assert not result['original_event_completion_calls']
            predicates.append(dict(block=196,**result))
        elif c['word']==0x4821:
            versions=[]
            for version,block in zip(['clean','current'],blocks,strict=True):
                versions.append(dict(version=version,**ctx.execute(picture,block,c)));ctx.machines.pop()
            assert versions[0]['original_picture_boundary_calls']==versions[1]['original_picture_boundary_calls']
            pictures.append(dict(block=196,source_offset=c['offset'],source_hex=c['whole_command_hex'],cases=versions))
        elif c['word']==0xA000:
            raw=bytes.fromhex(c['whole_command_hex']);isolated=b'CS\0\1'+struct.pack('<H',len(raw))+bytes(2)+raw;versions=[]
            for version,image in zip(['clean','current'],images,strict=True):
                result=walk(image.read_file('/__arm9__.bin'),isolated)
                assert result['error'] is None and result['stopped_offset']==result['logical_end']==len(isolated)
                assert len(result['rows'])==1 and result['rows'][0]['word']==0xA000 and result['rows'][0]['native_extent']==8
                versions.append(dict(version=version,**result))
            assert versions[0]['rows']==versions[1]['rows'] and versions[0]['opaque_effect_bridges']==versions[1]['opaque_effect_bridges']
            effects.append(dict(block=196,source_offset=c['offset'],source_hex=c['whole_command_hex'],versions=versions,
                packed_effect_body_bridged_not_actual_funds_item_or_stat_execution=True))
    for word in words:
        for previous in [0,1,2,3,0xFFFFFFFF]:
            for result in [0,0xFFFFFFFF]:
                resources.append(ctx.execute(namespace['control630A'],previous,result,word));ctx.machines.pop()
    assert len(predicates)==7 and len(pictures)==6 and len(effects)==14 and len(resources)==20 and not ctx.machines
    assert all(p['cases'][0]['original_picture_boundary_calls'][0]['descriptor']==[0,113,1,5] for p in pictures)
    leaves=[dict(offset=c['offset'],word=c['word'],extent=c['native_extent'],hex=c['whole_command_hex']) for c in commands
        if c['word'] not in [0x4000,0x100,0x200,0x300,0x400,0x2100,0x8000]]
    assert len(leaves)==30 and sum(c['word']==0 for c in leaves)==7
    remaining=[c for c in leaves if c['word']==0x6003];assert len(remaining)==1
    save(ROOT/'seven_unforced_predicates_six_picture_pairs_twenty_resource_cases_fourteen_opaque_effect_pairs.json',dict(
        candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        source_predicate_cases=predicates,source_picture_pairs=pictures,source630x_resource_words=words,source630x_boundary_cases=resources,
        source_A000_structural_pairs=effects,all30_nonrelative_nonspeech_nonchoice_nonpredicate_leaves_exact=leaves,
        source_picture_descriptors=[[0,113,1,5]],picture_descriptor_not_assumed_to_be_item113_or_its_display_name=True,
        source6003_exact_but_its_native_request_ownership_and_meaning_pending=remaining,
        source_declared_end_offsets=[c['offset'] for c in commands if c['word']==0],
        source_owned_adapters=dict(predicate=inspect.getsource(probe),picture=inspect.getsource(picture),resource=adapter),
        all7_predicates_unforced_original_numeric_results_preserved=True,
        original_no_source_C200_pause_typed_actor_style_or_dynamic_speaker_object=True,
        source_A000_packed_effect_semantics_funds_debits_inventory_and_FI_stat_effect_unbound=True,
        resource_picture_and_effect_bodies_unexecuted=True,source6003_and_guarded_seven_end_VM_contracts_pending=True,
        source_relative_sites52_native_checks_separate=True,actual_scene_eligibility_choices_outcomes_and_gameplay_unexecuted=True,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        source_control_scalar_interpretations_not_inferred_from_prices_or_item_prose=True,
        new_emulator_runs=0,new_review_credit=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('B196 seven unforced predicates,six source/current picture pairs,20 resource boundary cases and14 opaque effect pairs pass.6003/seven end VM/funds-item-stat semantics remain pending;no gameplay or credit.')
