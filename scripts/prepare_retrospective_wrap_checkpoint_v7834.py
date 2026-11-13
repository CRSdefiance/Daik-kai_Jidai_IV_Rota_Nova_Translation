"""Source-lock a zero-credit checkpoint for the first concrete retrospective wrap refinement."""
import ast
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
SOURCE=Path('scripts/checkpoint_name_consumer_v7829.py')
TARGET=Path('scripts/checkpoint_retrospective_wrap_v7834.py')
ROOT=Path('work/analysis/retrospective_wrap_checkpoint_tools_v7834')
FINDING="""The retrospective contraction/question-tag scan examined the 558 available recorded formatted_markup plans among6938 completed records. It found13 leads in11 native groups across all four storylines. Every lead binds exactly to one original source speech and one live V7821 speech with its complete preamble; all13 current raw bodies have no catalogue override. This is offline inventory and catalogue evidence, not new actual scene coverage. The other6380 records were not covered by this markup-only heuristic.

Lil B218 was reread as a complete13-speech clean/current exchange. All13 wordings are retained with individual reasons: practical Lil presses for a weapon's location while Ian explains his fascination with uncertain ancient legend. For R27, the automatic planner now proposes (Ian's interested? / That's a surprise.) instead of splitting That's / a surprise. No words, punctuation, macros, source controls, physical width or font change. Only this exact paragraph gains the ordinary that's/a boundary preference;12 compiled plans remain exact. All13 unmodified base-QA checks pass, without warning removal or waivers.

This is a pending retrospective layout proposal. New complete native characters/planes/bounds, storage/control/inverse, focused actual evidence, frozen policy and registered integration remain to be checked. No additional source/prose, completion or integrated-revision credit is added for revisiting already credited lines.

The original shared151-159 progressive nameplate finding remains: clean 水夫 supports Sailor, independently of the 配下/Retainer full-name field. Full-name and remaining indirect/typed/COMMON/UI consumers and all207 names remain open. Keep the full editorial objective and all other wrap/source/story/shop/town/random/Help/player-prose leads. MainV4701 stays unchanged; the separate unified test package remains canceled."""
NEXT="""Continue the full objective from verified V7835 and experimental current V7821. First advance the pending B218 R27 automatic-layout proposal in translations/lil_B218_retrospective_layout_manuscript_v1.json and work/analysis/retrospective_B218_predicate_plan_v7833/one_changed_automatic_plan12_exact_reuses_all13_unmodified_base_QA.json. The complete13 clean/current speeches were reviewed, all words retained, and only one automatic compiled plan changed. Obtain Lil's own current V7821 context when needed; do not substitute Maria's or historical RAM. Validate the changed native display and storage/controls/inverse, relevant actual behavior and policy, then integrate through the registered cumulative workflow and exact clean-input patch without duplicate editorial credit.

Keep all13 retrospective leads in work/analysis/completed_contraction_wrap_leads_v7831/completed_layout_contraction_andquestion_tag_leads_with_live_storage_refs.json. They are candidates, not automatic defects or global boundary rules. The heuristic covers558 existing markup plans, not all6938 records; extend coverage through exact source/current consumers. Evaluate each complete exchange and measure alternatives; retain ordinary wraps with reasons.

Continue all four storylines and earlier translated exchanges, broad practical shared shop/town/random capture, Help and all remaining player-facing prose, all207 names/roles/aliases and earlier unfinished inventories/counterpart/item/display leads. Preserve the original151-159 水夫/Sailor progressive-name retention and review their separate full-name/other consumers. Preserve every generated ROM, translation, draft, executed producer, failure, trace and proof. Keep graphics/all18 plaques and the later older-record technical re-audit separate. No canceled separate test package, promotion, pruning, commit or push."""
GATES='''def gates():
    prior,proof=map(read,[PRIOR,PROOF])
    plan=read('work/analysis/retrospective_B218_predicate_plan_v7833/one_changed_automatic_plan12_exact_reuses_all13_unmodified_base_QA.json')
    leads=read('work/analysis/completed_contraction_wrap_leads_v7831/completed_layout_contraction_andquestion_tag_leads_with_live_storage_refs.json')
    assert plan['manuscript_sha256']==sha(PROOF.read_bytes()) and len(proof['records'])==13
    assert plan['changed_IDs']==['DK4_MES_B218_R0027'] and proof['wording_retentions']==13
    assert proof['proposed_automatic_layout_revisions']==1 and proof['unchanged_exact_compiled_plans']==12
    assert proof['all13_complete_clean_andcurrent_exchanges_read'] and proof['proposed_formatting_native_storage_actual_policy_release_pending']
    assert leads['lead_count']==13 and len(leads['source_current_native_groups'])==11 and not leads['binding_issues']
    assert proof['no_new_completion_orintegrated_revision_counter_credit'] and not proof['new_credit']
    assert proof['current_ROM_sha256']==prior['candidate_sha256']
    assert sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256']
    assert sha(Path(prior['patch']).read_bytes())==prior['patch_sha256']
    return prior,proof'''
