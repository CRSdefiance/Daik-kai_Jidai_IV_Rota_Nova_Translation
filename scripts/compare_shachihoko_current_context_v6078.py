"""Consult older English only after the four complete clean exchanges were glossed."""
import re
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/shachihoko_current_context_v6078')
SOURCE=Path('work/analysis/shachihoko_source_context_v6075/four_complete_clean_exchanges_and_two_nonitem_sobriquet_contexts.json')
if __name__=='__main__':
    assert not ROOT.exists();context=read(SOURCE);assert context['no_older_English_story_comparison_or_ROM_mutation']
    candidate=Path('out/all_routes_combined_v6050_candidate.nds');rom=NdsImage.open(candidate);assert sha(candidate.read_bytes())=='2472f0c5203ca2b9692a8b4ce2ab64c0049febe598fc61fecc071adda0d3af43'
    arm=rom.read_file('/__arm9__.bin');inventory,walker,invsource=scoped_inventory();groups=[]
    for b in context['complete_four_source_exchanges']:
        blob=IlnkContainer.parse(rom.read_file(b['file_path'])).blocks[b['block']];commands,speeches=inventory(arm,blob);assert len(speeches)==len(b['records'])==20;rows=[]
        for source,speech in zip(b['records'],speeches,strict=True):
            at=speech['offset']+5;end=blob.index(0,at+1);raw=blob[at:end];assert raw[0]==source['source_selector'] and blob[at-5:at+1].hex()==source['complete_preamble_hex']
            rows.append(dict(**source,current_reference=dict(file_path=b['file_path'],block=b['block'],offset=at,bytes=len(raw),header_offset=at-5,record_index=blob[:at].count(b'\0')),current_native_extent=speech['native_extent'],current_hex=raw.hex(),older_English=raw[1:].decode('cp932')))
        groups.append(dict(file_path=b['file_path'],block=b['block'],source_block_sha256=b['source_block_sha256'],current_block_sha256=sha(blob),records=rows,all_current_native_commands=commands))
    pattern=re.compile(rb'(?<![A-Za-z])orca(?![A-Za-z])',re.I);rawhits=[]
    for path,data in [(p,v) for _,p,v in rom.iter_files()]+list(rom.iter_components()):
        for match in pattern.finditer(data):
            rawhits.append(dict(file_path=path,offset=match.start(),bounded_nearby_hex=data[max(0,match.start()-32):match.end()+64].hex(),raw_candidate_not_automatically_dialogue_or_semantic_item_use=True))
    sc=[];total=0
    for route in range(4):
        file=f'/data/SC{route}.DK4';bank=IlnkContainer.parse(rom.read_file(file)).blocks;total+=len(bank)
        for i,blob in enumerate(bank):
            for match in pattern.finditer(blob):sc.append(dict(file_path=file,block=i,offset=match.start(),bounded_nearby_hex=blob[max(0,match.start()-32):match.end()+64].hex()))
    assert total==1307 and len(groups)==4
    ROOT.mkdir(parents=True);save(ROOT/'four_complete_source_current_exchanges_and_raw_Orca_candidates.json',dict(candidate=str(candidate),candidate_sha256=sha(candidate.read_bytes()),clean_context=str(SOURCE),clean_context_sha256=sha(SOURCE.read_bytes()),
        source_first_order_preserved=True,groups=groups,all1307_current_source_blocks_scanned=total,typed_current_speech_comparison_objects=80,current_uncompressed_SC_word_Orca_candidates=sc,raw_ROM_file_component_word_Orca_candidates=rawhits,
        raw_hits_are_leads_not_complete_dynamic_consumer_proof=True,all_source_nickname_contexts_excluded_from_item_replacement=True,
        no_global_replacement_no_ROM_registry_ledger_change=True,individual_revision_retention_decisions_and_English_native_layout_pending=True,
        new_review_credit=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,Path(__file__)]}))
    for g in groups:
        print(g['file_path'],g['block'])
        for r in g['records']:
            if g['block']==204 or 'シャチホコ' in r['Japanese']:print(r['source_record_index'],repr(r['older_English']))
    print('current SC Orca candidates',sc,'raw component/file hits',[(r['file_path'],r['offset']) for r in rawhits])
