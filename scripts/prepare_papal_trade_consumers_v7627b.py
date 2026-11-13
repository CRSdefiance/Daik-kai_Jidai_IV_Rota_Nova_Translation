"""Preserve the captain2-only voice failure and bind a separate strict actual-route adapter."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/papal_trade_consumers_tools_v7627b')
if __name__=='__main__':
    assert not ROOT.exists()
    old="native=ctx.execute(env['names']);ctx.machines.pop();static=ctx.execute(selectors,[19,104]);ctx.machines.pop()"
    new="""voice_adapter=checked_text(inspect.getsource(selectors),{'assert captain==2':'assert EXPECTED_CAPTAIN in [0,1] and captain==EXPECTED_CAPTAIN'})
        voice_env={**selectors.__globals__,'EXPECTED_CAPTAIN':route};exec(compile(voice_adapter,__file__+'::actual-route-voice','exec'),voice_env)
        native=ctx.execute(env['names']);ctx.machines.pop();static=ctx.execute(voice_env['selectors'],[19,104]);ctx.machines.pop()"""
    changes={'from copy import deepcopy':'import inspect\nfrom copy import deepcopy','papal_trade_consumers_v7627':'papal_trade_consumers_v7627b',old:new,'source_owned_name_adapter=name_adapter,':'source_owned_name_adapter=name_adapter,source_owned_voice_adapter=voice_adapter,','new_emulator_runs=0,new_source_prose_reviews=0':'failed_7627_captain2_voice_guard_before_any_speech_checks_preserved=True,diagnostic_import_without_deps_path_preserved_not_rejection_credit=True,new_emulator_runs=0,new_source_prose_reviews=0'}
    tool=derive('scripts/prove_papal_trade_consumers_v7627.py','scripts/prove_papal_trade_consumers_v7627b.py',changes);ROOT.mkdir(parents=True)
    save(ROOT/'source_locked_actual_route_voice_binding.json',dict(tool=tool,original_Lil_voice_helper_andcaptain2_context_unchanged=True,new_voice_adapter_strict_actual_expected_captain0_or1_andall_native_instructions_preserved=True,prior_failed_attempt_printed_names_but_created_no_approved_speech_orgetter_proof=True,failed_attempt_not_an_unsafe_input_rejection_ornew_credit=True,all_high_native_constants_andmultiplicity_preserved=True,new_credit=0,full_goal_complete=False))
