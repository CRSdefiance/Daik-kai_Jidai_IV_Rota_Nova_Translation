"""Create and retain the exact combined approved target, without promotion or review credit."""
import json,os
from pathlib import Path
from dk4tool.patch import lil_B210_editorial_v1 as story,Al_Ferid_name_release_v1 as name
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/B210_Ferid_reference_v6539');ROM=Path('out/B210_Ferid_reference_v6539_RESEARCH_ONLY.nds');PARENT=Path('out/all_routes_combined_v6488_candidate.nds')
if __name__=='__main__':
    assert not ROOT.exists() and not ROM.exists();receipts=[read(f'work/analysis/{p}/atomic_validation_receipt.json') for p in ['lil_B210_atomic_v6535','Al_Ferid_atomic_v6538']]
    assert [r['negative_count'] for r in receipts]==[117,69] and all(r['all_negatives_reject_before_mutation'] for r in receipts);baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');image=NdsImage.open(PARENT);before=NdsImage.open(PARENT)
    proofs=[]
    for module,receipt in zip([story,name],receipts,strict=True):
        assert sha(Path(receipt['config']).read_bytes())==receipt['config_sha256'];proofs.append(module.apply_release(image,baseline,receipt['config']))
    assert [p for _,p,v in before.iter_files() if image.read_file(p)!=v]==[story.PATH] and [p for p,v in before.iter_components() if image.read_file(p)!=v]==[name.PATH]
    image.save(ROM);saved=NdsImage.open(ROM);assert all(saved.read_file(p)==v for _,p,v in image.iter_files()) and all(saved.read_file(p)==v for p,v in image.iter_components());ROOT.mkdir(parents=True)
    pins=Path('translations/rom_retention_pins.json');old=pins.read_bytes();values=json.loads(old);assert not any(Path(r['path']).resolve()==ROM.resolve() for r in values);values.append(dict(path=str(ROM.resolve()),reason='Approved combined B210 ten-record dialogue and actor17 Ferid typography reference;not registered or promoted. Preserve all prior artifacts. SHA256 '+sha(ROM.read_bytes())));encoded=(json.dumps(values,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode();(ROOT/'pins.before.json').write_bytes(old);assert pins.read_bytes()==old
    with pins.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    assert json.loads(pins.read_bytes())[:-1]==json.loads(old)
    save(ROOT/'combined_reference_receipt.json',dict(parent=str(PARENT),parent_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),SC2_sha256=sha(saved.read_file(story.PATH)),ARM9_sha256=sha(saved.read_file(name.PATH)),COMMON_sha256=sha(saved.read_file('/COMMON/MESFILE.DK4')),stage_proofs=proofs,all_other_files_components_exact=True,only_ten_source_bound_dialogue_records_and_five_owned_name_bytes_changed=True,all_earlier_pins_ROMs_translations_and_proofs_preserved=True,registered_cumulative_build_clean_input_patch_and_current_startup_pending=True,new_review_credit=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('Combined approved B210/Ferid reference saved and pinned; exact dialogue target and five-byte name asset, all other files/components unchanged.')
