"""Register the sealed B206 batch after the complete V6270 stack;preserve every prior profile."""
import ast,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import lil_B206_editorial_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B206_registration_v6326')
PROFILE='all-routes-unified-v6327'
VALIDATION=Path('work/analysis/lil_B206_atomic_v6325')
PARENT=Path('out/all_routes_combined_v6270_candidate.nds')
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists();receipt=read(VALIDATION/'atomic_validation_receipt.json');config=Path(receipt['config']);conf=read(config)
    assert receipt['positive_records']==28 and receipt['negative_count']==81 and receipt['all_negatives_reject_before_mutation']
    assert sha(config.read_bytes())==receipt['config_sha256'] and sha(PARENT.read_bytes())==receipt['parent_ROM_sha256']
    for p,h in conf['dependencies'].items():assert sha(Path(p).read_bytes())==h
    verified=read('work/analysis/editorial_handoff_verification_v6324/verified_handoff.json');assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==verified['ledger_sha256']
    registry_path,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py');raw,before=registry_path.read_bytes(),builder.read_bytes();registry=read(registry_path)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    prior=read(PARENT.with_suffix('.manifest.json'));assert len(prior['batches'])==595
    stage=b'''    lil_proof = profile_config.get('lil_B206_editorial')
    if lil_proof:
        from dk4tool.patch.lil_B206_editorial_v1 import apply_release as apply_lil_proof

        lil_proof_report = apply_lil_proof(candidate, baseline, lil_proof)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_proof_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_B206_editorial'] = {
            'release_config': lil_proof,
            'release_config_sha256': sha256(Path(lil_proof).read_bytes()),
            'proof': lil_proof_report}
        for key in ['manuscript', 'choice_manuscript']:
            more_batch = Path(lil_proof_report[key])
            if more_batch in release_batches:
                raise ValueError('B206 companions must run once after the complete V6270 stack')
            release_batches.append(more_batch)

'''
    anchor=b'    # Lexically valid "% o"';assert before.count(anchor)==1 and b"profile_config.get('lil_B206_editorial')" not in before
    after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec');assert after.index(b"profile_config.get('shady_man_label')")<after.index(stage)<after.index(anchor)
    assert [n.module for n in ast.walk(ast.parse('if True:\n'+stage.decode())) if isinstance(n,ast.ImportFrom)]==[owned.__name__]
    profile=deepcopy(registry['profiles']['all-routes-unified-v6270']);profile.update(status='experimental',lil_B206_editorial=owned.CONFIG,
        description='Complete V6270 plus all28 B206 ceramic-earring scene objects:24 speeches/four labels,16 revisions/12 justified retentions.42 source commands,eight relative sites,two menus,picture138,three47xx,three A000 and complete end preserved;1524-byte predecessor fully reversible.24 actual English panels/55 observations/217 complete text/name holds,five menus/13 holds and all three paths preserve source regions/results.81 timing,eight RNG,114 later RGB differences and queried final-state limits remain explicit. Shady Man already integrated;all207 names/aliases and wider editorial goal remain open.',
        note='81 pre-mutation semantic negatives approved. Registered cumulative build,exact clean-input patch and representative current startup/town checks pending. Main V4701 preserved.')
    updated=deepcopy(registry);updated['profiles'][PROFILE]=profile;encoded=(json.dumps(updated,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8')
    ROOT.mkdir(parents=True);save(ROOT/'release_stack.before.json',registry);(ROOT/'build_integrated_release.py.before').write_bytes(before);(ROOT/'builder.stage.bin').write_bytes(stage);save(ROOT/'release_stack.planned.json',updated)
    assert registry_path.read_bytes()==raw and builder.read_bytes()==before
    save(owned.CONFIG,conf);temporary=builder.with_name('build_integrated_release_v6326.tmp');assert not temporary.exists();temporary.write_bytes(after);os.replace(temporary,builder)
    with registry_path.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    restored=deepcopy(read(registry_path));restored['profiles'].pop(PROFILE);assert restored==registry and builder.read_bytes().replace(stage,b'',1)==before
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v6270',parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),release_config=owned.CONFIG,release_config_sha256=sha(Path(owned.CONFIG).read_bytes()),manuscripts=read(conf['reference_approval'])['manuscripts'],reference_map=conf['reference_map'],reference_map_sha256=sha(Path(conf['reference_map']).read_bytes()),registry_before_sha256=sha(raw),registry_after_sha256=sha(registry_path.read_bytes()),builder_before_sha256=sha(before),builder_after_sha256=sha(builder.read_bytes()),positive_proof=receipt['positive_proof'],negative_cases=receipt['negative_cases'],negative_count=81,all_negatives_reject_before_mutation=True,expected_manifest_batches=597,accepted_layers=114,promoted_profile_unchanged='all-routes-unified-v4701',producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    rows=[derive('scripts/build_lil_B201_v5947.py','scripts/build_lil_B206_v6327.py',{'B201':'B206','build_v5947':'build_v6327','combined_v5947':'combined_v6327','registration_v5946':'registration_v6326','all-routes-unified-v5947':'all-routes-unified-v6327'})]
    rows.append(derive('scripts/run_lil_B201_regressions_v5947.py','scripts/run_lil_B206_regressions_v6327.py',{'B201':'B206','regressions_v5947':'regressions_v6327'}))
    rows.append(derive('scripts/run_lil_B201_startup_v5949.py','scripts/run_lil_B206_startup_v6330.py',{'B201':'B206','runs_v5949':'runs_v6330','_v5949_':'_v6330_','version=5947':'version=6327'}))
    rows.append(derive('scripts/verify_lil_B201_startup_v5950.py','scripts/verify_lil_B206_startup_v6331.py',{'B201':'B206','startup_v5950':'startup_v6331','runs_v5949':'runs_v6330','combined_v5947':'combined_v6327','combined_v5891':'combined_v6270','generic_speaker_labels_runs_v5893':'shady_man_runs_v6272','V5891':'V6270','Current5947':'Current6327'}))
    rows.append(derive('scripts/record_lil_B201_startup_view_v5950.py','scripts/record_lil_B206_startup_view_v6331.py',{'B201':'B206','startup_v5950':'startup_v6331','V5891':'V6270'}))
    rows.append(derive('scripts/verify_lil_B201_release_v5948.py','scripts/verify_lil_B206_release_v6328.py',{'B201':'B206','release_v5948':'release_v6328','combined_v5947':'combined_v6327','combined_v5891':'combined_v6270','registration_v5946':'registration_v6326','build_v5947':'build_v6327','all-routes-unified-v5947':'all-routes-unified-v6327','all-routes-unified-v5891':'all-routes-unified-v6270','==589':'==597','manifest_batches=589':'manifest_batches=597','all589_':'all597_','123040':'123264',"profile_config.get('generic_speaker_labels')":"profile_config.get('shady_man_label')",'out/lil_B201_reference_v5934_RESEARCH_ONLY.nds':'out/lil_B206_reference_v6307_RESEARCH_ONLY.nds','V5891':'V6270'}))
    save(ROOT/'prepared_build_regression_startup_tools.json',dict(tools=rows,full_goal_complete=False));print('Registered experimental V6327:597 expected batches/114 accepted. B206 follows the complete V6270 stack;all earlier profiles/main V4701 preserved.')
