"""Read clean Japanese neighborhoods before reopening four historical wrap leads."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.review_early_shop_breaks_v4763e import reference
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/earlier_common_wraps_clean_v4975')
TARGETS=[682,764,774,775]
if __name__=='__main__':
    assert not ROOT.exists();clean=Path('work/clean.nds')
    assert sha(clean.read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    image=NdsImage.open(clean);common,arm=image.read_file('/COMMON/MESFILE.DK4'),image.read_file('/__arm9__.bin')
    entries=common_message_entries(common,arm)
    selected=sorted({n for t in TARGETS for n in range(t-3,t+4)})
    rows=[dict(message_ID=n,source_reference=reference(entries[n]),source_hex=entries[n].text.hex(),clean_Japanese=entries[n].text.decode('cp932'),target=n in TARGETS) for n in selected]
    ROOT.mkdir(parents=True);save(ROOT/'clean_only_target_and_neighbor_records.json',dict(clean_ROM=str(clean),clean_ROM_sha256=sha(clean.read_bytes()),
        clean_COMMON_sha256=sha(common),clean_ARM9_sha256=sha(arm),targets=TARGETS,records=rows,
        read_no_predecessor_English=True,new_editorial_credit=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    for r in rows:print(str(r['message_ID'])+(' * ' if r['target'] else '   ')+r['clean_Japanese'])
