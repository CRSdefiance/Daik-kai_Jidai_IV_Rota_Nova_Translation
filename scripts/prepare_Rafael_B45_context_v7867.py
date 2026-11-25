"""Capture only the needed own-current Rafael route with unchanged ordinary startup inputs."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Rafael_B45_context_tools_v7867');assert not root.exists()
    result=derive('scripts/capture_papal_trade_route_contexts_v7625.py','scripts/capture_Rafael_B45_context_v7867.py',{
        'Capture own-current Rafael/Hodram New Games through ordinary route-selection inputs.':
        'Capture own-current Rafael New Game through original ordinary inputs;not B45 activation.',
        'work/analysis/papal_trade_route_runs_v7625':'work/analysis/Rafael_B45_context_runs_v7867',
        'choices=[0,1]':'choices=[0]',
        'editorial_handoff_verification_v7623':'editorial_handoff_verification_v7866',
        'all-routes-unified-v7611':'all-routes-unified-v7857',
        'papal_trade_route{route}_v7625_V7611':'Rafael_B45_route{route}_v7867_V7857',
        'ordinary_route_selection_not_optional_papal_trade_activation':'ordinary_route_selection_not_optional_B45_activation',
    })
    root.mkdir(parents=True);save(root/'provenance.json',dict(derivation=result,
        only_Rafael_ordinary_NewGame_no_battery_observer_ROM_RAM_savestate_orforcing=True,
        old_route_identity_evidence_is_reference_current_captain_binding_pending=True,
        original_native_high_constants_andall_capture_guards_preserved=True,new_credit=0,full_goal_complete=False))
