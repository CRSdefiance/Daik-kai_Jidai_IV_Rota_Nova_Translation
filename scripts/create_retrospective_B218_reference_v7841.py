"""Pin a reversible one-block research image; no release or new parent approval is implied."""
import json,os
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/retrospective_B218_reference_v7841')
PLAN=Path('work/analysis/retrospective_B218_relocation_v7839b/all13_bound_one_changed_wrap15_commands_complete_clean_predecessor_inverse.json')
STORED=Path('work/analysis/retrospective_B218_stored_controls_v7840/one_changed_stored_plane13_dispatches_A00025_ends_andtwo_sheets_viewed.json')
PARENT=Path('out/all_routes_combined_v7821_candidate.nds')
ROM=Path('out/lil_B218_wrap_reference_v7841_RESEARCH_ONLY.nds')
if __name__=='__main__':
    assert not ROOT.exists() and not ROM.exists();plan,stored=read(PLAN),read(STORED);digest=sha(PARENT.read_bytes())
    assert digest==plan['candidate_sha256']==stored['candidate_sha256'] and stored['relocation_map_sha256']==sha(PLAN.read_bytes()) and stored['changed_parity_tail_zero_ink_complete_characters_bounds_andconsumption']
    parent,image=NdsImage.open(PARENT),NdsImage.open(PARENT);data=Path(plan['target_archive']).read_bytes();assert sha(data)==plan['target_archive_sha256'] and sha(parent.read_file('/data/SC2.DK4'))==plan['source_archive_sha256']
    image.replace_file('/data/SC2.DK4',data);image.save(ROM);saved=NdsImage.open(ROM)
    assert [p for _,p,v in parent.iter_files() if saved.read_file(p)!=v]==['/data/SC2.DK4'] and all(saved.read_file(p)==v for p,v in parent.iter_components())
    before,after=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks for im in [parent,saved]];assert len(before)==len(after)==336 and [i for i,(a,b) in enumerate(zip(before,after,strict=True)) if a!=b]==[218]
    ROOT.mkdir(parents=True);pins=Path('translations/rom_retention_pins.json');old=pins.read_bytes();values=json.loads(old);assert all(Path(v['path']).resolve()!=ROM.resolve() for v in values)
    values.append(dict(path=str(ROM.resolve()),reason='B218 retrospective R27 automatic-wrap research;13 source-bound speeches/15 original commands,one fresh changed native page/12 unchanged stored bodies,no relatives;complete1016-byte predecessor block inverse,name assets unchanged. Not a registered release or parent. Preserve every ROM. SHA256 '+sha(ROM.read_bytes())))
    encoded=(json.dumps(values,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8');(ROOT/'pins.before.json').write_bytes(old);assert pins.read_bytes()==old
    with pins.open('r+b') as f:f.write(encoded);f.truncate();f.flush();os.fsync(f.fileno())
    save(ROOT/'research_image_receipt.json',dict(parent=str(PARENT),parent_sha256=digest,research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),source_relocation_plan=str(PLAN),source_relocation_plan_sha256=sha(PLAN.read_bytes()),stored_target_proof=str(STORED),stored_target_proof_sha256=sha(STORED.read_bytes()),all335_other_blocks_and_every_other_file_component_exact=True,all_existing_ROMs_and_pins_preserved=True,pins_before_sha256=sha(old),pins_after_sha256=sha(encoded),registered_candidate=False,not_for_handoff_or_new_parent=True,external_references_current_actual_pages_atomic_release_and_startup_pending=True,new_emulator_runs=0,new_review_credit=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Pinned B218 one-block research image;335 other blocks/all other files/components remain exact. V7821/mainV4701 and all prior ROMs preserved.')
