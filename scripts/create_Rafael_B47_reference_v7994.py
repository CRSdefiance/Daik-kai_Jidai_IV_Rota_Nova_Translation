"""Preserve the exact research reference for targeted checks; never a registered handoff or new parent."""
import json,os
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B47_reference_v7994')
PLAN=Path('work/analysis/Rafael_B47_relocation_v7989/one_block15_speeches24_relative_fixups120_cases_exact_full_inverse.json')
STORED=Path('work/analysis/Rafael_B47_stored_v7990/all15_stored_bodies32_fresh28_reused_alignments16_exact_viewed_pages.json')
CONTROLS=Path('work/analysis/Rafael_B47_relocated_controls_v7991/15_stored_dispatches6_raw_predicates120_relative_cases25_seeded_ends.json')
VIEW=Path('work/analysis/Rafael_B47_native_review_v7988/15_paragraphs16_native_pages4_names_two_scoped_warnings_individual_wrap_review.json')
PARENT=Path('out/all_routes_combined_v7964_candidate.nds')
ROM=Path('out/Rafael_B47_reference_v7994_RESEARCH_ONLY.nds')
if __name__=='__main__':
    assert not ROOT.exists() and not ROM.exists();plan,stored,controls,view=map(read,[PLAN,STORED,CONTROLS,VIEW])
    candidate=read('translations/editorial_review_current_v1.json')['current_integrated_candidate']
    registry=read('translations/release_stack.json');manifest=read(candidate['manifest'])
    assert sha(PARENT.read_bytes())==candidate['sha256']==plan['candidate_sha256']==stored['candidate_sha256']==controls['candidate_sha256']
    assert candidate['profile']=='all-routes-unified-v7964' and manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert len(manifest['batches'])==635 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert stored['relocation_sha256']==sha(PLAN.read_bytes()) and stored['all15_native_ink_planes_exact_to_already_viewed']
    assert len(view['directly_viewed_sheets'])==4 and all(s['directly_viewed'] for s in view['directly_viewed_sheets'])
    assert len(controls['final_dispatches'])==15
    archive=Path(plan['target_archive']).read_bytes();assert sha(archive)==plan['target_archive_sha256']
    parent,image=NdsImage.open(PARENT),NdsImage.open(PARENT);assert sha(parent.read_file(plan['file_path']))==plan['source_archive_sha256']
    image.replace_file(plan['file_path'],archive);image.save(ROM);saved=NdsImage.open(ROM)
    assert [p for _,p,v in parent.iter_files() if saved.read_file(p)!=v]==['/data/SC0.DK4']
    assert all(saved.read_file(p)==v for p,v in parent.iter_components())
    a,b=[IlnkContainer.parse(im.read_file(plan['file_path'])).blocks for im in [parent,saved]]
    assert len(a)==len(b)==343 and [i for i,(x,y) in enumerate(zip(a,b,strict=True)) if x!=y]==[47]
    assert sha(b[47])==plan['groups'][0]['target_block_sha256']
    ROOT.mkdir(parents=True);pins=Path('translations/rom_retention_pins.json');before=pins.read_bytes();values=json.loads(before)
    assert all(Path(v['path']).resolve()!=ROM.resolve() for v in values)
    updated=values+[dict(path=str(ROM.resolve()),reason='Rafael B46 complete15-speech/16-page research reference from currentV7964,exact inverses/24 relocated spans/all stored/native checks. OnlyB47 changes. Unregistered research,not separate test package,new parent,promotion orhandoff. Preserve every ROM. SHA256 '+sha(ROM.read_bytes()))]
    encoded=(json.dumps(updated,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf8')
    (ROOT/'pins.before.json').write_bytes(before);assert pins.read_bytes()==before
    with pins.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    assert json.loads(pins.read_bytes())==updated and updated[:-1]==values
    save(ROOT/'research_image_receipt.json',dict(parent=str(PARENT),parent_sha256=sha(PARENT.read_bytes()),
        research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),source_relocation_plan=str(PLAN),source_relocation_plan_sha256=sha(PLAN.read_bytes()),
        stored_proof=str(STORED),stored_proof_sha256=sha(STORED.read_bytes()),only_changed_files=['/data/SC0.DK4'],only_changed_blocks=[47],
        all342_otherSC0_blocks_andall_other_files_components_exact=True,all_prior_ROM_pins_preserved=True,
        pins_before_sha256=sha(before),pins_after_sha256=sha(encoded),registered_candidate=False,not_for_handoff_ornew_parent=True,
        source_headers_andall_controls_preserved_except_mapped_lengths_andreviewed_prose=True,
        full_loader_caller_actual_policy_production_registered_release_andstartup_pending=True,
        evidence={str(p):sha(p.read_bytes()) for p in [PLAN,STORED,CONTROLS,VIEW,Path(__file__)]},
        new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('Pinned B47 research reference. OnlySC0 B47 changes;342others/allotherfiles/components exact. CurrentV7964/mainV4701 unchanged.')
