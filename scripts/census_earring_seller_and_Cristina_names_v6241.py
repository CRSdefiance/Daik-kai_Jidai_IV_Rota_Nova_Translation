"""Trace source-bound seller labels and both current Cristina spellings without relabeling prior reviews."""
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/earring_seller_Cristina_names_v6241')
if __name__=='__main__':
    assert not ROOT.exists();v=read('work/analysis/editorial_handoff_verification_v6226/verified_handoff.json');assert sha(Path(v['candidate']).read_bytes())==v['candidate_sha256'];clean,current=[NdsImage.open(p) for p in ['work/clean.nds',v['candidate']]];arms=[im.read_file('/__arm9__.bin') for im in [clean,current]];inventory,walker,invsource=scoped_inventory();sig=bytes.fromhex('0040ffff00ad');jpname='クリスティナ'.encode('cp932');groups=[];summary=[];total=0;unmapped=[]
    for route in range(4):
        path=f'/data/SC{route}.DK4';files=[im.read_file(path) for im in [clean,current]];banks=[IlnkContainer.parse(b).blocks for b in files];assert len(banks[0])==len(banks[1]);total+=len(banks[0]);selected=[]
        for number,(a,b) in enumerate(zip(*banks,strict=True)):
            if sig not in a and jpname not in a and not any(s in b.lower() for s in [b'cristina',b'christina']):continue
            walks=[];speeches=[]
            for arm,blob in zip(arms,[a,b],strict=True):
                commands,spoken=inventory(arm,blob);records=[]
                for sp in spoken:
                    at=sp['offset']+5;raw=blob[at:blob.index(0,at+1)];records.append(dict(record_index=blob[:at].count(b'\0'),source_selector=raw[0],hex=raw.hex(),complete_preamble_hex=blob[at-5:at+1].hex(),text=raw[1:].decode('cp932'),reference=dict(file_path=path,block=number,header_offset=at-5,offset=at,bytes=len(raw))))
                walks.append(commands);speeches.append(records)
            source,current_rows=speeches;direct=[r for r in source if r['source_selector']==173];source_name=[r for r in source if 'クリスティナ' in r['text']];current_name=[r for r in current_rows if any(s in r['text'].casefold() for s in ['cristina','christina'])]
            if not direct and not source_name and not current_name:continue
            aligned=[c['word'] for c in walks[0]]==[c['word'] for c in walks[1]] and len(source)==len(current_rows)
            pairs=[]
            if aligned:
                for s,t in zip(source,current_rows,strict=True):
                    if s in direct or s in source_name or t in current_name:pairs.append(dict(source=s,current=t,exact_complete_source_current_preamble_equal=s['complete_preamble_hex']==t['complete_preamble_hex']))
            else:unmapped.append(dict(file_path=path,block=number,source_speeches=len(source),current_speeches=len(current_rows),source_words=[c['word'] for c in walks[0]],current_words=[c['word'] for c in walks[1]],no_guessed_source_current_text_pair=True))
            group=dict(route=route,file_path=path,block=number,clean_file_sha256=sha(files[0]),current_file_sha256=sha(files[1]),clean_block_sha256=sha(a),current_block_sha256=sha(b),all_clean_native_commands=walks[0],all_current_native_commands=walks[1],all_clean_speech_records=source,all_current_speech_records=current_rows,direct_seller173_source_records=direct,explicit_source_Cristina_records=source_name,current_Cristina_or_Christina_records=current_name,source_current_native_word_order_and_speech_count_equal=aligned,paired_relevant_records=pairs)
            groups.append(group);selected.append(dict(block=number,direct_seller_speeches=len(direct),complete_source_speeches=len(source),source_name_mentions=len(source_name),current_Cristina_mentions=sum('cristina' in r['text'].casefold() for r in current_name),current_Christina_mentions=sum('christina' in r['text'].casefold() for r in current_name)))
        summary.append(dict(route=route,file_path=path,source_blocks=len(banks[0]),selected_blocks=selected))
    assert total==1307;ROOT.mkdir(parents=True);save(ROOT/'four_route_seller_full_exchanges_and_explicit_Cristina_spelling_census.json',dict(clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),current_ROM=v['candidate'],current_ROM_sha256=v['candidate_sha256'],all_four_source_files_and1307_block_bytes_prefiltered=True,source_blocks_scanned=total,route_census=summary,selected_complete_native_exchanges=groups,unmapped_source_current_blocks=unmapped,source_full_preamble173_native_inventory_confirmation_not_raw_single_byte_hits=True,no_claim_to_exclude_dynamic_selector_typed_alias_COMMON_menu_artwork_or_other_name_consumers=True,proper_name_spelling_is_not_new_identity_or_nationality_evidence=True,nameplate7_is_current_Cristina_Erneco=True,source173_primary_is_ayashii_hito_secondary_Arab_Sailor_not_automatically_player_facing=True,complete_source_gloss_precedes_B206_current_prose_authoring=True,no_prior_review_flags_rewritten_and_no_automatic_global_substitution=True,all207_name_review_remains_open=True,clean_inventory_walker=walker,clean_inventory_function=invsource,no_ROM_registry_ledger_or_review_credit_change=True,new_emulator_runs=0,new_review_credit=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    for r in summary:print('route',r['route'],r['selected_blocks'])
    print(dict(direct_seller_speeches=sum(len(g['direct_seller173_source_records']) for g in groups),selected_complete_exchanges=len(groups),unmapped=len(unmapped),source_name_mentions=sum(len(g['explicit_source_Cristina_records']) for g in groups),current_Cristina=sum(sum('cristina' in r['text'].casefold() for r in g['current_Cristina_or_Christina_records']) for g in groups),current_Christina=sum(sum('christina' in r['text'].casefold() for r in g['current_Cristina_or_Christina_records']) for g in groups),new_credit=0))
