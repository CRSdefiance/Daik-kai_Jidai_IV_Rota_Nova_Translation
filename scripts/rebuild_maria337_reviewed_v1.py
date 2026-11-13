"""Reconstruct12 complete SC3 exchanges using the qualified source-bound helper."""
import os
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.script.reviewed_scene_rebuild_v3 import rebuild_block
from dk4tool.dialogue.reviewed_two_choice_object_v1 import compile_choices
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.meaning_maria337_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

def main():
    out=ROOT/'reconstruction_v1'; assert not out.exists()
    paths=dict(source=ROOT/'formatting_v1/formatting_input.json',plan=ROOT/'plan_visual_v5/automatic_plans.json',native=ROOT/'final_native_v1.json',
        packet=ROOT/'current_v1/current_effective.json',objects=ROOT/'current_objects_v1/current_objects.json',
        menu=ROOT/'menu_native_approved_v1.json',styles=ROOT/'compiled_styles_v1/compiled_style_objects.json',approval=ROOT/'offline_display_approval_v1.json')
    d={k:load(p) for k,p in paths.items()}; source,plan,native,packet,objects,menu,styles,approval=[d[k] for k in paths]
    assert (len(source['records']),len(plan['records']),len(native['records']),native['pages'])==(337,335,335,339)
    assert source['blocks']==list(range(125,137)) and approval['all339_final_pages_directly_viewed'] and approval['all_names_andtwo_captions_directly_viewed']
    assert approval['final_native_proof_sha256']==digest(paths['native']) and approval['all_fifth_formatting_gates_still_pending']
    assert native['manuscript_sha256']==plan['manuscript_sha256']==styles['manuscript_sha256']==menu['manuscript_sha256']==digest(paths['source'])
    assert native['plan_sha256']==styles['plan_sha256']==digest(paths['plan'])
    assert all(x['runtime']==source['runtime'] for x in [native,packet,objects,menu,styles])
    assert not styles['objects'] and not objects['style_records'] and not objects['style_objects']
    assert menu['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass'] and len(menu['menus'])==1
    assert all(r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False) for r in source['records'])
    image=NdsImage.open(source['current_ROM']); assert digest(source['current_ROM'])==source['current_ROM_sha256']
    arm=image.read_file('/__arm9__.bin'); assert sha(arm)==source['runtime']['ARM9_sha256']
    archive=image.read_file(source['file_path']); assert sha(archive)==source['current_archive_sha256']==packet['current_archive_sha256']
    container=IlnkContainer.parse(archive); blocks=list(container.blocks); assert len(blocks)==303
    cleanimage=NdsImage.open('work/clean.nds'); cleanblocks=IlnkContainer.parse(cleanimage.read_file(source['file_path'])).blocks
    assert digest('work/clean.nds')=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    plans={r['id']:r for r in plan['records']}; assert all(r['compiled_hex']==plans[r['id']]['encoded_hex'] for r in native['records'])
    ordinary=[deepcopy(r) for r in source['records'] if r['kind']!='typed-choice-label']; typed=[r for r in source['records'] if r['kind']=='typed-choice-label']
    for r in ordinary:r['current_record_index']=r['current_reference']['record_index']
    assert len(ordinary)==335 and len(typed)==2 and all(r.get('native_object_kind') is None for r in ordinary)
    inventory,_,_=scoped_inventory(); groups=[]; changed=[]; out.mkdir()
    for block in source['blocks']:
        group=next(g for g in packet['groups'] if g['block']==block)
        current=blocks[block]; clean=cleanblocks[block]
        assert current==bytes.fromhex(group['current_block_hex']) and clean==bytes.fromhex(group['clean_block_hex'])
        compound=[]
        for obj in menu['menus']:
            if obj['block']!=block:continue
            rows=sorted([r for r in typed if r['block']==block and r['source_command_offset']==obj['source_command_offset']],key=lambda r:r['source_index'])
            before,prior=map(bytes.fromhex,[rows[0]['source_choice_object_hex'],rows[0]['current_choice_object_hex']])
            value=compile_choices(before,prior,rows,require_formatting=False); assert value.hex()==obj['target_object_hex']
            compound.append(dict(id=f'B{block}_C{obj["source_command_offset"]}_menu',word=0x2100,offset=rows[0]['current_reference']['command_offset'],
                source_hex=before.hex(),current_hex=prior.hex(),compiled_hex=value.hex(),records=rows))
        rows=[r for r in ordinary if r['block']==block]
        target,proof=rebuild_block(arm,clean,current,rows,plans,inventory,compound)
        assert len(target)<=9216
        if target!=current:changed.append(block)
        blocks[block]=target; path=out/f'B{block}_RESEARCH_ONLY.bin'; path.write_bytes(target)
        groups.append(dict(block=block,file_path=source['file_path'],current_sha256=sha(current),clean_sha256=sha(clean),target_sha256=sha(target),
            target_block=str(path),current_bytes=len(current),target_bytes=len(target),**proof))
    assert changed==source['blocks'] and len(groups)==12
    result=IlnkContainer(blocks).to_bytes(); parsed=IlnkContainer.parse(result)
    assert [i for i,(a,b) in enumerate(zip(container.blocks,parsed.blocks,strict=True)) if a!=b]==changed
    inverse=list(parsed.blocks)
    for number in changed:inverse[number]=container.blocks[number]
    assert IlnkContainer(inverse).to_bytes()==archive
    planned=deepcopy(image); planned.replace_file(source['file_path'],result)
    assert [p for _,p,v in image.iter_files() if planned.read_file(p)!=v]==[source['file_path']]
    assert all(planned.read_file(p)==v for p,v in image.iter_components())
    rom=out/'reviewed_RESEARCH_ONLY.nds'; planned.save(rom); reopened=NdsImage.open(rom)
    assert reopened.read_file(source['file_path'])==result and reopened.read_file('/__arm9__.bin')==arm
    reopened.replace_file(source['file_path'],archive); assert bytes(reopened.rom.save())==Path(source['current_ROM']).read_bytes()
    archivepath=out/'reviewed_RESEARCH_ONLY.DK4'; archivepath.write_bytes(result)
    assert sum(len(g['text_records']) for g in groups)==335 and sum(len(g['native_objects']) for g in groups)==1
    save(out/'reconstruction.json',dict(parent=source['current_ROM'],parent_sha256=source['current_ROM_sha256'],
        manuscript=str(paths['source']),manuscript_sha256=digest(paths['source']),source_manuscript=str(paths['source']),source_manuscript_sha256=digest(paths['source']),
        plan=str(paths['plan']),plan_sha256=digest(paths['plan']),native=str(paths['native']),native_sha256=digest(paths['native']),packet=str(paths['packet']),packet_sha256=digest(paths['packet']),
        menu=str(paths['menu']),menu_sha256=digest(paths['menu']),styles=str(paths['styles']),styles_sha256=digest(paths['styles']),
        source_archive_sha256=sha(archive),target_archive=str(archivepath),target_archive_sha256=sha(result),research_ROM=str(rom),research_ROM_sha256=digest(rom),
        groups=groups,changed_blocks=changed,reviewed_blocks=source['blocks'],unchanged_control_only_blocks=[],source_editorial_objects=337,source_speeches=335,speech_count=335,
        style_physical_speech_count=0,total_rendered_speech_count=335,typed_choice_count=2,compound_objects=1,FE_continuation_owners=0,FE_inserted_commands=0,
        command_count=sum(len(g['all_target_commands']) for g in groups),relative_sites=sum(len(g['relative_fixups']) for g in groups),
        full_clean_current_block_archive_andserialized_NDS_inverses_exact=True,all_other_files_components_exact=True,
        no_synthetic_FE_commands_or_source_credit=True,registered_market_runtime_andASCII_right_bound_preserved=True,
        stored_native_actual_controller_andregistered_release_pending=True,not_registered_candidate_or_natural_activation=True,new_credit=0,guide_photos=False,
        evidence={str(p):digest(p) for p in [*paths.values(),Path('dk4tool/script/reviewed_scene_rebuild_v3.py'),Path(__file__)]}))
    pins=Path('translations/rom_retention_pins.json'); before=pins.read_bytes(); values=load(pins)
    assert not any(Path(v['path']).resolve()==rom.resolve() for v in values)
    values.append(dict(path=str(rom.resolve()),reason='Preserve Maria337 source-qualified complete-exchange research; not a registered candidate. SHA256 '+digest(rom)))
    (out/'pins.before.json').write_bytes(before); pending=pins.with_name('rom_retention_pins.Maria337.pending.json'); assert not pending.exists(); save(pending,values)
    assert pins.read_bytes()==before; os.replace(pending,pins)
    print(dict(source_objects=337,physical_bodies=335,reviewed_blocks=12,changed_blocks=len(changed),complete_inverse_pass=True,stored_gameplay_release_pending=True))

if __name__=='__main__':main()
