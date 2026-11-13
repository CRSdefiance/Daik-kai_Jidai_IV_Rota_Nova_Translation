"""Combine disjoint proven command and FE observers for one paired B50 run."""
import ast,textwrap
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive,checked_text,native_numbers
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B50_run_tools_v8505');assert not root.exists()
    fe=Path('scripts/capture_Hodram_B49_FE_v8419.py');tail=Path('scripts/run_Hodram_B49_tail_v8416.py')
    fes=fe.read_text(encoding='utf-8');tails=tail.read_text(encoding='utf-8')
    contract=fes[fes.index("    contract=read('work/analysis/script_sources_v733/source_contract.json')"):fes.index('    root.mkdir(parents=True);contractpath=')]
    contract=checked_text('if True:\n'+contract,{}) .split('\n',1)[1]
    snapshot=tails[tails.index('    def snapshot(o,frame):'):tails.index('    class Proxy:')]
    snapshot=checked_text('if True:\n'+snapshot,{'menu_frame':'FE_hold_frame'}).split('\n',1)[1]
    helper=Path('scripts/Hodram_B50_readonly_FE_v8505.py');assert not helper.exists()
    imports='''"""Read-only FE factory and held-state exporter from immutable B49 producers."""
import ctypes as ct,inspect,struct,textwrap
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts import observe_lil_modal_v1733 as original
from scripts.inspect_committed_gpu_v646 import CORE,CORE_SHA
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save

def create(corelib,folder,cap,arm,body):
'''
    factory=imports+contract+'''    contractpath=folder/'modal_source_contract.json';save(contractpath,contract)
    observer=Observer(corelib,cap/'modal_observer',contractpath);observer.install()
    return observer,contractpath,adapter

def export_held(o,frame,folder,snapshots):
'''+textwrap.indent(textwrap.dedent(snapshot),'    ')+'''    snapshot(o,frame)
'''
    compile(factory,str(helper),'exec')
    assert native_numbers(factory)==native_numbers('if True:\n'+contract)+native_numbers('if True:\n'+snapshot)
    helper.write_text(factory,encoding='utf-8')
    runner=derive('scripts/run_Hodram_B49_v8407.py','scripts/run_Hodram_B50_v8505.py',{
        'from scripts import observe_lil_B180_v4810 as original':'from scripts import observe_lil_B180_v4810 as original\nfrom scripts import Hodram_B50_readonly_FE_v8505 as modal',
        'Hodram_B49_scene_runs_v8407':'Hodram_B50_scene_runs_v8505',
        'Hodram_B49_fixtures_v8406':'Hodram_B50_fixtures_v8504',
        'choices=[49]':'choices=[50]',
        'frames={49:10001}[block]':'frames={50:10001}[block]',
        '_v8407':'_v8505',
        '    observers=[]':'    observers=[];modals=[];snapshots=[];modal_metadata=[]\n    held_frames=list(range(4030,4811,60))\n    model=read("work/analysis/Hodram_B50_models_v8506/native_models.json")\n    FE_body=next(m for m in model["native_models"][version] if m["source_selector"]==254)["expanded_native_hex"]',
        "o=Observer(core,cap/'observer');o.install();observers.append(o);old=core.retro_run;old.restype=None":"o=Observer(core,cap/'observer');o.install();observers.append(o)\n                m,mc,adapter=modal.create(core,folder,cap,arm,FE_body);modals.append(m)\n                assert {v['slot'] for v in o.slots}.isdisjoint({v['slot'] for v in m.slots})\n                modal_metadata.append(dict(contract=str(mc),contract_sha256=sha(mc.read_bytes()),adapter=adapter,exact_FE_body_hex=FE_body,command_andFE_host_slots_disjoint=True))\n                old=core.retro_run;old.restype=None",
        '                def run():o.next_frame();old()':'                def run():\n                    o.next_frame();m.next_frame();old()\n                    assert o.header[0]==m.header[0]\n                    if m.header[0] in held_frames:modal.export_held(m,int(m.header[0]),folder,snapshots)',
        'captures=sorted(set(range(2350,frames,60))|{frames-1})':'captures=sorted(set(range(2350,frames,60))|{frames-1,*held_frames})',
        "'--dump-ram']":"'--capture-native-state-at',*map(str,held_frames),'--dump-ram']",
        '        for o in observers:o.close()':'        for m in reversed(modals):m.close()\n        for o in reversed(observers):o.close()',
        '    for o in observers:o.save()':'    for m in modals:m.save()\n    for o in observers:o.save()\n    save(folder/"combined_readonly_FE_evidence.json",dict(modal_observers=modal_metadata,held_snapshots=snapshots,held_frames=held_frames,helper_source=str(Path(modal.__file__)),helper_sha256=sha(Path(modal.__file__).read_bytes()),both_observers_disjoint_readonly=True,new_credit=0,full_goal_complete=False))',
        "    op=cap/'observer/commands.json';assert read(op)['all_host_slots_restored_and_core_file_exact']":"    op=cap/'observer/commands.json';assert read(op)['all_host_slots_restored_and_core_file_exact']\n    mp=cap/'modal_observer/actual_modal_contexts.json';md=read(mp)\n    assert len(modals)==1 and modals[0].snapshot_count==1 and not modals[0].errors\n    assert md['all_host_slots_restored_and_core_file_exact'] and not md['errors'] and not md['mismatches']\n    assert len(snapshots)==len(held_frames)",
        'observer_sha256=sha(op.read_bytes()),run_plan=':'observer_sha256=sha(op.read_bytes()),modal_observer=str(mp),modal_observer_sha256=sha(mp.read_bytes()),combined_FE_evidence=str(folder/"combined_readonly_FE_evidence.json"),combined_FE_evidence_sha256=sha((folder/"combined_readonly_FE_evidence.json").read_bytes()),run_plan=',
    })
    root.mkdir(parents=True);save(root/'derivations.json',dict(runner=runner,FE_factory_source=str(fe),FE_factory_source_sha256=sha(fe.read_bytes()),held_export_source=str(tail),held_export_source_sha256=sha(tail.read_bytes()),helper=str(helper),helper_sha256=sha(helper.read_bytes()),FE_contract_andadapter_stage=contract,held_export_stage=snapshot,all_native_high_integer_constants_andmultiplicity_preserved_in_source_stages=True,identical_ordinary_inputs_andfull_original_commands=True,new_credit=0,full_goal_complete=False))
