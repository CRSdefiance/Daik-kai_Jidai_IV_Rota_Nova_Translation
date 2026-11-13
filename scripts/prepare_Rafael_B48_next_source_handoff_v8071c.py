"""Preserve independent B49 source-only progress in the reversible B48 handoff."""
import ast
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
PACKET='work/analysis/Rafael_next_clean_v8073/complete_clean_SC0_B49_EV0_andcoverage_before_current_English.json'
NAMES='work/analysis/Rafael_B49_clean_names_v8074/seven_clean_static_identity_fields_before_current_English.json'
GLOSS='work/analysis/Rafael_B49_clean_gloss_v8075/61_first_clean_glosses_seven_source_identities_before_current_English.json'
PENDING='Rafael_SC0B49_source_gloss_pending_controls_current_andrelease_v8071'
if __name__=='__main__':
    source=Path('scripts/complete_Rafael_B48_v8071b.py').read_text(encoding='utf8');tree=ast.parse(source)
    n=next(n for n in tree.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='NEXT')
    old=ast.literal_eval(n.value)
    note="B49 source-only progress is already saved: 61 complete first clean glosses and seven original identities for Lil and Camille's North Sea confrontation. Current English bodies and name fields remain unread. Event49 requires39 and excludes151; review full event39 context and prove native entry, the apparent 0xC281 control, predicates/queries, branch alternatives R238/R244, callers and names before comparison or a localized manuscript. Do not infer chronology from block order or turn the proposed 協定 into a formal alliance without mechanic/context evidence. Source packet: "+PACKET+". Clean identities: "+NAMES+". Fresh glosses: "+GLOSS+". These source-only artifacts bind the verified V8045 ledger while B48 tests ran; the clean ROM remains exact. B49 has no completion or source/prose credit. Continue from these files without redoing first-source work."
    pending="dict(source_packet="+repr(PACKET)+",clean_names="+repr(NAMES)+",fresh_gloss="+repr(GLOSS)+",physical_source_objects=61,clean_static_identities=7,current_English_bodies_andnames_unread=True,source_gloss_only_no_localized_manuscript=True,native_controls_event39_context_paths_names_current_comparison_andrelease_pending=True,completion_credit_added=0,source_prose_credit_added=0,full_goal_complete=False)"
    changes={
        ast.get_source_segment(source,n):'NEXT='+repr(note+'\n\n'+old),
        "Path('work/analysis/Rafael_B48_atomic_positive_v8063/positive_receipt.json'),Path(__file__)":"Path('work/analysis/Rafael_B48_atomic_positive_v8063/positive_receipt.json'),Path("+repr(PACKET)+"),Path("+repr(NAMES)+"),Path("+repr(GLOSS)+"),Path(__file__)",
        "    prior_scope=old[prior['unfinished_scope']]":"    put(["+repr(PENDING)+"],"+pending+")\n    prior_scope=old[prior['unfinished_scope']]",
        "    inventory=deepcopy(read(prior_scope['path']));inventory['next_focus']=NEXT":"    inventory=deepcopy(read(prior_scope['path']));inventory['next_focus']=NEXT\n    inventory["+repr(PENDING)+"]="+pending,
        "strict_own_Rafael_current_input=read(START)['current_native_input'],next_required=NEXT,unfinished_scope=SCOPE,":"strict_own_Rafael_current_input=read(START)['current_native_input'],next_required=NEXT,unfinished_scope=SCOPE,pending_source_batch="+repr(PENDING)+",",
    }
    print(derive('scripts/complete_Rafael_B48_v8071b.py','scripts/complete_Rafael_B48_v8071c.py',changes))
