"""Register the validated Hodram stage after the full V8259 stack; no promotion."""
import json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import hodram_three_blocks_editorial_v2 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.Hodram_three_blocks_release_paths_v8290 import PARENT
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_three_blocks_registration_v8299')
PROFILE='all-routes-unified-v8300'
POSITIVE=Path('work/analysis/Hodram_atomic_positive_v8297b/one_whole_NDS_commit_exact_reference_andunchanged_precommit_input.json')
NEGATIVE=Path('work/analysis/Hodram_atomic_challenges_v8298/actual_changing_semantic_precommit_rejections.json')
if __name__=='__main__':
    assert not ROOT.exists();positive,negative=map(read,[POSITIVE,NEGATIVE]);conf=read(owned.CONFIG)
    assert positive['single_complete_NDS_commit'] and positive['original_object_identity_andall_files_components_bytes_unchanged_until_commit']
    assert negative['negative_count']==len(negative['cases'])==71 and negative['all_expected_semantic_guards_match']
    assert negative['dependency_gate_bypassed_buttrusted_frozen_andnative_source_guards_preserved'] and negative['all_rejected_inputs_zero_whole_NDS_commits']
    assert all(c['rejected'] and c['commit_calls']==0 and c['actual_input_changes_asserted'] and c['dependency_digest_gate_deliberately_bypassed'] for c in negative['cases'])
    assert negative['all_protected_files_hash_exact']
    for p,h in conf['dependencies'].items():assert sha(Path(p).read_bytes())==h
    assert sha(PARENT.read_bytes())==conf['parent_ROM_sha256'] and positive['planned_output_sha256']==conf['reference_ROM_sha256']
    verified=read('work/analysis/editorial_handoff_verification_v8292/verified_handoff.json')
    assert verified['candidate_sha256']==conf['parent_ROM_sha256'] and sha(Path('translations/editorial_review_current_v1.json').read_bytes())==verified['ledger_sha256']
    rp,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py');raw,before=rp.read_bytes(),builder.read_bytes();registry=read(rp)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert len(read(PARENT.with_suffix('.manifest.json'))['batches'])==640
    stage='''    hodram_three_blocks_editorial_config = profile_config.get('hodram_three_blocks_editorial')
    if hodram_three_blocks_editorial_config:
        from dk4tool.patch.hodram_three_blocks_editorial_v2 import apply_release as apply_hodram_three_blocks_editorial

        hodram_three_blocks_editorial_report = apply_hodram_three_blocks_editorial(candidate, baseline, hodram_three_blocks_editorial_config)
        for hodram_three_blocks_file in hodram_three_blocks_editorial_report['files']:
            hodram_three_blocks_path = hodram_three_blocks_file['file_path']
            grouped.setdefault(hodram_three_blocks_path, [])
            changed_records.setdefault(hodram_three_blocks_path, []).extend(row['id'] for row in hodram_three_blocks_file['changed_records'])
            relocation_checks.setdefault(hodram_three_blocks_path, {})['hodram_three_blocks_editorial'] = {
                'release_config': hodram_three_blocks_editorial_config,
                'release_config_sha256': sha256(Path(hodram_three_blocks_editorial_config).read_bytes()),
                'proof': hodram_three_blocks_editorial_report}
        for hodram_three_blocks_manuscript in hodram_three_blocks_editorial_report['manuscripts']:
            more_batch = Path(hodram_three_blocks_manuscript)
            if more_batch in release_batches:
                raise ValueError('Hodram B137/B45/B46 stage must run once after the complete V8259 stack')
            release_batches.append(more_batch)

'''
    anchor='    # Lexically valid "% o"';text=before.decode('utf8')
    assert text.count(anchor)==1 and "profile_config.get('hodram_three_blocks_editorial')" not in text
    after=checked_text(text,{anchor:stage+anchor}).encode('utf8')
    assert after.index(b"profile_config.get('gerhard_surname_editorial')")<after.index(stage.encode())<after.index(anchor.encode())
    profile=deepcopy(registry['profiles']['all-routes-unified-v8259'])
    profile.update(status='experimental',hodram_three_blocks_editorial=owned.CONFIG,
        description='Complete V8259 plus clean-Japanese whole-exchange Hodram SC1B137/B45/B46 editorial review:28records,16 revisions and12 justified retentions.',
        note='Natural-dialogue-v2:whole clean exchanges/prior27B44callbacks,approved names/six scoped retentions,all28 single native pages/three source silences/full216px automatic wrapping. Preserve60commands/28sixbyte preambles/8relative sites/two raw queries/normal valuecarry/original4800-layout0-hide4700. Three clean source/fullparent inverses and325loads650modes/caller census pass. Six paired initialized opening fixtures100006frames coverall56source/revised pages/262body-name holds;not natural optional activation ororiginal location. B137 latercaptain0/SC0B44 isnot normalHodram continuity. All command/timing/RNG/UI/nativecomponent/calendar/532laterRGB andfixture limits preserved. Frozen policy579 expectedrejections;71independent semanticprecommit corruptions withdigestbypass/zero commits. Positive onecompleteNDS commit matchesfull8276reference. Registered Adernkatz/Blades/allunowned files/components preserved. Fullfour-story/sharedtown-shop/random/Help/remainingprose/207names/retrospectivewrap goal active;graphics/latertechnicalaudit separate. No separate requestedpackage,promotion,pruning,commit orpush;main4701 unchanged.')
    updated=deepcopy(registry);updated['profiles'][PROFILE]=profile
    encoded=(json.dumps(updated,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf8')
    ROOT.mkdir(parents=True);(ROOT/'release_stack.before.raw').write_bytes(raw);save(ROOT/'release_stack.before.json',registry)
    (ROOT/'build_integrated_release.py.before').write_bytes(before);(ROOT/'builder.stage.bin').write_bytes(stage.encode());save(ROOT/'release_stack.planned.json',updated)
    assert rp.read_bytes()==raw and builder.read_bytes()==before
    temporary=builder.with_name('build_integrated_release_v8299.tmp');assert not temporary.exists();temporary.write_bytes(after);os.replace(temporary,builder)
    with rp.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    restored=deepcopy(read(rp));restored['profiles'].pop(PROFILE)
    assert restored==registry and builder.read_bytes().replace(stage.encode(),b'',1)==before
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v8259',parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),
        release_config=owned.CONFIG,release_config_sha256=sha(Path(owned.CONFIG).read_bytes()),manuscripts=conf['manuscripts'],reference_map=conf['reference_map'],
        registry_before_sha256=sha(raw),registry_after_sha256=sha(rp.read_bytes()),builder_before_sha256=sha(before),builder_after_sha256=sha(builder.read_bytes()),
        positive_proof=str(POSITIVE),positive_proof_sha256=sha(POSITIVE.read_bytes()),negative_cases=str(NEGATIVE),negative_cases_sha256=sha(NEGATIVE.read_bytes()),negative_count=71,
        all_negatives_reject_before_any_wholeNDS_commit=True,expected_manifest_batches=641,accepted_layers=114,promoted_profile_unchanged='all-routes-unified-v4701',
        reference_ROM=conf['reference_ROM'],reference_ROM_sha256=conf['reference_ROM_sha256'],producer_sha256=sha(Path(__file__).read_bytes()),new_credit=0,full_goal_complete=False))
    print('Registered experimental V8300 aftercompleteV8259:641expected manifest batches/114accepted;main unchanged;completioncredit pending verified release.')
