"""Append B210 and the separately reviewed name field after the full V6488 stack."""
import ast,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import lil_B210_editorial_v1 as story,Al_Ferid_name_release_v1 as name
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/B210_Ferid_registration_v6540');PROFILE='all-routes-unified-v6541';PARENT=Path('out/all_routes_combined_v6488_candidate.nds')
if __name__=='__main__':
    assert not ROOT.exists() and not any(Path(m.CONFIG).exists() for m in [story,name]);receipts=[read(f'work/analysis/{p}/atomic_validation_receipt.json') for p in ['lil_B210_atomic_v6535','Al_Ferid_atomic_v6538']];configs=[]
    assert [r['positive_records'] for r in receipts]==[10,1] and [r['negative_count'] for r in receipts]==[117,69] and all(r['all_negatives_reject_before_mutation'] for r in receipts)
    for r in receipts:
        p=Path(r['config']);assert sha(p.read_bytes())==r['config_sha256'];conf=read(p)
        for dep,h in conf['dependencies'].items():assert sha(Path(dep).read_bytes())==h
        configs.append(conf)
    assert sha(PARENT.read_bytes())==receipts[0]['parent_ROM_sha256'];ref=read('work/analysis/B210_Ferid_reference_v6539/combined_reference_receipt.json');assert sha(Path(ref['research_ROM']).read_bytes())==ref['research_ROM_sha256']
    verified=read('work/analysis/editorial_handoff_verification_v6533/verified_handoff.json');assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==verified['ledger_sha256']
    registry_path,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py');raw,before=registry_path.read_bytes(),builder.read_bytes();registry=read(registry_path)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701' and len(read(PARENT.with_suffix('.manifest.json'))['batches'])==600
    parts=[]
    for key,module,path in [('lil_B210_editorial',story,'/data/SC2.DK4'),('Al_Ferid_name',name,'/__arm9__.bin')]:
        assert ("profile_config.get('"+key+"')").encode() not in before
        parts.append(f'''    added_config = profile_config.get('{key}')
    if added_config:
        from {module.__name__} import apply_release as apply_added

        added_report = apply_added(candidate, baseline, added_config)
        grouped.setdefault('{path}', [])
        changed_records.setdefault('{path}', []).extend(row['id'] for row in added_report['changed_records'])
        relocation_checks.setdefault('{path}', {{}})['{key}'] = {{
            'release_config': added_config,
            'release_config_sha256': sha256(Path(added_config).read_bytes()),
            'proof': added_report}}
        added_batch = Path(added_report['manuscript'])
        if added_batch in release_batches:
            raise ValueError('{key} must run once after the complete V6488 stack')
        release_batches.append(added_batch)

'''.encode())
    stage=b''.join(parts);anchor=b'    # Lexically valid "% o"';assert before.count(anchor)==1;after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec')
    assert after.index(b"profile_config.get('lil_B209_editorial')")<after.index(parts[0])<after.index(parts[1])<after.index(anchor)
    assert [n.module for n in ast.walk(ast.parse('if True:\n'+stage.decode())) if isinstance(n,ast.ImportFrom)]==[story.__name__,name.__name__]
    profile=deepcopy(registry['profiles']['all-routes-unified-v6488']);profile.update(status='experimental',lil_B210_editorial=story.CONFIG,Al_Ferid_name=name.CONFIG,
        description='Complete V6488 plus ten Lil B210 whole-exchange objects: six revisions/four justified retentions. Preserve Al hearsay, red-blade impression, subjective judgments and Lil conditional practical interest without invented sword identity or location. All12 commands,688-byte predecessor inverse,ten original216x64 single pages,80 logical/compiled plus40 stored alignments and39 actual body/name holds. Preserve six timing/four RNG/three duration/116 later RGB and final-state differences without broad simulation equivalence. Separate uniquely owned actor17 additional-name typography changes only full-width F to ASCII in Ferid;all621 pointers,code,fonts,cache plan and123264-byte extent unchanged. Four getters/32 name alignments/complete planes and own target startup pass;full catalogue UI unvisited. All four routes/earlier dialogue/shared town/random/Help/prose/retrospective wraps and207 names remain open;graphics and later older-record re-audit separate.',
        note='117 dialogue plus69 name semantic rejection tests precede each single write;post-name ten dispatch results exact. Cumulative patch/current startup pending. Main V4701 preserved;no automatic promotion.')
    updated=deepcopy(registry);updated['profiles'][PROFILE]=profile;encoded=(json.dumps(updated,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode();ROOT.mkdir(parents=True);save(ROOT/'release_stack.before.json',registry);(ROOT/'build_integrated_release.py.before').write_bytes(before);(ROOT/'builder.stage.bin').write_bytes(stage);save(ROOT/'release_stack.planned.json',updated)
    assert registry_path.read_bytes()==raw and builder.read_bytes()==before
    for module,conf in zip([story,name],configs,strict=True):save(module.CONFIG,conf)
    temporary=builder.with_name('build_integrated_release_v6540.tmp');assert not temporary.exists();temporary.write_bytes(after);os.replace(temporary,builder)
    with registry_path.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    restored=deepcopy(read(registry_path));restored['profiles'].pop(PROFILE);assert restored==registry and builder.read_bytes().replace(stage,b'',1)==before
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v6488',parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),release_configs=[m.CONFIG for m in [story,name]],release_config_sha256=[sha(Path(m.CONFIG).read_bytes()) for m in [story,name]],registry_before_sha256=sha(raw),registry_after_sha256=sha(registry_path.read_bytes()),builder_before_sha256=sha(before),builder_after_sha256=sha(builder.read_bytes()),validation_receipts=receipts,negative_counts=[117,69],all_negatives_reject_before_mutation=True,expected_manifest_batches=602,accepted_layers=114,promoted_profile_unchanged='all-routes-unified-v4701',reference_ROM=ref['research_ROM'],reference_ROM_sha256=ref['research_ROM_sha256'],producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('Registered experimental V6541:602 expected batches/114 accepted;all earlier profiles andmain V4701 preserved.')
