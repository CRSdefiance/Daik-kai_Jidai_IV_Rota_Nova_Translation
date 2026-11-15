"""Rebind the user's paired-speaker label concern to the exact current native consumers."""
import inspect,struct
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.patch.generic_speaker_label_data_v1 import BASE,POOL,TABLE,cstring
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Al_Ferid_exact_native_context_v6520 import CurrentContext
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.prove_lil_B167_names_v4124b import names
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/paired_role_current_consumers_v6598');INPUT=Path('work/analysis/current_V6584_native_v6593/current_native_input.json');QUEUE=Path('work/analysis/names_scope_v5708/speaker_names_and_role_labels_review_scope.json')
if __name__=='__main__':
    assert not ROOT.exists();source=inspect.getsource(names);adapter=checked_text(source,{'for ident in [2,4,13,23,109]:':'for ident in [164,165]:','all_ten_original_consumers_and_owned_or_readonly_memory_paths_exact':'all_four_original_consumers_and_owned_or_readonly_memory_paths_exact'});env=dict(names.__globals__);exec(compile(adapter,__file__+'::paired-role-labels','exec'),env);ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');proof=ctx.execute(env['names']);ctx.machines.pop();assert not ctx.machines and len(proof['rows'])==4
    payload=bytes(MainCodeFile(ctx.arm,BASE).sections[3].data[:-48]);fields=[]
    for ident in [164,165]:
        for delta in [0,4,8]:
            at=TABLE+ident*32+delta;ptr=struct.unpack_from('<I',ctx.arm,at)[0]
            value=cstring(payload,ptr-POOL) if POOL<=ptr<POOL+len(payload) else cstring(ctx.arm,ptr-BASE) if ptr else b''
            fields.append(dict(actor_ID=ident,column=delta,pointer_field=at,current_pointer=ptr,current_terminated_hex=value.hex(),current_field_English=value[:-1].decode('cp932') if ptr else None))
    save(ROOT/'four_current_pair_role_getters_exact_fields_and_historical_queue.json',dict(candidate=str(ctx.rompath),candidate_sha256=read(INPUT)['current_ROM_sha256'],historical_queue=str(QUEUE),historical_queue_sha256=sha(QUEUE.read_bytes()),historical_findings=read(QUEUE)['source_bound_initial_findings'],four_current_getters=proof,current_raw_fields=fields,source_owned_adapter=adapter,current_native_context_plan=str(ctx.proof_path),current_native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),complete_shared_exchange_source_current_and_actual_nameplate_review_still_pending=True,no_new_label_approval_ROM_ledger_or_completion_credit=True,new_emulator_runs=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print([(r['actor_ID'],r['consumer'],r['text']) for r in proof['rows']])
