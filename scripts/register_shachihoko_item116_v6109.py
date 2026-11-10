"""Append the approved coordinated item correction after all591 V6050 batches."""
import ast,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import shachihoko_item116_editorial_v2 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/shachihoko_registration_v6109')
PROFILE='all-routes-unified-v6110'
VALIDATION=Path('work/analysis/shachihoko_atomic_v6108b/atomic_validation_receipt.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v6091/verified_handoff.json')
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists();proof=read(VALIDATION);confpath=Path(proof['config']);conf=read(confpath)
    assert proof['all_negatives_reject_before_any_image_mutation'] and proof['negative_count']==35 and proof['positive_records']==2 and sha(confpath.read_bytes())==proof['config_sha256']
    assert sha(Path(proof['positive_proof']).read_bytes())==proof['positive_proof_sha256']
    for p,h in conf['dependencies'].items():assert sha(Path(p).read_bytes())==h
    prior=read(PRIOR);parent=Path(prior['candidate']);assert sha(parent.read_bytes())==prior['candidate_sha256']==proof['parent_ROM_sha256'] and sha(Path('translations/editorial_review_current_v1.json').read_bytes())==prior['ledger_sha256']
    regpath,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py');raw,before=regpath.read_bytes(),builder.read_bytes();registry=read(regpath)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert len(read(parent.with_suffix('.manifest.json'))['batches'])==591
    stage=b'''    item_config = profile_config.get('shachihoko_item116_editorial')
    if item_config:
        from dk4tool.patch.shachihoko_item116_editorial_v2 import apply_release as apply_item116

        item_report = apply_item116(candidate, baseline, item_config)
        for item_path in ['/__arm9__.bin', '/COMMON/MESFILE.DK4']:
            grouped.setdefault(item_path, [])
            changed_records.setdefault(item_path, []).extend(row['id'] for row in item_report['changed_records'] if row['file_path'] == item_path)
            relocation_checks.setdefault(item_path, {})['shachihoko_item116_editorial'] = {
                'release_config': item_config,
                'release_config_sha256': sha256(Path(item_config).read_bytes()),
                'proof': item_report}
        more_batch = Path(item_report['manuscript'])
        if more_batch in release_batches:
            raise ValueError('Item116 correction must run once after the complete V6050 stack')
        release_batches.append(more_batch)

'''
    anchor=b'    # Lexically valid "% o"';assert before.count(anchor)==1 and b"profile_config.get('shachihoko_item116_editorial')" not in before
    after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec');assert [n.module for n in ast.walk(ast.parse('if True:\n'+stage.decode())) if isinstance(n,ast.ImportFrom)]==[owned.__name__]
    profile=deepcopy(registry['profiles'][prior['profile']]);profile.update(status='experimental',shachihoko_item116_editorial=owned.CONFIG,
        description='Complete V6050 plus source-bound item116 Shachihoko title and COMMON2931/private description correction. Both active descriptions agree;all217 other descriptions/names,all story files/fonts/graphics and existing controls remain. The full134-character paragraph is preserved through a224-byte owned late-pool extension. Fresh31 whole startup/town screens and6 actor/captain models match V6050;native autoload/cache/arena/ABI extents pass.218 actual-snapshot description lookups and item-name getters/436 callers,24 native detail planes,8 actual menu fields plus current card/acquisition glyphs pass. Ordinary menu open/hold/back-to-port is observed in a whole clean B204 initialized-Amsterdam fixture;not natural event activation or earned route progress.',
        note='Two complete v2 records and35 pre-commit negative controls approved. Registered ROM/clean-input patch/regressions pending. One previously uncredited COMMON description may receive disjoint credit after integration;static item title/generic notice are not duplicate dialogue credit. All207 actor names/aliases,all routes and wider editorial scope stay open. Main V4701,all prior profiles,ROMs and translations preserved;graphics and later older-record re-audit separate.')
    updated=deepcopy(registry);updated['profiles'][PROFILE]=profile;encoded=(json.dumps(updated,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8')
    ROOT.mkdir(parents=True);save(ROOT/'release_stack.before.json',registry);(ROOT/'build_integrated_release.py.before').write_bytes(before);(ROOT/'builder.stage.bin').write_bytes(stage);save(ROOT/'release_stack.planned.json',updated)
    assert regpath.read_bytes()==raw and builder.read_bytes()==before and not Path(owned.CONFIG).exists();save(owned.CONFIG,conf)
    temp=builder.with_name('build_integrated_release_v6109.tmp');assert not temp.exists();temp.write_bytes(after);os.replace(temp,builder)
    with regpath.open('r+b') as f:f.write(encoded);f.truncate();f.flush();os.fsync(f.fileno())
    restored=deepcopy(read(regpath));restored['profiles'].pop(PROFILE);assert restored==registry and builder.read_bytes().replace(stage,b'',1)==before
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile=prior['profile'],parent_ROM=str(parent),parent_ROM_sha256=sha(parent.read_bytes()),
        release_config=owned.CONFIG,release_config_sha256=sha(Path(owned.CONFIG).read_bytes()),registry_before_sha256=sha(raw),registry_after_sha256=sha(regpath.read_bytes()),builder_before_sha256=sha(before),builder_after_sha256=sha(builder.read_bytes()),
        expected_manifest_batches=592,accepted_layers=114,negative_count=35,all_negatives_reject_before_any_image_mutation=True,
        all_previous_profiles_and_promoted_V4701_preserved=True,prior_verified_handoff=str(PRIOR),prior_verified_handoff_sha256=sha(PRIOR.read_bytes()),
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Registered experimental V6110 after completeV6050:592 expected batches/114 accepted;35 pre-commit negatives pass. Every prior profile/mainV4701 preserved.')
