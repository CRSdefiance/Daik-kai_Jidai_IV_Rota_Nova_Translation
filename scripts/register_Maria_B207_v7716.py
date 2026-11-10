"""Append the sealed Maria exchange after every V7660 layer; preserve all existing profiles."""
import json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import maria_B207_editorial_v2 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Maria_B207_final_paths_v7712 import PARENT
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B207_registration_v7716')
PROFILE='all-routes-unified-v7717'
VALIDATION=Path('work/analysis/maria_B207_atomic_challenges_v7715b/atomic_validation_receipt.json')
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists();r=read(VALIDATION);config=Path(r['config']);conf=read(config);cases=read(r['negative_cases'])
    assert r['positive_records']==18 and r['negative_count']==len(cases)==163 and all(c['rejected'] and c['commit_calls']==0 for c in cases) and r['all_negatives_reject_before_any_files_list_commit']
    assert r['all_dependency_digests_deliberately_bypassed'] and sha(config.read_bytes())==r['config_sha256'] and sha(PARENT.read_bytes())==r['parent_ROM_sha256'] and sha(Path(r['negative_cases']).read_bytes())==r['negative_cases_sha256']
    for p,h in conf['dependencies'].items():assert sha(Path(p).read_bytes())==h
    verified=read('work/analysis/editorial_handoff_verification_v7710/verified_handoff.json');assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==verified['ledger_sha256']
    rp,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py');raw,before=rp.read_bytes(),builder.read_bytes();registry=read(rp)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701' and len(read(PARENT.with_suffix('.manifest.json'))['batches'])==628
    stage=b'''    maria_B207_config = profile_config.get('maria_B207_editorial')
    if maria_B207_config:
        from dk4tool.patch.maria_B207_editorial_v2 import apply_release as apply_maria_B207

        maria_B207_report = apply_maria_B207(candidate, baseline, maria_B207_config)
        for maria_B207_file in maria_B207_report['files']:
            maria_B207_path = maria_B207_file['file_path']
            grouped.setdefault(maria_B207_path, [])
            changed_records.setdefault(maria_B207_path, []).extend(row['id'] for row in maria_B207_file['changed_records'])
            relocation_checks.setdefault(maria_B207_path, {})['maria_B207_editorial'] = {
                'release_config': maria_B207_config,
                'release_config_sha256': sha256(Path(maria_B207_config).read_bytes()),
                'proof': maria_B207_report}
        for maria_B207_manuscript in maria_B207_report['manuscripts']:
            more_batch = Path(maria_B207_manuscript)
            if more_batch in release_batches:
                raise ValueError('Maria B207 must run once after the complete V7660 stack')
            release_batches.append(more_batch)

'''
    anchor=b'    # Lexically valid "% o"';assert before.count(anchor)==1 and b"profile_config.get('maria_B207_editorial')" not in before
    after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec')
    assert after.index(b"profile_config.get('papal_trade_editorial')")<after.index(stage)<after.index(anchor)
    profile=deepcopy(registry['profiles']['all-routes-unified-v7660'])
    profile.update(status='experimental',maria_B207_editorial=owned.CONFIG,
        description='Complete V7660 plus18 clean-Japanese whole-exchange Maria SC3B207 decisions:13 revisions/five justified retentions. Preserve Carlo/Filippo familiarity,tentative unspecified recovery,aboard-ship fact,great-grandfather,papal direct rule/donations/trade decline,reported finds,prospective blessings andconditional discovery. Carlo Sinat/Trader are scoped retained labels;Filippo is a body alias,European is excluded from names,item106 unchanged. Preserve distinct CS0101,20 commands18 complete preambles,A0001456->1458,end1464->1466 andseparate storage tail2. Fullclean/predecessor inverse;one final files-list assignment aftercomplete validation.',
        note='18 positives/89 policy corruptions andone full-ROM positive/163 production corruptions pass. Preserve original failed v1 positive and156 rejections/seven blocked commit traps;v2 closes document file/route/ROM-hash identity gaps. All dependency hashes bypassed forproduction challenges.72 logical/72 compiled alignments,72 stored alignments(28 fresh44 own-context reuse),seven zero-ink tails,all18 one-page native paragraphs andseven informational row-count reasons/no warnings.303 native loads606 parent modes,shipped caller census,actual original7-command Maria initializer including2000 A-wait. Paired16001-frame disclosed complete source/English fixtures cover18 speeches/74 complete body74 headers each,zero partial orunknown traces,all27 original commands/normal returns and18 identical scene/portrait/header pairs. All36 panes/nine sheets viewed. Exits8696/8694;Hangzhou return8780 isinitialized,not original optional location. Preserve19 command/eight duration rows,104/123 lateRGB differences,models/persistent_objects/calendar/actors differences andseeds1942423083/327589790. No fullRAM/everyframe/future/broad simulation/causal-equivalence claim. Existing exact system-only unlock isexplicit andearned=false. Natural optional activation/location,earned progress,full mechanics/routes/hardware andfull207 names remainopen. Preserve full four-storyline/earlier dialogue/town/shop/random/Help/prose/retrospective-wrap scope,all prior artifacts,graphics separation andlater technical re-audit. MainV4701 unchanged;no separatepackage,promotion,pruning,commit orpush.')
    updated=deepcopy(registry);updated['profiles'][PROFILE]=profile;encoded=(json.dumps(updated,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf8')
    ROOT.mkdir(parents=True);(ROOT/'release_stack.before.raw').write_bytes(raw);save(ROOT/'release_stack.before.json',registry);(ROOT/'build_integrated_release.py.before').write_bytes(before);(ROOT/'builder.stage.bin').write_bytes(stage);save(ROOT/'release_stack.planned.json',updated)
    assert rp.read_bytes()==raw and builder.read_bytes()==before;save(owned.CONFIG,conf);temporary=builder.with_name('build_integrated_release_v7716.tmp');assert not temporary.exists();temporary.write_bytes(after);os.replace(temporary,builder)
    with rp.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    restored=deepcopy(read(rp));restored['profiles'].pop(PROFILE);assert restored==registry and builder.read_bytes().replace(stage,b'',1)==before
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v7660',parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),release_config=owned.CONFIG,release_config_sha256=sha(Path(owned.CONFIG).read_bytes()),manuscripts=conf['manuscripts'],reference_map=conf['reference_map'],reference_map_sha256=sha(Path(conf['reference_map']).read_bytes()),registry_before_sha256=sha(raw),registry_after_sha256=sha(rp.read_bytes()),builder_before_sha256=sha(before),builder_after_sha256=sha(builder.read_bytes()),positive_proof=r['positive_proof'],negative_cases=r['negative_cases'],negative_count=163,all_negatives_reject_before_commit=True,expected_manifest_batches=629,accepted_layers=114,promoted_profile_unchanged='all-routes-unified-v4701',reference_ROM=conf['reference_ROM'],reference_ROM_sha256=conf['reference_ROM_sha256'],original_seven_guard_gaps_preserved_andclosed_in_v2=True,producer_sha256=sha(Path(__file__).read_bytes()),new_credit=0,full_goal_complete=False))
    print('Registered experimental V7717:629 expected batches/114 accepted;all prior profiles andmainV4701 unchanged.')
