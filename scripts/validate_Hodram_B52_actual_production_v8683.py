"""Independent reader of all six existing B52 fixture traces/body/name masks."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.hodram_B52_profile_v1 import contract,validate_approved_batch,validate_runtime
from dk4tool.patch.hodram_B52_actual_evidence_v1 import check_actual
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B52_actual_production_v8683')
DOC=Path('translations/hodram_B52_editorial_manuscript_v6.json')
PATHS=dict(fixtures='work/analysis/Hodram_B52_fixtures_v8648/two_whole_scripts.json',
    actual='work/analysis/Hodram_B52_actual_v8651/B52/paired_actual_dialogue_headers_flow_returns.json',
    opposition_actual='work/analysis/Hodram_B52_opposition_actual_v8653/B52/paired_actual_dialogue_headers_flow_returns.json',
    focus_actual='work/analysis/Hodram_B52_focus_actual_v8657/B52/paired_actual_dialogue_headers_flow_returns.json',
    models='work/analysis/Hodram_B52_models_v8650/native_models.json',
    relocation='work/analysis/Hodram_B52_references_v8647/source_current_final_map.json',
    native_validation='work/analysis/Hodram_B52_native_production_v8667/native_production_validation.json')

if __name__=='__main__':
    assert not ROOT.exists()
    doc,data=read(DOC),{k:read(p) for k,p in PATHS.items()}
    frozen=contract();validate_approved_batch(doc)
    parent,clean=NdsImage.open(doc['current_ROM']),NdsImage.open('work/clean.nds');validate_runtime(parent)
    assert sha(Path(PATHS['models']).read_bytes())==frozen['dependencies'][str(Path(PATHS['models']).resolve())]
    assert data['native_validation']['positive_native_pages']==6 and data['native_validation']['evidence'][PATHS['models']]==sha(Path(PATHS['models']).read_bytes())
    # Reuse the exact independently validated model bytes; do not rerun the
    # already completed native page renderer to validate the existing captures.
    native=dict(bodies={},names={})
    for version,rows in data['models']['native_models'].items():
        native['bodies'][version]={}
        for row in rows:
            copied=deepcopy(row)
            copied['expanded_body']=bytes.fromhex(row['expanded_native_hex'])
            for page in copied['pages']:
                page['native_plane_bytes']=Path(page['native_plane']).read_bytes()
                assert sha(page['native_plane_bytes'])==page['native_plane_sha256']
            native['bodies'][version][row['id']]=copied
    for row in data['models']['name_planes']:
        plane=Path(row['native_plane']).read_bytes();assert sha(plane)==row['native_plane_sha256']
        native['names'][row['actor_ID']]=dict(plane=plane,text=row['text'],width=row['original_pair_flush_width'])
    rebuilt=dict(target_archive=Path(data['relocation']['target_archive']).read_bytes())

    def require(value,message):
        if not value:raise ValueError('B52 actual production:'+message)

    result=check_actual(data,doc['records'],parent,clean,rebuilt,native,read,require)
    assert result['summary']['complete_actual_holds']==138 and result['summary']['whole_actual_frames']==50406
    negatives=[]

    def reject(label,mutate):
        changed=deepcopy(data);mutate(changed);assert changed!=data
        try:check_actual(changed,doc['records'],parent,clean,rebuilt,native,read,require)
        except ValueError as error:
            assert 'Native dependency changed' not in str(error)
            negatives.append(dict(label=label,actual_changed_input=True,rejected=True,diagnostic=str(error)))
        else:raise AssertionError('Changed actual evidence accepted:'+label)

    reject('whole-fixture-body',lambda d:d['fixtures']['fixtures'][0].__setitem__('fixture_block_hex',d['fixtures']['fixtures'][0]['fixture_block_hex']+'00'))
    reject('natural-activation-overclaim',lambda d:d['fixtures']['fixtures'][1].__setitem__('initialized_original_Hodram_opening_not_original_event_location_oractivation',False))
    reject('default-actual-frame-count',lambda d:d['actual']['groups'][0].__setitem__('actual_frames',10000))
    reject('default-complete-name',lambda d:d['actual']['groups'][0]['speeches'][0].__setitem__('name','Port Captain'))
    reject('opposition-end-kind',lambda d:d['opposition_actual']['groups'][0]['script_return']['native_result'].__setitem__(0,0))
    reject('opposition-unvisited-withdrawal',lambda d:d['opposition_actual']['groups'][0].__setitem__('unvisited_conditional_text_IDs',[]))
    reject('focused-complete-leading-glyph',lambda d:d['focus_actual']['groups'][0]['speeches'][0]['complete_holds'][0].__setitem__('complete_black_ASCII_gray_CP932_gray_leading_internal_final_glyph_masks_equal',False))
    assert len(negatives)==7
    ROOT.mkdir(parents=True)
    save(ROOT/'actual_production_validation.json',dict(summary=result['summary'],negative_count=7,negative_cases=negatives,
         all_actual_fixtures_full_ROM_inverses_inputs_callbacks_resident_payloads_selected_commands_bothends_andglyphholds_independent=True,
         all_138_holds12_pages50406frames_checked_without_new_capture=True,
         exact_independent_native_model_results_reused_not_reexecuted=True,
         all_meaningful_changed_inputs_reject_withfrozen_guards_active=True,
         natural_event_activation_original_location_live_backing_causality_fullroute_orhardware_not_claimed=True,
         no_ROM_atomic_commit_registration_orcompletion_credit=True,full_goal_complete=False,
         evidence={str(p):sha(Path(p).read_bytes()) for p in [DOC,*PATHS.values(),__file__,'dk4tool/patch/hodram_B52_actual_evidence_v1.py']}))
    print('B52 existing actual production:6coldboots/50406frames/138complete body-name holds/12pages,all3speeches/bothchoices/distinct ends;7 changed evidence defects reject. No new capture orROM commit.')
