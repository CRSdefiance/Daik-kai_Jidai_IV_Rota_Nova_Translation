"""Preserve five prepared tools and finish the branch-only dependency adapter."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive,native_numbers
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B190_source_tools_v5314')
if __name__=='__main__':
    assert not ROOT.exists()
    pairs=[('map_lil_B186_source_v5132.py','map_lil_B190_source_v5314.py'),('reconcile_lil_B188_voices_v5233.py','reconcile_lil_B190_voices_v5315.py'),
        ('prove_lil_B186_dispatches_v5135.py','prove_lil_B190_dispatches_v5316.py'),('prove_lil_B186_entry_v5136.py','prove_lil_B190_entry_v5317.py'),
        ('prove_lil_B188_names_v5237.py','prove_lil_B190_names_v5319.py')]
    preserved=[]
    for a,b in pairs:
        source,target=[Path('scripts')/n for n in [a,b]];text=target.read_text(encoding='utf-8');compile(text,str(target),'exec')
        assert native_numbers(source.read_text(encoding='utf-8'))==native_numbers(text)
        preserved.append(dict(source=str(source),successor=str(target),successor_sha256=sha(target.read_bytes()),native_high_constants_exact=True))
    branch=derive('scripts/prove_lil_B186_branches_v5134.py','scripts/prove_lil_B190_branches_v5318.py',{
        'B186':'B190','source_v5132/all12':'source_v5314/all17','branches_v5134':'branches_v5318'})
    ROOT.mkdir(parents=True);save(ROOT/'prepared_current_source_native_contracts.json',dict(preserved_first_five_derivations=preserved,branch_derivation=branch,
        previous_preparation_stopped_on_unused_voice_key_in_branch_only_tool=True,stopped_producer='scripts/prepare_lil_B190_source_v5314.py',
        no_existing_producer_or_output_overwritten=True,previous_goal_turn_classification='progress',previous_goal_turn_evidence='work/analysis/editorial_handoff_verification_v5310/verified_handoff.json',
        current_candidate='out/all_routes_combined_v5304_candidate.nds',clean_only_glosses=17,source_commands=29,source_controls=6,source_stored_logical=[608,606],source_tailzeros=2,
        exact_hex77_9F_equal_decimal119_159_guarded=True,conditional500_predicate_six_relative_sites_three_alternatives_require_distinct_checks=True,
        no_predecessor_English_ROM_registry_or_credit_change=True,full_goal_complete=False))
