"""One-block research image from complete V5580;never a playable handoff or parent."""
from pathlib import Path
import json
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_lil_B196_research_v5618 import PARENT,ROM,PLAN
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B196_research_v5619')
STORED=Path('work/analysis/lil_B196_stored_v5616/all24_final_stored_targets96_macro_cases_and_complete_planes.json')

if __name__=='__main__':
    assert not ROOT.exists() and not ROM.exists()
    prior=read('work/analysis/editorial_handoff_verification_v5614/verified_handoff.json')
    plan,stored=map(read,[PLAN,STORED])
    digest=sha(PARENT.read_bytes());assert digest==prior['candidate_sha256']==plan['candidate_sha256']==stored['candidate_sha256']
    assert stored['relocation_plan_sha256']==sha(PLAN.read_bytes()) and plan['manuscript_sha256']==stored['manuscript_sha256']
    assert stored['all24_final_targets_complete_native_planes_equal_reviewed_planes'] and stored['current_final_stored_macro_alignment_cases']==96
    menus=read('work/analysis/lil_B196_stored_choices_v5617/six_final_typed_objects_twelve_references_and_both_even_alignments.json')
    assert menus['candidate_sha256']==digest and menus['relocation_plan_sha256']==sha(PLAN.read_bytes())
    assert menus['all_six_stored_objects_and_twelve_actual_offsets_record_indices_labels_and_counts_exact']
    assert menus['fresh_count_calls']==12 and menus['fresh_label_pointer_calls']==24
    parent,image=NdsImage.open(PARENT),NdsImage.open(PARENT)
    data=Path(plan['target_SC2']).read_bytes();assert sha(data)==plan['target_SC2_sha256']
    assert sha(parent.read_file('/data/SC2.DK4'))==plan['source_SC2_sha256']
    image.replace_file('/data/SC2.DK4',data);image.save(ROM);result=NdsImage.open(ROM)
    assert [p for _,p,v in parent.iter_files() if result.read_file(p)!=v]==['/data/SC2.DK4']
    assert all(result.read_file(p)==v for p,v in parent.iter_components())
    before,after=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks for im in [parent,result]]
    assert len(before)==len(after)==336 and [i for i,(a,b) in enumerate(zip(before,after,strict=True)) if a!=b]==[196]
    ROOT.mkdir(parents=True)
    pins=Path('translations/rom_retention_pins.json');old=pins.read_bytes();values=json.loads(old)
    assert all(Path(v['path']).resolve()!=ROM.resolve() for v in values)
    values.append(dict(path=str(ROM.resolve()),reason='B196 one-block reference/current-font relocation,source/control/gameplay research. Preserve every ROM. SHA256 '+sha(ROM.read_bytes())))
    newline='\r\n' if b'\r\n' in old else '\n'
    encoded=(json.dumps(values,ensure_ascii=False,indent=2)+'\n').replace('\n',newline).encode('utf-8')
    assert pins.read_bytes()==old;pins.write_bytes(encoded)
    save(ROOT/'research_image_receipt.json',dict(parent=str(PARENT),parent_sha256=digest,research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),
        all335_other_SC2_blocks_and_every_other_file_component_exact=True,
        source_relocation_plan=str(PLAN),source_relocation_plan_sha256=sha(PLAN.read_bytes()),stored_target_proof=str(STORED),stored_target_proof_sha256=sha(STORED.read_bytes()),
        all24_final_targets_complete_native_planes_equal_reviewed_planes=True,current_final_stored_macro_alignment_cases=96,
        stored_menu_proof='work/analysis/lil_B196_stored_choices_v5617/six_final_typed_objects_twelve_references_and_both_even_alignments.json',stored_menu_proof_sha256=sha(Path('work/analysis/lil_B196_stored_choices_v5617/six_final_typed_objects_twelve_references_and_both_even_alignments.json').read_bytes()),all6_stored_menus12_labels_bound_before_ROM_mutation=True,registered_candidate=False,not_for_user_handoff_or_new_parent=True,whole_loader_references_relocated_controls_representative_and_release_pending=True,
        actual_selected_B196_IDs=[],new_emulator_runs=0,all_existing_ROMs_and_pins_preserved=True,
        pins_before_sha256=sha(old),pins_after_sha256=sha(encoded),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Pinned one-block B196 research image;335 other blocks and every other file/component exact to V5580. Not a release or new parent.')
