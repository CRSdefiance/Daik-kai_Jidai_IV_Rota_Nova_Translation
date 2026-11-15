"""Use the unchanged source-bound scene and FE continuation planners for one complete exchange."""
import os
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.script.reviewed_scene_rebuild_v3 import rebuild_block
from dk4tool.script.reviewed_FE_pagination_v1 import insert_FE_continuations
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B50_FE_resolution_20261109_v3')
OUT=ROOT/'reconstruction_v1'
def main():
    assert not OUT.exists()
    source_path=ROOT/'source16_manuscript.json';physical_path=ROOT/'physical17_manuscript.json'
    source,physical=map(load,[source_path,physical_path]);approval=load(ROOT/'offline_approval_v1.json')
    native_path=Path(approval['native']);native=load(native_path);plan_path=Path(approval['plan']);layout=load(plan_path)
    assert digest(native_path)==approval['native_sha256'] and digest(plan_path)==approval['plan_sha256']
    assert approval['all17_final_panels_directly_viewed'] and native['runtime']==source['runtime']==physical['runtime']
    for p,h in approval['evidence'].items():assert digest(p)==h
    assert len(source['records'])==16 and len(physical['records'])==len(layout['records'])==len(native['records'])==17
    image=NdsImage.open(source['current_ROM']);assert digest(source['current_ROM'])==source['current_ROM_sha256']
    arm=image.read_file('/__arm9__.bin');assert sha(arm)==native['runtime']['ARM9_sha256']
    archive=image.read_file('/data/SC3.DK4');assert sha(archive)==source['current_archive_sha256']
    bank=IlnkContainer.parse(archive);blocks=list(bank.blocks)
    clean=IlnkContainer.parse(NdsImage.open('work/clean.nds').read_file('/data/SC3.DK4')).blocks[50]
    inventory,_,_=scoped_inventory();current=blocks[50]
    plans={r['id']:deepcopy(r) for r in layout['records']};owner=physical['pagination_owners'][0]
    ident=owner['source_ID'];first_id,second_id=owner['child_IDs']
    source_plans={r['id']:deepcopy(plans[r['id']]) for r in source['records'] if r['id']!=ident}
    first_plan=deepcopy(plans[first_id]);first_plan.update(id=ident,logical_English=owner['unchanged_logical_English'],
        expected_native_pages=2,native_FE_child_pages=[plans[first_id],plans[second_id]],
        encoded_hex_is_first_native_panel_only=True,complete_paragraph_owned_by_two_native_FE_commands=True)
    source_plans[ident]=first_plan
    rows=deepcopy(source['records'])
    for row in rows:row['current_record_index']=row['current_reference']['record_index']
    intermediate,firstproof=rebuild_block(arm,clean,current,rows,source_plans,inventory,[])
    first=next(r for r in firstproof['text_records'] if r['id']==ident)
    pages=[dict(native_child_page=i+1,logical_English=plans[k]['logical_English'],encoded_hex=plans[k]['encoded_hex']) for i,k in enumerate(owner['child_IDs'])]
    insertion=[dict(source_ID=ident,first_command_offset=first['new_offset']-5,first_stored_hex=first['stored_hex'],
        complete_source_preamble_hex=owner['complete_source_preamble_hex'],continuation_encoded_hex=pages[1]['encoded_hex'],
        pages=pages,unchanged_logical_English=owner['unchanged_logical_English'])]
    final,pagination=insert_FE_continuations(arm,intermediate,insertion,inventory)
    negatives=[]
    for kind in ['wrong-speaker','wrong-first-offset','changed-first-page','changed-child-prose','omitted-closing-clause','wrong-child-index','changed-child-control']:
        attempt=deepcopy(insertion)
        if kind=='wrong-speaker':attempt[0]['complete_source_preamble_hex']='0040ffff0000'
        elif kind=='wrong-first-offset':attempt[0]['first_command_offset']+=2
        elif kind=='changed-first-page':attempt[0]['first_stored_hex']='fe41'
        elif kind=='changed-child-prose':attempt[0]['pages'][1]['logical_English']+=' changed'
        elif kind=='omitted-closing-clause':attempt[0]['unchanged_logical_English']=attempt[0]['pages'][0]['logical_English']
        elif kind=='wrong-child-index':attempt[0]['pages'][1]['native_child_page']=3
        else:attempt[0]['continuation_encoded_hex']='00'+attempt[0]['continuation_encoded_hex'][2:]
        try:insert_FE_continuations(arm,intermediate,attempt,inventory)
        except (AssertionError,ValueError):negatives.append(kind)
        else:raise AssertionError('Pagination accepted '+kind)
    assert len(negatives)==7
    mapping={r['old_offset']:r['new_offset'] for r in pagination['original_command_map']}
    children=pagination['continuations'];assert len(children)==1 and children[0]['source_ID']==ident
    native_texts=[]
    for text in firstproof['text_records']:
        key=first_id if text['id']==ident else text['id'];at=mapping[text['new_offset']-5]+5
        raw=bytes.fromhex(text['stored_hex']);assert final[at:at+len(raw)+1]==raw+b'\0'
        native_texts.append({**text,'id':key,'source_editorial_ID':text['id'],'new_offset':at,'new_record_index':final[:at].count(b'\0')})
    child=children[0];at=child['new_command_offset']+5;raw=bytes.fromhex(child['stored_hex'])
    assert final[at:at+len(raw)+1]==raw+b'\0'
    native_texts.append(dict(id=second_id,source_editorial_ID=ident,old_offset=next(r for r in source['records'] if r['id']==ident)['current_reference']['offset'],
        new_offset=at,new_record_index=final[:at].count(b'\0'),source_hex=owner['source_hex'],current_hex=owner['current_hex'],
        compiled_hex=child['encoded_hex'],stored_hex=child['stored_hex'],parity_space_added=child['stored_hex']!=child['encoded_hex'],native_child_page=2))
    native_texts.sort(key=lambda r:r['new_offset'])
    assert [r['id'] for r in native_texts]==[r['id'] for r in physical['records']]
    assert {r['id'] for r in native_texts}==set(plans)
    actual_commands,actual_speeches=inventory(arm,final)
    assert len(actual_speeches)==17 and len(actual_commands)==len(inventory(arm,current)[0])+1
    OUT.mkdir();block_path=OUT/'B50_RESEARCH_ONLY.bin';block_path.write_bytes(final)
    (OUT/'B50_first_pages_INTERMEDIATE_NOT_PLAYABLE.bin').write_bytes(intermediate)
    save(OUT/'source16_plans.json',dict(records=list(source_plans.values()),failures=[],source_objects=16,native_panels=17,new_credit=0))
    blocks[50]=final;resource=IlnkContainer(blocks).to_bytes()
    assert [i for i,(a,b) in enumerate(zip(bank.blocks,blocks,strict=True)) if a!=b]==[50]
    inverse=list(blocks);inverse[50]=current;assert IlnkContainer(inverse).to_bytes()==archive
    research=deepcopy(image);research.replace_file('/data/SC3.DK4',resource)
    assert [p for _,p,v in image.iter_files() if research.read_file(p)!=v]==['/data/SC3.DK4']
    assert all(research.read_file(p)==v for p,v in image.iter_components())
    rom=OUT/'reviewed_FE_paginated_RESEARCH_ONLY.nds';research.save(rom)
    reopened=NdsImage.open(rom);assert reopened.read_file('/data/SC3.DK4')==resource
    reopened.replace_file('/data/SC3.DK4',archive);assert bytes(reopened.rom.save())==Path(source['current_ROM']).read_bytes()
    archive_path=OUT/'reviewed_RESEARCH_ONLY.DK4';archive_path.write_bytes(resource)
    group=dict(block=50,file_path='/data/SC3.DK4',target_block=str(block_path),target_sha256=sha(final),
        current_sha256=sha(current),clean_sha256=sha(clean),current_bytes=len(current),target_bytes=len(final),
        text_records=native_texts,native_objects=[],first_page_reconstruction=firstproof,FE_pagination=pagination,
        command_map=pagination['original_command_map'],relative_fixups=pagination['relative_fixups'],
        all_target_commands=actual_commands,new_logical_end=pagination['new_logical_end'])
    save(OUT/'reconstruction.json',dict(parent=source['current_ROM'],parent_sha256=source['current_ROM_sha256'],
        manuscript=str(physical_path),manuscript_sha256=digest(physical_path),source_manuscript=str(source_path),source_manuscript_sha256=digest(source_path),
        plan=str(plan_path),plan_sha256=digest(plan_path),native=str(native_path),native_sha256=digest(native_path),
        source_archive_sha256=sha(archive),target_archive=str(archive_path),target_archive_sha256=sha(resource),research_ROM=str(rom),research_ROM_sha256=digest(rom),
        groups=[group],changed_blocks=[50],reviewed_blocks=[50],unchanged_control_only_blocks=[],
        source_editorial_objects=16,source_speeches=16,speech_count=17,total_rendered_speech_count=17,
        style_physical_speech_count=0,typed_choice_count=0,compound_objects=0,native_speech_commands=17,
        complete_native_display_pages=17,command_count=len(actual_commands),relative_sites=len(pagination['relative_fixups']),
        full_clean_current_block_archive_andserialized_NDS_inverses_exact=True,all_other_files_components_exact=True,
        all_original_scene_controls_andconditional_scopes_preserved=True,
        source_owned_exact_FE_control_repeated_once=True,seven_FE_pagination_invalid_cases_rejected=negatives,
        registered_market_runtime_andASCII_right_bound_preserved=True,stored_native_actual_controller_andregistered_release_pending=True,
        not_registered_candidate_or_natural_activation=True,new_credit=0,guide_photos=False,
        evidence={str(p):digest(p) for p in [source_path,physical_path,plan_path,native_path,ROOT/'offline_approval_v1.json',
            Path('dk4tool/script/reviewed_scene_rebuild_v3.py'),Path('dk4tool/script/reviewed_FE_pagination_v1.py'),Path(__file__)]}))
    pins=Path('translations/rom_retention_pins.json');before=pins.read_bytes();values=load(pins)
    assert not any(Path(v['path']).resolve()==rom.resolve() for v in values)
    values.append(dict(path=str(rom.resolve()),reason='Preserve complete Maria B50 research with exact-source FE continuation. SHA256 '+digest(rom)))
    (OUT/'pins.before.json').write_bytes(before);pending=pins.with_name('rom_retention_pins.Maria_B50_FE.pending.json');assert not pending.exists();save(pending,values)
    assert pins.read_bytes()==before;os.replace(pending,pins)
    print('Reconstructed16 sources/17 native panels;all original commands/scopes,seven rejects andwhole-ROM inverse pass. Stored/actual/release pending.')
if __name__=='__main__':main()
