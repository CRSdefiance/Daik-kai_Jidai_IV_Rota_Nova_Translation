"""Prepare four full source/revised block fixtures with original opening initialization."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B31_B53_fixture_tools_v8739');assert not root.exists()
    receipt=derive('scripts/create_Hodram_B52_fixtures_v8648.py','scripts/create_Hodram_B31_B53_fixtures_v8739.py',{
        'Hodram_B52_fixtures_v8648':'Hodram_B31_B53_fixtures_v8739','Hodram_B52_reference_v8645':'Hodram_B31_B53_reference_v8736',
        'Hodram_B52_relocation_v8642':'Hodram_B31_B53_relocation_v8728','Hodram_B52_references_v8647':'Hodram_B31_B53_references_v8738',
        'all14_commands3_full_preambles4_relatives_zeroqueries_twochoices4_opaque_controls_andboth_terminals_bound':'all18_commands3_fullpreambles4relatives1query8opaquecontrols_andtwo_normal_terminals_bound',
        'Hodram_B52_current_v8631':'Hodram_B31_B53_current_v8722',
        "group=dict(group,all_source_commands=current['groups'][0]['all_source_commands'])":"group=dict(group,all_source_commands=next(g for g in current['groups'] if g['block']==group['block'])['all_source_commands'])",
        "sum(c['word']==0 for c in parsed)==2":"sum(c['word']==0 for c in parsed)==1",
        '_v8648_RESEARCH_ONLY':'_v8739_RESEARCH_ONLY',
        'assert len(planned)==2 and sum(len(f[\'all_original_exchange_commands\']) for f in fixtures)==28':'assert len(planned)==4 and sum(len(f[\'all_original_exchange_commands\']) for f in fixtures)==36',
        'B52 with original eight':'B31/B53 with original eight','updated[:-2]':'updated[:-4]',
        'two_whole_scripts.json':'four_whole_scripts.json',
        'all14_commands3_speeches4_relative_sites_two_typed_labels_both_distinct_endwords_preserved_perversion':'each_complete9command_block_source_speeches_allrelatives_queries_opaquecontrols_andnormalend_preserved',
        'registered_current_V8609_mainV4701_unchanged':'registered_current_V8704_mainV4701_unchanged',
        'new_ROMs=2':'new_ROMs=4',
        'Pinned two complete B52 fixtures:original8initializers34bytes;all14commands3speeches4relatives2typedlabels2distinctends perversion.No runtime forcing,credit orregistered release.':'Pinned four complete B31/B53 fixtures:original8initializers34bytes;all9commands perfixture,wholequery/branch/effect/end content.No runtime forcing,credit orregistered release.',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=receipt,all_native_high_integer_constants_andmultiplicity_preserved=True,
        original8_initializer_commands34bytes_andwhole_selected_blocks_preserved=True,
        four_complete_scripts_not_force_selected_B31_branch_ororiginal_event_activation=True,
        prior_pins_andall_ROMs_preserved=True,no_registry_promotion_orcredit=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False))
