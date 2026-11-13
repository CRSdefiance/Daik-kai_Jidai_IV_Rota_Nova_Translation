"""Keep later fixture re-entry explicit without rejecting a prior complete exchange."""
from scripts.source_locked_derivation_v5118 import derive
if __name__=='__main__':
    print(derive('scripts/audit_Rafael_B48_actual_v8051.py','scripts/audit_Rafael_B48_actual_v8051b.py',{
        'Rafael_B48_actual_v8051':'Rafael_B48_actual_v8051b',
        "assert finished and not unknown and not trace['unreturned_at_capture_end']":"assert finished and not unknown\n        assert all(trace['rows'][u['entry_row']]['frame']>pairs[-1]['returned'] for u in trace['unreturned_at_capture_end'])",
        "unreturned_following_dialogues=trace['unreturned_at_capture_end'],review_sheets=sheets,":"unreturned_following_dialogues=trace['unreturned_at_capture_end'],\n            later_fixture_reentry_frames=[p['frame'] for p in following if p['route']==0 and p['block']==44 and p['offset']==8],\n            complete_first_exchange_distinguished_from_later_fixture_reentry=True,review_sheets=sheets,",
    }))
