"""Read complete clean dye/map callback; bind earlier clean opening title distinctions and refine B50 glosses before English."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.prove_papal_trade_entries_v7628 import parse_events
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B50_context_v8135')
GLOSS=Path('work/analysis/Rafael_B50_clean_gloss_v8131/28_first_clean_glosses_three_source_identities_before_current_English.json')
MACROS=Path('work/analysis/Rafael_B50_macros_names_v8133/three_clean_FA_FI_paragraphs12_fresh_alignments_six_exact_reused_name_getters.json')
ITEM=Path('work/analysis/Rafael_B50_pigment_v8134/original4821_descriptor181_clean_current_Red_Dye_andbounded_consumer_path.json')
VERIFIED=Path('work/analysis/editorial_handoff_verification_v8128/verified_handoff.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
CALLBACK={
 5:'Lil thinks the Old Parchment may be the map to a Proof of Conquest; this begins as her hypothesis.',
 15:'Camille says it looks like ordinary paper but supposes that some trick is hidden in it.',
 20:'Fernando says nothing is written on it and suspects some hidden mechanism.',
 26:'Lil wonders whether the named Red Dye could help.',
 30:'Lil has no other idea and becomes emphatically certain that this must be what to use. Preserve her assertiveness as characterization, not an independent mechanic guarantee before the result.',
 42:'Fernando asks how she intends to use it.',
 57:'Camille stammers Lil\'s FI name token and asks what she is doing.',
 64:'Lil explains that she will pour or apply it over the paper like this.',
 76:'Fernando notices something appearing on the paper.',
 82:'Lil triumphantly says her guess was right and that they now have the North Sea Proof of Conquest map.',
 92:'Camille praises FI and proposes going to look for the Proof immediately.',
 98:'Fernando praises her observation and also urges setting out to find the Proof.',
 105:'Lil declares her ambition that the North Sea will now be hers; this does not give Rafael those events or certify B50 scheduler state.',
}
REFINED={
 23:'Lil rejects Rafael\'s bland response and hands over the key to deciphering the map that records the treasure location. The adjacent original4821 descriptor181 and clean metadata紅色の顔料/currentRedDye bind the pigment identity; the complete clean Lil B131 callback shows dye revealing a map on parchment. Do not imply that this is a new map or treasure, or that Rafael already owns that parchment or has enacted the Lil-route callback.',
 40:'Camille politely greets Rafael and checks whether he is Mr. FA, whose current default is the surname Castor. Preserve FA as a runtime substitution; do not replace it with the FI given-name token.',
 57:'Lil answers with affected casual innocence: she only gave him that dye because she will no longer need it. The Red Dye identity is now source/native-bound; the source still does not explain the life-event occasion or name a new occupation.',
 61:'Camille realizes that FA (default Castor), addressed respectfully as a company/force leader, is now the dominant power in the North Sea and accepts the handover. The earlier complete clean opening explicitly distinguishes captain of the ship,admiral of the fleet,and leader of the company;総帥 is the last role,not a new military rank. Preserve present regional dominance and natural respectful address without literal Leader Castor or an invented promotion.',
 108:'Camille politely dismisses concern about the congratulatory gesture,calls Lil to leave,and bids FI (default Rafael) well with deferential company-leader address. FI is distinct from earlier FA. Natural American direct address may convey this deference through polite phrasing rather than inventing Director,General or another unsupported rank;the company/regional leadership context must remain clear.',
}
if __name__=='__main__':
    assert not ROOT.exists();first,macros,item,verified,ledger=map(read,[GLOSS,MACROS,ITEM,VERIFIED,LEDGER])
    assert sha(LEDGER.read_bytes())==verified['ledger_sha256'] and verified['completed']==7143
    assert first['source_only_no_current_B50_English_exposed_no_localized_manuscript'] and macros['current_B50_English_dialogue_body_still_unread']
    image=NdsImage.open('work/clean.nds');arm=image.read_file('/__arm9__.bin');block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[131]
    inventory,walker,inventory_source=scoped_inventory();commands,speeches=inventory(arm,block);assert len(commands)==49 and len(speeches)==len(CALLBACK)==13
    rows=[]
    completed={(r.get('file_path',f.get('file_path')),r['id']):r for f in ledger['completed_editorial_families'] for r in f['records']}
    for s in speeches:
        at=s['offset']+5;raw=block[at:block.index(0,at+1)];index=block[:at].count(b'\0');ident=f'DK4_MES_B131_R{index:04d}'
        old=completed['/data/SC2.DK4',ident];assert raw.hex()==old['source_hex'] and raw[1:].decode('cp932')==old['source_Japanese']
        rows.append(dict(id=ident,file_path='/data/SC2.DK4',block=131,source_record_index=index,source_reference=dict(block=131,offset=at,bytes=len(raw),record_index=index,header_offset=at-5),source_hex=raw.hex(),source_complete_preamble_hex=block[at-5:at+1].hex(),source_Japanese=raw[1:].decode('cp932'),source_gloss=CALLBACK[index],previous_completed_source_record_reused=True,new_editorial_credit=0))
    opening=IlnkContainer.parse(image.read_file('/data/SC0.DK4')).blocks[44]
    family=next(f for f in ledger['completed_editorial_families'] if f.get('file_path')=='/data/SC0.DK4' and len(f['records'])==117 and all(r['block']==44 for r in f['records']))
    titles=[]
    for r in family['records']:
        at=r['source_reference']['offset'];raw=bytes.fromhex(r['source_hex']);assert opening[at:at+len(raw)+1]==raw+b'\0'
        if r['source_record_index'] in [316,321,327,330,337]:
            titles.append(dict(id=r['id'],source_reference=r['source_reference'],source_hex=r['source_hex'],source_Japanese=r['source_Japanese'],prior_completed_English=r['logical_English'] if 'logical_English' in r else r['english'],prior_complete_exchange_reused_no_new_credit=True))
    assert len(titles)==5 and any('艦長' in r['source_Japanese'] and '提督' in r['source_Japanese'] and '総帥' in r['source_Japanese'] for r in titles)
    records=deepcopy(first['records'])
    for r in records:r['refined_source_gloss']=REFINED.get(r['source_record_index'],r['first_clean_source_gloss'])
    ROOT.mkdir(parents=True);save(ROOT/'complete13_clean_Lil_B131_dye_map_context_andfive_B44_title_refs.json',dict(
        clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),clean_ARM9_sha256=sha(arm),
        callback_file='/data/SC2.DK4',callback_block=131,callback_block_sha256=sha(block),all49_callback_commands=commands,callback_records=rows,
        callback_source_events=[e for e in parse_events(image.read_file('/data/EV2.DK4')) if e['script_block']==131],
        all13_clean_callback_speeches_read_andglossed=True,callback_proves_Lil_dye_onparchment_map_reveal_not_Rafael_progress_orpossession=True,
        prior_Rafael_opening_family_ID=family['id'],prior_complete117_source_record_refs_rechecked_without_repeating_translation=True,
        five_clean_title_references=titles,ship_captain_fleet_admiral_andcompany_leader_are_distinct_source_roles=True,
        source_B50_title_is_company_orforce_head_not_license_for_new_military_rank=True,
        no_new_B131_orB44_credit_orprose_change=True,source_owned_inventory_walker=walker,source_owned_inventory_function=inventory_source))
    cp=ROOT/'complete13_clean_Lil_B131_dye_map_context_andfive_B44_title_refs.json'
    save(ROOT/'28_refined_glosses_dye_identity_FA_FI_title_context_before_current_B50_English.json',dict(
        first_source_gloss=str(GLOSS),first_source_gloss_sha256=sha(GLOSS.read_bytes()),context=str(cp),context_sha256=sha(cp.read_bytes()),
        source_macro_proof=str(MACROS),source_macro_proof_sha256=sha(MACROS.read_bytes()),item_proof=str(ITEM),item_proof_sha256=sha(ITEM.read_bytes()),
        records=records,complete_B50_exchange_reviewed_including_internal_thoughts_selfcorrection_andunresolved_occasion=True,
        all28_current_B50_English_bodies_still_unread=True,known_B49_names_andexisting_item_title_usage_previously_exposed_not_new_B50_prose=True,
        preserve_FA2_FI1_Camille_name_andall_original37commands=True,
        no_marriage_romance_pregnancy_retirement_political_rank_ornewbiography_invented=True,
        fullresource_effects_natural_event50_scheduler_original_location_andcurrent_comparison_pending=True,
        new_credit=0,new_emulator_runs=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [GLOSS,MACROS,ITEM,VERIFIED,Path(__file__)]}))
    print('B50 contextual source:all28glosses refined,complete13-speech clean dye/map callback read,117prior opening refs bound/five distinct-title refs. Current B50English bodies unread;zero credit.')
