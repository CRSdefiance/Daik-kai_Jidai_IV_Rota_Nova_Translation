"""Prepare exact own-V8172 Lil context for thefive surname consumers;ordinary inputs only."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Lil_Gerhard_context_tools_v8197')
if __name__=='__main__':
    assert not ROOT.exists()
    source=Path('scripts/capture_Hodram_current_v8186.py').read_text('utf8')
    identity=next(l for l in source.splitlines() if "identity=Path(" in l)
    inputs=next(l for l in source.splitlines() if "source=Path(" in l)
    cap=derive('scripts/capture_Hodram_current_v8186.py','scripts/capture_Lil_Gerhard_current_v8197.py',{
        identity:"    identity=Path('work/analysis/Hodram_B137_B45_B46_clean_names_v8182/six_clean_static_identity_fields_before_current_English.json');assert any(r['source_actor_ID']==2 for r in read(identity)['records']);scope=dict(route_identity='Lil',expected_original_captain_ID=2)",
        inputs:"    source=Path('work/analysis/lil_B111_B119_runs_v3253/newgame_inputs.json')",
        'choices=[1]':'choices=[2]','Hodram_B137_B45_B46_context_runs_v8186':'Lil_Gerhard_context_runs_v8197',
        'Hodram_B137_B45_B46_route{route}_v8186_V8172':'Lil_Gerhard_route{route}_v8197_V8172',
        'Capture own-current Hodram New Game through original ordinary inputs;not B137/B45/B46 activation.':'Capture own-current Lil New Game through original ordinary inputs;not optional Stockholm/Hamburg activation.',
        'ordinary_route_selection_not_optional_B137_B45_B46_activation':'ordinary_route_selection_not_optional_Gerhard_Stockholm_Hamburg_activation',
    })
    context=derive('scripts/papal_trade_route_native_context_v7626.py','scripts/Lil_current_route_context_v8198.py',{
        "self.doc['expected_original_captain_ID'] in [0,1]":"self.doc['expected_original_captain_ID'] in [2]",
    })
    bind=derive('scripts/bind_Hodram_current_v8187.py','scripts/bind_Lil_Gerhard_current_v8198.py',{
        'scripts.papal_trade_route_native_context_v7626':'scripts.Lil_current_route_context_v8198',
        'Hodram_current_binding_v8187':'Lil_Gerhard_current_binding_v8198',
        'Hodram_B137_B45_B46_context_runs_v8186/route1':'Lil_Gerhard_context_runs_v8197/route2',
        'current_V8172_Hodram_native_v8187':'current_V8172_Lil_native_v8198',
        "plan['expected_original_captain_ID']==1":"plan['expected_original_captain_ID']==2","get(0x7F244)==1":"get(0x7F244)==2",
        'route=1,actual_original_captain_ID=1':'route=2,actual_original_captain_ID=2',
        'expected_original_captain_ID=1':'expected_original_captain_ID=2','actual_original_captain_ID=1':'actual_original_captain_ID=2',
        'captain1':'captain2','Hodram':'Lil','ordinary_NewGame_only_not_optional_B137_B45_B46_activation':'ordinary_NewGame_only_not_optional_Gerhard_Stockholm_Hamburg_activation',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivations.json',dict(derivations=[cap,context,bind],
        existing_ordinary_Lil_schedule_used_unchanged=True,expected_actor2_requires_actual_snapshot_confirmation=True,
        context_class_only_expected_captain_scope_changes_all_runtime_pool_code_memory_guards_preserved=True,
        no_ROM_RAM_role_roster_funds_flags_RNG_orresults_forced=True,new_credit=0,full_goal_complete=False))
    print('Prepared ownV8172 Lil capture/strictcaptain2 nativecontext forGerhard nameconsistency;no optional event activated.')
