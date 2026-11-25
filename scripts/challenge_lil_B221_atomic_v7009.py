"""Reject actual-changing B221 control, provenance, pagination and choice corruptions before writes."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import lil_B221_editorial_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B221_atomic_v7009')
POSITIVE=Path('work/analysis/lil_B221_atomic_v7008/positive_receipt.json')

if __name__=='__main__':
    assert not ROOT.exists()
    positive=read(POSITIVE);config=Path(positive['config']);conf=read(config)
    docpath=Path(conf['manuscript']);menupath=Path(conf['choice_manuscript']);mappath=Path(conf['reference_map'])
    doc,menu,mapping=map(read,[docpath,menupath,mappath])
    oldpath=Path(doc['native_approved_manuscript']);oldmenu=Path(menu['native_approved_manuscript'])
    actualpath=Path(doc['actual_English_proof']);namepath=Path(doc['speaker_name_review']);laterpath=Path(doc['later_scope_proof']);viewpath=Path(doc['actual_English_view'])
    actual,names,later,view=map(read,[actualpath,namepath,laterpath,viewpath])
    baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');parent=Path(positive['parent_ROM'])
    original=owned.load;parent_image=NdsImage.open(parent);cases=[]
    paths=[config,docpath,menupath,oldpath,oldmenu,mappath,actualpath,namepath,laterpath,viewpath,
        Path(owned.__file__),Path('translations/release_stack.json'),Path('translations/editorial_review_current_v1.json'),parent]
    before={str(p):sha(p.read_bytes()) for p in paths}
    tests=[
        ('current-archive-hash','conf',lambda c:c.update(source_SC2_sha256='0'*64)),
        ('runtime-hash','conf',lambda c:c.update(required_runtime_arm9_sha256='0'*64)),
        ('COMMON-hash','conf',lambda c:c.update(required_runtime_common_sha256='0'*64)),
        ('target-archive-hash','conf',lambda c:c.update(target_SC2_sha256='0'*64)),
        ('clean-ROM-hash','conf',lambda c:c.update(clean_ROM_sha256='0'*64)),
        ('missing-prior-cumulative-file','conf',lambda c:c['source_files'].pop(next(iter(c['source_files'])))),
        ('missing-map-flag','conf',lambda c:c['required_map_flags'].pop()),
        ('source-reference','doc',lambda d:d['records'][0]['source_reference'].update(offset=d['records'][0]['source_reference']['offset']+1)),
        ('incomplete-source','doc',lambda d:d['records'][0].update(source_hex=d['records'][0]['source_hex'][:-2])),
        ('invented-substitution','doc',lambda d:d['records'][0].update(english=d['records'][0]['english']+' {MACRO:FA}')),
        ('unreviewed-formatting','doc',lambda d:d['records'][0]['review'].update(formatting=False)),
        ('broaden-warning-waiver','doc',lambda d:d['records'][0].update(qa_waivers=['weak-line-ending'])),
        ('false-retention-justification','doc',lambda d:next(r for r in d['records'] if r['editorial_decision']=='retain-wording').update(retention_reason=None)),
        ('omitted-R67-auxiliary-boundary-reason','doc',lambda d:next(r for r in d['records'] if r['source_record_index']==67).update(reviewed_ordinary_boundaries=[])),
        ('lost-R46-page-continuation','doc',lambda d:next(r for r in d['records'] if r['source_record_index']==46).update(native_page_count=1)),
        ('lost-R60-page-boundary-reason','doc',lambda d:next(r for r in d['records'] if r['source_record_index']==60).update(reviewed_native_page_boundary=None)),
        ('ordinary-paragraph-eight-rows','doc',lambda d:d['records'][0].update(native_profile_maximum_total_rows=8)),
        ('missing-normal-end-reference','map',lambda m:m['blocks'][0]['complete_end_map'].clear()),
        ('wrong-normal-end-reference','map',lambda m:m['blocks'][0]['complete_end_map'][0].update(target_offset=1222)),
        ('flagged-end-instead-of-original-normal','map',lambda m:m['blocks'][0]['complete_end_map'][0].update(source_hex='00000080')),
        ('misbound-final-reference','map',lambda m:m['blocks'][0]['text_records'][0].update(new_offset=m['blocks'][0]['text_records'][0]['new_offset']+2)),
        ('changed-complete-preamble','map',lambda m:m['blocks'][0]['text_records'][0].update(source_preamble_hex='0040ffff0011')),
        ('false-actual-speech-scope','doc',lambda d:d['records'][0].update(actual_record_observed=False)),
        ('changed-A000-operands','map',lambda m:m['blocks'][0]['original_A000_map'][0].update(source_hex='00a0ffff48000110')),
        ('invented-C200','map',lambda m:m['blocks'][0]['original_C200_map'].append(dict(source_offset=1194,target_offset=1210,extent=2,source_hex='00c2'))),
        ('missing-relative-site','map',lambda m:m['blocks'][0]['relative_skip_fixups'].pop()),
        ('stale-relative-span','map',lambda m:m['blocks'][0]['relative_skip_fixups'][2].update(target_span=m['blocks'][0]['relative_skip_fixups'][2]['source_span'])),
        ('misbound-relative-destination','map',lambda m:m['blocks'][0]['relative_skip_fixups'][1].update(new_matched_skip_target=m['blocks'][0]['relative_skip_fixups'][1]['new_matched_skip_target']+2)),
        ('wrong-original-choice-condition','map',lambda m:m['blocks'][0]['relative_skip_fixups'][0].update(condition='last_result_equals1')),
        ('wrong-source-relative-operand','map',lambda m:m['blocks'][0]['relative_skip_fixups'][0].update(source_span=6)),
        ('lost-nested-branch-ancestor','map',lambda m:next(r for r in m['blocks'][0]['command_map'] if r['source_0100_ancestors']).update(target_0100_ancestors=[])),
        ('missing-complete-choice-object','map',lambda m:m['blocks'][0]['choice_commands'].clear()),
        ('wrong-choice-source-command','map',lambda m:m['blocks'][0]['choice_commands'][0].update(old_offset=152)),
        ('reversed-choice-label-references','map',lambda m:m['blocks'][0]['choice_commands'][0]['label_references'].reverse()),
        ('broken-choice-offset-table','map',lambda m:m['blocks'][0]['choice_commands'][0].update(target_hex='002100000000596573004e6f0000')),
        ('misbound-choice-target-pointer','map',lambda m:m['blocks'][0]['choice_commands'][0]['label_references'][0].update(new_offset=134)),
        ('changed-choice-index','menu',lambda d:d['records'][0].update(option_index=1)),
        ('changed-choice-answer','menu',lambda d:d['records'][0].update(english='No')),
        ('unreviewed-choice-formatting','menu',lambda d:d['records'][0]['review'].update(formatting=False)),
        ('lost-choice-retention-reason','menu',lambda d:d['records'][0].update(fresh_retained_wording_justification='')),
        ('erased-second-actual-page','actual',lambda a:next(r for r in a['versions'][0]['actual_panels'] if r['native_pages']==2)['actual_complete_page_holds'][1].clear()),
        ('forced-zero-residual-on-No-path','actual',lambda a:a['versions'][1].update(normal_terminal_result=[0,0])),
        ('closed-unreviewed-Shopkeeper-layer','names',lambda n:n.update(actor85_wider_ten_role_Shopkeeper_layer_still_pending=False)),
        ('unviewed-English-scenes','view',lambda v:v.update(visual_review_pending=True)),
        ('hidden-later-world-limit','later',lambda d:d.update(no_full_RAM_every_frame_future_sequence_broad_simulation_or_complete_causal_claim=False)),
        ('hidden-command-UI-difference','later',lambda d:d['measurements'][0]['command_UI_word_differences'].append(dict(source_offset=1196,source=[0],English=[1]))),
    ]
    bases=dict(conf=conf,doc=doc,menu=menu,map=mapping,actual=actual,names=names,later=later,view=view)
    for label,kind,edit in tests:
        values={k:deepcopy(v) for k,v in bases.items()};edit(values[kind])
        assert values[kind]!=bases[kind],'No-op negative:'+label
        old=deepcopy(read(oldpath));old['records']=deepcopy(values['doc']['records'])
        old_m=deepcopy(read(oldmenu));old_m['records']=deepcopy(values['menu']['records'])
        overrides={config.resolve():values['conf'],docpath.resolve():values['doc'],menupath.resolve():values['menu'],mappath.resolve():values['map'],
            oldpath.resolve():old,oldmenu.resolve():old_m,actualpath.resolve():values['actual'],namepath.resolve():values['names'],laterpath.resolve():values['later'],viewpath.resolve():values['view']}
        image=NdsImage.open(parent);writes=[];replace=image.replace_file
        def tracked(*args,**kwargs):writes.append(args[0]);return replace(*args,**kwargs)
        image.replace_file=tracked
        owned.load=lambda p:deepcopy(overrides[Path(p).resolve()]) if Path(p).resolve() in overrides else original(p)
        try:owned.apply_release(image,baseline,config)
        except (ValueError,AssertionError,KeyError) as exc:cases.append(dict(case=label,rejected=True,error=str(exc),archive_writes=len(writes)))
        else:raise AssertionError('Corruption accepted:'+label)
        finally:owned.load=original
        assert not writes and all(image.read_file(p)==v for _,p,v in parent_image.iter_files()) and all(image.read_file(p)==v for p,v in parent_image.iter_components())
        print('Rejected',label,flush=True)
    assert len(cases)==46 and all(c['archive_writes']==0 for c in cases)
    for path,digest in before.items():assert sha(Path(path).read_bytes())==digest
    ROOT.mkdir(parents=True);save(ROOT/'negative_cases.json',cases)
    receipt=deepcopy(positive);receipt.update(negative_cases=str(ROOT/'negative_cases.json'),negative_count=len(cases),
        all_negatives_reject_before_mutation=True,virtual_JSON_tests_semantics_behind_valid_physical_hashes=True,
        all_source_doc_config_registry_ledger_and_ROM_files_unchanged=True,
        both_choice_residuals_two_continuations_all_four_relatives_and_separate_name_limits_explicit=True,full_goal_complete=False)
    save(ROOT/'atomic_validation_receipt.json',receipt)
    print('46 distinct B221 corruptions rejected before writes;all source artifacts and every ROM file/component unchanged.')
