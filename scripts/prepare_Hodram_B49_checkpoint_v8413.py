"""Reversible full-scope checkpoint for B49 native/storage/reference andselected actual progress."""
import inspect
from pathlib import Path
from scripts import checkpoint_Hodram_B49_v8391 as previous
from scripts.source_locked_derivation_v5118 import derive,checked_text
from scripts.verify_village_wrap_v608 import save

PROOFS={**previous.PROOFS,
 'first_manuscript':previous.PROOFS['manuscript'],
 'manuscript':'translations/hodram_B49_editorial_manuscript_v2.json',
 'first_layout':'work/analysis/Hodram_B49_layout_v8393/automatic_plans.json',
 'wrap_comparison_a':'work/analysis/Hodram_B49_wrap_compare_v8393a/read_only_wrap_comparison.json',
 'wrap_comparison_b':'work/analysis/Hodram_B49_wrap_compare_v8393b/read_only_wrap_comparison.json',
 'layout':'work/analysis/Hodram_B49_layout_v8394/automatic_plans.json',
 'pages':'work/analysis/Hodram_B49_pages_v8395/compiled_native_pages.json',
 'layout_guards':'work/analysis/Hodram_B49_layout_guards_v8396/focused_guard_rejections.json',
 'native_view':'work/analysis/Hodram_B49_native_review_v8397/native_body_review.json',
 'relocation':'work/analysis/Hodram_B49_relocation_v8398/reconstruction.json',
 'stored':'work/analysis/Hodram_B49_stored_v8399/stored_bodies.json',
 'menu':'work/analysis/Hodram_B49_menu_v8400/menu_provider_and_planes.json',
 'controls':'work/analysis/Hodram_B49_controls_v8401d/stored_controls.json',
 'picture_diagnostic':'work/analysis/Hodram_B49_picture_probe_v8401c/differences.json',
 'independent':'work/analysis/Hodram_B49_independent_v8402/independent_reconstruction.json',
 'reference':'work/analysis/Hodram_B49_reference_v8403/research_image_receipt.json',
 'menu_view':'work/analysis/Hodram_B49_reference_v8403/menu_direct_review.json',
 'loaders':'work/analysis/Hodram_B49_loaders_v8404/325_whole_native_loads_cache_hits650_initial_parent_modes.json',
 'references':'work/analysis/Hodram_B49_references_v8405b/references.json',
 'fixtures':'work/analysis/Hodram_B49_fixtures_v8406/two_whole_scripts.json',
 'models':'work/analysis/Hodram_B49_models_v8408/native_models.json',
 'actual':'work/analysis/Hodram_B49_actual_v8409/B49/paired_actual_dialogue_headers_flow_returns.json',
 'comparison':'work/analysis/Hodram_B49_comparison_v8410/paired_selected_path_comparison.json',
 'difference_sheet':'work/analysis/Hodram_B49_difference_view_v8411/sheet.json',
 'actual_view':'work/analysis/Hodram_B49_actual_review_v8412/selected_path_review.json',
}
SUMMARY="""Registered cumulative V8377 remains current; main V4701 and the canonical baseline are unchanged. Exact totals remain 7205 completed, 7208 credited source-prose/drafts, 4474 integrated revisions and 2731 justified retentions. SC0 368, SC1 125, SC2 4915, SC3 197, COMMON 1600 complete/1603 source-prose; route subset5605 is not the whole-goal denominator. Preserve every ROM, translation, draft, executed producer, proof and failed attempt. No separate user test package, promotion, pruning, commit or push.

B49 still has sixteen uncredited decisions: fourteen speeches and two canonical typed options, seven revisions and nine individually justified retentions. Clean-first whole-exchange meaning, characterization, item84 Heavenly Wristband/item148 Ullr's Bow, approved Proof of Supremacy term and source/current references remain unchanged. Manuscriptv2 adds native-body formatting evidence to v1 prose without changing a word. All sixteen final formatting gates remain false.

Automatic plan8394 uses the full216px width, original protected-break compiler, measured6/9/15 defaults and source-qualified ellipses. Fourteen one-page native bodies/56 alignments pass complete first/internal/final glyphs, bounds andconsumption. The New World directions now have three balanced32/33/32-cell rows with no word changes. Seven source line-count infos remain; zero warnings/waivers. R15 silence and R67 mixed leading ellipsis/ASCII are complete. Earlier8393 layouts/comparisons are preserved. Fourteen changed-input guard rejections8396 pass; no global Unicode, NUL, font, viewport orQA relaxation.

Sparse reconstruction8398 and independent36-command-atom reconstruction8402 produce the same whole block/archive. All36commands,14six-byte preambles,eight relative sites/40fresh cases,one raw8000query,one typed2100menu,two item148 layouts[2,0,0]/[0,0,0],two hide boundaries,seven opaque effects andfull4-byte terminal/separate tails survive. Six compiler parity tails receive24fresh alignments; eight exact bodies reuse32cases; every viewed inkplane isunchanged andno extra page appears. Both clean/current blocks, predecessor archive andwhole predecessor ROM recover exactly. All324otherSC1blocks/allother files/components areexact.

The typed table is22bytes versus26 currentbytes. Only No.'s three storage spaces are removed; both choice wordings/order remain unchanged. Six original provider/even-alignment cases,18 bridged modal returns andeight complete current/target style planes pass. The constructor preserves the same60px caption width/rectangle; No. isproperly centered. This isoffline native evidence; actual B49 menu backing/controller selection/normal dismissal remain pending. Stored controls8401d verify14dispatches/one original null FE,query raw[2,0,0,0,0,0],four picture/hide calls and25normal value-carry ends. The stopped8401/8401b verifiers and8401c diagnostic remain preserved: exact source_offset field binding andthe hide call's carried r3 pointer require the exact command-relocation delta,not blind equality. No native value is discarded. Fresh325load-cache paths/650parent modes/326actions andshipped-code census8405b pass; selected event49 requires48. The earlier8405 two-event-membership assertion ispreserved;selected B49 packet hasonly event49,while8384 separately verifies prerequisite48.

Two complete-script entry fixtures8406 withoriginal8Hodram initializers34bytes andidentical ordinary inputs8407 produced20002actual frames. Actual audit8409 anddirectview8412 cover six source plus six English pages/66complete body-and-name holds, both Hodram Bergstrom/Lil Argot headers,standalone ellipsis,three-row directions,andoriginal item148 layout2 show/hide. Whole scripts retain every command; original opening state selects the no-item branch andleaves eight conditional speeches/two choices unvisited. Normalreturns are5213 Japanese/5216 English,both[0,0]. No inventory, flags, RNG, roles, funds, results orcontroller timing were forced. This isinitialized entry-fixture coverage,not natural optional-event activation,original location,earned progress,fullroute orhardware coverage.

Comparison8410 retains two speech-duration differences,zero UI-request differences anddifferent PRNG values atsource offsets324/416/424/980. Final sampled seeds both1633251573,five checked native components/whole actors/captain1 match; rawcalendar0/[0,0,0] remains uninterpreted. Later79of81RGBpairs match;5350Port-tooltip edge/highlight and6130later sailing-menu first-row highlight differ andwere directlyviewed. Following commands withframes are notidentical. Matching finalsample doesnot prove every-frame causality,future RNG outcomes orbroad simulation. All older B48/Gerhard/Rafael/Hodram timing/RNG/component/calendar/RGB/fixture-entry limitations remain intact.

Full objective remains allfour stories, earlier translated dialogue,shared shops/towns/random scenes,Help/remaining prose,all207names/roles/aliases/custom-name risks andretrospective premature wraps. Copyevery priorlead/family/history. Graphics/all18plaques andlater older-record technical re-audit remain separate. B49 adds zero completion/source-prose credit until remaining required checks andregistered integration pass."""

