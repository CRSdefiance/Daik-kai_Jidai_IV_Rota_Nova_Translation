"""Rebuild26 complete exchanges with two source-owned FE continuations in one block."""
from copy import deepcopy
from pathlib import Path
import os
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.script.reviewed_scene_rebuild_v3 import rebuild_block
from dk4tool.script.reviewed_FE_pagination_v1 import insert_FE_continuations
from dk4tool.dialogue.reviewed_two_choice_object_v1 import compile_choices
from dk4tool.dialogue.reviewed_actor_style_object_v1 import compile_styles
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.rebuild_maria328_reviewed_v1 import pagination_rejects
from scripts.meaning_maria330_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

def main():
    out=ROOT/'reconstruction_v1';assert not out.exists()
    paths=dict(source=ROOT/'formatting_v1/formatting_input.json',physical=ROOT/'formatting_FE_v2/physical_manuscript.json',
        plan=ROOT/'plan_continuity_v10/automatic_plans.json',native=ROOT/'final_native_v1.json',packet=ROOT/'current_v1/current_effective.json',
        objects=ROOT/'current_objects_v1/current_objects.json',menu=ROOT/'menu_native_approved_v1.json',styles=ROOT/'compiled_styles_v1/compiled_style_objects.json',
        approval=ROOT/'offline_display_approval_v1.json',parent=Path('work/maria328_release_v1/registered_release_verification.json'))
    d={k:load(p) for k,p in paths.items()};source,physical,layout,native,packet,objects,menus,styles,approval,parent=[d[k] for k in paths]
    assert (len(source['records']),len(physical['records']),len(layout['records']),len(native['records']),native['pages'])==(330,332,330,330,338)
    assert approval['all338_final_pages_directly_viewed'] and approval['all_names_andtwo_captions_directly_viewed'] and approval['all_fifth_formatting_gates_still_pending']
    assert approval['final_native_proof_sha256']==digest(paths['native'])
    assert layout['manuscript_sha256']==native['manuscript_sha256']==styles['manuscript_sha256']==menus['manuscript_sha256']==digest(paths['physical'])
    assert native['plan_sha256']==styles['plan_sha256']==digest(paths['plan'])
    assert all(x['runtime']==physical['runtime'] for x in [native,packet,objects,menus,styles])
    assert styles['native_target_slot_cases']==48 and sum(len(n['rejected']) for n in styles['compiler_negatives'])==54
    assert menus['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass'] and menus['offline_visual_approved'] and not menus['direct_view_pending']
    assert all(r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False) for r in source['records'])
    assert not parent['own_registered_startup_pending'] and parent['clean_input_patch_byte_exact']
    assert digest('translations/release_stack.json')==parent['registry_sha256']
    assert source['current_ROM_sha256']==parent['candidate_sha256'] and digest(source['current_ROM'])==source['current_ROM_sha256']
    image=NdsImage.open(source['current_ROM']);arm=image.read_file('/__arm9__.bin');assert sha(arm)==native['runtime']['ARM9_sha256']
    archive=image.read_file(source['file_path']);assert sha(archive)==source['current_archive_sha256']==packet['current_archive_sha256']
    container=IlnkContainer.parse(archive);blocks=list(container.blocks);inventory,_,_=scoped_inventory()
    plans={r['id']:deepcopy(r) for r in layout['records']};owners={p['source_ID']:p for p in physical['pagination_owners']}
    assert set(owners)=={'DK4_MES_B116_R0041','DK4_MES_B116_R0051'}
    compiled={r['id']:deepcopy(plans[r['id']]) for r in source['records'] if r['kind']!='typed-choice-label' and r['id'] not in owners}
    for ident,owner in owners.items():
        first,second=owner['child_IDs'];assert ' '.join(plans[k]['logical_English'] for k in [first,second])==owner['unchanged_logical_English']
        firstplan=deepcopy(plans[first]);firstplan.update(id=ident,logical_English=owner['unchanged_logical_English'],expected_native_pages=2,
            native_FE_child_pages=[plans[first],plans[second]],encoded_hex_is_first_native_panel_only=True)
        compiled[ident]=firstplan
    assert len(compiled)==328
    ordinary=[r for r in source['records'] if r['kind'] in ['progressive','system-FE'] and r.get('native_object_kind')!='4100-style-alternative']
    alternatives=[r for r in source['records'] if r.get('native_object_kind')=='4100-style-alternative'];typed=[r for r in source['records'] if r['kind']=='typed-choice-label']
    assert (len(ordinary),len(alternatives),len(typed))==(293,35,2)
    out.mkdir();bridgednative=out/'native_pages.json';save(bridgednative,native)
    bridgedmenus=out/'menus.json';save(bridgedmenus,menus)
    groups=[];changed=[];all_rejects=[];inserted=0
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
            compound.append(dict(id=f'B{block}_C{proof["source_command_offset"]}_menu',word=0x2100,offset=rows[0]['current_reference']['command_offset'],
                source_hex=before.hex(),current_hex=prior.hex(),compiled_hex=value.hex(),records=rows))
        for proof in styles['objects']:
            if proof['block']!=block:continue
            rows=sorted([r for r in alternatives if r['block']==block and r['source_command_offset']==proof['source_command_offset']],key=lambda r:r['source_reference']['offset'])
            before,prior=map(bytes.fromhex,[proof['source_object_hex'],proof['current_object_hex']])
            value=compile_styles(before,prior,rows,compiled,require_formatting=False);assert value.hex()==proof['target_object_hex']
            compound.append(dict(id=f'B{block}_C{proof["source_command_offset"]}_styles',word=0x4100,offset=proof['current_command_offset'],
                source_hex=before.hex(),current_hex=prior.hex(),compiled_hex=value.hex(),records=rows))
        rows=[r for r in ordinary if r['block']==block];intermediate,proof=rebuild_block(arm,clean,current,rows,compiled,inventory,compound);target=intermediate
        blockowners={ident:o for ident,o in owners.items() if o['source_reference']['block']==block}
        if blockowners:
            insertion=[]
            for ident,owner in blockowners.items():
                text=next(r for r in proof['text_records'] if r['id']==ident)
                pages=[dict(native_child_page=i+1,logical_English=plans[k]['logical_English'],encoded_hex=plans[k]['encoded_hex']) for i,k in enumerate(owner['child_IDs'])]
                insertion.append(dict(source_ID=ident,first_command_offset=text['new_offset']-5,first_stored_hex=text['stored_hex'],
                    complete_source_preamble_hex=owner['complete_source_preamble_hex'],continuation_encoded_hex=pages[1]['encoded_hex'],pages=pages,
                    unchanged_logical_English=owner['unchanged_logical_English']))
            target,pagination=insert_FE_continuations(arm,intermediate,insertion,inventory);inserted+=len(insertion)
            for i,item in enumerate(insertion):
                rotated=insertion[i:]+insertion[:i]
                all_rejects.append(dict(source_ID=item['source_ID'],rejected=pagination_rejects(arm,intermediate,rotated,inventory)))
            mapping={r['old_offset']:r['new_offset'] for r in pagination['original_command_map']};texts=[]
            for item in proof['text_records']:
                ident=item['id'];key=blockowners[ident]['child_IDs'][0] if ident in blockowners else ident;at=mapping[item['new_offset']-5]+5
                texts.append({**item,'id':key,'source_editorial_ID':ident,'new_offset':at,'new_record_index':target[:at].count(b'\0')})
            for child in pagination['continuations']:
                ident=child['source_ID'];owner=blockowners[ident];at=child['new_command_offset']+5
                texts.append(dict(id=owner['child_IDs'][1],source_editorial_ID=ident,old_offset=next(r for r in rows if r['id']==ident)['current_reference']['offset'],
                    new_offset=at,new_record_index=target[:at].count(b'\0'),source_hex=owner['source_hex'],current_hex=owner['current_hex'],
                    compiled_hex=child['encoded_hex'],stored_hex=child['stored_hex'],parity_space_added=child['stored_hex']!=child['encoded_hex'],native_child_page=2))
            moved=[{**o,'new_offset':mapping[o['new_offset']]} for o in proof['native_objects']]
            commands=inventory(arm,target)[0];byat={c['offset']:c for c in commands}
            commandmap=[{**m,'new_offset':mapping[m['new_offset']],'new_extent':byat[mapping[m['new_offset']]]['native_extent']} for m in proof['command_map']]
            secondfix={f['old_offset']:f for f in pagination['relative_fixups']}
            fixes=[{**f,**{k:secondfix[f['new_offset']][k] for k in ['new_offset','new_span','new_target']}} for f in proof['relative_fixups']]
            (out/f'B{block}_INTERMEDIATE_NOT_PLAYABLE.bin').write_bytes(intermediate)
            proof=dict(proof,text_records=sorted(texts,key=lambda r:r['new_offset']),native_objects=moved,command_map=commandmap,relative_fixups=fixes,
                all_target_commands=commands,new_logical_end=pagination['new_logical_end'],first_page_reconstruction=proof,FE_pagination=pagination)
        if target!=current:changed.append(block)
        blocks[block]=target;path=out/f'B{block}_RESEARCH_ONLY.bin';path.write_bytes(target)
        groups.append(dict(block=block,file_path=source['file_path'],current_sha256=sha(current),clean_sha256=sha(clean),target_sha256=sha(target),
            target_block=str(path),current_bytes=len(current),target_bytes=len(target),**proof))
    assert [g['block'] for g in groups]==source['blocks'] and len(groups)==26 and changed and set(changed)<=set(source['blocks'])
    assert inserted==2 and len(all_rejects)==2 and sum(len(p['rejected']) for p in all_rejects)==14
    result=IlnkContainer(blocks).to_bytes();parsed=IlnkContainer.parse(result)
    assert [i for i,(a,b) in enumerate(zip(container.blocks,parsed.blocks,strict=True)) if a!=b]==changed
    inverse=list(parsed.blocks)
    for block in changed:inverse[block]=container.blocks[block]
    assert IlnkContainer(inverse).to_bytes()==archive
    planned=deepcopy(image);planned.replace_file(source['file_path'],result)
    assert [p for _,p,v in image.iter_files() if planned.read_file(p)!=v]==[source['file_path']]
    assert all(planned.read_file(p)==v for p,v in image.iter_components())
    rom=out/'reviewed_RESEARCH_ONLY.nds';planned.save(rom);reopened=NdsImage.open(rom)
    assert reopened.read_file(source['file_path'])==result and reopened.read_file('/__arm9__.bin')==arm
    reopened.replace_file(source['file_path'],archive);assert bytes(reopened.rom.save())==Path(source['current_ROM']).read_bytes()
    archivepath=out/'reviewed_RESEARCH_ONLY.DK4';archivepath.write_bytes(result)
    assert sum(len(g['text_records']) for g in groups)==295 and sum(len(g['native_objects']) for g in groups)==7
    evidence={str(p):digest(p) for p in [*paths.values(),Path('dk4tool/script/reviewed_scene_rebuild_v3.py'),Path('dk4tool/script/reviewed_FE_pagination_v1.py'),Path(__file__)]}
    save(out/'reconstruction.json',dict(parent=source['current_ROM'],parent_sha256=source['current_ROM_sha256'],
        manuscript=str(paths['physical']),manuscript_sha256=digest(paths['physical']),source_manuscript=str(paths['source']),source_manuscript_sha256=digest(paths['source']),
        plan=str(paths['plan']),plan_sha256=digest(paths['plan']),native=str(bridgednative),native_sha256=digest(bridgednative),
        packet=str(paths['packet']),packet_sha256=digest(paths['packet']),menu=str(bridgedmenus),menu_sha256=digest(bridgedmenus),styles=str(paths['styles']),styles_sha256=digest(paths['styles']),
        source_archive_sha256=sha(archive),target_archive=str(archivepath),target_archive_sha256=sha(result),research_ROM=str(rom),research_ROM_sha256=digest(rom),groups=groups,
        changed_blocks=changed,reviewed_blocks=source['blocks'],unchanged_control_only_blocks=[],source_editorial_objects=330,source_speeches=293,speech_count=295,
        style_physical_speech_count=35,total_rendered_speech_count=330,typed_choice_count=2,compound_objects=7,
        command_count=sum(len(g['all_target_commands']) for g in groups),relative_sites=sum(len(g['relative_fixups']) for g in groups),
        full_clean_current_block_archive_andserialized_NDS_inverses_exact=True,all_other_files_components_exact=True,
        source_owned_exact_FE_controls_repeated_once_per_owner=True,FE_continuation_owners=2,FE_inserted_commands=2,per_owner_FE_pagination_rejections=all_rejects,
        registered_market_runtime_andASCII_right_bound_preserved=True,stored_native_actual_controller_andregistered_release_pending=True,
        not_registered_candidate_or_natural_activation=True,new_credit=0,guide_photos=False,evidence=evidence))
    pins=Path('translations/rom_retention_pins.json');before=pins.read_bytes();values=load(pins)
    assert not any(Path(v['path']).resolve()==rom.resolve() for v in values)
    values.append(dict(path=str(rom.resolve()),reason='Preserve Maria330 complete-exchange research with two exact source-owned FE continuations; not a registered candidate. SHA256 '+digest(rom)))
    (out/'pins.before.json').write_bytes(before);pending=pins.with_name('rom_retention_pins.Maria330.pending.json');assert not pending.exists();save(pending,values)
    assert pins.read_bytes()==before;os.replace(pending,pins)
    print(dict(source_objects=330,physical_bodies=330,reviewed_blocks=26,changed_blocks=len(changed),FE_insertions=inserted,negative_cases=14,
        complete_inverse_pass=True,stored_gameplay_release_pending=True))

if __name__=='__main__':main()
