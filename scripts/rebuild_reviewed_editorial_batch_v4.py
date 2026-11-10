"""Materialize complete reviewed speeches, personality objects and menus in research."""
import argparse
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.reviewed_scene_rebuild_v3 import rebuild_block
from dk4tool.dialogue.reviewed_choice_object_v2 import compile_choices
from dk4tool.dialogue.reviewed_actor_style_object_v1 import compile_styles
from scripts.audit_story_glyph_consistency import load,save
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for arg in ['manuscript','plan','packet','native','menu','styles','out']:parser.add_argument('--'+arg,type=Path,required=True)
    args=parser.parse_args();assert not args.out.exists()
    doc,layout,packet,native,menu,styles=map(load,[args.manuscript,args.plan,args.packet,args.native,args.menu,args.styles])
    digest=sha(args.manuscript.read_bytes())
    assert layout['manuscript_sha256']==native['manuscript_sha256']==menu['manuscript_sha256']==styles['manuscript_sha256']==digest
    assert native['plan_sha256']==styles['plan_sha256']==sha(args.plan.read_bytes())
    assert len(doc['records'])==323 and doc['physical_speech_objects']==len(layout['records'])==len(native['records'])==308 and not layout['failures']
    assert menu['offline_visual_approved'] and not menu['direct_view_pending']
    ordinary=[r for r in doc['records'] if r['kind'] in ['progressive','system-FE'] and r.get('native_object_kind')!='4100-style-alternative']
    alternatives=[r for r in doc['records'] if r.get('native_object_kind')=='4100-style-alternative']
    typed=[r for r in doc['records'] if r['kind']=='typed-choice-label']
    assert (len(ordinary),len(alternatives),len(typed))==(260,48,15)
    image=NdsImage.open(doc['current_ROM']);assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']==native['runtime']['candidate_sha256']
    assert menu['runtime']==styles['runtime']==native['runtime']
    arm=image.read_file('/__arm9__.bin');archive=image.read_file(doc['file_path'])
    assert sha(arm)==native['runtime']['ARM9_sha256'] and sha(archive)==doc['current_archive_sha256']==packet['current_archive_sha256']
    container=IlnkContainer.parse(archive);blocks=list(container.blocks);inventory,_,_=scoped_inventory()
    compiled={r['id']:r for r in layout['records']};args.out.mkdir(parents=True)
    groups=[];changed=[]
    for group in packet['groups']:
        block=group['block'];current=blocks[block];clean=bytes.fromhex(group['clean_block_hex'])
        assert current.hex()==group['current_block_hex'] and sha(current)==group['current_block_sha256'] and sha(clean)==group['clean_block_sha256']
        assert inventory(arm,current)[0]==group['all_current_commands'] and inventory(arm,clean)[0]==group['all_source_commands']
        compound=[]
        for proof in menu['menus']:
            if proof['block']!=block:continue
            rows=sorted([r for r in typed if r['block']==block and r['source_command_offset']==proof['source_command_offset']],key=lambda r:r['source_index'])
            source,prior=map(bytes.fromhex,[rows[0]['source_choice_object_hex'],rows[0]['current_choice_object_hex']])
            value=compile_choices(source,prior,rows,require_formatting=False);assert value.hex()==proof['target_object_hex']
            compound.append(dict(id=f'B{block}_C{proof["source_command_offset"]}_menu',word=0x2200,
                offset=rows[0]['current_reference']['command_offset'],source_hex=source.hex(),current_hex=prior.hex(),compiled_hex=value.hex(),records=rows))
        for proof in styles['objects']:
            if proof['block']!=block:continue
            rows=sorted([r for r in alternatives if r['block']==block and r['source_command_offset']==proof['source_command_offset']],key=lambda r:r['source_reference']['offset'])
            source,prior=map(bytes.fromhex,[proof['source_object_hex'],proof['current_object_hex']])
            value=compile_styles(source,prior,rows,compiled,require_formatting=False);assert value.hex()==proof['target_object_hex']
            compound.append(dict(id=f'B{block}_C{proof["source_command_offset"]}_styles',word=0x4100,
                offset=proof['current_command_offset'],source_hex=source.hex(),current_hex=prior.hex(),compiled_hex=value.hex(),records=rows))
        records=[r for r in ordinary if r['block']==block]
        target,proof=rebuild_block(arm,clean,current,records,compiled,inventory,compound)
        if target!=current:changed.append(block)
        else:assert block==128 and not records and not compound and current==clean
        blocks[block]=target;path=args.out/f'B{block}_RESEARCH_ONLY.bin';path.write_bytes(target)
        groups.append(dict(block=block,file_path=doc['file_path'],current_sha256=sha(current),clean_sha256=sha(clean),target_sha256=sha(target),
            target_block=str(path),current_bytes=len(current),target_bytes=len(target),**proof))
    assert [g['block'] for g in groups]==doc['blocks'] and len(changed)==19
    result=IlnkContainer(blocks).to_bytes();parsed=IlnkContainer.parse(result)
    assert [i for i,(a,b) in enumerate(zip(container.blocks,parsed.blocks,strict=True)) if a!=b]==changed
    inverse=list(parsed.blocks)
    for block in changed:inverse[block]=container.blocks[block]
    assert IlnkContainer(inverse).to_bytes()==archive
    planned=deepcopy(image);planned.replace_file(doc['file_path'],result)
    assert [p for _,p,data in image.iter_files() if planned.read_file(p)!=data]==[doc['file_path']]
    assert all(planned.read_file(p)==data for p,data in image.iter_components())
    restored=deepcopy(planned);restored.replace_file(doc['file_path'],archive);assert bytes(restored.rom.save())==bytes(image.rom.save())
    archivepath=args.out/'reviewed_RESEARCH_ONLY.DK4';archivepath.write_bytes(result)
    rom=args.out/'reviewed_RESEARCH_ONLY.nds';rom.write_bytes(bytes(planned.rom.save()))
    reopened=NdsImage.open(rom);assert reopened.read_file(doc['file_path'])==result and reopened.read_file('/__arm9__.bin')==arm
    save(args.out/'reconstruction.json',dict(parent=doc['current_ROM'],parent_sha256=doc['current_ROM_sha256'],
        manuscript=str(args.manuscript),manuscript_sha256=digest,plan=str(args.plan),plan_sha256=sha(args.plan.read_bytes()),
        packet=str(args.packet),packet_sha256=sha(args.packet.read_bytes()),native=str(args.native),native_sha256=sha(args.native.read_bytes()),
        menu=str(args.menu),menu_sha256=sha(args.menu.read_bytes()),styles=str(args.styles),styles_sha256=sha(args.styles.read_bytes()),
        source_archive_sha256=sha(archive),target_archive=str(archivepath),target_archive_sha256=sha(result),research_ROM=str(rom),research_ROM_sha256=sha(rom.read_bytes()),
        groups=groups,changed_blocks=changed,reviewed_blocks=doc['blocks'],unchanged_control_only_blocks=[128],speech_count=260,
        style_physical_speech_count=48,total_rendered_speech_count=308,typed_choice_count=15,compound_objects=13,
        command_count=sum(len(g['command_map']) for g in groups),relative_sites=sum(len(g['relative_fixups']) for g in groups),
        unchanged_blocks=len(blocks)-len(changed),all_other_files_components_exact=True,full_clean_current_block_archive_andserialized_NDS_inverses_exact=True,
        registered_right_bound_runtime_andprevious_name_fields_preserved=True,stored_native_pages_gameplay_andregistered_release_pending=True,new_credit=0,
        producers={str(p):sha(p.read_bytes()) for p in [Path(__file__),Path('dk4tool/script/reviewed_scene_rebuild.py'),Path('dk4tool/script/reviewed_scene_rebuild_v2.py'),Path('dk4tool/script/reviewed_scene_rebuild_v3.py')]}))
    pins=Path('translations/rom_retention_pins.json');saved=load(pins);absolute=str(rom.resolve())
    if not any(p['path']==absolute for p in saved):saved.append(dict(path=absolute,reason='B111-B130 complete source-bound reconstruction; keep for ongoing editorial/storage/gameplay and registered release proofs.'))
    save(pins,saved)
    print(dict(ordinary_speeches=260,style_alternatives=48,menu_labels=15,changed_blocks=19,commands=sum(len(g['command_map']) for g in groups),relative_sites=sum(len(g['relative_fixups']) for g in groups),research_ROM=str(rom),sha256=sha(rom.read_bytes())),flush=True)

if __name__=='__main__':main()
