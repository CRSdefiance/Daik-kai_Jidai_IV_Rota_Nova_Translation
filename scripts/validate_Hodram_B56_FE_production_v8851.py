"""Validate all original live FE memory/RGB evidence and reject actual changed fields."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_B54_B60_FE_actual_v1 import check_FE_live
from scripts.Hodram_B54_B60_verified_inputs_v8846 import verified_inputs,DOC
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B56_FE_production_validation_v8851')
MODULE=Path('dk4tool/patch/hodram_B54_B60_FE_actual_v1.py')
def require(value,label):
    if not value:raise ValueError('B56 original live FE: '+label)
if __name__=='__main__':
    assert not ROOT.exists();doc,data,frozen,parent,clean,reference,rebuilt,native,protected=verified_inputs()
    protected|={MODULE,Path(__file__)};before={str(p):sha(p.read_bytes()) for p in protected};oldrom=parent.rom;oldbytes=bytes(parent.rom.save())
    result=check_FE_live(data,parent,read,require);assert result['original_paint_contexts']==2 and result['complete_same_run_FE_holds']==6
    cases=[]
    def reject(label,mutate):
        changed=deepcopy(data);mutate(changed);assert changed!=data,label
        try:check_FE_live(changed,parent,read,require)
        except ValueError as error:
            message=str(error);assert 'Native dependency changed' not in message and 'Frozen Hodram-B54-B60 contract changed' not in message
            cases.append(dict(label=label,actual_changed_input=True,rejected=True,diagnostic=message))
        else:raise AssertionError('Changed FE actual evidence accepted:'+label)
        assert parent.rom is oldrom and bytes(parent.rom.save())==oldbytes
    reject('wrong-typed-font-metrics',lambda d:d['B56_FE']['groups'][0].__setitem__('captured_original_font_metrics','00'*24))
    reject('wrong-palette',lambda d:d['B56_FE']['groups'][0].__setitem__('palette_hex','00'*32))
    reject('missing-complete-FE-hold',lambda d:d['B56_FE']['groups'][1]['complete_actual_holds'].pop())
    reject('wrong-complete-bitmap-view',lambda d:d['B56_FE']['groups'][0].__setitem__('captured_original_bitmap_view','00'*100))
    reject('invented-geometry-inference',lambda d:d['B56_FE']['groups'][0].__setitem__('original_native_source_consumer_not_geometry_inferred_from_incidental_r1',False))
    reject('unbound-physical-plane',lambda d:next(r for r in d['models']['native_models']['revised_English'] if r['source_selector']==254)['pages'][0].__setitem__('physical_plane_sha256','0'*64))
    reject('invented-new-FE-frame-credit',lambda d:d['B56_FE'].__setitem__('actual_frames',28004))
    reject('lost-readonly-scope',lambda d:d['B56_FE'].__setitem__('read_only_callbacks_host_slots_andcore_restored',False))
    assert len(cases)==8 and {str(p):sha(p.read_bytes()) for p in protected}==before
    ROOT.mkdir(parents=True);save(ROOT/'independent_FE_actual_validation.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),FE_actual_summary=result,negative_cases=cases,negative_count=len(cases),all_negatives_changed_semantic_inputs_with_frozen_guards_enabled=True,all_protected_files_ROMs_registry_ledger_exact_original_NDS_object_identity_andwhole_bytes_unchanged=True,protected_hashes=before,no_new_capture_orproducer_replay_orframe_credit=True,new_emulator_runs=0,new_credit=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [DOC,MODULE,Path(__file__),Path('scripts/Hodram_B54_B60_verified_inputs_v8846.py')]}))
    print('Original live FE:2paint contexts/6held bitmaps/palettes/VRAM/physicalRGB pass;8semantic defects reject.No capture replay orcredit.',flush=True)