if __name__=='__main__':
    assert not TARGET.exists() and not ROOT.exists()
    source=SOURCE.read_text(encoding='utf-8');tree=ast.parse(source)
    assignments={n.targets[0].id:ast.get_source_segment(source,n) for n in tree.body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
    gates=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='gates')
    changes={
        assignments['FINDING']:'FINDING='+repr(FINDING),
        assignments['NEXT']:'NEXT='+repr(NEXT),
        ast.get_source_segment(source,gates):GATES,
        "work/analysis/name_consumer_checkpoint_v7829":"work/analysis/retrospective_wrap_checkpoint_v7834",
        "editorial_handoff_verification_v7830":"editorial_handoff_verification_v7835",
        "editorial_handoff_verification_v7827":"editorial_handoff_verification_v7830",
        "work/analysis/retainer_source_consumer_v7828/nine_roles_original_Sailor_nameplate_distinct_from_internal_subordinate_field.json":"translations/lil_B218_retrospective_layout_manuscript_v1.json",
        "shared151_159_original_progressive_name_consumer_v7829":"retrospective_B218_predicate_layout_pending_v7834",
        "unfinished_editorial_scope_v7829":"unfinished_editorial_scope_v7834",
        "old['unfinished_editorial_scope_v7826']":"old['unfinished_editorial_scope_v7829']",
        "direct_progressive_nameplates_retained=9":"wordings_retained=13,pending_layout_revisions=1,other_exact_compiled_reuses=12",
        "full_name_andother_consumers_open=True":"native_storage_actual_policy_andrelease_pending=True",
        """Path('scripts/review_retainer_source_name_consumer_v7828.py'),
            Path('scripts/review_retainer_source_name_consumer_v7828b.py'),
            Path('work/analysis/retainer_source_consumer_repair_v7828b/provenance.json'),
            Path('work/analysis/maria_B36_completion_repair_v7826b/provenance.json')""":"""Path('work/analysis/completed_contraction_wrap_leads_v7831/completed_layout_contraction_andquestion_tag_leads_with_live_storage_refs.json'),
            Path('work/analysis/retrospective_B218_wrap_gloss_v7832/thirteen_fresh_clean_exchange_glosses_before_full_current_layout_review.json'),
            Path('work/analysis/retrospective_B218_predicate_plan_v7833/one_changed_automatic_plan12_exact_reuses_all13_unmodified_base_QA.json'),
            Path('scripts/plan_retrospective_B218_predicate_v7833.py')""",
        """direct_progressive_nameplate_retentions=9,these_are_name_decisions_not_new_dialogue_completion_credit=True,""":"""wording_retentions=13,pending_automatic_wrap_revisions=1,no_duplicate_dialogue_credit=True,""",
        "earlier_broad_inference_superseded_only_for_explicit_source_progressive_branch=True":"only13_metadata_leads_andone_pending_changed_plan_not_broad_wrap_approval=True",
        "full_name_andremaining_consumers_open=True":"full_scope_all13_other_wrap_leads_andnames_remain_open=True",
        "## V7829: Original shared speaker-name consumer clarified; V7821 current":"## V7834: Retrospective wrap scan and one pending automatic refinement; V7821 current",
        "# Current editorial handoff - V7829; V7821 current":"# Current editorial handoff - V7834; V7821 current",
        "Six name-consumer checkpoint targets staged":"Six retrospective-wrap checkpoint targets staged",
        "Six audited name-consumer checkpoint targets applied":"Six audited retrospective-wrap checkpoint targets applied",
        """shared151_159_original_progressive_Sailor_source_verified=True,
                shared151_159_internal_role_not_progressive_display_source=True,
                shared151_159_full_name_andother_consumers_remain_open=True,
                source_name_consumer_proof=str(PROOF),source_name_consumer_proof_sha256=sha(PROOF.read_bytes()),""":"""retrospective_B218_R27_layout_pending=True,retrospective_wrap_leads=13,
                recorded_markup_plans_scanned=558,completed_records_not_in_markup_scan=6380,
                pending_layout_manuscript=str(PROOF),pending_layout_manuscript_sha256=sha(PROOF.read_bytes()),""",
        "V7830 verified:original Sailor consumer clarified":"V7835 verified:13wrap leads/one pending automatic refinement recorded",
    }
    result=derive(str(SOURCE),str(TARGET),changes)
    ROOT.mkdir(parents=True);save(ROOT/'provenance.json',dict(derivation=result,
        zero_credit_only_pending_retrospective_layout=True,all_original_inverse_hash_andworkspace_guards_preserved=True,
        no_native_high_numeric_constant_change=True,full_goal_complete=False))
