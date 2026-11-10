"""Prepare tested block payloads; wait for the current cumulative build before ROM composition."""
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.script.rafael_story_rebuild_with_fu_v1 import rebuild_block
from scripts.audit_story_glyph_consistency import load,save
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory

ROOT=Path('work/analysis/Rafael_B36_B41_stored_blocks_20261104')
DOC=Path('work/analysis/Rafael_B36_B41_formatting_20261104/formatting_input.json')
PLAN=DOC.parent/'speech_display_approved_v3/all175_compiled_plans.json'
NATIVE=DOC.parent/'speech_display_approved_v3/all175_native_pages.json'
PACKET=Path('work/analysis/Rafael_B36_B41_current_20261104/current_effective.json')

if __name__=='__main__':
    assert not ROOT.exists()
    doc,plans,native,packet=map(load,[DOC,PLAN,NATIVE,PACKET])
    assert len(doc['records'])==len(plans['records'])==len(native['records'])==175
    assert plans['manuscript_sha256']==native['manuscript_sha256']==sha(DOC.read_bytes()) and native['plan_sha256']==sha(PLAN.read_bytes())
    assert not plans['failures'] and native['all177_final_pages_directly_viewed']
    image=NdsImage.open(doc['current_ROM'])
    assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']==native['runtime']['candidate_sha256']
    archive=image.read_file(doc['file_path']);assert sha(archive)==doc['current_archive_sha256']==packet['current_archive_sha256']
    bank=IlnkContainer.parse(archive).blocks
    assert len(bank)==343
    inventory,_,_=scoped_inventory()
    compiled={r['id']:r for r in plans['records']}
    ROOT.mkdir()
    groups=[]
    for group in packet['groups']:
        number=group['block'];clean=bytes.fromhex(group['clean_block_hex']);current=bank[number]
        assert sha(current)==group['current_block_sha256'] and sha(clean)==group['clean_block_sha256']
        assert inventory(image.read_file('/__arm9__.bin'),current)[0]==group['all_current_commands']
        assert inventory(image.read_file('/__arm9__.bin'),clean)[0]==group['all_source_commands']
        target,proof=rebuild_block(image.read_file('/__arm9__.bin'),clean,current,[r for r in doc['records'] if r['block']==number],compiled,inventory)
        path=ROOT/f'B{number}_RESEARCH_ONLY.bin'
        path.write_bytes(target)
        groups.append(dict(block=number,file_path=doc['file_path'],clean_sha256=sha(clean),current_sha256=sha(current),target_sha256=sha(target),
            target_block=str(path),current_bytes=len(current),target_bytes=len(target),**proof))
    assert [g['block'] for g in groups]==list(range(36,42))
    save(ROOT/'block_reconstruction.json',dict(parent=doc['current_ROM'],parent_sha256=doc['current_ROM_sha256'],
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),plan=str(PLAN),plan_sha256=sha(PLAN.read_bytes()),
        native=str(NATIVE),native_sha256=sha(NATIVE.read_bytes()),packet=str(PACKET),packet_sha256=sha(PACKET.read_bytes()),
        source_archive_sha256=sha(archive),groups=groups,speech_count=175,relative_sites=sum(len(g['relative_fixups']) for g in groups),
        command_count=sum(len(g['command_map']) for g in groups),no_ROM_orwhole_archive_created=True,
        complete_clean_current_block_inverses_pass=True,whole_archive_NDS_composition_andinverse_pending=True,
        compose_only_after_current_registered_tutorial_build_andown_startup_pass=True,new_credit=0,guide_photos=False,
        producers={str(p):sha(p.read_bytes()) for p in [Path(__file__),Path('dk4tool/script/rafael_story_rebuild_with_fu_v1.py'),Path('dk4tool/script/reviewed_scene_rebuild.py')]}))
    print('Six block payloads/175 speeches/',sum(len(g['relative_fixups']) for g in groups),'relative operands;complete block inverses pass;no ROM composed.')
