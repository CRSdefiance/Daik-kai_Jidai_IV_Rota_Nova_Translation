"""Compare native current bodies after whole-source review; distinguish generic mention from item title."""
from pathlib import Path
import struct
from scripts.materialize_all_item_names_v1 import TABLE as ITEM_TABLE,c_string
from scripts.current_build_native_context_v6261b import CurrentContext,BASE
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B208_effective_v6401');SOURCE=Path('work/analysis/lil_B208_source_v6390/all24_clean_current_complete_context.json')
DISPATCH=Path('work/analysis/lil_B208_dispatches_v6394/all24_source_current_dispatches_two_actors_one_FE_no_macros_and5_control_leaves.json');VIEW=Path('work/analysis/lil_B208_source_view_v6400/all24_source_panels_names_thought_FE_notice_and_return_viewed.json')
NAMES=Path('work/analysis/lil_B208_source_names_v6393/two_exact_source_name_fields_voices_and_distinct_name_consumers.json');INPUT=Path('work/analysis/current_V6380_native_v6389/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();packet,dispatch,view,names=map(read,[SOURCE,DISPATCH,VIEW,NAMES]);assert packet['all24_clean_panel_glosses_before_predecessor_English_comparison'] and not view['visual_review_pending'] and view['actual_source_speeches']==24
    cases=[r for r in dispatch['speech_dispatch_cases'] if r['version']=='current-English'];assert len(cases)==24;rows=[]
    for r,c in zip(packet['records'],cases,strict=True):
        fe=r['source_selector']==254;assert r['id']==c['id'] and c['registered_catalog_match'] is None and c['source_voice_class']==(None if fe else {7:3,170:0}[r['source_selector']])
        boundary=next(b for b in c['boundaries'] if b['kind']==('unexecuted-FE-modal-body' if fe else 'unexecuted-progressive-body'));raw=bytes.fromhex(boundary['text_hex']);assert raw==bytes.fromhex(r['current_hex'])[1:]
        assert c['resolved_actor_ID']==(None if fe else r['source_selector']) and bool(c['FE_original_null_actor_calls'])==fe
        text=raw.decode('cp932');rows.append(dict(id=r['id'],source_record_index=r['source_record_index'],kind=r['kind'],source_reference=r['source_reference'],current_reference=r['current_reference'],source_hex=r['source_hex'],current_hex=r['current_hex'],fresh_source_gloss=r['fresh_source_gloss'],current_raw_storage_English=text,current_effective_runtime_template_hex=raw.hex(),current_effective_runtime_template_English=text,effective_predecessor_paragraph=' '.join(text.split()),registered_runtime_catalogue_match=None,original_current_dispatch_bound=True,isolated_native_UI_boundary_unexecuted=True,actual_source_panel_observed=True,no_English_display_or_prose_approval_yet=True))
    ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');clean=NdsImage.open('work/clean.nds');arm=clean.read_file('/__arm9__.bin');fields=[]
    for label,code in [('clean',arm),('current',ctx.arm)]:
        at=ITEM_TABLE+40*24;pointer=struct.unpack_from('<I',code,at)[0];value=c_string(code,pointer-BASE);fields.append(dict(version=label,pointer_field=at,pointer=pointer,file_offset=pointer-BASE,whole24byte_row_hex=code[at:at+24].hex(),terminated_hex=(value+b'\0').hex(),text=value.decode('cp932')))
    assert [r['text'] for r in fields]==['紅毛の女海賊の宝剣','Red-Haired Pirate Sword']
    attribute=[]
    for label,code in [('clean',arm),('current',ctx.arm)]:
        value=code[0x1482DC:0x1482E4];attribute.append(dict(version=label,file_path='/__arm9__.bin',offset=0x1482DC,bytes=8,whole_slot_hex=value.hex(),text=value.split(b'\0')[0].decode('cp932')))
    assert [r['text'] for r in attribute]==['魅力','Charm']
    entries=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),arm);terms=[]
    for i,e in enumerate(entries):
        if '女海賊' not in e.text.decode('cp932',errors='replace'):continue
        t=ctx.entries[i];terms.append(dict(message_ID=i,source_Japanese=e.text.decode('cp932'),source_hex=e.text.hex(),source_reference=dict(block=e.block,offset=e.block_offset,bytes=len(e.text)),current_English=t.text.decode('cp932'),current_hex=t.text.hex(),current_reference=dict(block=t.block,offset=t.block_offset,bytes=len(t.text))))
    assert not ctx.machines
    save(ROOT/'all24_effective_current_paragraphs_related_item40_and_exact_Charm_UI_label.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),original_current_dispatch_proof=str(DISPATCH),original_current_dispatch_proof_sha256=sha(DISPATCH.read_bytes()),whole_source_review=str(VIEW),whole_source_review_sha256=sha(VIEW.read_bytes()),records=rows,related_item40_title_fields=fields,source_scene_uses_generic_female_pirate_sword_not_red_hair_epithet=True,do_not_add_item_title_red_hair_to_source_speeches_or_identify_historical_pirate=True,exact_Charm_attribute_label_fields=attribute,early_gloss_Charisma_pending_metadata_superseded_by_actual_Charm_slot=True,related_source_current_item_descriptions=terms,existing_item_and_attribute_consumers_bound_without_new_item_or_UI_credit=True,source_names=names['source_name_fields'],two_contextual_name_retention_reasons=str(VIEW),source_170_unused_nationality_field_not_name_or_biography=True,no_name_asset_or_207_entry_global_approval=True,all24_current_dispatch_bodies_equal_raw_storage_no_catalogue_override=True,one_FE_null_actor_and_private_thought_consumer_scope_preserved=True,current_owned_COMMON_parser_bound_through_strict6261b=True,current_native_context_plan=str(ctx.proof_path),current_native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),clean_gloss_and_complete_source_view_precede_this_comparison=True,prose_decisions_native_English_display_and_registered_release_pending=True,new_review_credit=0,new_ROMs=0,new_emulator_runs=0,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,DISPATCH,VIEW,NAMES,INPUT,Path(__file__)]},full_goal_complete=False))
    for r in rows:print(r['source_record_index'],r['effective_predecessor_paragraph'])
    print('Related item40 title and actual Charm UI slot bound. Source speech has no red-hair epithet. All24 bodies equal raw storage;no new credit.')
