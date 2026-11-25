"""Freeze a source-owned all-route direct151–159 consumer census."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/retainer_census_tools_v7740');assert not root.exists()
    proof=derive('scripts/census_couple_speaker_uses_v5773b.py','scripts/census_retainer_speaker_uses_v7740.py',{
        'work/analysis/couple_label_clean_context_v5766/four_complete_clean_route_exchanges_and_exact_couple_name_fields.json':
        'work/analysis/maria_story_names_macros_v7727/eight_static_speakers_sixteen_getters_clean_fields_actual_source_macros.json',
        'couple_speaker_uses_v5773b':'retainer_speaker_uses_v7740',
        '[164,165]':'[151,152,153,154,155,156,157,158,159]',
        'couple':'retainer',
        'initial_tea_context':'initial_Maria_informant_context',
    })
    root.mkdir(parents=True);save(root/'provenance.json',dict(derivation=proof,clean_only_complete_native_exchanges=True,current_English_dialogue_unread=True,new_credit=0,full_goal_complete=False))
    print('Frozen clean all-route direct151–159 census;no generic role replacement orcredit.')
