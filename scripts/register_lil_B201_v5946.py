"""Register B201 after the current name-data stage, retaining all prior profiles."""
import ast,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import lil_B201_editorial_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B201_registration_v5946')
PROFILE='all-routes-unified-v5947'
VALIDATION=Path('work/analysis/lil_B201_atomic_v5945')
PARENT=Path('out/all_routes_combined_v5891_candidate.nds')
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists();receipt=read(VALIDATION/'atomic_validation_receipt.json');config=Path(receipt['config']);conf=read(config)
    assert receipt['positive_records']==26 and receipt['negative_count']==68 and receipt['all_negatives_reject_before_mutation']
    assert sha(config.read_bytes())==receipt['config_sha256'] and sha(PARENT.read_bytes())==receipt['parent_ROM_sha256']
    for p,h in conf['dependencies'].items():assert sha(Path(p).read_bytes())==h
    verified=read('work/analysis/editorial_handoff_verification_v5927/verified_handoff.json');assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==verified['ledger_sha256']
    registry_path,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py');raw,before=registry_path.read_bytes(),builder.read_bytes();registry=read(registry_path)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    prior=read(PARENT.with_suffix('.manifest.json'));assert len(prior['batches'])==587
    stage=b'''    lil_proof = profile_config.get('lil_B201_editorial')
    if lil_proof:
        from dk4tool.patch.lil_B201_editorial_v1 import apply_release as apply_lil_proof

        lil_proof_report = apply_lil_proof(candidate, baseline, lil_proof)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_proof_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_B201_editorial'] = {
            'release_config': lil_proof,
            'release_config_sha256': sha256(Path(lil_proof).read_bytes()),
            'proof': lil_proof_report}
        for key in ['manuscript', 'choice_manuscript']:
            more_batch = Path(lil_proof_report[key])
            if more_batch in release_batches:
                raise ValueError('B201 companions must run once after the complete V5891 stack')
            release_batches.append(more_batch)

'''
    anchor=b'    # Lexically valid "% o"';assert before.count(anchor)==1 and b"profile_config.get('lil_B201_editorial')" not in before
    after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec');assert after.index(b"profile_config.get('generic_speaker_labels')")<after.index(stage)<after.index(anchor)
    assert [n.module for n in ast.walk(ast.parse('if True:\n'+stage.decode())) if isinstance(n,ast.ImportFrom)]==[owned.__name__]
    profile=deepcopy(registry['profiles']['all-routes-unified-v5891']);profile.update(status='experimental',lil_B201_editorial=owned.CONFIG,
        description='Complete V5891 plus B201 rigging negotiation,Buy/Pass,purchase and refusal:26 source objects,12 revisions/14 justified retentions. All44 commands,24 preambles,15 opaque leaves,four relative sites,one2100,three FE,two FI and single end preserved.24 actual English panels/37 observations/144 complete native holds and both visibly selected choices match source regions/results.54 timings,30 interval RNG and21 later RGB differences remain explicit;final state and future-world equivalence not claimed. Trader retained contextually;207-name review remains open.',
        note='68 pre-mutation semantic negatives approved;registered cumulative build,clean-input patch and current startup pending. Main V4701 preserved.')
    updated=deepcopy(registry);updated['profiles'][PROFILE]=profile;encoded=(json.dumps(updated,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8')
    ROOT.mkdir(parents=True);save(ROOT/'release_stack.before.json',registry);(ROOT/'build_integrated_release.py.before').write_bytes(before);(ROOT/'builder.stage.bin').write_bytes(stage);save(ROOT/'release_stack.planned.json',updated)
    assert registry_path.read_bytes()==raw and builder.read_bytes()==before
    save(owned.CONFIG,conf);temporary=builder.with_name('build_integrated_release_v5946.tmp');assert not temporary.exists();temporary.write_bytes(after);os.replace(temporary,builder)
    with registry_path.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    restored=deepcopy(read(registry_path));restored['profiles'].pop(PROFILE);assert restored==registry and builder.read_bytes().replace(stage,b'',1)==before
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v5891',parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),release_config=owned.CONFIG,release_config_sha256=sha(Path(owned.CONFIG).read_bytes()),manuscripts=read(conf['reference_approval'])['manuscripts'],reference_map=conf['reference_map'],reference_map_sha256=sha(Path(conf['reference_map']).read_bytes()),registry_before_sha256=sha(raw),registry_after_sha256=sha(registry_path.read_bytes()),builder_before_sha256=sha(before),builder_after_sha256=sha(builder.read_bytes()),positive_proof=receipt['positive_proof'],negative_cases=receipt['negative_cases'],negative_count=68,all_negatives_reject_before_mutation=True,expected_manifest_batches=589,accepted_layers=114,promoted_profile_unchanged='all-routes-unified-v4701',producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    rows=[derive('scripts/build_lil_B200_v5872.py','scripts/build_lil_B201_v5947.py',{'B200':'B201','build_v5872':'build_v5947','combined_v5872':'combined_v5947','registration_v5871':'registration_v5946','all-routes-unified-v5872':'all-routes-unified-v5947'})]
    rows.append(derive('scripts/run_lil_B200_regressions_v5872.py','scripts/run_lil_B201_regressions_v5947.py',{'B200':'B201','regressions_v5872':'regressions_v5947'}))
    rows.append(derive('scripts/run_lil_B200_startup_v5874.py','scripts/run_lil_B201_startup_v5949.py',{'B200':'B201','runs_v5874':'runs_v5949','_v5874_':'_v5949_','version=5872':'version=5947'}))
    rows.append(derive('scripts/verify_lil_B200_startup_v5875.py','scripts/verify_lil_B201_startup_v5950.py',{'B200':'B201','startup_v5875':'startup_v5950','runs_v5874':'runs_v5949','combined_v5872':'combined_v5947','combined_v5816':'combined_v5891','lil_B199_runs_v5818':'generic_speaker_labels_runs_v5893','V5816':'V5891','Current5872':'Current5947'}))
    rows.append(derive('scripts/record_lil_B200_startup_view_v5875.py','scripts/record_lil_B201_startup_view_v5950.py',{'B200':'B201','startup_v5875':'startup_v5950','V5816':'V5891'}))
    save(ROOT/'prepared_build_regression_startup_tools.json',dict(tools=rows,full_goal_complete=False));print('Registered experimental V5947:589 batches/114 accepted;B201 follows current speaker-name data. All earlier profiles/main V4701 preserved.')
