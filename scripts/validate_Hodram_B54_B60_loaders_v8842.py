"""Independently bind all original loader/cache/parent/census records and reject defects."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.hodram_B54_B60_profile_v1 import contract,validate_approved_batch,validate_runtime
from dk4tool.patch.hodram_B54_B60_loaders_v1 import check_loaders_and_census
from scripts.review_Hodram_B54_B60_actual_v8825 import PROOFS
from scripts.verify_village_wrap_v608 import read,save
PROOFS={**PROOFS,'current':'work/analysis/Hodram_B54_B60_current_v8799/current_effective.json'}
ROOT=Path('work/analysis/Hodram_B54_B60_loader_validation_v8842')
DOC=Path('translations/hodram_B54_B60_editorial_manuscript_v4.json')
REFS=Path('work/analysis/Hodram_B54_B60_reference_validation_v8836/independent_reference_validation.json')
MODULE=Path('dk4tool/patch/hodram_B54_B60_loaders_v1.py')
def require(value,label):
    if not value:raise ValueError('B54-B60 production loaders: '+label)
if __name__=='__main__':
    assert not ROOT.exists();doc=read(DOC);data={k:read(p) for k,p in PROOFS.items()};frozen=contract();validate_approved_batch(doc)
    refs=read(REFS);assert refs['manuscript_sha256']==sha(DOC.read_bytes()) and refs['positive_entire_archive_whole_reference_ROM_all318_unownedblocks_files_components_andallinverses']
    parent,reference=[NdsImage.open(p) for p in [doc['current_ROM'],doc['reference_ROM']]];validate_runtime(parent)
    rebuilt=dict(groups=[dict(g,target_block=Path(g['target_block']).read_bytes()) for g in data['relocation']['groups']])
    protected={Path(p) for p in frozen['dependencies']}|{DOC,REFS,MODULE,Path(__file__),Path('translations/release_stack.json'),Path('translations/editorial_review_current_v1.json'),Path('translations/rom_retention_pins.json'),Path(doc['current_ROM']),Path(doc['reference_ROM']),Path('work/clean.nds')}
    before={str(p):sha(p.read_bytes()) for p in protected};oldrom=parent.rom;oldbytes=bytes(parent.rom.save())
    result=check_loaders_and_census(data,parent,reference,rebuilt,read,require)
    assert [result[k] for k in ['native_whole_loads_cache_hits_bound','initial_parent_modes_bound','original_EV1_actions_bound']]==[325,650,326]
    cases=[]
    def reject(label,mutate):
        d,r=deepcopy(data),deepcopy(rebuilt);mutate(d,r);assert d!=data or r!=rebuilt,label
        try:check_loaders_and_census(d,parent,reference,r,read,require)
        except ValueError as error:
            text=str(error);assert 'Native dependency changed' not in text and 'Frozen Hodram-B54-B60 contract changed' not in text,(label,text)
            cases.append(dict(label=label,actual_changed_input=True,rejected=True,diagnostic=text))
        else:raise AssertionError('Changed loader evidence accepted:'+label)
    reject('incomplete-native-loads',lambda d,r:d['loaders'].__setitem__('fresh_native_whole_loads_andcache_hits',324))
    reject('wrong-load-proof-digest',lambda d,r:d['loaders'].__setitem__('load_sha256','0'*64))
    reject('wrong-parent-mode-proof-digest',lambda d,r:d['loaders'].__setitem__('parent_mode_sha256','0'*64))
    reject('wrong-shipped-code-census-unit',lambda d,r:d['references']['native_call_census']['units'][0].__setitem__('sha256','0'*64))
    reject('wrong-original-block-entry',lambda d,r:d['references']['original_selected_actions'][0].__setitem__('native_selected_block',60))
    reject('invented-event-prerequisite',lambda d,r:d['references']['source_event_records'][0].__setitem__('must_be_completed',[15]))
    reject('unqualified-natural-activation-scope',lambda d,r:d['loaders'].__setitem__('controlled_native_route_global_inputs_not_ordinary_event_activation',False))
    reject('changed-reconstructed-payload',lambda d,r:r['groups'][0].__setitem__('target_block',r['groups'][0]['target_block']+b'\0'))
    reject('wrong-exact-reused-parent-count',lambda d,r:d['loaders'].__setitem__('exact_reused_initial_parent_modes',635))
    reject('wrong-prior-parent-case-proof-digest',lambda d,r:d['loaders'].__setitem__('prior_mode_proof_sha256','0'*64))
    reject('incomplete-fresh-seven-block-set',lambda d,r:d['loaders'].__setitem__('fresh_parent_blocks',[54]))
    assert len(cases)==11 and {str(p):sha(p.read_bytes()) for p in protected}==before and parent.rom is oldrom and bytes(parent.rom.save())==oldbytes
    ROOT.mkdir(parents=True);save(ROOT/'independent_loader_validation.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),loader_summary=result,
        exact_previous_full_reference_reconstruction_inputs_reused_without_reexecution=True,reference_validation=str(REFS),reference_validation_sha256=sha(REFS.read_bytes()),
        negative_cases=cases,negative_count=11,every_negative_actual_input_changed_andsemantic_guard_rejected=True,
        all_frozen_guards_enabled_andprotected_files_ROMs_registry_ledger_exact=True,protected_hashes=before,
        no_native_load_capture_producer_orwhole_reference_replay_no_ROMcommit_orcredit=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [DOC,REFS,MODULE,Path(__file__)]}))
    print('Production loader/census reader:325loads/14fresh636exact-reused parentmodes/326actions/seven entries/fresh shippedcode scan pass;11semantic defects reject. No native-loader/capture replay,ROMcommit orcredit.',flush=True)
