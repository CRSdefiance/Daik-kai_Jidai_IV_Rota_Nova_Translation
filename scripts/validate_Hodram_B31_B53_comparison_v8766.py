"""Independently recompute saved state/timing/RGB comparisons with semantic defects."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_B31_B53_comparison_v1 import check_comparisons
from scripts.Hodram_B31_B53_verified_inputs_v8763 import verified_inputs,DOC
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B31_B53_comparison_validation_v8766')
ACTUAL=Path('work/analysis/Hodram_B31_B53_actual_validation_v8764/independent_actual_validation.json')
MODULE=Path('dk4tool/patch/hodram_B31_B53_comparison_v1.py')

def require(value,label):
    if not value:raise ValueError('B31/B53 comparison production: '+label)

if __name__=='__main__':
    assert not ROOT.exists();actual=read(ACTUAL)
    assert actual['manuscript_sha256']==sha(DOC.read_bytes()) and actual['all_four_whole_fixture_inverses_all_saved_trace_fields_body_name_holds_andnormal_returns_independently_checked'] and actual['negative_count']==13
    for p,h in actual['evidence'].items():assert sha(Path(p).read_bytes())==h,p
    doc,data,frozen,parent,clean,reference,rebuilt,native,protected=verified_inputs()
    protected|={ACTUAL,MODULE,Path(__file__)};before={str(p):sha(p.read_bytes()) for p in protected};oldrom=parent.rom;oldbytes=bytes(parent.rom.save())
    result=check_comparisons(data,parent,read,require)
    assert result['later_full_RGB_pairs_recomputed']==68 and len(result['groups'])==2
    assert [g['command_differences'] for g in result['groups']]==[2,1] and all(all(g['five_native_component_equality'].values()) and g['whole_actors_equal'] for g in result['groups'])
    cases=[]
    def reject(label,mutate):
        d=deepcopy(data);mutate(d);assert d!=data,label
        try:check_comparisons(d,parent,read,require)
        except ValueError as error:
            message=str(error);assert 'Native dependency changed' not in message and 'Frozen Hodram-B31-B53 contract changed' not in message,(label,message)
            cases.append(dict(label=label,actual_changed_input=True,rejected=True,diagnostic=message))
        else:raise AssertionError('Changed comparison evidence accepted:'+label)
        assert parent.rom is oldrom and bytes(parent.rom.save())==oldbytes
    reject('missing-whole-block-pair',lambda d:d['comparison']['groups'].pop())
    reject('wrong-block-membership',lambda d:d['comparison']['groups'][0].__setitem__('block',53))
    reject('unsupported-input-case',lambda d:d['comparison']['groups'][0].__setitem__('ordinary_default_input_case',False))
    reject('suppressed-source-decoded-length-difference',lambda d:d['comparison']['groups'][0]['command_comparison_differences'].pop())
    reject('invented-duration-difference',lambda d:d['comparison']['groups'][0]['duration_differences'].append(dict(source_command_ordinal=0,word=0,clean=0,revised=1)))
    reject('wrong-complete-speaker-header-comparison',lambda d:d['comparison']['groups'][0]['scene_pairs'][0].__setitem__('complete_header_region_RGB_equal',False))
    reject('wrong-final-captain',lambda d:d['comparison']['groups'][0]['final_native_values'][0].__setitem__('captain_ID',2))
    reject('wrong-final-whole-actors',lambda d:d['comparison']['groups'][0]['final_native_values'][0].__setitem__('whole_actor_sha256','0'*64))
    reject('wrong-final-RNG-comparison',lambda d:d['comparison']['groups'][0]['final_PRNG_seeds'].__setitem__(0,0))
    reject('wrong-existing-parser-result-carry',lambda d:d['comparison']['groups'][0]['script_returns'][0]['native_result'].__setitem__(1,0))
    reject('missing-complete-later-framebuffer-pair',lambda d:d['comparison']['groups'][0]['later_RGB_comparisons'].pop())
    reject('invented-opaque-control-meaning',lambda d:d['comparison']['groups'][0].__setitem__('opaque_effect_semantics_not_inferred_from_structural_preservation',False))
    assert len(cases)==12 and {str(p):sha(p.read_bytes()) for p in protected}==before and parent.rom is oldrom and bytes(parent.rom.save())==oldbytes
    ROOT.mkdir(parents=True);save(ROOT/'independent_comparison_validation.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),comparison_summary=result,
        four_saved_complete_final_snapshots_native_components_wholeactors_captain_RNG_calendar_and68_full_RGBpairs_recomputed=True,
        all_three_decodedlength_differences_andzero_duration_UI_request_boundary_RNG_followingcommand_differences_preserved=True,
        exact_previous_actual_reader_proof_bound_without_replaying_captures_oractual_reader=True,
        negative_cases=cases,negative_count=len(cases),all_negatives_changed_semantic_inputs_with_frozen_guards_enabled=True,
        all_protected_files_ROMs_registry_ledger_exact_original_NDS_object_identity_andwhole_bytes_unchanged=True,protected_hashes=before,
        no_future_simulation_natural_activation_fullcatalogue_fullroute_hardware_orunvisited_shortvariant_claim=True,
        new_emulator_runs=0,new_credit=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [DOC,ACTUAL,MODULE,Path(__file__),Path('scripts/Hodram_B31_B53_verified_inputs_v8763.py')]}))
    print('Comparison production:4saved final snapshots/5native components/actors/captain1/RNG/calendar/68fullRGBpairs pass;12semantic defects reject. No capture replay,ROMcommit orcredit.',flush=True)
