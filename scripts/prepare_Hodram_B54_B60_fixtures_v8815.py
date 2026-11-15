"""Six representative complete exchanges,paired languages,without forcing conditional paths."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B54_B60_fixture_tools_v8815');assert not root.exists()
    result=derive('scripts/create_Hodram_B31_B53_fixtures_v8739.py','scripts/create_Hodram_B54_B60_fixtures_v8815.py',{
        'Hodram_B31_B53_fixtures_v8739':'Hodram_B54_B60_fixtures_v8815',
        'Hodram_B31_B53_reference_v8736':'Hodram_B54_B60_reference_v8812',
        'Hodram_B31_B53_relocation_v8728':'Hodram_B54_B60_relocation_v8809',
        'Hodram_B31_B53_references_v8738':'Hodram_B54_B60_references_v8814',
        'all18_commands3_fullpreambles4relatives1query8opaquecontrols_andtwo_normal_terminals_bound':'all152commands82fullpreambles24relatives6queries33nonprose_controls7normalends_bound',
        'Hodram_B31_B53_current_v8722':'Hodram_B54_B60_current_v8799',
        "for group in mapping['groups']:\n        group=dict(group,":"for group in mapping['groups']:\n        if group['block']==55:continue\n        group=dict(group,",
        '_v8739_RESEARCH_ONLY':'_v8815_RESEARCH_ONLY',
        "assert len(planned)==4 and sum(len(f['all_original_exchange_commands']) for f in fixtures)==36":"assert len(planned)==12 and sum(len(f['all_original_exchange_commands']) for f in fixtures)==298",
        'B31/B53 with original eight':'B54/B56/B57/B58/B59/B60 with original eight',
        'updated[:-4]':'updated[:-12]',
        'four_whole_scripts.json':'twelve_whole_scripts.json',
        'each_complete9command_block_source_speeches_allrelatives_queries_opaquecontrols_andnormalend_preserved':'each_complete_selected_exchange_source_speeches_allrelatives_queries_opaquecontrols_andnormalend_preserved',
        'registered_current_V8704_mainV4701_unchanged':'registered_current_V8778_mainV4701_unchanged',
        'new_ROMs=4':'new_ROMs=12',
        'Pinned four complete B31/B53 fixtures:original8initializers34bytes;all9commands perfixture,wholequery/branch/effect/end content.No runtime forcing,credit orregistered release.':'Pinned12 representative source/English fixtures:6complete blocks/298exchange commands;original8initializers34bytes;B55offline-only fornow.No forced path,roster,progress,credit orrelease.',
    })
    root.mkdir(parents=True);save(root/'source_locked_fixture_derivation.json',dict(derivation=result,
        representative_blocks=[54,56,57,58,59,60],offline_only_block=55,
        rationale='B54 tests the newcomer worker and complete exchange;B56 distinct FE null-actor andprogressive transition;B57 respectful learner speech andname macros;B58 actual unforced branching/public accusations/quest;B59 map/item show-hide andtwo-page speeches;B60 longer personal account andmultipage behavior. B55 sole guild message shares already-proved progressive/name macro behavior andremains offline,notactualcoverage.',
        all_original_commands_preserved_in_each_selected_scene=True,no_query_roster_eventflag_RNG_orresult_forcing=True,
        all_prior_artifacts_andROMs_preserved=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False))
