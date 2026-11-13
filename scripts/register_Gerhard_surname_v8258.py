"""Register the validated sparse surname stage after the complete V8172 stack; never promote."""
import json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import gerhard_surname_editorial_v2 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.Gerhard_surname_release_paths_v8238 import PARENT
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Gerhard_surname_registration_v8258')
PROFILE='all-routes-unified-v8259'
POSITIVE=Path('work/analysis/Gerhard_atomic_positive_v8256/one_whole_NDS_commit_exact_reference_andunchanged_precommit_input.json')
NEGATIVE=Path('work/analysis/Gerhard_atomic_challenges_v8257/actual_changing_semantic_precommit_rejections.json')
if __name__=='__main__':
    assert not ROOT.exists();positive,negative=map(read,[POSITIVE,NEGATIVE]);conf=read(owned.CONFIG)
    assert positive['single_complete_NDS_commit'] and positive['original_object_identity_andall_files_components_bytes_unchanged_until_commit']
    assert negative['negative_count']==len(negative['cases'])==107 and negative['all_expected_semantic_guards_match']
    assert negative['dependency_gate_bypassed_buttrusted_frozen_contract_andnative_source_guards_not_weakened'] and negative['zero_wholeNDS_commit_calls_forall_failed_inputs']
    assert all(c['rejected'] and c['commit_calls']==0 and c['actual_input_change_asserted'] and c['dependency_digest_gate_deliberately_bypassed'] for c in negative['cases'])
    assert negative['all_watched_sources_ROMs_configs_proofs_registry_ledger_andpins_hash_exact'] and negative['trusted_frozen_contract_revalidated_before_andafter']
    for p,h in conf['dependencies'].items():assert sha(Path(p).read_bytes())==h
    assert sha(PARENT.read_bytes())==conf['parent_ROM_sha256'] and positive['planned_output_sha256']==conf['reference_ROM_sha256']
    verified=read('work/analysis/editorial_handoff_verification_v8250/verified_handoff.json')
    assert verified['candidate_sha256']==conf['parent_ROM_sha256'] and sha(Path('translations/editorial_review_current_v1.json').read_bytes())==verified['ledger_sha256']
    rp,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py');raw,before=rp.read_bytes(),builder.read_bytes();registry=read(rp)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert len(read(PARENT.with_suffix('.manifest.json'))['batches'])==639
    stage='''    gerhard_surname_editorial_config = profile_config.get('gerhard_surname_editorial')
    if gerhard_surname_editorial_config:
        from dk4tool.patch.gerhard_surname_editorial_v2 import apply_release as apply_gerhard_surname_editorial

        gerhard_surname_editorial_report = apply_gerhard_surname_editorial(candidate, baseline, gerhard_surname_editorial_config)
        for gerhard_surname_file in gerhard_surname_editorial_report['files']:
            gerhard_surname_path = gerhard_surname_file['file_path']
            grouped.setdefault(gerhard_surname_path, [])
            changed_records.setdefault(gerhard_surname_path, []).extend(row['id'] for row in gerhard_surname_file['changed_records'])
            relocation_checks.setdefault(gerhard_surname_path, {})['gerhard_surname_editorial'] = {
                'release_config': gerhard_surname_editorial_config,
                'release_config_sha256': sha256(Path(gerhard_surname_editorial_config).read_bytes()),
                'proof': gerhard_surname_editorial_report}
        for gerhard_surname_manuscript in gerhard_surname_editorial_report['manuscripts']:
            more_batch = Path(gerhard_surname_manuscript)
            if more_batch in release_batches:
                raise ValueError('Gerhard surname stage must run once after the complete V8172 stack')
            release_batches.append(more_batch)

'''
    anchor='    # Lexically valid "% o"';text=before.decode('utf8')
    assert text.count(anchor)==1 and "profile_config.get('gerhard_surname_editorial')" not in text
    after=checked_text(text,{anchor:stage+anchor}).encode('utf8')
    assert after.index(b"profile_config.get('rafael_B50_editorial')")<after.index(stage.encode())<after.index(anchor.encode())
    profile=deepcopy(registry['profiles']['all-routes-unified-v8172'])
    profile.update(status='experimental',gerhard_surname_editorial=owned.CONFIG,
        description='Complete V8172 plus Gerhard Adernkatz consistency:five previously reviewed SC2 speeches andone owned12-byte name field;zero duplicate editorial credit.',
        note='Natural-dialogue-v2 whole295-speech clean-name context;14 consistent/20 final Latin consumers;protect separate Blades8/pointers/all otherbytes. Five source-bound216px single pages,fullcontrols225/preambles130/relatives44/125unowned speeches/334otherSC2blocks andcomplete inverses. All5actual bodies/30bodyholds/262nameholds,wholeB27 actual35of51 withcaptain0tail limitation,wholeB74 actual75of79/defaultmenu0,focusedintro8 bypassesoutercondition explicitly. Preserve all176008-frame timing/RNG/components/bytes/calendar/RGB/fixture limits;no fullroute/hardware/simulation claim. Frozen policy260expectedrejections;independent107precommit proofcorruptions withdigestbypass/zero wholeNDS commits;one completeNDS commit onpositive exactfullreference. Hodram28newdrafts16revisions12retentions andall28nativebodypages remainseparate,pendingstored/nameheader/actual4800-layout0-hide4700/frozenpolicy/integration. Fullfour-story/sharedtown-shop/random/Help/remainingprose/207names/retrospectivewrapobjectiveactive;graphicsandlaterolder-recordtechnicalauditseparate. No separateunifiedtestpackage,promotion,pruning,commit orpush;main4701 unchanged.')
    updated=deepcopy(registry);updated['profiles'][PROFILE]=profile
    encoded=(json.dumps(updated,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf8')
    ROOT.mkdir(parents=True);(ROOT/'release_stack.before.raw').write_bytes(raw);save(ROOT/'release_stack.before.json',registry)
    (ROOT/'build_integrated_release.py.before').write_bytes(before);(ROOT/'builder.stage.bin').write_bytes(stage.encode('utf8'));save(ROOT/'release_stack.planned.json',updated)
    assert rp.read_bytes()==raw and builder.read_bytes()==before
    temporary=builder.with_name('build_integrated_release_v8258.tmp');assert not temporary.exists();temporary.write_bytes(after);os.replace(temporary,builder)
    with rp.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    restored=deepcopy(read(rp));restored['profiles'].pop(PROFILE)
    assert restored==registry and builder.read_bytes().replace(stage.encode(),b'',1)==before
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v8172',parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),
        release_config=owned.CONFIG,release_config_sha256=sha(Path(owned.CONFIG).read_bytes()),manuscripts=conf['manuscripts'],reference_map=conf['reference_map'],
        registry_before_sha256=sha(raw),registry_after_sha256=sha(rp.read_bytes()),builder_before_sha256=sha(before),builder_after_sha256=sha(builder.read_bytes()),
        positive_proof=str(POSITIVE),positive_proof_sha256=sha(POSITIVE.read_bytes()),negative_cases=str(NEGATIVE),negative_cases_sha256=sha(NEGATIVE.read_bytes()),negative_count=107,
        all_negatives_reject_before_any_wholeNDS_commit=True,expected_manifest_batches=640,accepted_layers=114,promoted_profile_unchanged='all-routes-unified-v4701',
        reference_ROM=conf['reference_ROM'],reference_ROM_sha256=conf['reference_ROM_sha256'],producer_sha256=sha(Path(__file__).read_bytes()),new_credit=0,full_goal_complete=False))
    print('Registered experimental V8259 aftercompleteV8172:640expected manifest batches/114accepted;main unchanged/zero duplicatecredit.')
