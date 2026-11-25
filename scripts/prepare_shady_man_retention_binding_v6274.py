"""Prepare preservation and own-current-ROM native snapshot binding successors."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/shady_man_retention_binding_tools_v6274')
if __name__=='__main__':
    assert not ROOT.exists();tools=[]
    tools.append(derive('scripts/pin_generic_speaker_labels_v5896.py','scripts/pin_shady_man_label_v6274.py',{'generic_speaker_labels_retention_v5896':'shady_man_label_retention_v6274','generic_speaker_labels_release_v5895':'shady_man_label_release_v6271','three-label':'one-label','V5891':'V6270'}))
    tools.append(derive('scripts/bind_current_V6220_native_v6228.py','scripts/bind_current_V6270_native_v6278.py',{
      'current_build_native_context_v6097':'current_build_native_context_v6261','V6220':'V6270','current_V6220_native_v6228':'current_V6270_native_v6278',
      "v=read('work/analysis/editorial_handoff_verification_v6226/verified_handoff.json')":"v=read('work/analysis/editorial_handoff_verification_v6276/verified_handoff.json')",
      'lil_B205_release_v6221':'shady_man_label_release_v6271','lil_B205_runs_v6222':'shady_man_runs_v6272',
      'not_B206_or_any_later_event_activation':'not_natural_B206_or_any_later_event_activation',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'pin_and_exact_current_snapshot_binding_tools.json',dict(tools=tools,all_native_high_integer_constants_preserved=True,full_goal_complete=False));print('V6270 preservation and own actual snapshot binding tools prepared.')
