"""Build/pin coordinated title/description storage research with explicit growth hazard."""
import json,os
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.shachihoko_item116_research_v1 import transform
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/shachihoko_item116_research_v6094')
DOC=Path('translations/shachihoko_item116_editorial_manuscript_v1.json')
BIND=Path('work/analysis/shachihoko_description_consumers_v6092/current218_live_description_getters_two_item_callers_and_exact_owned_representations.json')
ROM=Path('out/shachihoko_item116_v6094_expanded_RESEARCH_ONLY.nds')
if __name__=='__main__':
    assert not ROOT.exists() and not ROM.exists();doc,binding=map(read,[DOC,BIND]);parent_path=Path(doc['current_ROM']);assert sha(parent_path.read_bytes())==doc['current_ROM_sha256']
    before=NdsImage.open(parent_path);clean=NdsImage.open('work/clean.nds');arm,common,plan=transform(before.read_file('/__arm9__.bin'),before.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'),doc,binding)
    image=NdsImage.open(parent_path);image.replace_file('/__arm9__.bin',arm);image.replace_file('/COMMON/MESFILE.DK4',common);image.save(ROM);after=NdsImage.open(ROM)
    assert [p for _,p,v in before.iter_files() if after.read_file(p)!=v]==['/COMMON/MESFILE.DK4'] and [p for p,v in before.iter_components() if after.read_file(p)!=v]==['/__arm9__.bin']
    ROOT.mkdir(parents=True);(ROOT/'target_ARM9.bin').write_bytes(arm);(ROOT/'target_COMMON.bin').write_bytes(common)
    save(ROOT/'coordinated_research_receipt.json',dict(parent=str(parent_path),parent_sha256=sha(parent_path.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),binding=str(BIND),binding_sha256=sha(BIND.read_bytes()),data_plan=plan,
        actual_boot_compatibility_native_consumers_full_fonts_and_registered_release_pending=True,
        no_handoff_or_new_integrated_parent_claim=True,new_review_credit=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [DOC,BIND,Path(__file__),Path('dk4tool/patch/shachihoko_item116_research_v1.py')]}))
    pins=Path('translations/rom_retention_pins.json');raw=pins.read_bytes();values=json.loads(raw);assert not any(Path(r['path']).resolve()==ROM.resolve() for r in values)
    added=dict(path=str(ROM.resolve()),reason='Coordinated item116 title/COMMON+compiled description expansion research;known growth startup risk unverified. Preserve every ROM. SHA256 '+sha(ROM.read_bytes()))
    encoded=(json.dumps(values+[added],ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8');(ROOT/'pins.before.json').write_bytes(raw);assert pins.read_bytes()==raw
    with pins.open('r+b') as f:f.write(encoded);f.truncate();f.flush();os.fsync(f.fileno())
    save(ROOT/'pin_receipt.json',dict(new_ROM=str(ROM),new_ROM_sha256=sha(ROM.read_bytes()),all_prior_pins_preserved=True,pins_before_sha256=sha(raw),pins_after_sha256=sha(encoded),ROMs_deleted=0,full_goal_complete=False))
    print(dict(research_ROM=str(ROM),payload_before=plan['original_payload_bytes'],payload_after=plan['new_payload_bytes'],COMMON_delta=plan['COMMON_delta'],compiled_rows=plan['compiled_rows'],boot_and_native_checks_pending=True))
