"""Preserve a one-block research reference from complete registered V8377; never a handoff."""
import json,os
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B49_reference_v8403')
PLAN=Path('work/analysis/Hodram_B49_relocation_v8398/reconstruction.json')
INDEPENDENT=Path('work/analysis/Hodram_B49_independent_v8402/independent_reconstruction.json')
STORED=Path('work/analysis/Hodram_B49_stored_v8399/stored_bodies.json')
CONTROLS=Path('work/analysis/Hodram_B49_controls_v8401d/stored_controls.json')
MENU=Path('work/analysis/Hodram_B49_menu_v8400/menu_provider_and_planes.json')
PARENT=Path('out/all_routes_combined_v8377_candidate.nds')
ROM=Path('out/Hodram_B49_reference_v8403_RESEARCH_ONLY.nds')

if __name__=='__main__':
    assert not ROOT.exists() and not ROM.exists()
    plan,independent,stored,controls,menu=map(read,[PLAN,INDEPENDENT,STORED,CONTROLS,MENU])
    candidate=read('translations/editorial_review_current_v1.json')['current_integrated_candidate']
    registry=read('translations/release_stack.json');manifest=read(candidate['manifest'])
    assert sha(PARENT.read_bytes())==candidate['sha256']==plan['candidate_sha256']==stored['candidate_sha256']==controls['candidate_sha256']==menu['candidate_sha256']
    assert candidate['profile']=='all-routes-unified-v8377' and manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert len(manifest['batches'])==642 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert stored['all14_ink_planes_exact_to_already_viewed'] and len(controls['final_dispatches'])==14
    assert independent['whole_target_block_andarchive_byte_equal_to_sparse_rebuild'] and independent['relocation_sha256']==sha(PLAN.read_bytes())
    sheet=menu['review_sheet'];assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    assert menu['reviewed_complete_first_internal_final_glyphs_centering_bounds_andcanaries_pass'] and menu['complete_native_caption_style_planes']==8
    archive=Path(plan['target_archive']).read_bytes();assert sha(archive)==plan['target_archive_sha256']
    parent,image=NdsImage.open(PARENT),NdsImage.open(PARENT);original=parent.read_file('/data/SC1.DK4')
    assert sha(original)==plan['source_archive_sha256']
    image.replace_file('/data/SC1.DK4',archive);payload=bytes(image.rom.save())
    assert [p for _,p,v in parent.iter_files() if image.read_file(p)!=v]==['/data/SC1.DK4']
    assert all(image.read_file(p)==v for p,v in parent.iter_components())
    before=IlnkContainer.parse(original).blocks;after=IlnkContainer.parse(archive).blocks
    assert len(before)==len(after)==325 and [i for i,(a,b) in enumerate(zip(before,after,strict=True)) if a!=b]==[49]
    assert sha(after[49])==plan['groups'][0]['target_block_sha256']
    image.replace_file('/data/SC1.DK4',original);assert bytes(image.rom.save())==PARENT.read_bytes()
    ROOT.mkdir(parents=True)
    save(ROOT/'menu_direct_review.json',dict(native_menu_proof=str(MENU),native_menu_proof_sha256=sha(MENU.read_bytes()),directly_viewed_sheet=sheet,reviewed_two_choices_in_both_current_andproposed_forms=True,reason='All right. is complete andunchanged. No. retains its wording andperiod;removing three storage-onlyspaces centers its visible letters. The original maximum-width provider keeps the same60px caption width andmenu rectangle. Both styles have complete independent native ink. This isoffline native preview,not an actual UI backing orcontroller capture.',formatting_actual_backing_controller_selection_andnormal_dismissal_pending=True,new_credit=0))
    ROM.write_bytes(payload);saved=NdsImage.open(ROM)
    assert saved.read_file('/data/SC1.DK4')==archive and all(saved.read_file(p)==v for p,v in parent.iter_components())
    pins=Path('translations/rom_retention_pins.json');pin_before=pins.read_bytes();values=json.loads(pin_before)
    assert all(Path(v['path']).resolve()!=ROM.resolve() for v in values)
    updated=values+[dict(path=str(ROM.resolve()),reason='B49 complete14speech/twochoice research reference from fullregisteredV8377;onlySC1B49 changes;all324otherblocks/files/components exact;fullROMinverse. Not handoff,newparent,promotion orseparateuserpackage. Preserve every ROM. SHA256 '+sha(payload))]
    encoded=(json.dumps(updated,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf8')
    (ROOT/'pins.before.json').write_bytes(pin_before);assert pins.read_bytes()==pin_before
    with pins.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    assert json.loads(pins.read_bytes())==updated and updated[:-1]==values
    save(ROOT/'research_image_receipt.json',dict(parent=str(PARENT),parent_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(payload),source_relocation_plan=str(PLAN),source_relocation_plan_sha256=sha(PLAN.read_bytes()),only_changed_files=['/data/SC1.DK4'],only_changed_blocks=[49],all324_otherSC1_blocks_andall_other_files_components_exact=True,complete_parent_ROM_inverse_byte_exact=True,independent_reconstruction=str(INDEPENDENT),independent_reconstruction_sha256=sha(INDEPENDENT.read_bytes()),native_menu_direct_review=str(ROOT/'menu_direct_review.json'),native_menu_direct_review_sha256=sha((ROOT/'menu_direct_review.json').read_bytes()),all_prior_ROM_pins_preserved=True,pins_before_sha256=sha(pin_before),pins_after_sha256=sha(encoded),registered_candidate=False,not_for_handoff_ornew_parent=True,loader_caller_actual_policy_atomic_registered_release_andstartup_pending=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [PLAN,INDEPENDENT,STORED,CONTROLS,MENU,Path(__file__)]}))
    print('Pinned B49 research reference from completeV8377. OnlySC1B49 changes;324others/files/components exact;wholeparentROM inverse exact.No promotion orcredit.')
