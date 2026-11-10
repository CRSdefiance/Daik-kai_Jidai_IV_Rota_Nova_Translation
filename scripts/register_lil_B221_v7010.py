"""Register the validated B221 companions after the complete V6956 stack."""
import ast,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import lil_B221_editorial_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B221_registration_v7010')
PROFILE='all-routes-unified-v7011'
VALIDATION=Path('work/analysis/lil_B221_atomic_v7009')
PARENT=Path('out/all_routes_combined_v6956_candidate.nds')
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    receipt=read(VALIDATION/'atomic_validation_receipt.json');config=Path(receipt['config']);conf=read(config)
    assert receipt['positive_records']==16 and receipt['negative_count']==46 and receipt['all_negatives_reject_before_mutation']
    cases=read(receipt['negative_cases']);assert len(cases)==46 and all(c['rejected'] and c['archive_writes']==0 for c in cases)
    assert sha(config.read_bytes())==receipt['config_sha256'] and sha(PARENT.read_bytes())==receipt['parent_ROM_sha256']
    for p,h in conf['dependencies'].items():assert sha(Path(p).read_bytes())==h,p
    verified=read('work/analysis/editorial_handoff_verification_v6991/verified_handoff.json')
    assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==verified['ledger_sha256']
    registry_path,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py')
    raw,before=registry_path.read_bytes(),builder.read_bytes();registry=read(registry_path)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    prior=read(PARENT.with_suffix('.manifest.json'));assert len(prior['batches'])==611
    template=Path('scripts/register_lil_B201_v5946.py');tree=ast.parse(template.read_text(encoding='utf-8'))
    stages=[n.value.value for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='stage' for t in n.targets)]
    assert len(stages)==1 and isinstance(stages[0],bytes)
    stage=stages[0].replace(b'B201',b'B221').replace(b'V5891',b'V6956')
    anchor=b'    # Lexically valid "% o"'
    assert before.count(anchor)==1 and b"profile_config.get('lil_B221_editorial')" not in before
    after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec')
    assert after.index(b"profile_config.get('lil_B220_editorial')")<after.index(stage)<after.index(anchor)
    assert [n.module for n in ast.walk(ast.parse('if True:\n'+stage.decode())) if isinstance(n,ast.ImportFrom)]==[owned.__name__]
    profile=deepcopy(registry['profiles']['all-routes-unified-v6956'])
    profile.update(status='experimental',lil_B221_editorial=owned.CONFIG,
        description='Complete V6956 plus B221 Crusades and Saladin exchange:14 speeches and two choices,8 revisions/8 justified retentions. All21 original commands,four relative sites,one typed Yes/No menu,A000 and complete normal end preserved;1208-byte inverse/1224-byte target. Both ordinary-input English fixture paths cover all14 speeches,30 native page observations and118 complete body/name holds;two long paragraphs use two original pages. Character viewpoints and hearsay remain attributed;no invented historical facts or effects. Current Lil Argot,Al Shin/full Al Ferid Shin preserved;ten Shopkeeper labels and wider207-name review remain separate.',
        note='46 distinct corruptions reject before any archive write. Source/English exit differs478 frames;17/18 timing differences,13 interval RNG differences each and155 later RGB differences per path remain documented for technical re-audit. Registered build,exact clean-input patch and current startup pending. Main V4701 preserved.')
    updated=deepcopy(registry);updated['profiles'][PROFILE]=profile
    encoded=(json.dumps(updated,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8')
    ROOT.mkdir(parents=True);save(ROOT/'release_stack.before.json',registry)
    (ROOT/'build_integrated_release.py.before').write_bytes(before);(ROOT/'builder.stage.bin').write_bytes(stage)
    save(ROOT/'release_stack.planned.json',updated)
    assert registry_path.read_bytes()==raw and builder.read_bytes()==before
    save(owned.CONFIG,conf);temporary=builder.with_name('build_integrated_release_v7010.tmp')
    assert not temporary.exists();temporary.write_bytes(after);os.replace(temporary,builder)
    with registry_path.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    restored=deepcopy(read(registry_path));restored['profiles'].pop(PROFILE)
    assert restored==registry and builder.read_bytes().replace(stage,b'',1)==before
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v6956',parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),
        release_config=owned.CONFIG,release_config_sha256=sha(Path(owned.CONFIG).read_bytes()),manuscripts={conf[k]:sha(Path(conf[k]).read_bytes()) for k in ['manuscript','choice_manuscript']},
        reference_ROM=conf['reference_ROM'],reference_ROM_sha256=conf['reference_ROM_sha256'],
        reference_map=conf['reference_map'],reference_map_sha256=sha(Path(conf['reference_map']).read_bytes()),
        registry_before_sha256=sha(raw),registry_after_sha256=sha(registry_path.read_bytes()),builder_before_sha256=sha(before),builder_after_sha256=sha(builder.read_bytes()),
        source_stage_template=str(template),source_stage_template_sha256=sha(template.read_bytes()),positive_proof=receipt['positive_proof'],negative_cases=receipt['negative_cases'],negative_count=46,
        all_negatives_reject_before_mutation=True,expected_manifest_batches=613,accepted_layers=114,promoted_profile_unchanged='all-routes-unified-v4701',producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Registered experimental V7011:613 batches/114 accepted;all earlier profiles and main V4701 preserved.',flush=True)
