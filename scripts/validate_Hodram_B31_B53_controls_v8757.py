"""Independently validate native controls; reuse completed glyph/reference inputs by exact hashes."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.hodram_B31_B53_profile_v1 import contract,validate_approved_batch,validate_runtime
from dk4tool.patch.hodram_B31_B53_controls_v1 import check_controls,FLOW
from scripts.review_Hodram_B31_B53_actual_v8744 import PROOFS
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B31_B53_controls_validation_v8757')
DOC=Path('translations/hodram_B31_B53_editorial_manuscript_v5.json')
NAMES=Path('translations/hodram_B31_B53_speaker_name_review_v3.json')
NATIVE=Path('work/analysis/Hodram_B31_B53_native_validation_v8754/independent_native_validation.json')
REFERENCES=Path('work/analysis/Hodram_B31_B53_reference_validation_v8756/independent_reference_validation.json')
MODULE=Path('dk4tool/patch/hodram_B31_B53_controls_v1.py')
def require(value,label):
    if not value:raise ValueError('B31/B53 production controls: '+label)
if __name__=='__main__':
    assert not ROOT.exists();doc=read(DOC);data={k:read(p) for k,p in PROOFS.items()};data.update(manuscript=doc,names=read(NAMES),result_flow=read(FLOW))
    frozen=contract();validate_approved_batch(doc);nativeproof,refproof=map(read,[NATIVE,REFERENCES])
    assert nativeproof['manuscript_sha256']==refproof['manuscript_sha256']==sha(DOC.read_bytes())
    assert nativeproof['six_complete_source_andstored_native_pages_two_current_progressive_names_andall_independent_pixels_exact'] and refproof['positive_complete18command_native_inventories_and3disjoint_source_current_final_references']
    parent,reference=[NdsImage.open(p) for p in [doc['current_ROM'],doc['reference_ROM']]];validate_runtime(parent)
    bank=IlnkContainer.parse(reference.read_file('/data/SC1.DK4')).blocks
    rebuilt=dict(target_blocks={g['block']:Path(g['target_block']).read_bytes() for g in data['relocation']['groups']})
    native=dict(bodies={'revised_English':{}})
    for row in data['models']['native_models']['revised_English']:
        binding=frozen['record_bindings'][row['id']];body=bytes.fromhex(row['expanded_native_hex'])
        assert row['input_hex']==binding['stored_hex'] and bytes.fromhex(binding['stored_hex'])[1:]==body
        native['bodies']['revised_English'][row['id']]=dict(expanded_body=body)
    for g in data['relocation']['groups']:assert rebuilt['target_blocks'][g['block']]==bank[g['block']] and sha(bank[g['block']])==g['target_block_sha256']
    protected={Path(p) for p in frozen['dependencies']}|{DOC,NAMES,NATIVE,REFERENCES,MODULE,Path(__file__),Path('translations/release_stack.json'),Path('translations/editorial_review_current_v1.json'),Path('translations/rom_retention_pins.json'),Path(doc['current_ROM']),Path(doc['reference_ROM']),Path('work/clean.nds')}
    before={str(p):sha(p.read_bytes()) for p in protected};before_rom=bytes(parent.rom.save());before_object=parent.rom
    result=check_controls(data,doc['records'],parent,reference,rebuilt,native,read,require)
    assert [result[k] for k in ['independent_final_dispatches','relative_sites','native_relative_cases','raw_query_cases','original_EV1_entries','opaque_structural_decode_pairs','normal_seeded_ends','original_result_channel_cases']]==[3,4,20,1,4,8,50,50]
    cases=[]
    def reject(label,mutate):
        d,b,n=deepcopy(data),deepcopy(rebuilt),deepcopy(native);mutate(d,b,n);assert d!=data or b!=rebuilt or n!=native,label
        try:check_controls(d,doc['records'],parent,reference,b,n,read,require)
        except ValueError as error:
            text=str(error);assert 'Native dependency changed' not in text and 'Frozen Hodram-B31-B53 contract changed' not in text,(label,text)
            cases.append(dict(label=label,actual_changed_input=True,rejected=True,diagnostic=text))
        else:raise AssertionError('Changed controls evidence accepted:'+label)
        assert parent.rom is before_object and bytes(parent.rom.save())==before_rom
    reject('wrong-source-context-hash',lambda d,b,n:d['source_controls'].__setitem__('current_native_input_sha256','0'*64))
    reject('invented-original-event-completion',lambda d,b,n:d['source_controls']['original_EV1_entry']['rows'][0].__setitem__('original_completion_flag_in_current_opening',1))
    reject('wrong-caller-result-channel',lambda d,b,n:d['result_flow']['caller_fragment_cases'][0].__setitem__('next_parser_r3',1))
    reject('untrusted-dispatch-adapter',lambda d,b,n:d['source_display']['source_owned_dispatch_adapters'].__setitem__('dispatch',d['source_display']['source_owned_dispatch_adapters']['dispatch']+'\n# untrusted'))
    reject('untrusted-macro-body-adapter',lambda d,b,n:d['source_display'].__setitem__('source_owned_macro_body_adapter',d['source_display']['source_owned_macro_body_adapter']+'\n# untrusted'))
    reject('missing-source-block',lambda d,b,n:d['relocation']['groups'].pop())
    reject('truncated-target-block',lambda d,b,n:b['target_blocks'].__setitem__(53,b['target_blocks'][53][:-2]))
    reject('wrong-relocated-relative-endpoint',lambda d,b,n:d['relocation']['groups'][0]['relocated_skip_cases'][0]['cases'][0].__setitem__('next_offset',d['relocation']['groups'][0]['relocated_skip_cases'][0]['cases'][0]['next_offset']+2))
    reject('wrong-stored-dispatch-actor',lambda d,b,n:d['stored']['records'][0]['original_dispatch'].__setitem__('resolved_actor_ID',113))
    reject('wrong-computed-stored-text',lambda d,b,n:n['bodies']['revised_English'][doc['records'][0]['id']].__setitem__('expanded_body',n['bodies']['revised_English'][doc['records'][0]['id']]['expanded_body']+b'x'))
    reject('wrong-unforced-query-sixword-result',lambda d,b,n:d['stored']['fresh_target_query_cases'][0]['native_result'].__setitem__(1,0))
    reject('truncated-declared-target-terminal',lambda d,b,n:d['relocation']['groups'][1]['all_target_commands'][-1].__setitem__('native_extent',2))
    assert len(cases)==12 and {str(p):sha(p.read_bytes()) for p in protected}==before and parent.rom is before_object and bytes(parent.rom.save())==before_rom
    ROOT.mkdir(parents=True);save(ROOT/'independent_controls_validation.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),native_control_summary=result,
        exact_prior_native_models_andwhole_reference_reconstruction_inputs_reused_without_reexecution=True,
        prior_native_validation=str(NATIVE),prior_native_validation_sha256=sha(NATIVE.read_bytes()),prior_reference_validation=str(REFERENCES),prior_reference_validation_sha256=sha(REFERENCES.read_bytes()),
        negative_cases=cases,negative_count=12,every_negative_actual_input_changed_andsemantic_guard_rejected=True,
        all_frozen_andtrusted_adapter_guards_active_protected_files_ROMs_registry_ledger_andinputs_hash_exact=True,protected_hashes=before,
        original_NDS_object_identity_andwhole_bytes_unchanged_afterpositive_andallnegative_cases=True,
        no_original_query_flags_roles_roster_RNG_oractual_scene_predicates_forced=True,
        native_structural_arguments_seeded_resultwords_andcaller_fragments_not_new_gameplay=True,
        production_loaders_actual_comparison_readers_atomic_registered_patch_startup_andcredit_pending=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [DOC,NAMES,NATIVE,REFERENCES,MODULE,FLOW,Path(__file__)]}))
    print('Independent controls:3dispatches/20relative cases/1rawquery/8opaquepairs/50normalends/50callerfragments/4EV1getters pass;12semantic defects reject.No nativeglyph/capture replay,ROMcommit orcredit.',flush=True)