NEXT="""Continue from verifiedV8414/currentregisteredV8377,using own captain1 input8380 forRAM-dependent checks. Reuse completed B49 source/prose/native pages/parity/storage/relative/control/inverse/loaders/caller andselected actual proofs; do not repeat unchanged checks. Use manuscriptv2, source/current packet8387b, automatic plan8394, reconstructed archive8398, independent8402 andpinned research reference8403. The all-four-story objective remains active and7205completed stays unchanged.

Resolve concrete remaining display risks withfocused initialized tests: original B49 typed2100 menu's complete glyphs/highlight/backing ownership, both choices andnormal dismissal/result routing; R67 source-bound mixed ellipsis+English inactual progressive display; outgoing wristband FE R81, its absent personal header andtransition backto original commands; item148 layout0/hide ifneeded forits distinct behavior. Preserve original source controls andtyped-table offset/NUL/even-zero rules. Disclose any bounded display fixture separately fromwhole-event activation. Do not force possession/quest flags/RNG/results orclaim the unvisited original paths earned or naturally activated. Exhaustive playthroughs/individual visits to every conditional line are not required.

Once necessary tests pass, record final sixteen source/current/stored references andindividual formatting approvals,freeze natural-dialogue-v2 policy withscoped ellipsis/ordinary New-World wrap bindings andmeaningful changed-input checks,implement one complete-NDS atomic commit andregister after the entireV8377 stackwith explicit Gerhard Adernkatz dependency. Use only build_integrated_release.py forregistered cumulative integration,verify exactclean-input patch andownstartup,then credit16once only: projected7221completed/7224source-prose/4481revised/2740retained/SC1141/routesubset5621,subject tofinal exact arithmetic. Keep canonical.source versus fullparent.rom distinction; compare actual in-memory bytes andcommit image.rom,not files-list-only.

Preserve all fullscope leads:12contraction/questiontags,unscanned beyond558plans,weak-before-row/page-before-readability,COMMON750-752/preLF6435,wider actor104/105/113/147 families,Janus Pasar/Pasha consumers,ceramics17wrap,Cristina/Christina,HansRetzel/Letzel,Samwellmiddle,SourceItem/LocalProduct,Alexandria caller,Aksum Gold Seal,Armadillo/SteelHide,HerophilusMedicine,イギリス,AlShin/AlFeridShin,Sailor151-159versusRetainer,all207names/aliases/customnames andall copiedhistorical discoveries. Keep older normal-end carry,nineteenth-cell,B47/B48/B50 metadata/caller/fixture-entry errata andall previous measured timing/RNG/component/calendar/RGB limitations. Broad practical town/random capture, honest offline/gameplay distinctions,registered integration andexact patch remain required. Preserve all artifacts/main4701/canonicalbaseline;no separatepackage/promotion/pruning/commit/push. Graphics/later older-record technical audit stayseparate."""

