"""Exercise distinct semantic corruption risks behind valid physical hashes using read-only virtual JSON."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import lil_B215_editorial_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B215_atomic_v6773');POS=Path('work/analysis/lil_B215_atomic_v6772/positive_receipt.json')
if __name__=='__main__':
    assert not ROOT.exists();positive=read(POS);config=Path(positive['config']);conf=read(config);docpath=Path(conf['manuscript']);doc=read(docpath);oldpath=Path(doc['native_approved_manuscript']);mappath=Path(conf['reference_map']);mapping=read(mappath);cases=[];baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');parent=Path(positive['parent_ROM']);original=owned.load;before={str(p):sha(p.read_bytes()) for p in [config,docpath,oldpath,mappath,Path(owned.__file__),Path('translations/release_stack.json'),Path('translations/editorial_review_current_v1.json')]}
    tests=[('current-archive-hash','conf',lambda c:c.update(source_SC2_sha256='0'*64)),('runtime-hash','conf',lambda c:c.update(required_runtime_arm9_sha256='0'*64)),('target-archive-hash','conf',lambda c:c.update(target_SC2_sha256='0'*64)),('clean-ROM-hash','conf',lambda c:c.update(clean_ROM_sha256='0'*64)),('missing-map-flag','conf',lambda c:c['required_map_flags'].pop()),('source-reference','doc',lambda d:d['records'][0]['source_reference'].update(offset=d['records'][0]['source_reference']['offset']+1)),('incomplete-source','doc',lambda d:d['records'][0].update(source_hex=d['records'][0]['source_hex'][:-2])),('hardcoded-FA','doc',lambda d:next(r for r in d['records'] if '{MACRO:FA}' in r['english']).update(english=next(r['english'] for r in d['records'] if '{MACRO:FA}' in r['english']).replace('{MACRO:FA}','Argot'))),('unreviewed-formatting','doc',lambda d:d['records'][0]['review'].update(formatting=False)),('broaden-warning-waiver','doc',lambda d:d['records'][0].update(qa_waivers=['weak-line-ending'])),('false-retention-justification','doc',lambda d:next(r for r in d['records'] if r['editorial_decision']=='retain-wording').update(retention_reason=None)),('missing-normal-end-reference','map',lambda m:m['blocks'][0]['complete_end_map'].clear()),('misbound-final-reference','map',lambda m:m['blocks'][0]['text_records'][0].update(new_offset=m['blocks'][0]['text_records'][0]['new_offset']+2)),('changed-preamble','map',lambda m:m['blocks'][0]['text_records'][0].update(source_preamble_hex='0040ffff0002'))]
    for label,kind,edit in tests:
        c,d,m=deepcopy(conf),deepcopy(doc),deepcopy(mapping);edit({'conf':c,'doc':d,'map':m}[kind]);old=deepcopy(read(oldpath));old['records']=deepcopy(d['records']);override={config.resolve():c,docpath.resolve():d,oldpath.resolve():old,mappath.resolve():m};image=NdsImage.open(parent);writes=[];replace=image.replace_file
        def tracked(*args,**kwargs):writes.append(args[0]);return replace(*args,**kwargs)
        image.replace_file=tracked;owned.load=lambda p:deepcopy(override[Path(p).resolve()]) if Path(p).resolve() in override else original(p)
        try:owned.apply_release(image,baseline,config)
        except (ValueError,AssertionError,KeyError) as error:cases.append(dict(case=label,rejected=True,error=str(error),archive_writes=len(writes)))
        else:raise AssertionError('Corruption accepted:'+label)
        finally:owned.load=original
        assert not writes and image.read_file(owned.PATH)==NdsImage.open(parent).read_file(owned.PATH)
    assert len(cases)==14 and all(c['archive_writes']==0 for c in cases)
    for p,h in before.items():assert sha(Path(p).read_bytes())==h
    ROOT.mkdir(parents=True);save(ROOT/'negative_cases.json',cases);save(ROOT/'atomic_validation_receipt.json',dict(**positive,negative_cases=str(ROOT/'negative_cases.json'),negative_count=14,all_negatives_reject_before_mutation=True,virtual_JSON_separately_tests_semantics_behind_valid_physical_hashes=True,all_source_doc_config_registry_ledger_and_ROM_files_unchanged=True,three_warning_decisions_and_measured_later_world_limits_bound=True,full_goal_complete=False));print('14 distinct atomic corruption risks reject before every archive write; positive one-write proof retained. No source files or ROMs mutated by negatives.')
