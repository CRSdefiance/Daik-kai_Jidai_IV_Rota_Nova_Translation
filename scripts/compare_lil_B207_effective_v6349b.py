"""Compare complete current runtime paragraphs only after the clean source gloss and source-view review."""
from pathlib import Path
import struct
from scripts.materialize_all_item_names_v1 import TABLE as ITEM_TABLE,c_string
from scripts.current_build_native_context_v6261b import BASE
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v6261b import CurrentContext
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B207_effective_v6349b')
SOURCE=Path('work/analysis/lil_B207_source_v6338/all13_clean_current_complete_context.json')
DISPATCH=Path('work/analysis/lil_B207_dispatches_v6342/all13_source_current_dispatches_two_actors_no_macros_and2_control_leaves.json')
VIEW=Path('work/analysis/lil_B207_source_view_v6348/all13_source_speeches_nameplates_and_town_return_viewed.json')
NAMES=Path('work/analysis/lil_B207_source_names_v6341/two_exact_source_name_fields_voices_and_distinct_name_consumers.json')
INPUT=Path('work/analysis/current_V6327_native_v6337/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();packet,dispatch,view,names=map(read,[SOURCE,DISPATCH,VIEW,NAMES]);assert packet['all13_clean_speech_glosses_before_predecessor_English_comparison'] and not view['visual_review_pending'] and view['actual_source_speeches']==13
    current=[c for c in dispatch['speech_dispatch_cases'] if c['version']=='current-English'];assert len(current)==13;rows=[]
    for r,c in zip(packet['records'],current,strict=True):
        assert r['id']==c['id'] and c['registered_catalog_match'] is None and c['source_voice_class'] in [3,6]
        boundary=next(b for b in c['boundaries'] if b['kind']=='unexecuted-progressive-body');raw=bytes.fromhex(boundary['text_hex']);assert raw==bytes.fromhex(r['current_hex'])[1:]
        text=raw.decode('cp932');rows.append(dict(id=r['id'],source_record_index=r['source_record_index'],source_reference=r['source_reference'],current_reference=r['current_reference'],source_hex=r['source_hex'],current_hex=r['current_hex'],fresh_source_gloss=r['fresh_source_gloss'],current_raw_storage_English=text,current_effective_runtime_template_hex=raw.hex(),current_effective_runtime_template_English=text,effective_predecessor_paragraph=' '.join(text.split()),registered_runtime_catalogue_match=None,original_current_dispatch_bound=True,isolated_native_UI_boundary_unexecuted=True,actual_source_speech_observed=True,no_English_display_or_prose_approval_yet=True))
    ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');clean=NdsImage.open('work/clean.nds');source_items=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'));terms=[]
    for n,entry in enumerate(source_items):
        if 'ミノタウロス' not in entry.text.decode('cp932',errors='replace'):continue
        target=ctx.entries[n];terms.append(dict(message_ID=n,source_Japanese=entry.text.decode('cp932'),source_hex=entry.text.hex(),source_reference=dict(block=entry.block,offset=entry.block_offset,bytes=len(entry.text)),current_English=target.text.decode('cp932'),current_hex=target.text.hex(),current_reference=dict(block=target.block,offset=target.block_offset,bytes=len(target.text))))
    # COMMON owns the item description;the218-row ARM9 table owns its title.
    field=ITEM_TABLE+41*24;title_fields=[]
    for label,code in [('clean',clean.read_file('/__arm9__.bin')),('current',ctx.arm)]:
        pointer=struct.unpack_from('<I',code,field)[0];value=c_string(code,pointer-BASE)
        title_fields.append(dict(version=label,pointer_field=field,pointer=pointer,file_offset=pointer-BASE,whole24byte_row_hex=code[field:field+24].hex(),terminated_hex=(value+b'\0').hex(),text=value.decode('cp932')))
    item=dict(item_ID=41,file_path='/__arm9__.bin',fields=title_fields,source_Japanese=title_fields[0]['text'],current_English=title_fields[1]['text'])
    assert item['source_Japanese']=='ミノタウロスの斧' and item['current_English']=='Minotaur Axe'
    assert len(terms)==1 and terms[0]['message_ID']==2856 and 'ミノタウロス' in terms[0]['source_Japanese'] and 'Minotaur' in terms[0]['current_English'] and not ctx.machines
    save(ROOT/'all13_effective_current_paragraphs_and_source_item_name.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),original_current_dispatch_proof=str(DISPATCH),original_current_dispatch_proof_sha256=sha(DISPATCH.read_bytes()),whole_source_review=str(VIEW),whole_source_review_sha256=sha(VIEW.read_bytes()),records=rows,item_name_binding=item,existing_source_current_Minotaur_descriptions=terms,existing_item_title_and_description_bound_without_new_item_credit=True,source_names=names['source_name_fields'],Emilio_given_name_and_Ferog_working_surname_preserve_clean_identity=True,existing_mixed_width_F_is_a_separate_native_encoding_metrics_lead=True,no_name_bytes_or_207_entry_global_approval=True,current_owned_COMMON_parser_bound_through_strict6261b=True,legacy_Refit_parser_guard_rejected_current_ARM9_not_weakened=True,current_native_context_plan=str(ctx.proof_path),current_native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),all13_current_dispatch_bodies_equal_raw_storage_no_catalogue_override=True,clean_gloss_and_complete_source_view_precede_this_comparison=True,prose_decisions_native_English_display_and_registered_release_pending=True,new_review_credit=0,new_ROMs=0,new_emulator_runs=0,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,DISPATCH,VIEW,NAMES,INPUT,Path(__file__)]},full_goal_complete=False))
    print('All13 runtime paragraphs equal stored bodies;no overrides. ARM9 item41:',item['source_Japanese'],'->',item['current_English'],';COMMON description2856 bound separately. No new item or prose credit.')
