"""Preserve syntax-failed8285; remove one surplus closing parenthesis."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_checkpoint_tools_v8285b');assert not root.exists()
    # The failed original cannot be parsed by checked_text; repair syntax first,
    # then compare the complete parsed native constants through the normal guard.
    source=Path('scripts/checkpoint_Hodram_display_v8285.py');raw=source.read_text(encoding='utf8')
    old='original_event_activation_not_observed=True,B137_later_fixture_captain0_not_normal_Hodram_continuity=True))'
    assert raw.count(old)==1
    repaired=raw.replace(old,old[:-1]);compile(repaired,str(source)+'::one-parenthesis-repair','exec')
    root.mkdir(parents=True);intermediate=root/'syntax_repaired_source.py';intermediate.write_text(repaired,encoding='utf8')
    result=derive(str(intermediate),'scripts/checkpoint_Hodram_display_v8285b.py',{
        'Hodram_display_checkpoint_v8285':'Hodram_display_checkpoint_v8285b',
        'editorial_handoff_verification_v8286':'editorial_handoff_verification_v8286b',
        'Hodram28_stored_names_actual_display_approved_pending_frozen_policy_atomic_registered_v8285':'Hodram28_stored_names_actual_display_approved_pending_frozen_policy_atomic_registered_v8285b',
        'unfinished_editorial_scope_v8285':'unfinished_editorial_scope_v8285b',
        'V8285':'V8285b','V8286':'V8286b',
    })
    save(root/'syntax_only_successor.json',dict(derivation=result,original_preserved=str(source),
        exact_single_surplus_parenthesis_removed_before_outputs=True,no_counter_ROM_orworkflow_semantics_changed=True))
