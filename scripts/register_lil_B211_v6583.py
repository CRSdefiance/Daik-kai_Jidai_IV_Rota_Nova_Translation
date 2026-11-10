"""Append the sealed twelve-record B211 layer after the complete V6541 name/data stack."""
import ast,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import lil_B211_editorial_v2 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B211_registration_v6583');PROFILE='all-routes-unified-v6584';VALIDATION=Path('work/analysis/lil_B211_atomic_v6582');PARENT=Path('out/all_routes_combined_v6541_candidate.nds')
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists();receipt=read(VALIDATION/'atomic_validation_receipt.json');config=Path(receipt['config']);conf=read(config);assert receipt['positive_records']==12 and receipt['negative_count']==146 and receipt['all_negatives_reject_before_mutation'] and receipt['independent_aggregate_and_per_record_47_body35_name12_FE_holds_bound'];assert sha(config.read_bytes())==receipt['config_sha256'] and sha(PARENT.read_bytes())==receipt['parent_ROM_sha256']
    for p,h in conf['dependencies'].items():assert sha(Path(p).read_bytes())==h
    verified=read('work/analysis/editorial_handoff_verification_v6580/verified_handoff.json');assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==verified['ledger_sha256'];registry_path,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py');raw,before=registry_path.read_bytes(),builder.read_bytes();registry=read(registry_path);assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701' and len(read(PARENT.with_suffix('.manifest.json'))['batches'])==602
    stage=b'''    lil_proof = profile_config.get('lil_B211_editorial')
    if lil_proof:
        from dk4tool.patch.lil_B211_editorial_v2 import apply_release as apply_lil_proof

        lil_proof_report = apply_lil_proof(candidate, baseline, lil_proof)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_proof_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_B211_editorial'] = {
            'release_config': lil_proof,
            'release_config_sha256': sha256(Path(lil_proof).read_bytes()),
            'proof': lil_proof_report}
        more_batch = Path(lil_proof_report['manuscript'])
        if more_batch in release_batches:
            raise ValueError('B211 must run once after the complete V6541 stack and Al Ferid name asset')
        release_batches.append(more_batch)

'''
    anchor=b'    # Lexically valid "% o"';assert before.count(anchor)==1 and b"profile_config.get('lil_B211_editorial')" not in before;after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec');assert after.index(b"profile_config.get('Al_Ferid_name')")<after.index(stage)<after.index(anchor);assert [n.module for n in ast.walk(ast.parse('if True:\n'+stage.decode())) if isinstance(n,ast.ImportFrom)]==[owned.__name__]
    profile=deepcopy(registry['profiles']['all-routes-unified-v6541']);profile.update(status='experimental',lil_B211_editorial=owned.CONFIG,description='Complete V6541 plus twelve Lil B211 whole-exchange objects:8 revisions/4 justified retentions. Preserve gentle swan companionship/wistful envy,unknown long shiny object,uncertain near-Amsterdam direction andinvitation. Nine progressive/three null-actor FE objects,one originalFI,all14 commands/12 preambles/A000/end and640-byte predecessor inverse;target728stored/726logical/tail2. Twelve original single pages,96 logical/compiled+48 stored alignments,seven zero-ink tails,32 name alignments andactual47body/35name/12FE holds. Five rowcount reasons/four exact word-clause-question boundaries;complete off-to question classified narrowly without global safety waiver. Ten timing/6RNG/4duration/110 laterRGB18prompt92broader anddifferent final calendar/models/PRNG preserved without broad simulation equivalence. Lil Argot/Cristina Erneco retained;no new name asset orduplicate credit. Full four-storyline/earlier dialogue/shared town/random/Help/prose/wrap/207-name objective active;graphics/later older-record re-audit separate.',note='146 independent pre-mutation semantic negatives and63 layout-policy negatives pass. Compilerv2 additionally binds aggregate/per-record47body35name12FE evidence;the memory-only v1 probe andall predecessors are preserved. Clean-input cumulative patch/current startup pending. Main V4701 unchanged;no automatic promotion.')
    updated=deepcopy(registry);updated['profiles'][PROFILE]=profile;encoded=(json.dumps(updated,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode();ROOT.mkdir(parents=True);save(ROOT/'release_stack.before.json',registry);(ROOT/'build_integrated_release.py.before').write_bytes(before);(ROOT/'builder.stage.bin').write_bytes(stage);save(ROOT/'release_stack.planned.json',updated);assert registry_path.read_bytes()==raw and builder.read_bytes()==before;save(owned.CONFIG,conf);temporary=builder.with_name('build_integrated_release_v6583.tmp');assert not temporary.exists();temporary.write_bytes(after);os.replace(temporary,builder)
    with registry_path.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    restored=deepcopy(read(registry_path));restored['profiles'].pop(PROFILE);assert restored==registry and builder.read_bytes().replace(stage,b'',1)==before;save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v6541',parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),release_config=owned.CONFIG,release_config_sha256=sha(Path(owned.CONFIG).read_bytes()),manuscript=conf['manuscript'],reference_map=conf['reference_map'],reference_map_sha256=sha(Path(conf['reference_map']).read_bytes()),registry_before_sha256=sha(raw),registry_after_sha256=sha(registry_path.read_bytes()),builder_before_sha256=sha(before),builder_after_sha256=sha(builder.read_bytes()),positive_proof=receipt['positive_proof'],negative_cases=receipt['negative_cases'],negative_count=146,all_negatives_reject_before_mutation=True,expected_manifest_batches=603,accepted_layers=114,promoted_profile_unchanged='all-routes-unified-v4701',reference_ROM=conf['reference_ROM'],reference_ROM_sha256=conf['reference_ROM_sha256'],producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('Registered experimental V6584:603 expected batches/114 accepted;all earlier profiles andmain V4701 preserved.')
