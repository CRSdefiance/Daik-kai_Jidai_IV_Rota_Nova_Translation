"""Pin seven-block research image from complete V8778; never a handoff candidate."""
import json,os
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B54_B60_reference_v8812')
PARENT=Path('out/all_routes_combined_v8778_candidate.nds')
ROM=Path('out/Hodram_B54_B60_reference_v8812_RESEARCH_ONLY.nds')
PLAN=Path('work/analysis/Hodram_B54_B60_relocation_v8809/reconstruction.json')
INDEPENDENT=Path('work/analysis/Hodram_B54_B60_independent_v8810/independent_reconstruction.json')
STORED=Path('work/analysis/Hodram_B54_B60_stored_v8811/stored_pages_controls_andreferences.json')
DOC=Path('translations/hodram_B54_B60_editorial_manuscript_v2.json')
NAMES=Path('translations/hodram_B54_B60_speaker_name_review_v1.json')

if __name__=='__main__':
    assert not ROOT.exists() and not ROM.exists();plan,independent,stored,doc,names=map(read,[PLAN,INDEPENDENT,STORED,DOC,NAMES])
    assert plan['manuscript_sha256']==independent['manuscript_sha256']==stored['manuscript_sha256']==sha(DOC.read_bytes())
    assert sha(NAMES.read_bytes())==doc['names_packet_sha256'] and len(names['records'])==10
    assert all(all(r['review'][k] for k in ['source','context','localization','naturalness']) for r in names['records'])
    candidate=read('translations/editorial_review_current_v1.json')['current_integrated_candidate'];registry=read('translations/release_stack.json');manifest=read(candidate['manifest'])
    assert candidate['profile']=='all-routes-unified-v8778' and sha(PARENT.read_bytes())==candidate['sha256']==doc['current_ROM_sha256']==plan['candidate_sha256']==stored['candidate_sha256']
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes()) and len(manifest['batches'])==647 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert independent['whole_target_blocks_andarchive_byte_equal_to_sparse_rebuild'] and stored['all82_complete_leading_internal_final_glyphs_independent_planes_bounds_consumption_andpagination_pass']
    parent,image=NdsImage.open(PARENT),NdsImage.open(PARENT);original=parent.read_file('/data/SC1.DK4');archive=Path(plan['target_archive']).read_bytes()
    assert sha(original)==plan['source_archive_sha256'] and sha(archive)==plan['target_archive_sha256']==independent['target_archive_sha256']
    image.replace_file('/data/SC1.DK4',archive);payload=bytes(image.rom.save());assert sha(payload)==independent['independently_reconstructed_complete_target_ROM_sha256']
    assert [p for _,p,v in parent.iter_files() if image.read_file(p)!=v]==['/data/SC1.DK4'] and all(image.read_file(p)==v for p,v in parent.iter_components())
    before,after=[IlnkContainer.parse(a).blocks for a in [original,archive]]
    assert len(before)==len(after)==325 and [i for i,(a,b) in enumerate(zip(before,after,strict=True)) if a!=b]==list(range(54,61))
    image.replace_file('/data/SC1.DK4',original);assert bytes(image.rom.save())==bytes(parent.rom.save())==PARENT.read_bytes()
    ROOT.mkdir(parents=True);ROM.write_bytes(payload);assert sha(ROM.read_bytes())==sha(payload)
    pins=Path('translations/rom_retention_pins.json');raw=pins.read_bytes();values=json.loads(raw);assert not any(Path(v['path']).resolve()==ROM.resolve() for v in values)
    updated=values+[dict(path=str(ROM.resolve()),reason='B54-B60 seven-block82-record research reference from complete registeredV8778;onlySC1blocks54-60 change.318otherblocks/allotherfiles/components andwholeROMinverse exact. Not handoff,parent,promotion orseparateuserpackage. Preserve every ROM. SHA256 '+sha(payload))]
    (ROOT/'pins.before.json').write_bytes(raw);encoded=(json.dumps(updated,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf8');assert pins.read_bytes()==raw
    with pins.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    assert json.loads(pins.read_bytes())==updated and updated[:-1]==values
    save(ROOT/'research_image_receipt.json',dict(parent=str(PARENT),parent_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(payload),
        source_relocation_plan=str(PLAN),source_relocation_plan_sha256=sha(PLAN.read_bytes()),only_changed_files=['/data/SC1.DK4'],only_changed_blocks=list(range(54,61)),
        all318_otherSC1_blocks_andall_other_files_components_exact=True,complete_parent_ROM_inverse_byte_exact=True,
        independent_reconstruction=str(INDEPENDENT),independent_reconstruction_sha256=sha(INDEPENDENT.read_bytes()),all_prior_ROM_pins_preserved=True,pins_before_sha256=sha(raw),pins_after_sha256=sha(encoded),
        registered_candidate=False,not_for_handoff_ornew_parent=True,loader_caller_actual_fullname_policy_atomic_registered_release_andstartup_pending=True,
        new_credit=0,new_emulator_runs=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [PLAN,INDEPENDENT,STORED,DOC,NAMES,Path(__file__)]}))
    print('Pinned seven-block82-record research reference from V8778;all318 otherblocks/files/components/wholeROMinverse exact.No promotion,release orcredit.',flush=True)
