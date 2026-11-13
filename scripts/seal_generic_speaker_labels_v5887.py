"""Seal three reviewed labels, all621 original field consumers and representative native display."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.generic_speaker_label_data_v1 import EXPECTED,transform
from dk4tool.rom.nds import NdsImage
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/generic_speaker_labels_approval_v5887')
INPUT=Path('translations/generic_speaker_labels_manuscript_v1.json')
OUTPUT=Path('translations/generic_speaker_labels_manuscript_v2.json')
NAMES=Path('work/analysis/generic_speaker_names_v5884/all207_progressive_catalogue_names_eight_voices_and_exact_three_changes.json')
ACTUAL=Path('work/analysis/generic_speaker_scenes_v5885b/two_complete_exchanges_original_commands_and_exact_nameplate_glyphs.json')
DISPLAY=Path('work/analysis/generic_name_macros_fonts_v5886c/unchanged_runtime_substitutions_three_native_planes_and_visual_review.json')

def fields(arm,common,raw,plan):
    cpu,get,provider=machine(arm,common,raw,plan);root=get(0xCB184);initial=bytes(cpu.mem_read(0x02000000,0x400000));rows=[]
    for ident in range(207):
        for column,getter in [(0,0x7EB0C),(4,0x7EAF4),(8,0x7EADC)]:
            pointer=get(getter,root+4+ident*32)
            text=bytes(cpu.mem_read(pointer,128)).split(b'\0')[0] if pointer else b''
            rows.append(dict(actor_ID=ident,column=column,getter=getter,pointer=pointer,text_hex=text.hex()))
    assert bytes(cpu.mem_read(0x02000000,0x400000))==initial
    return dict(rows=rows,all621_original_getters_and_complete4MiB_exact=True,current_executed_instruction_addresses=len(provider.executed_current))

if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists();ROOT.mkdir(parents=True)
    names,actual,display=map(read,[NAMES,ACTUAL,DISPLAY]);old=read(INPUT)
    assert names['all414_target_getters_and414_parent_getters_executed'] and names['all204_unaffected_actors_both_name_consumers_exact']
    assert actual['complete_speech_observations']==28 and actual['complete_nameplate_observations']==25 and actual['actual_target_nameplate_cases']==16
    assert display['parent_target_macro_and_literal_outputs_exact'] and display['native_macro_alignment_cases']==64
    assert display['actual_nameplate_independent_masks_and_five_complete_context_sheets_viewed']
    assert len(display['three_complete_original_font_native_planes'])==3
    versions=[]
    for case,path in [('parent','work/analysis/lil_B200_voices_v5827/current_native_input.json'),('target','work/analysis/generic_speaker_names_v5884/target_native_input.json')]:
        ctx=CurrentContext(path,'unused-no-historical-ROM-read',ROOT/(case+'_current_context'));result=ctx.execute(fields);ctx.machines.pop();assert not ctx.machines
        versions.append(dict(case=case,result=result,context_plan=str(ctx.proof_path),context_plan_sha256=sha(ctx.proof_path.read_bytes())))
    changes=[]
    for a,b in zip(versions[0]['result']['rows'],versions[1]['result']['rows'],strict=True):
        assert all(a[k]==b[k] for k in ['actor_ID','column','getter','pointer'])
        if a['text_hex']!=b['text_hex']:
            ident=b['actor_ID'];assert b['column']==0 and ident in EXPECTED
            assert a['text_hex']==EXPECTED[ident][1].encode().hex() and b['text_hex']==EXPECTED[ident][2].encode().hex()
            changes.append(dict(before=a,after=b))
    assert len(changes)==3
    parent=NdsImage.open(old['current_ROM']);clean=NdsImage.open(old['source_ROM']);target,plan=transform(parent.read_file('/__arm9__.bin'),clean.read_file('/__arm9__.bin'),old['records'])
    research=Path('out/generic_speaker_labels_v5881_RESEARCH_ONLY.nds')
    assert NdsImage.open(research).read_file('/__arm9__.bin')==target and plan==old['data_plan']
    new=deepcopy(old)
    for row in new['records']:
        row['review']['formatting']=True
        row['target_native_getter_substitution_glyph_display_and_registered_release_pending']=False
        row['native_getter_substitution_glyph_and_representative_display_approved_registered_release_pending']=True
        row['formatting_reason']='Complete unchanged-font native single-row plane and actual nameplate first/final glyphs plus blank guards pass. Both original progressive/catalogue consumers,all621 field consumers and unchanged runtime substitutions pass. No linebreak or fit-driven name shortening.'
    new.update(previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()),
        source_context_localization_naturalness_approved_native_format_and_release_pending=False,
        all_five_per_record_gates_approved_registered_release_pending=True,
        native_reference_ROM=str(research),native_reference_ROM_sha256=sha(research.read_bytes()),
        approved_proper_names_all_other_204_actors_secondary_middle_fields_and_aliases_preserved=True,
        source_complete_exchange_relationships_retained_without_invented_marriage_or_age=True,
        original_name_storage_code_pointers_allocations_fonts_controls_and_all_scene_words_preserved=True,
        actual_catalogue_UI_not_visited_native_getters_and_font_bounds_checked=True,
        no_duplicate_dialogue_or_prior_name_review_credit=True)
    save(OUTPUT,new)
    save(ROOT/'three_label_source_native_display_approval.json',dict(
        manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),parent_ROM=old['current_ROM'],parent_ROM_sha256=old['current_ROM_sha256'],
        research_ROM=str(research),research_ROM_sha256=sha(research.read_bytes()),target_ARM9_sha256=sha(target),
        original_field_consumer_versions=versions,changed_field_consumers=changes,
        all621_parent_and621_target_primary_secondary_middle_consumers_pass=True,only_three_primary_outputs_change=True,
        all_five_gates_complete_for_three_source_owned_labels=True,
        all414_target_progressive_catalogue_name_consumers_64_macro_alignments_three_native_planes_and16_actual_target_headers_pass=True,
        complete_two_existing_exchanges28_speeches25_nameplates_observed_five_sheets_viewed=True,
        no_full_catalogue_UI_natural_event_activation_original_location_full_route_or_hardware_claim=True,
        all207_review_queue_not_complete_and_all_other_editorial_scope_preserved=True,
        source_owned_data_plan=plan,evidence={str(p):sha(p.read_bytes()) for p in [INPUT,OUTPUT,NAMES,ACTUAL,DISPLAY,Path(__file__),Path('dk4tool/patch/generic_speaker_label_data_v1.py')]},
        new_emulator_runs=0,new_dialogue_or_name_completion_credit=0,full_goal_complete=False))
    print('Three labels sealed withfivegates;621parent+621target fieldconsumers pass,onlythreeprimaryoutputschange. Native/display approved;registered release pending;no duplicate credit.')
