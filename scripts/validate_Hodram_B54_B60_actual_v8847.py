"""Validate the production saved-capture reader and reject changed fixture/actual evidence."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_B54_B60_actual_evidence_v1 import check_actual,check_fixtures
from scripts.Hodram_B54_B60_verified_inputs_v8846 import verified_inputs,DOC,NATIVE,REFERENCES,ACTUAL
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B54_B60_actual_validation_v8847')
MODULE=Path('dk4tool/patch/hodram_B54_B60_actual_evidence_v1.py')

def require(value,label):
    if not value:raise ValueError('B54-B60 actual production: '+label)

if __name__=='__main__':
    assert not ROOT.exists();doc,data,frozen,parent,clean,reference,rebuilt,native,protected=verified_inputs()
    protected|={MODULE,Path(__file__)};before={str(p):sha(p.read_bytes()) for p in protected};oldrom=parent.rom;oldbytes=bytes(parent.rom.save())
    result=check_actual(data,doc['records'],parent,clean,rebuilt,native,read,require)
    summary=result['summary'];assert [summary[k] for k in ['whole_actual_frames','complete_actual_page_occurrences','complete_actual_holds','unique_speech_IDs']]==[130014,150,676,63]
    assert len(result['canonical_fixtures'])==12
    cases=[]
    def reject(label,mutate,fixture_only=False):
        d,n,rows=deepcopy(data),deepcopy(native),deepcopy(doc['records']);mutate(d,n,rows)
        assert d!=data or n!=native or rows!=doc['records'],label
        try:
            if fixture_only:check_fixtures(d,rows,parent,clean,rebuilt,require,54)
            else:check_actual(d,rows,parent,clean,rebuilt,n,read,require)
        except ValueError as error:
            message=str(error);assert 'Native dependency changed' not in message and 'Frozen Hodram-B54-B60 contract changed' not in message,(label,message)
            cases.append(dict(label=label,actual_changed_input=True,rejected=True,diagnostic=message))
        else:raise AssertionError('Changed actual evidence accepted:'+label)
        assert parent.rom is oldrom and bytes(parent.rom.save())==oldbytes
    reject('truncated-original-initializer-prefix',lambda d,n,r:d['fixtures']['fixtures'][0].__setitem__('original_opening_prelude_hex',d['fixtures']['fixtures'][0]['original_opening_prelude_hex'][:-2]),True)
    reject('wrong-entire-fixture-ROM-digest',lambda d,n,r:d['fixtures']['fixtures'][0].__setitem__('research_ROM_sha256','0'*64),True)
    reject('changed-command-shift',lambda d,n,r:d['fixtures']['fixtures'][0].__setitem__('constant_shift_bytes',32),True)
    reject('missing-original-command',lambda d,n,r:d['fixtures']['fixtures'][0]['all_original_exchange_commands'].pop(),True)
    reject('invented-actual-event-activation',lambda d,n,r:d['fixtures']['fixtures'][0].__setitem__('initialized_original_Hodram_opening_not_original_event_location_oractivation',False),True)
    reject('wrong-actual-run-length',lambda d,n,r:d['B54_actual']['groups'][0].__setitem__('actual_frames',6000))
    reject('wrong-normal-result-carry',lambda d,n,r:d['B54_actual']['groups'][0]['normal_return']['native_result'].__setitem__(1,1))
    reject('incomplete-body-name-holds',lambda d,n,r:d['B54_actual']['groups'][0]['speeches'][0]['complete_holds'].pop())
    reject('invented-short-variant-visit',lambda d,n,r:d['B58_actual']['groups'][0].__setitem__('unvisited_conditional_text_IDs',[]))
    reject('unapproved-actual-speaker-name',lambda d,n,r:d['B54_actual']['groups'][0]['speeches'][0].__setitem__('name','Hayreddin'))
    def flip_name(d,n,r):
        p=bytearray(n['names'][1]['plane']);p[0]^=1;n['names'][1]['plane']=bytes(p)
    reject('computed-name-leading-pixel-defect',flip_name)
    reject('B53-parser-result-conflated-with-mode',lambda d,n,r:d['B60_actual']['groups'][0]['normal_return'].__setitem__('previous_parser_result_value',1))
    reject('offline-short-status-mislabeled-as-gameplay',lambda d,n,r:r[4].__setitem__('actual_observation_status','paired-initialized-whole-script-every-page-observed'))
    reject('wrong-focused-run-length',lambda d,n,r:d['focus_actual']['groups'][0].__setitem__('actual_frames',7000))
    reject('missing-English-continuation-page-selection',lambda d,n,r:next(s for s in d['B59_actual']['groups'][1]['speeches'] if s['pages']==2)['page_selections'].pop())
    reject('invented-FE-speaker-header',lambda d,n,r:next(s for s in d['B56_actual']['groups'][0]['speeches'] if s['source_selector']==254).__setitem__('name','Girl'))
    assert len(cases)==16 and {str(p):sha(p.read_bytes()) for p in protected}==before and parent.rom is oldrom and bytes(parent.rom.save())==oldbytes
    ROOT.mkdir(parents=True);save(ROOT/'independent_actual_validation.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),actual_summary=summary,
        all_twelve_whole_fixture_inverses_fourteen_saved_runs_all_pages_FE_body_name_holds_andnormal_returns_independently_checked=True,
        prior_verified_native_andreference_inputs_hydrated_by_exact_hash_without_unchanged_reexecution=True,
        native_validation=str(NATIVE),reference_validation=str(REFERENCES),qualified_actual=str(ACTUAL),
        negative_cases=cases,negative_count=len(cases),all_negatives_changed_semantic_inputs_with_frozen_guards_enabled=True,
        all_protected_files_ROMs_registry_ledger_exact_original_NDS_object_identity_andwhole_bytes_unchanged=True,protected_hashes=before,
        B55_and18_B58_conditionals_still_offline_only_no_predicates_orflags_forced=True,new_emulator_runs=0,new_credit=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [DOC,NATIVE,REFERENCES,ACTUAL,MODULE,Path(__file__),Path('scripts/Hodram_B54_B60_verified_inputs_v8846.py')]}))
    print('Actual production:12whole fixture inverses/14saved runs130014frames/676complete holds/150pages/63utterances pass;16semantic defects reject.19offline only;no captures,ROMcommit orcredit.',flush=True)