EXTRA="""    assert doc['predecessor_manuscript_sha256']==sha(Path(PROOFS['first_manuscript']).read_bytes()) and data['native_view']['manuscript_sha256']==sha(Path(PROOFS['manuscript']).read_bytes())
    assert not data['layout']['failures'] and len(data['pages']['records'])==14 and data['pages']['fresh_compiled_alignment_cases']==56
    assert data['layout_guards']['negative_count']==14 and data['native_view']['reviewed_body_pages']==14
    assert data['native_view']['all_original_QA_infos']==7 and data['native_view']['warnings']==data['native_view']['waivers']==0
    assert data['stored']['fresh_native_alignment_cases']==24 and data['stored']['exact_reused_native_alignment_cases']==32 and data['stored']['all14_ink_planes_exact_to_already_viewed']
    assert data['relocation']['source_relative_sites']==8 and data['relocation']['relocated_native_skip_cases']==40 and data['independent']['whole_target_block_andarchive_byte_equal_to_sparse_rebuild']
    assert data['reference']['complete_parent_ROM_inverse_byte_exact'] and data['reference']['all324_otherSC1_blocks_andall_other_files_components_exact']
    assert data['menu']['even_alignment_provider_cases']==6 and data['menu']['bridged_modal_return_cases']==18 and data['menu']['complete_native_caption_style_planes']==8
    assert data['menu_view']['reviewed_two_choices_in_both_current_andproposed_forms']
    assert len(data['controls']['final_dispatches'])==14 and len(data['controls']['normal_seeded_ends'])==25
    assert data['loaders']['fresh_native_whole_loads_andcache_hits']==325 and data['loaders']['fresh_initial_parent_modes']==650 and data['references']['external_references_complete']
    assert len(data['fixtures']['fixtures'])==2 and data['actual_view']['actual_frames']==20002 and data['actual_view']['actual_complete_source_andEnglish_body_name_holds']==66
    assert not data['actual']['unresolved'] and data['actual_view']['all_four_sheets_directly_viewed'] and len(data['actual_view']['unvisited_conditional_text_IDs'])==8
    assert data['actual_view']['later_RGB_equal_pairs']==79 and data['actual_view']['later_RGB_total_pairs']==81 and len(data['actual_view']['different_script_boundary_RNG_values'])==4
    for fixture in data['fixtures']['fixtures']:assert sha(Path(fixture['research_ROM']).read_bytes())==fixture['research_ROM_sha256']
    for version in ['clean_Japanese','revised_English']:
        terminal=Path('work/analysis/Hodram_B49_scene_runs_v8407')/('route1_B49_'+version)/'terminal.json';t=read(terminal)
        assert t['terminal'] and t['frames']==10001 and sha(Path(t['report']).read_bytes())==t['report_sha256'] and sha(Path(t['observer']).read_bytes())==t['observer_sha256']
"""

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B49_checkpoint_tools_v8413');assert not root.exists()
    source=Path(previous.__file__).read_text('utf8');a=source.index('PROOFS=');b=source.index('\ndef restore');c=source.index('def gates():');d=source.index("if __name__=='__main__':",c)
    gates=checked_text(inspect.getsource(previous.gates),{
        "data['logical']['manuscript_sha256']==sha(Path(PROOFS['manuscript']).read_bytes())":"data['logical']['manuscript_sha256']==sha(Path(PROOFS['first_manuscript']).read_bytes())",
        '    return prior,data':EXTRA+'    return prior,data',
    })
    p=source.index('        pending=dict(');q=source.index('        oldpending=',p)
    pending="""        pending=dict(status='B49-sixteen-prose-native-storage-reference-approved-selected-six-actual-pending-focused-menu-FE-policy-registered-integration',file_path='/data/SC1.DK4',blocks=[49],records=16,physical_speeches=14,typed_choice_labels=2,proposed_revisions=7,justified_retentions=9,manuscript=PROOFS['manuscript'],names=PROOFS['names'],proofs=PROOFS,all_four_prose_gates_true_all_formatting_gates_false=True,automatic_body_pages=14,body_alignments=56,fresh_stored_alignments=24,exact_reused_stored_alignments=32,relative_sites=8,relocated_relative_cases=40,normal_end_value_carry_cases=25,typed_menu_provider_alignments=6,bridged_modal_returns=18,complete_menu_style_planes=8,native_whole_load_cache_paths=325,parent_entry_modes=650,actual_frames=20002,actual_selected_speech_pairs=6,actual_complete_body_name_holds=66,actual_unvisited_speeches=8,actual_unvisited_B49_choice_labels=2,both_whole_block_inverses_whole_archive_andROM_inverse_exact=True,all324_other_SC1_blocks_andall_other_files_components_exact=True,actual_boundary_RNG_timing_andtwo_later_RGB_differences_retained=True,focused_UI_backing_controller_results_FE_mixed_ellipsis_andregistered_release_pending=True,new_credit=0,full_goal_complete=False)
"""
    result=derive(str(Path(previous.__file__)),'scripts/checkpoint_Hodram_B49_v8413.py',{
        source[a:b]:'PROOFS='+repr(PROOFS)+'\nSUMMARY='+repr(SUMMARY)+'\nNEXT='+repr(NEXT)+'\n',source[c:d]:gates+'\n',source[p:q]:pending,
        'Hodram_B49_checkpoint_v8391':'Hodram_B49_checkpoint_v8413',
        'editorial_handoff_verification_v8392':'editorial_handoff_verification_v8414',
        'editorial_handoff_verification_v8383':'editorial_handoff_verification_v8392',
        'Hodram_SC1B49_sixteen_contextual_logical_drafts_pending_formatting_actual_registered_v8391':'Hodram_SC1B49_native_stored_references_actualsix_pending_focused_UI_registered_v8413',
        'unfinished_editorial_scope_v8391':'unfinished_editorial_scope_v8413',
        'superseded_by_source_prose_checkpoint':'superseded_by_native_stored_selected_actual_checkpoint',
        'B49whole-exchange sixteen prose decisions andlogical56;formatting andactualnext':'B49 native14/storage/reference/actual6 verified;focused menu andFE next',
        'Hodram_B49_source_prose_checkpoint':'Hodram_B49_native_stored_selected_actual_checkpoint',
        'new_actual_frames=0,new_research_ROMs=0':'new_actual_frames=20002,new_research_ROMs=3',
        'new_emulator_runs=0,new_actual_frames':'new_emulator_runs=2,new_actual_frames',
        'zero-credit six drafts':'zero-credit sixteen pending records',
        'B49sixteen prose decisions/7revisions9retentions/56logicalalignments;formatting_actual_registeredintegration pending.':'B49native14/stored56/reference/actualsixpairs66holds;focusedUI_FE_policy_registered integration pending.',
        'V8391':'V8413','V8392':'V8414',
        'Preserve a reversible zero-credit six-outcome-draft checkpoint after V8300 integration.':'Preserve full objective andverified B49 native/storage/reference/selected actual progress without credit.',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(derivation=result,all_prior_scope_leads_history_counts_records_andcurrent_registered_ROM_preserved=True,all_native_high_integer_constants_andmultiplicity_preserved=True,previous_count_question_added_no_editorial_credit_current_turn_makes_verified_progress=True,all_captures_terminal_andreaped=True,new_credit=0,full_goal_complete=False))
