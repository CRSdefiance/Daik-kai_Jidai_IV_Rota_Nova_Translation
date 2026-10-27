"""Refresh14 untouched source/current speeches against the independently verified V3526."""
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B141_source_v3532b')
LEAD=Path('work/analysis/B141_SC3_B109_next_source_v3495/all40_clean_current_source_and_packed_control_leads.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v3531b/verified_handoff.json')
HISTORY=Path('work/analysis/lil_remaining_B139_B140_source_v3456/next67_B139_B140_clean_current_context.json')
if __name__=='__main__':
    assert not ROOT.exists();prior,lead,history=map(read,[PRIOR,LEAD,HISTORY]);lp=Path('translations/editorial_review_current_v1.json');assert sha(lp.read_bytes())==prior['ledger_sha256'];ledger=read(lp)
    image,clean=NdsImage.open(prior['candidate']),NdsImage.open('work/clean.nds');assert sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256'];path='/data/SC2.DK4';jp,en=[IlnkContainer.parse(im.read_file(path)).blocks[141] for im in [clean,image]]
    group=deepcopy(next(b for b in lead['blocks'] if b['file_path']==path));assert sha(jp)==group['source_block_sha256'] and sha(en)==group['current_block_sha256']
    inventory,walker,inventory_source=scoped_inventory();walks=[inventory(im.read_file('/__arm9__.bin'),b)[0] for im,b in [(clean,jp),(image,en)]];shape=lambda w:[(c['offset'],c['word'],c['native_extent'],c['ancestor_0100_offsets']) for c in w]
    assert shape(walks[0])==shape(walks[1]) and len(walks[0])==37
    for a,b in zip(*walks,strict=True):
        if a['word'] in [0x100,0x200,0x300,0x400]:
            assert jp[a['offset']:a['offset']+4]==en[b['offset']:b['offset']+4]
        elif a['word']!=0x4000:assert a['whole_command_hex']==b['whole_command_hex']
    known={historical_key(r) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['record_keys']};rows=group['records'];assert len(rows)==14 and not known&{historical_key(r) for r in rows}
    for i,r in enumerate(rows):
        for data,ref,field in [(jp,r['source_reference'],'source_hex'),(en,r['current_reference'],'current_hex')]:
            at=ref['offset'];v=bytes.fromhex(r[field]);assert data[at:at+len(v)]==v and data[at+len(v)]==0 and data[ref['header_offset']:ref['header_offset']+6].hex()==r['source_complete_preamble_hex']
        r.update(kind='progressive',source_presentation_prefix_hex=format(r['source_selector'],'02x'),native_command_extent=r['source_native_extent'],spoken_sequence_index=i,current_macro_dispatch_consumer_and_complete_native_display_pending=True,source_prose_or_completion_credit_added=0)
    assert image.read_file('/data/EV2.DK4')==clean.read_file('/data/EV2.DK4')
    group.update(clean_block_sha256=sha(jp),all_clean_native_commands=walks[0],all_current_native_commands=walks[1],source_current_native_command_shape_exact=True)
    assert sha(Path(history['actual_historical_snapshot']).read_bytes())==history['actual_historical_snapshot_sha256']
    ROOT.mkdir(parents=True);(ROOT/'complete_clean_exchange.txt').write_text('\n\n'.join(r['id']+'\n'+r['source_Japanese'] for r in rows),encoding='utf-8');(ROOT/'explicit_unmatched_native_walk.txt').write_text(walker,encoding='utf-8');(ROOT/'scoped_inventory_source.txt').write_text(inventory_source,encoding='utf-8')
    save(ROOT/'all14_clean_current_complete_context.json',dict(format='dk4-editorial-source-context-packet-v1',file_path=path,source_ROM='work/clean.nds',source_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),current_ROM=prior['candidate'],current_ROM_sha256=prior['candidate_sha256'],current_ARM9_sha256=sha(image.read_file('/__arm9__.bin')),source_SC2_sha256=sha(clean.read_file(path)),current_SC2_sha256=sha(image.read_file(path)),original_EV2_sha256=sha(image.read_file('/data/EV2.DK4')),actual_historical_snapshot=history['actual_historical_snapshot'],actual_historical_snapshot_sha256=history['actual_historical_snapshot_sha256'],historical_snapshot_ROM=history['historical_snapshot_ROM'],historical_snapshot_is_Lil_London_not_selected_B141=True,blocks=[group],records=rows,typed_choice_records=[],typed_actor_style_records=[],source_macro_counts=group['source_macro_counts'],total_editorial_objects=14,speech_objects=14,ordinary_source_speeches=14,system_FE_panels=0,source_selectors=[2,9,20,171],source_native_commands=37,all23_non_speech_owned_headers_and_leaf_controls_exact_current=True,unreviewed_exact_B142_copy_navigation_leads=[c for c in lead['nontrivial_raw_exact_copy_candidates'] if c['file_path']==path],native_voices_FI_money_predicates630A_effect_entry_and_branches_pending=True,current_native_full_gloss_and_oldEnglish_comparison_pending=True,source_prose_credit_added=0,completion_credit_added=0,new_emulator_runs=0,evidence={str(p):sha(p.read_bytes()) for p in [LEAD,PRIOR,HISTORY,Path(__file__)]},producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('B14114 source/current speeches,37 commands,13 exact relative headers and10 exact leaf controls refreshed on V3526;FI1 and monetary controls pending;no review credit.')
