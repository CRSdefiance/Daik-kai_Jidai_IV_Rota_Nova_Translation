"""Inventory exact current surname spellings andwhole clean source exchanges;no edits ornew reviewcredit."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Gerhard_surname_consumers_v8196')
PRIOR=Path('work/analysis/editorial_handoff_verification_v8195/verified_handoff.json')
ALIASES=['Ardelknatts','Ardelnkatts','Adernkatz','Adelnkatz']
def offsets(raw,needle):
    result=[];at=raw.find(needle)
    while at>=0:result.append(at);at=raw.find(needle,at+1)
    return result
if __name__=='__main__':
    assert not ROOT.exists();prior=read(PRIOR);candidate=Path(prior['candidate']);current,clean=[NdsImage.open(p) for p in [candidate,'work/clean.nds']]
    assert sha(candidate.read_bytes())==prior['candidate_sha256']
    components=list(current.iter_components());files=[(p,v) for _,p,v in current.iter_files()]
    occurrences=[]
    for file,raw in components+files:
        for variant in ALIASES:
            for at in offsets(raw,variant.encode('ascii')):
                start=raw.rfind(b'\0',0,at)+1;end=raw.find(b'\0',at);assert end>=at
                occurrences.append(dict(file_path=file,offset=at,variant=variant,terminated_owner_start=start,terminated_owner_end=end,
                    owner_hex=raw[start:end].hex(),owner_CP932=raw[start:end].decode('cp932',errors='backslashreplace')))
    assert sum(r['variant']=='Ardelknatts' for r in occurrences)==6 and sum(r['variant']=='Adernkatz' for r in occurrences)==14
    inventory,walker,fn=scoped_inventory();arm=clean.read_file('/__arm9__.bin');groups=[];selected=[]
    targets={'/data/SC0.DK4':[84,85],'/data/SC2.DK4':[27,74],'/data/SC3.DK4':[59]}
    for file,numbers in targets.items():
        sourcebank,nowbank=[IlnkContainer.parse(im.read_file(file)).blocks for im in [clean,current]]
        for number in numbers:
            original,now=sourcebank[number],nowbank[number]
            sourcecommands,sourcespeeches=inventory(arm,original)
            currentcommands,currentspeeches=inventory(current.read_file('/__arm9__.bin'),now)
            assert [c['word'] for c in sourcecommands]==[c['word'] for c in currentcommands] and len(sourcespeeches)==len(currentspeeches)
            rows=[]
            for sourcecommand,currentcommand in zip(sourcespeeches,currentspeeches,strict=True):
                at=sourcecommand['offset']+5;end=original.index(0,at+1);raw=original[at:end];index=original[:at].count(b'\0')
                ca=currentcommand['offset']+5;ce=now.index(0,ca+1);cur=now[ca:ce]
                assert original[at-5:at+1]==now[ca-5:ca+1]
                matches=[v for v in ALIASES if v.encode() in cur]
                row=dict(id=f'DK4_MES_B{number}_R{index:04d}',file_path=file,block=number,source_record_index=index,source_selector=raw[0],
                    source_reference=dict(offset=at,bytes=len(raw),header_offset=at-5),source_hex=raw.hex(),source_complete_preamble_hex=original[at-5:at+1].hex(),
                    source_Japanese=raw[1:].decode('cp932',errors='backslashreplace'),source_0100_ancestors=sourcecommand['ancestor_0100_offsets'],
                    contains_source_surname='アーデルンカッツ'.encode('cp932') in raw,contains_current_surname=bool(matches),current_variants=matches)
                if matches:
                    row.update(current_reference=dict(offset=ca,bytes=len(cur),header_offset=ca-5,record_index=now[:ca].count(b'\0')),current_hex=cur.hex(),current_body_CP932=cur[1:].decode('cp932'),
                        current_source_preamble_exact=True,current_effective_dispatch_not_yet_verified=True)
                    selected.append(row)
                rows.append(row)
            groups.append(dict(file_path=file,block=number,clean_block_sha256=sha(original),current_block_sha256=sha(now),clean_block_hex=original.hex(),
                all_clean_commands=sourcecommands,all_current_commands=currentcommands,complete_clean_source_records=rows,
                full_exchange_not_isolated_surname_fragment=True,no_new_whole_dialogue_editorial_credit=True))
    assert sum(r['current_variants'].count('Ardelknatts')*r.get('current_body_CP932','').count('Ardelknatts') for r in selected)==5
    source_jp='アーデルンカッツ'.encode('cp932')
    retained_raw_JP=[dict(file_path=p,offsets=offsets(v,source_jp),raw_source_orcatalogue_keys_not_automatically_player_facing=True) for p,v in components+files if source_jp in v]
    ROOT.mkdir(parents=True);save(ROOT/'all20_current_Latin_occurrences_five_whole_clean_exchanges.json',dict(
        candidate=str(candidate),candidate_sha256=prior['candidate_sha256'],source_ROM='work/clean.nds',source_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),
        variants=ALIASES,current_Latin_occurrences=occurrences,counts=dict(Ardelknatts=6,Adernkatz=14,Ardelnkatts=0,Adelnkatz=0),groups=groups,
        current_story_record_consumers=selected,current_raw_Japanese_surname_occurrences=retained_raw_JP,
        one_Ardelknatts_ARM9_name_slot_five_Ardelknatts_SC2_mentions=True,
        fourteen_Adernkatz_occurrences_in_ARM9_SC0_SC3_already_exist=True,
        current_Hodram_B137_B45_B46_body_English_not_exposed=True,
        effective_runtime_catalogue_UI_font_full_context_gloss_decision_andregistered_correction_pending=True,
        native_inventory_walker=walker,native_inventory_function=fn,new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [PRIOR,Path(__file__)]}))
    print('Variants6Ardelknatts/14Adernkatz;5wholecleansource blocks:',[(g['file_path'],g['block'],len(g['complete_clean_source_records'])) for g in groups])
    for r in selected:print(r['file_path'],r['id'],repr(r['source_Japanese']),'CURRENT',repr(r['current_body_CP932']))
    print('Raw Japanese retained occurrences',[(r['file_path'],len(r['offsets'])) for r in retained_raw_JP],'not automatically active display defects.')
