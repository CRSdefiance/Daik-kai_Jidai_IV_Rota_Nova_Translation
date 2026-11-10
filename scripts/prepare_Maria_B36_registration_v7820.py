"""Freeze registered integration andthe unchanged required build/regression runners."""
import ast
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/maria_B36_registration_tools_v7820')
if __name__=='__main__':
    assert not ROOT.exists();source=Path('scripts/register_Maria_story_v7778.py').read_text('utf8')
    call=next(n for n in ast.walk(ast.parse(source)) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute)
        and isinstance(n.func.value,ast.Name) and n.func.value.id=='profile' and n.func.attr=='update')
    old={k.arg:ast.get_source_segment(source,k.value) for k in call.keywords}
    description="Complete V7779 plus16 clean-Japanese whole-exchange decisions for Maria's confrontation with Lil, SC3B36:9 revisions and7 individually justified retentions. Preserve differing beliefs about Kuhn, Southeast Asia's people, the underworld accusation, intended betrayal, fear, proof challenge, refusal and exasperation. Preserve original FO-before-FI order naturally; no invented rank, kinship, romance, attack, rescue, method, deadline, reconciliation or guaranteed mechanic."
    note="All16 native single pages,64 logical/compiled/stored alignment cases,11 zero-ink parity tails,9 individual row-count infos andno warnings/waivers. Three actors2/3/10,six getters,FI2/FO1 andscopedFI5/FA2/FO7;Lil/Maria/Xien progressive headers areobserved,fullcatalogueUI/full207/shared151-159 semantics remainopen. All22 commands/six numeric leaves,6000/633D/623D/632A/A000/fourbyte end,fullclean/predecessor block andarchive inverse;302 otherSC3 blocks/allotherfiles/components exact. Original303native loads606parentmodes andcaller census bound. Paired16001-frame initialized source/English fixtures playall16 speeches/29commands each:32complete panes,132complete body+header holds,zero partials/unknowns/unplayed. Allsource andEnglish black/ASCII-gray/CP932-gray/name masks,16upperRGBpairs andresults/UI agree. Preserveexits8213/8216,18command/sixduration rows,108/131lateRGBdifferences,allrawRNG/component/calendar/actor/after-scene measurements andno broad equivalence claim. Existingexactsystem-onlyunlock isdisclosed,earned=false;initializedHangzhou return8300 isnot naturaloptional location/activation/fullmechanics/routes/hardware.16positive/81policyrejections;oneatomicpositive/120actual-changingproductionrejections withdependencychecks bypassed andno negative commits. Allprior drafts,producer failures,proofs,traces,ROMs,profiles,fullobjective,graphicsseparation andlatertechnicalaudit preserved.MainV4701unchanged;no separatepackage,promotion,pruning,commit orpush."
    results=[]
    results.append(derive('scripts/register_Maria_story_v7778.py','scripts/register_Maria_B36_v7820.py',{
        old['description']:repr(description),old['note']:repr(note),
        'maria_story_editorial_v3':'maria_B36_editorial_v1',
        'Maria_story_final_paths_v7771':'Maria_B36_final_paths_v7816b',
        'maria_story_registration_v7778':'maria_B36_registration_v7820',
        "PROFILE='all-routes-unified-v7779'":"PROFILE='all-routes-unified-v7821'",
        'maria_story_atomic_challenges_v7776':'maria_B36_atomic_challenges_v7819',
        "result['positive_records']==67 and result['negative_count']==len(cases)==256":"result['positive_records']==16 and result['negative_count']==len(cases)==120",
        'editorial_handoff_verification_v7774':'editorial_handoff_verification_v7817d',
        "['batches'])==629":"['batches'])==630",
        "after.index(b\"profile_config.get('maria_B207_editorial')\")":"after.index(b\"profile_config.get('maria_story_editorial')\")",
        'maria_story':'maria_B36','all-routes-unified-v7717':'all-routes-unified-v7779','V7717':'V7779',
        'Maria67':'Maria B36','negative_count=256':'negative_count=120',
        'expected_manifest_batches=630':'expected_manifest_batches=631',
        'Registered experimentalV7779:630expectedbatches':'Registered experimentalV7821:631expectedbatches',
    }))
    results.append(derive('scripts/build_Maria_story_v7779.py','scripts/build_Maria_B36_v7821.py',{
        'maria_story_build_v7779':'maria_B36_build_v7821','all_routes_combined_v7779_candidate':'all_routes_combined_v7821_candidate',
        'maria_story_registration_v7778':'maria_B36_registration_v7820','all-routes-unified-v7779':'all-routes-unified-v7821',
    }))
    results.append(derive('scripts/run_Maria_story_regressions_v7779.py','scripts/run_Maria_B36_regressions_v7821.py',{
        'maria_story_regressions_v7779':'maria_B36_regressions_v7821',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'provenance.json',dict(derivations=results,
        only_new_sealed_B36_layer_after_complete_V7779=True,
        sole_registered_builder_andrequired110_regressions_unchanged=True,
        all_prior_profiles_accepted_layers_mainV4701_andartifacts_preserved=True,
        no_separate_test_package_promotion_pruning_commit_orpush=True,new_credit=0,full_goal_complete=False))
