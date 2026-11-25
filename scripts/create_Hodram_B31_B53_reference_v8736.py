"""Pin a two-block research reference from complete registered V8704; no handoff."""
import json,os
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B31_B53_reference_v8736')
PARENT=Path('out/all_routes_combined_v8704_candidate.nds')
ROM=Path('out/Hodram_B31_B53_reference_v8736_RESEARCH_ONLY.nds')
PLAN=Path('work/analysis/Hodram_B31_B53_relocation_v8728/reconstruction.json')
INDEPENDENT=Path('work/analysis/Hodram_B31_B53_independent_v8734/independent_reconstruction.json')
STORED=Path('work/analysis/Hodram_B31_B53_stored_v8729/stored_pages_controls_andreferences.json')
DOC=Path('translations/hodram_B31_B53_editorial_manuscript_v3.json')
NAMES=Path('work/analysis/Hodram_actor34_name_review_v8735/scoped_name_retention_andunchanged_prose.json')
if __name__=='__main__':
    assert not ROOT.exists() and not ROM.exists();plan,independent,stored,doc,names=map(read,[PLAN,INDEPENDENT,STORED,DOC,NAMES])
    assert names['manuscript_sha256']==sha(DOC.read_bytes()) and names['all3_approved_prose_records_compiledbytes_exact_source_current_refs_andreview_gates_unchanged']
    assert read(doc['predecessor_manuscript'])['records']==doc['records'] and sha(Path(doc['predecessor_manuscript']).read_bytes())==plan['manuscript_sha256']==independent['manuscript_sha256']==stored['manuscript_sha256']
    candidate=read('translations/editorial_review_current_v1.json')['current_integrated_candidate'];registry=read('translations/release_stack.json');manifest=read(candidate['manifest'])
    assert candidate['profile']=='all-routes-unified-v8704' and sha(PARENT.read_bytes())==candidate['sha256']==doc['current_ROM_sha256']==plan['candidate_sha256']==stored['candidate_sha256']
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes()) and len(manifest['batches'])==646 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert independent['whole_target_blocks_andarchive_byte_equal_to_sparse_rebuild'] and independent['relocation_sha256']==sha(PLAN.read_bytes()) and stored['complete3stored_first_internal_final_glyphs_independent_planes_bounds_consumption_andpagination_pass']
    assert len(stored['records'])==3 and all(r['source_reference'] and r['current_reference'] and r['final_reference'] for r in stored['records'])
    parent,image=NdsImage.open(PARENT),NdsImage.open(PARENT);original=parent.read_file('/data/SC1.DK4');archive=Path(plan['target_archive']).read_bytes()
    assert sha(original)==plan['source_archive_sha256'] and sha(archive)==plan['target_archive_sha256']==independent['target_archive_sha256']
    image.replace_file('/data/SC1.DK4',archive);payload=bytes(image.rom.save());assert sha(payload)==independent['independently_reconstructed_complete_target_ROM_sha256']
    assert [p for _,p,v in parent.iter_files() if image.read_file(p)!=v]==['/data/SC1.DK4'] and all(image.read_file(p)==v for p,v in parent.iter_components())
    before,after=[IlnkContainer.parse(a).blocks for a in [original,archive]];assert len(before)==len(after)==325 and [i for i,(a,b) in enumerate(zip(before,after,strict=True)) if a!=b]==[31,53]
    image.replace_file('/data/SC1.DK4',original);assert bytes(image.rom.save())==bytes(parent.rom.save())==PARENT.read_bytes()
    ROOT.mkdir(parents=True);ROM.write_bytes(payload);assert ROM.read_bytes()==payload
    pins=Path('translations/rom_retention_pins.json');raw=pins.read_bytes();values=json.loads(raw);assert not any(Path(v['path']).resolve()==ROM.resolve() for v in values)
    updated=values+[dict(path=str(ROM.resolve()),reason='B31/B53 three-speech research reference from complete registeredV8704;onlySC1blocks31and53 change,323otherblocks/allotherfiles/components andwholeROMinverse exact. Not handoff,parent,promotion orseparateuserpackage. Preserve every ROM. SHA256 '+sha(payload))]
    (ROOT/'pins.before.json').write_bytes(raw);encoded=(json.dumps(updated,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf8');assert pins.read_bytes()==raw
    with pins.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    assert json.loads(pins.read_bytes())==updated and updated[:-1]==values
    save(ROOT/'research_image_receipt.json',dict(parent=str(PARENT),parent_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(payload),
        source_relocation_plan=str(PLAN),source_relocation_plan_sha256=sha(PLAN.read_bytes()),only_changed_files=['/data/SC1.DK4'],only_changed_blocks=[31,53],
        all323_otherSC1_blocks_andall_other_files_components_exact=True,complete_parent_ROM_inverse_byte_exact=True,
        independent_reconstruction=str(INDEPENDENT),independent_reconstruction_sha256=sha(INDEPENDENT.read_bytes()),all_prior_ROM_pins_preserved=True,pins_before_sha256=sha(raw),pins_after_sha256=sha(encoded),
        registered_candidate=False,not_for_handoff_ornew_parent=True,loader_caller_actual_policy_atomic_registered_release_andstartup_pending=True,
        new_credit=0,new_emulator_runs=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [PLAN,INDEPENDENT,STORED,DOC,NAMES,Path(__file__)]}))
    print('Pinned B31/B53researchreference fromfullV8704;onlytwoSC1blocks change,323unownedblocks/allotherfiles/components/fullROMinverse exact.No registered release orcredit.',flush=True)
