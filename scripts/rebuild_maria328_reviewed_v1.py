"""Reconstruct21 complete exchanges and one source-owned FE continuation in research."""
import os
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.script.reviewed_scene_rebuild_v3 import rebuild_block
from dk4tool.script.reviewed_FE_pagination_v1 import insert_FE_continuations
from dk4tool.dialogue.reviewed_choice_object_v2 import compile_choices
from dk4tool.dialogue.reviewed_actor_style_object_v1 import compile_styles
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.meaning_maria328_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

def pagination_rejects(arm,block,owners,inventory):
    rejected=[]
    for kind in ['wrong-speaker','wrong-first-offset','changed-first-page','changed-child-prose','omitted-closing-clause','wrong-child-index','changed-child-control']:
        attempt=deepcopy(owners)
        if kind=='wrong-speaker':attempt[0]['complete_source_preamble_hex']='0040ffff0000'
        elif kind=='wrong-first-offset':attempt[0]['first_command_offset']+=2
        elif kind=='changed-first-page':attempt[0]['first_stored_hex']='fe41'
        elif kind=='changed-child-prose':attempt[0]['pages'][1]['logical_English']+=' changed'
        elif kind=='omitted-closing-clause':attempt[0]['unchanged_logical_English']=attempt[0]['pages'][0]['logical_English']
        elif kind=='wrong-child-index':attempt[0]['pages'][1]['native_child_page']=3
        else:attempt[0]['continuation_encoded_hex']='00'+attempt[0]['continuation_encoded_hex'][2:]
        try:insert_FE_continuations(arm,block,attempt,inventory)
        except (AssertionError,ValueError):rejected.append(kind)
        else:raise AssertionError('Accepted invalid pagination: '+kind)
    assert len(rejected)==7
    return rejected

