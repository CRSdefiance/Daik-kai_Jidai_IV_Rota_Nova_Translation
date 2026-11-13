"""Create/pin a data-only three-label research image from the full cumulative parent."""
import json,os
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.generic_speaker_label_data_v1 import transform
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/generic_speaker_labels_research_v5881')
DOC=Path('translations/generic_speaker_labels_manuscript_v1.json')
ROM=Path('out/generic_speaker_labels_v5881_RESEARCH_ONLY.nds')
if __name__=='__main__':
    assert not ROOT.exists() and not ROM.exists();doc=read(DOC);source=Path(doc['current_ROM']);assert sha(source.read_bytes())==doc['current_ROM_sha256']
    before=NdsImage.open(source);clean=NdsImage.open('work/clean.nds');arm,plan=transform(before.read_file('/__arm9__.bin'),clean.read_file('/__arm9__.bin'),doc['records'])
    assert arm==Path(doc['target_ARM9']).read_bytes() and sha(arm)==doc['target_ARM9_sha256'] and plan==doc['data_plan']
    image=NdsImage.open(source);image.replace_file('/__arm9__.bin',arm);image.save(ROM);after=NdsImage.open(ROM)
    assert [p for _,p,v in before.iter_files() if after.read_file(p)!=v]==[]
    assert [p for p,v in before.iter_components() if after.read_file(p)!=v]==['/__arm9__.bin']
    assert after.read_file('/__arm9__.bin')==arm
    ROOT.mkdir(parents=True);pins=Path('translations/rom_retention_pins.json');raw=pins.read_bytes();values=json.loads(raw)
    assert not any(Path(r['path']).resolve()==ROM.resolve() for r in values)
    added=dict(path=str(ROM.resolve()),reason='Source-owned Man/Woman/Stranger data-only native/display research. Preserve every ROM. SHA256 '+sha(ROM.read_bytes()))
    encoded=(json.dumps(values+[added],ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8');(ROOT/'pins.before.json').write_bytes(raw)
    assert pins.read_bytes()==raw
    with pins.open('r+b') as f:f.write(encoded);f.truncate();f.flush();os.fsync(f.fileno())
    save(ROOT/'research_image_receipt.json',dict(parent=str(source),parent_sha256=sha(source.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),changed_components=['/__arm9__.bin'],changed_files=[],data_plan=plan,
        all_story_dialogue_UI_graphics_fonts_and_other_components_exact_to_registered_V5872=True,
        no_name_table_pointer_native_instruction_or_allocation_change=True,no_registered_candidate_or_new_parent_claim=True,
        target_native_consumers_first_last_glyphs_substitutions_and_representative_scenes_pending=True,
        new_pin=added,all_prior_pins_ROMs_translations_and_proofs_preserved=True,pins_before_sha256=sha(raw),pins_after_sha256=sha(encoded),
        producer_sha256=sha(Path(__file__).read_bytes()),new_emulator_runs=0,new_name_completion_credit=0,full_goal_complete=False))
    print('Pinned three-label data-only research ROM;all files and all non-ARM9 components exact to V5872. Target native/display/release checks pending.')
