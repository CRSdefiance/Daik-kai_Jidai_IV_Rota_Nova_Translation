"""Uncredited clean-only scope inventory; not a translation or display approval."""
from pathlib import Path
import traceback
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_lessons_v1717 import inventory
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_after_China_clean_scope_v2922')
if __name__=='__main__':
    assert not ROOT.exists();path=Path('work/clean.nds');image=NdsImage.open(path);arm=image.read_file('/__arm9__.bin');sc2=image.read_file('/data/SC2.DK4');blocks=IlnkContainer.parse(sc2).blocks
    assert sha(path.read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    results=[];failures=[]
    for n in [57,58,59,60,61,62,63,64,65,66,121]:
        block=blocks[n]
        try:commands,speeches=inventory(arm,block)
        except AssertionError:
            failures.append(dict(block=n,source_block_sha256=sha(block),diagnostic=traceback.format_exc(),no_object_skipped_or_reviewed=True));continue
        rows=[]
        for command in speeches:
            at=command['offset']+5;raw=block[at:block.index(b'\0',at)]
            rows.append(dict(id=f'DK4_MES_B{n}_R{block[:at].count(bytes([0])):04d}',offset=at,bytes=len(raw),source_hex=raw.hex(),source_preamble_hex=block[at-5:at+1].hex(),prefix=raw[0],Japanese=raw[1:].decode('cp932'),native_extent=command['native_extent'],ancestor_0100_offsets=command['ancestor_0100_offsets']))
        result=dict(block=n,source_block_sha256=sha(block),commands=commands,records=rows,speeches=len(rows),FE_panels=sum(r['prefix']==254 for r in rows),choice_commands=sum(c['word']==0x2100 for c in commands),prefixes=sorted({r['prefix'] for r in rows}))
        results.append(result)
    ROOT.mkdir(parents=True);save(ROOT/'clean_next_exchange_inventory.json',dict(source_ROM=str(path),source_ROM_sha256=sha(path.read_bytes()),source_SC2_sha256=sha(sc2),blocks=results,unclassified=failures,producer_sha256=sha(Path(__file__).read_bytes()),editorial_credit_added=0,not_a_manuscript_or_native_consumer_approval=True,full_goal_complete=False))
    print([(r['block'],len(r['commands']),r['speeches'],r['FE_panels'],r['choice_commands'],r['prefixes']) for r in results]);print('Unclassified blocks:',[r['block'] for r in failures]);print('Clean-only scope inventory;zero editorial credit.')
