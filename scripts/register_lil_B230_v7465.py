"""Append B230 after the complete registered V7418 without changing promotion."""
import json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import lil_B230_editorial_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B230_registration_v7465');PROFILE='all-routes-unified-v7466'
VALIDATION=Path('work/analysis/lil_B230_atomic_v7464');PARENT=Path('out/all_routes_combined_v7418_candidate.nds')
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists();r=read(VALIDATION/'atomic_validation_receipt.json');config=Path(r['config']);conf=read(config);cases=read(r['negative_cases'])
    assert r['positive_records']==17 and r['negative_count']==len(cases)==253 and all(c['rejected'] and c['archive_writes']==0 for c in cases) and r['all_negatives_reject_before_mutation'] and r['all17_actual17_pages67_body67_headers_bound'] and r['original_A00025_ends_and_explicit_comparison_limits_bound']
    assert sha(config.read_bytes())==r['config_sha256'] and sha(PARENT.read_bytes())==r['parent_ROM_sha256'] and sha(Path(r['negative_cases']).read_bytes())==r['negative_cases_sha256']
    for p,h in conf['dependencies'].items():assert sha(Path(p).read_bytes())==h
    verified=read('work/analysis/editorial_handoff_verification_v7461/verified_handoff.json');assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==verified['ledger_sha256']
    rp,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py');raw,before=rp.read_bytes(),builder.read_bytes();registry=read(rp)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701' and len(read(PARENT.with_suffix('.manifest.json'))['batches'])==622
    stage=b'''    lil_proof = profile_config.get('lil_B230_editorial')
    if lil_proof:
        from dk4tool.patch.lil_B230_editorial_v1 import apply_release as apply_lil_proof

        lil_proof_report = apply_lil_proof(candidate, baseline, lil_proof)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_proof_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_B230_editorial'] = {
            'release_config': lil_proof,
            'release_config_sha256': sha256(Path(lil_proof).read_bytes()),
            'proof': lil_proof_report}
        more_batch = Path(lil_proof_report['manuscript'])
        if more_batch in release_batches:
            raise ValueError('B230 must run once after the complete V7418 stack')
        release_batches.append(more_batch)

'''
    anchor=b'    # Lexically valid "% o"';assert before.count(anchor)==1 and b"profile_config.get('lil_B230_editorial')" not in before
    after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec');assert after.index(b"profile_config.get('lil_B229_editorial')")<after.index(stage)<after.index(anchor)
    profile=deepcopy(registry['profiles']['all-routes-unified-v7418']);profile.update(status='experimental',lil_B230_editorial=owned.CONFIG,description='Complete V7418 plus17 clean-Japanese B230 whole-exchange decisions:nine revisions andeight justified retentions. Preserve the phoenix opinion question,conditional wish,heard iron/flame-forged helmet report,uncertain exact item52 Phoenix Bascinet name,anticipated battle-usefulness pitch,cheeky memory joke,casual Africa/India callback,Britain clue,personal research beyond northern Europe,warm praise,determined personal someday vow andhopeful close. Event230/action231 requires229. Progressive Lil Argot/Samwell Khan remain;full Samwell ダ Khan catalogue middle stays unapproved. Source988/logical988/tail0 fully inverts;target980/logical978/tail2. All19 commands/17 preambles,selectors2/22,voices3/2,zero macros,A000976->966 andfour-byte end984->974 remain. Seventeen native pages,136 logical/compiled68 stored32 exact reused name alignments,six zero-ink tails,seven row reasons andzero warnings/waivers preserve all base QA.',note='Seventeen policy positives/76 rejections and253 freshly executed actual-changing production corruptions must pass before the sole archive write. All28 observed commands/results/UI,17 scene/portrait pairs and67 body/header holds pass. Source/English normal exits6935/6933,seventeen timing/RNG comparison rows,six durations,88of151 later RGB differences,models/persistent/calendar/actor differences,captains2/2,final seeds2748498268/2743647194 andB120 ends11736/11736 remain explicit. Item52 uses static current ARM9 storage,distinct from item53 deployed-payload-relative offset132. Clean/current COMMON688 supports Britain distinct from England;unchanged Japanese country-table literal remains anunapproved consumer lead. Initialized B22 doesnot prove natural230 activation,original location,earned229,full effects,routes orhardware. No whole-RAM/every-frame/future/broad-simulation orcomplete causal claim. Preserve the country-reader guard failure/successor,earlier weak-in layout warning/refinements andconsole-only duplicate word. Full editorial/name/earlier-wrap objective andall artifacts remain;mainV4701 unchanged;exact patch/current startup pending;no automatic promotion.')
    updated=deepcopy(registry);updated['profiles'][PROFILE]=profile;encoded=(json.dumps(updated,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode()
    ROOT.mkdir(parents=True);(ROOT/'release_stack.before.raw').write_bytes(raw);save(ROOT/'release_stack.before.json',registry);(ROOT/'build_integrated_release.py.before').write_bytes(before);(ROOT/'builder.stage.bin').write_bytes(stage);save(ROOT/'release_stack.planned.json',updated)
    assert rp.read_bytes()==raw and builder.read_bytes()==before;save(owned.CONFIG,conf);temporary=builder.with_name('build_integrated_release_v7465.tmp');assert not temporary.exists();temporary.write_bytes(after);os.replace(temporary,builder)
    with rp.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    restored=deepcopy(read(rp));restored['profiles'].pop(PROFILE);assert restored==registry and builder.read_bytes().replace(stage,b'',1)==before
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v7418',parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),release_config=owned.CONFIG,release_config_sha256=sha(Path(owned.CONFIG).read_bytes()),manuscript=conf['manuscript'],reference_map=conf['reference_map'],reference_map_sha256=sha(Path(conf['reference_map']).read_bytes()),registry_before_sha256=sha(raw),registry_after_sha256=sha(rp.read_bytes()),builder_before_sha256=sha(before),builder_after_sha256=sha(builder.read_bytes()),positive_proof=r['positive_proof'],negative_cases=r['negative_cases'],negative_count=253,all_negatives_reject_before_mutation=True,expected_manifest_batches=623,accepted_layers=114,promoted_profile_unchanged='all-routes-unified-v4701',reference_ROM=conf['reference_ROM'],reference_ROM_sha256=conf['reference_ROM_sha256'],producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Registered experimental V7466:623 expected batches/114 accepted. All earlier profiles andmainV4701 preserved.')
