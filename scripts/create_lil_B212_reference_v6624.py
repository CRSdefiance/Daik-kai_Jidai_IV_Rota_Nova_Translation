"""Pin a reversible one-block research image; no release or new parent approval is implied."""
import json,os
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B212_reference_v6624')
PLAN=Path('work/analysis/lil_B212_relocation_v6622/all14_objects10_spans_three_exact_ends_full884_inverse_RESEARCH.json')
STORED=Path('work/analysis/lil_B212_stored_v6623/all9_final_stored_targets36_alignments_and9_complete_pages.json')
PARENT=Path('out/all_routes_combined_v6584_candidate.nds')
ROM=Path('out/lil_B212_reference_v6624_RESEARCH_ONLY.nds')
if __name__=='__main__':
    assert not ROOT.exists() and not ROM.exists();plan,stored=read(PLAN),read(STORED);digest=sha(PARENT.read_bytes())
    assert digest==plan['candidate_sha256']==stored['candidate_sha256'] and stored['relocation_plan_sha256']==sha(PLAN.read_bytes()) and stored['all_final_stored_targets_equal_reviewed_complete_native_ink']
    parent,image=NdsImage.open(PARENT),NdsImage.open(PARENT);data=Path(plan['target_SC2']).read_bytes();assert sha(data)==plan['target_SC2_sha256'] and sha(parent.read_file('/data/SC2.DK4'))==plan['source_SC2_sha256']
    image.replace_file('/data/SC2.DK4',data);image.save(ROM);saved=NdsImage.open(ROM)
    assert [p for _,p,v in parent.iter_files() if saved.read_file(p)!=v]==['/data/SC2.DK4'] and all(saved.read_file(p)==v for p,v in parent.iter_components())
    before,after=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks for im in [parent,saved]];assert len(before)==len(after)==336 and [i for i,(a,b) in enumerate(zip(before,after,strict=True)) if a!=b]==[212]
    ROOT.mkdir(parents=True);pins=Path('translations/rom_retention_pins.json');old=pins.read_bytes();values=json.loads(old);assert all(Path(v['path']).resolve()!=ROM.resolve() for v in values)
    values.append(dict(path=str(ROM.resolve()),reason='B212 all14 branching dialogue/choice objects, nine single-page progressive speeches, ten relative operands and three exact ends including00000080;all884 predecessor bytes reversible, name asset unchanged. Not a registered release or parent. Preserve every ROM. SHA256 '+sha(ROM.read_bytes())))
    encoded=(json.dumps(values,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8');(ROOT/'pins.before.json').write_bytes(old);assert pins.read_bytes()==old
    with pins.open('r+b') as f:f.write(encoded);f.truncate();f.flush();os.fsync(f.fileno())
    save(ROOT/'research_image_receipt.json',dict(parent=str(PARENT),parent_sha256=digest,research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),source_relocation_plan=str(PLAN),source_relocation_plan_sha256=sha(PLAN.read_bytes()),stored_target_proof=str(STORED),stored_target_proof_sha256=sha(STORED.read_bytes()),all335_other_blocks_and_every_other_file_component_exact=True,all_existing_ROMs_and_pins_preserved=True,pins_before_sha256=sha(old),pins_after_sha256=sha(encoded),registered_candidate=False,not_for_handoff_or_new_parent=True,external_references_current_actual_pages_atomic_release_and_startup_pending=True,new_emulator_runs=0,new_review_credit=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Pinned B212 one-block research image;335 other blocks/all other files/components remain exact. V6584/mainV4701 and all prior ROMs preserved.')