def main():
    out=ROOT/'reconstruction_v1';assert not out.exists()
    sourcepath=ROOT/'formatting_v1/formatting_input.json';physicalpath=ROOT/'formatting_FE_v1/physical_manuscript.json'
    planpath=ROOT/'plan_visual_v6/automatic_plans.json';nativepath=ROOT/'final_native_v1.json'
    packetpath=ROOT/'current_v1/current_effective.json';objectpath=ROOT/'current_objects_v1/current_objects.json'
    menupath=ROOT/'menu_native_v1/menu_provider_and_planes.json';stylepath=ROOT/'compiled_styles_v1/compiled_style_objects.json'
    approvalpath=ROOT/'offline_display_approval_v1.json'
    source,physical,layout,native,packet,objects,menus,styles,approval=map(load,[sourcepath,physicalpath,planpath,nativepath,packetpath,objectpath,menupath,stylepath,approvalpath])
    assert (len(source['records']),len(physical['records']),len(layout['records']),len(native['records']),native['pages'])==(328,329,314,314,321)
    assert approval['all321_final_pages_directly_viewed'] and approval['all_fifth_formatting_gates_still_pending']
    assert approval['final_native_proof_sha256']==digest(nativepath)
    assert layout['manuscript_sha256']==native['manuscript_sha256']==styles['manuscript_sha256']==digest(physicalpath)
    assert native['plan_sha256']==styles['plan_sha256']==digest(planpath)
    assert native['runtime']==packet['runtime']==objects['runtime']==menus['runtime']==styles['runtime']==physical['runtime']
    assert styles['native_target_slot_cases']==32 and sum(len(n['rejected']) for n in styles['compiler_negatives'])==36
    assert menus['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']
    assert all(r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False) for r in source['records'])
    image=NdsImage.open(source['current_ROM']);assert digest(source['current_ROM'])==source['current_ROM_sha256']
    arm=image.read_file('/__arm9__.bin');assert sha(arm)==native['runtime']['ARM9_sha256']
    archive=image.read_file(source['file_path']);assert sha(archive)==source['current_archive_sha256']==packet['current_archive_sha256']
    container=IlnkContainer.parse(archive);blocks=list(container.blocks);inventory,_,_=scoped_inventory()
    plans={r['id']:deepcopy(r) for r in layout['records']};owner=physical['pagination_owners'][0]
    assert len(physical['pagination_owners'])==1 and owner['source_ID']=='DK4_MES_B87_R0139'
    ident=owner['source_ID'];first_id,second_id=owner['child_IDs']
    assert ' '.join(plans[k]['logical_English'] for k in [first_id,second_id])==owner['unchanged_logical_English']
    compiled={r['id']:deepcopy(plans[r['id']]) for r in source['records'] if r['kind']!='typed-choice-label' and r['id']!=ident}
    firstplan=deepcopy(plans[first_id]);firstplan.update(id=ident,logical_English=owner['unchanged_logical_English'],expected_native_pages=2,
        native_FE_child_pages=[plans[first_id],plans[second_id]],encoded_hex_is_first_native_panel_only=True)
    compiled[ident]=firstplan;assert len(compiled)==313
    out.mkdir()
    macro=load(ROOT/'formatting_v1/native_macro_measurements.json');assert macro['runtime']==native['runtime']
    nativebridge=deepcopy(native);nativebridge.update(source_owned_progressive_macro_adapter=macro['source_owned_progressive_adapter'],
        metadata_only_macro_adapter_bridge=True,original_native_receipt=str(nativepath),original_native_receipt_sha256=digest(nativepath))
    bridgednative=out/'native_pages.json';save(bridgednative,nativebridge)
    menubridge=dict(manuscript=str(physicalpath),manuscript_sha256=digest(physicalpath),runtime=native['runtime'],menus=menus['menus'],
        offline_visual_approved=True,direct_view_pending=False,original_receipt=str(menupath),original_receipt_sha256=digest(menupath),new_credit=0)
    bridgedmenus=out/'menus.json';save(bridgedmenus,menubridge)
    ordinary=[r for r in source['records'] if r['kind'] in ['progressive','system-FE'] and r.get('native_object_kind')!='4100-style-alternative']
    alternatives=[r for r in source['records'] if r.get('native_object_kind')=='4100-style-alternative']
    typed=[r for r in source['records'] if r['kind']=='typed-choice-label']
    assert (len(ordinary),len(alternatives),len(typed))==(289,24,15)
    groups=[];changed=[];all_rejects=[]
    for group in packet['groups']:
        block=group['block'];current=blocks[block];clean=bytes.fromhex(group['clean_block_hex'])
        assert current.hex()==group['current_block_hex'] and sha(current)==group['current_block_sha256'] and sha(clean)==group['clean_block_sha256']
        assert inventory(arm,current)[0]==group['all_current_commands'] and inventory(arm,clean)[0]==group['all_source_commands']
        compound=[]
        for proof in menus['menus']:
            if proof['block']!=block:continue
            rows=sorted([r for r in typed if r['block']==block and r['source_command_offset']==proof['source_command_offset']],key=lambda r:r['source_index'])
            before,prior=map(bytes.fromhex,[rows[0]['source_choice_object_hex'],rows[0]['current_choice_object_hex']])
            value=compile_choices(before,prior,rows,require_formatting=False);assert value.hex()==proof['target_object_hex']
            compound.append(dict(id=f'B{block}_C{proof["source_command_offset"]}_menu',word=0x2200,offset=rows[0]['current_reference']['command_offset'],
                source_hex=before.hex(),current_hex=prior.hex(),compiled_hex=value.hex(),records=rows))
        for proof in styles['objects']:
            if proof['block']!=block:continue
            rows=sorted([r for r in alternatives if r['block']==block and r['source_command_offset']==proof['source_command_offset']],key=lambda r:r['source_reference']['offset'])
            before,prior=map(bytes.fromhex,[proof['source_object_hex'],proof['current_object_hex']])
            value=compile_styles(before,prior,rows,compiled,require_formatting=False);assert value.hex()==proof['target_object_hex']
            compound.append(dict(id=f'B{block}_C{proof["source_command_offset"]}_styles',word=0x4100,offset=proof['current_command_offset'],
                source_hex=before.hex(),current_hex=prior.hex(),compiled_hex=value.hex(),records=rows))
        rows=[r for r in ordinary if r['block']==block]
        intermediate,proof=rebuild_block(arm,clean,current,rows,compiled,inventory,compound)
        target=intermediate
        if block==87:
            text=next(r for r in proof['text_records'] if r['id']==ident)
            pages=[dict(native_child_page=i+1,logical_English=plans[k]['logical_English'],encoded_hex=plans[k]['encoded_hex']) for i,k in enumerate([first_id,second_id])]
            insertion=[dict(source_ID=ident,first_command_offset=text['new_offset']-5,first_stored_hex=text['stored_hex'],
                complete_source_preamble_hex=owner['complete_source_preamble_hex'],continuation_encoded_hex=pages[1]['encoded_hex'],pages=pages,
                unchanged_logical_English=owner['unchanged_logical_English'])]
            target,pagination=insert_FE_continuations(arm,intermediate,insertion,inventory)
            all_rejects=pagination_rejects(arm,intermediate,insertion,inventory)
            mapping={r['old_offset']:r['new_offset'] for r in pagination['original_command_map']}
            texts=[]
            for item in proof['text_records']:
                key=first_id if item['id']==ident else item['id'];at=mapping[item['new_offset']-5]+5
                texts.append({**item,'id':key,'source_editorial_ID':item['id'],'new_offset':at,'new_record_index':target[:at].count(b'\0')})
            child=pagination['continuations'][0];at=child['new_command_offset']+5
            texts.append(dict(id=second_id,source_editorial_ID=ident,old_offset=next(r for r in rows if r['id']==ident)['current_reference']['offset'],
                new_offset=at,new_record_index=target[:at].count(b'\0'),source_hex=owner['source_hex'],current_hex=owner['current_hex'],
                compiled_hex=child['encoded_hex'],stored_hex=child['stored_hex'],parity_space_added=child['stored_hex']!=child['encoded_hex'],native_child_page=2))
            moved_objects=[{**o,'new_offset':mapping[o['new_offset']]} for o in proof['native_objects']]
            commands=inventory(arm,target)[0];byat={c['offset']:c for c in commands}
            commandmap=[{**m,'new_offset':mapping[m['new_offset']],'new_extent':byat[mapping[m['new_offset']]]['native_extent']} for m in proof['command_map']]
            secondfix={f['old_offset']:f for f in pagination['relative_fixups']}
            fixes=[{**f,**{k:secondfix[f['new_offset']][k] for k in ['new_offset','new_span','new_target']}} for f in proof['relative_fixups']]
            (out/'B87_INTERMEDIATE_NOT_PLAYABLE.bin').write_bytes(intermediate)
            proof=dict(proof,text_records=sorted(texts,key=lambda r:r['new_offset']),native_objects=moved_objects,
                command_map=commandmap,relative_fixups=fixes,all_target_commands=commands,new_logical_end=pagination['new_logical_end'],
                first_page_reconstruction=proof,FE_pagination=pagination)
        assert target!=current;changed.append(block);blocks[block]=target
        path=out/f'B{block}_RESEARCH_ONLY.bin';path.write_bytes(target)
        groups.append(dict(block=block,file_path=source['file_path'],current_sha256=sha(current),clean_sha256=sha(clean),target_sha256=sha(target),
            target_block=str(path),current_bytes=len(current),target_bytes=len(target),**proof))
    assert changed==source['blocks'] and len(changed)==21
    result=IlnkContainer(blocks).to_bytes();parsed=IlnkContainer.parse(result)
    assert [i for i,(a,b) in enumerate(zip(container.blocks,parsed.blocks,strict=True)) if a!=b]==changed
    inverse=list(parsed.blocks)
    for block in changed:inverse[block]=container.blocks[block]
    assert IlnkContainer(inverse).to_bytes()==archive
    planned=deepcopy(image);planned.replace_file(source['file_path'],result)
    assert [p for _,p,v in image.iter_files() if planned.read_file(p)!=v]==[source['file_path']]
    assert all(planned.read_file(p)==v for p,v in image.iter_components())
    rom=out/'reviewed_RESEARCH_ONLY.nds';planned.save(rom)
    reopened=NdsImage.open(rom);assert reopened.read_file(source['file_path'])==result and reopened.read_file('/__arm9__.bin')==arm
    reopened.replace_file(source['file_path'],archive);assert bytes(reopened.rom.save())==Path(source['current_ROM']).read_bytes()
    archivepath=out/'reviewed_RESEARCH_ONLY.DK4';archivepath.write_bytes(result)
    assert sum(len(g['text_records']) for g in groups)==290 and sum(len(g['native_objects']) for g in groups)==9
    evidence=[sourcepath,physicalpath,planpath,nativepath,packetpath,objectpath,menupath,stylepath,approvalpath,
        Path('dk4tool/script/reviewed_scene_rebuild_v3.py'),Path('dk4tool/script/reviewed_FE_pagination_v1.py'),Path(__file__)]
    save(out/'reconstruction.json',dict(parent=source['current_ROM'],parent_sha256=source['current_ROM_sha256'],
        manuscript=str(physicalpath),manuscript_sha256=digest(physicalpath),source_manuscript=str(sourcepath),source_manuscript_sha256=digest(sourcepath),
        plan=str(planpath),plan_sha256=digest(planpath),native=str(bridgednative),native_sha256=digest(bridgednative),
        packet=str(packetpath),packet_sha256=digest(packetpath),menu=str(bridgedmenus),menu_sha256=digest(bridgedmenus),styles=str(stylepath),styles_sha256=digest(stylepath),
        source_archive_sha256=sha(archive),target_archive=str(archivepath),target_archive_sha256=sha(result),research_ROM=str(rom),research_ROM_sha256=digest(rom),
        groups=groups,changed_blocks=changed,reviewed_blocks=changed,unchanged_control_only_blocks=[],source_editorial_objects=328,
        source_speeches=289,speech_count=290,style_physical_speech_count=24,total_rendered_speech_count=314,typed_choice_count=15,compound_objects=9,
        command_count=sum(len(g['all_target_commands']) for g in groups),relative_sites=sum(len(g['relative_fixups']) for g in groups),
        full_clean_current_block_archive_andserialized_NDS_inverses_exact=True,all_other_files_components_exact=True,
        source_owned_exact_FE_control_repeated_once=True,seven_FE_pagination_invalid_cases_rejected=all_rejects,
        registered_market_runtime_andASCII_right_bound_preserved=True,stored_native_actual_controller_andregistered_release_pending=True,
        not_registered_candidate_or_natural_activation=True,new_credit=0,guide_photos=False,evidence={str(p):digest(p) for p in evidence}))
    pins=Path('translations/rom_retention_pins.json');before=pins.read_bytes();values=load(pins)
    assert not any(Path(v['path']).resolve()==rom.resolve() for v in values)
    values.append(dict(path=str(rom.resolve()),reason='Preserve complete Maria328 research and exact-source FE continuation; not a registered candidate. SHA256 '+digest(rom)))
    (out/'pins.before.json').write_bytes(before);pending=pins.with_name('rom_retention_pins.Maria328.pending.json');assert not pending.exists();save(pending,values)
    assert pins.read_bytes()==before;os.replace(pending,pins)
    print('Reconstructed328 source objects/314 physical bodies across21 blocks;FE continuation,seven rejects andwhole-ROM inverse pass. Stored/gameplay/release pending.')

if __name__=='__main__':main()
