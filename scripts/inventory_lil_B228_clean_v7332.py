"""Preserve the entire next clean-Japanese block before exposing old English."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B228_clean_inventory_v7332')
if __name__=='__main__':
    assert not ROOT.exists();clean=Path('work/clean.nds');image=NdsImage.open(clean)
    arm=image.read_file('/__arm9__.bin');file=image.read_file('/data/SC2.DK4');block=IlnkContainer.parse(file).blocks[228]
    inventory,walker,inventory_source=scoped_inventory();commands,speeches=inventory(arm,block);rows=[]
    for speech in speeches:
        at=speech['offset']+5;end=block.index(0,at+1);raw=block[at:end]
        r=dict(source_record_index=block[:at].count(b'\0'),header_offset=at-5,offset=at,bytes=len(raw),
            source_selector=raw[0],source_hex=raw.hex(),complete_preamble_hex=block[at-5:at+1].hex(),
            Japanese=raw[1:].decode('cp932'),native_extent=speech['native_extent'])
        rows.append(r)
    ROOT.mkdir(parents=True)
    save(ROOT/'all_clean_B228_speeches_before_predecessor_comparison.json',dict(
        source_ROM=str(clean),source_ROM_sha256=sha(clean.read_bytes()),file_path='/data/SC2.DK4',block=228,
        clean_ARM9_sha256=sha(arm),clean_SC2_sha256=sha(file),clean_block_sha256=sha(block),clean_block_hex=block.hex(),
        clean_stored_bytes=len(block),commands=commands,records=rows,
        physical_speech_objects=len(rows),typed_choice_or_actor_style_commands=[c for c in commands if c['word'] in [0x2100,0x2200,0x4100]],
        source_controls=list(sorted({c['word'] for c in commands})),
        clean_inventory_walker=walker,clean_inventory_function=inventory_source,
        read_no_predecessor_English=True,new_emulator_runs=0,new_review_credit=0,
        source_context_gloss_and_all_editorial_gates_pending=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    for r in rows:print(r['source_record_index'],format(r['source_selector'],'02X'),r['Japanese'].replace('\n',' / '))
    print(dict(stored_bytes=len(block),commands=len(commands),speeches=len(rows),no_old_English_read=True,credit=0))
