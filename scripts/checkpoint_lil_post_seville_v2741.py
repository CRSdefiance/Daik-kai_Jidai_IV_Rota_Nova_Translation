"""Record34 fresh source/prose/native reviews; preserve pending release gates."""
from pathlib import Path
from copy import deepcopy
from shutil import copy2
from collections import Counter
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_post_Seville_checkpoint_v2741')
DOC=Path('translations/lil_post_seville_and_egypt_warning_editorial_manuscript_v4.json')
SOURCE=Path('work/analysis/lil_post_Seville_source_v2732/complete34_clean_current_native_context.json')
CONTROL=Path('work/analysis/lil_post_Seville_controls_v2734c/source_bound_34_preambles_and_B132_warning_predicate.json')
BRANCH=Path('work/analysis/lil_post_Seville_branches_v2733/original_relative_skip_operand_proof.json')
FONTS=Path('work/analysis/lil_post_Seville_fonts_v2739/current_macro_QA_and_progressive_font_proof.json')
APPROVAL=Path('work/analysis/lil_post_Seville_font_approval_v2740/approval_receipt.json')
FAMILY='Lil-post-Seville-and-Egypt-warning-B30-B31-B132-34'
SUMMARY=' '.join([
    'V2741 freshly reviews 34 complete speeches in Lil SC2 B30, B31 and B132: Valdes defeat and Clifford farewell, the port-worker Pirate King warning, and the earlier barkeep warning about the southern Mediterranean.',
    'Twenty-two revisions and 12 individually justified retentions preserve the complete exchanges and every stored conditional alternative.',
    'Restore Valdes shocked reaction, Spain strongest-fleet claim and shame before his sovereign; both alternative alliance descriptions; the confusion and divided-forces cause of defeat; Lil question about Clifford plans; and his dependence on royal orders.',
    'The Crown and my sovereign preserve the Japanese Majesty references without the old invented male monarch. Lil uneasy fragment, Clifford qualified hope and their reciprocal farewells retain wording that already works.',
    'Restore the full Pirate King of the Mediterranean title, local rumors, port-departure sequence, Egypt location, urgency, Janus stammer and exact FI name substitution, and Fernando cannot-pass-up-the-trade-opportunity reasoning.',
    'Remove the unsupported Clifford attribution at B31 R59. Original 8100 at B31 offset132 calls the completion getter with event132; its positive branch reaches Lil recognition of the warning. Complete B132 is the barkeep warning, with original must-not-completed dependencies31/32. The earlier B26 New World restriction does not establish the Egypt attribution.',
    'Barkeep ojisan is first-person older-man self-reference, not invented kinship. Gerhard two identical private thoughts remain separate reviewed conditional objects and do not reveal the unnamed man.',
    'All34 have exact clean/current references, fresh glosses and localization notes, and all five per-record gates. Source walking binds91 commands,34 complete preambles and32 relative sites. Native source/current skip tests pass320 cases.',
    'Sixty-eight historical copied-London dispatcher/macro contexts bind ordinary actor IDs2/4/9/16/20/28/31/92/113 and the original54020 progressive consumer. Catalog names are not claimed observed nameplates; UI preparation and native panel bodies are explicit unexecuted boundaries in that probe.',
    'Eight current original predicate cases pass with actor/model/event state exact. The preserved2734 probe stopped on an unclassified four-byte write. Diagnostic2734b identifies the original unaligned-operand helper2A5BC: STR at2A5D8 copies the misaligned four-byte operand to literal scratch02279600. Successor2734c binds every such write to the exact source operand and restores only that word; all unowned4MiB bytes and the entire restored context are exact. No event,roster,RNG or outcome is forced.',
    'A local source/runtime-bound nine-actor profile preserves printable71/5C and low control prefixes without changing global mappings. Current checks bind34 complete216x64 native/independent font planes,272 logical/compiled macro alignment calls,34 full QA reports and seven scope rejection controls.',
    'Visual review catches four awkward phrase boundaries after the initial2737 automated passes. Successor2738 refines only those four paragraphs, and2739 passes32 new macro calls/four new planes while reusing30 unchanged planes/240 calls under exact text,source,runtime,profile and preview hashes.',
    'All five sheets were viewed or hash-identical to previously viewed sheets. The four revised passages now have complete phrases, including no isolated about,were warned,Dont/forget or What does/he mean. Eleven individually justified source-line-count notes remain; no orphan,predicate,weak-ending,missing-glyph,control,overflow or blank-page waiver is granted.',
    'Complete resized branch/reference maps, external-entry and loader proofs, final parity-padding checks, representative reconciliation and guarded registered cumulative integration remain pending. No B30/B31/B132 activation, new portrait/nameplate observation, new emulator run or current startup is claimed.',
    'Fresh coverage is2310 reread /2276 integrated-reconciled /34 pending. Source/prose rises to2313, including483 SC2; completion remains2276, with1592 historically revised and684 retained. Completed route records remain677; source/prose route records rise to711. Three market COMMON entries750-752 and all wider untouched prose remain open.',
    'Registered cumulative experimental V2724 remains496 batches/114 accepted layers with its exactly reconstructable clean-input patch. ROM,registry,builder,profiles,manifest and patch are unchanged; V1492 remains promoted. All generated ROMs, earlier translations, clean/canonical inputs and executed proofs are preserved.',
    'Every never-reviewed storyline, shared shop/town dialogue, random scene and remaining player-facing prose stays in scope. Five named-target2187-2191 leads remain uncredited. Raw rejected-object classification, SC3 B109, separate graphics/all18 plaques and the later older-record technical re-audit remain open. Full goal active; all jobs terminal.'
])

if __name__=='__main__':
    assert not ROOT.exists();lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=deepcopy(ledger)
    previous=Path('work/analysis/editorial_handoff_verification_v2729/verified_handoff.json');assert sha(lp.read_bytes())==read(previous)['ledger_sha256']
    doc,source,control,branch,font,approval=map(read,[DOC,SOURCE,CONTROL,BRANCH,FONTS,APPROVAL]);rows=doc['records'];ids=[r['id'] for r in rows]
    assert len(rows)==len(set(ids))==34 and Counter(r['editorial_decision'] for r in rows)=={'revise':22,'retain-wording':12}
    assert all(all(r['review'].values()) and r['source_meaning'] and r['localization_note'] for r in rows)
    assert source['total_editorial_objects']==34 and sum(len(b['all_clean_native_commands']) for b in source['blocks'])==91
    assert len(branch['cases'])==320 and len(branch['operands_requiring_adjustment_when_resizing'])==32
    assert len(control['dispatch_cases'])==68 and len(control['current_original_predicate_cases'])==8 and control['warning_reference_is_B132_Barkeep_not_Clifford']
    assert font['manuscript_sha256']==sha(Path(doc['previous_manuscript']).read_bytes()) and len(font['cases'])==34 and font['current_original_macro_alignment_calls']==272
    assert approval['manuscript_sha256']==sha(DOC.read_bytes()) and approval['all5_review_sheets_viewed_or_exact_previously_viewed'] and approval['narrow_line_count_notes']==11
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871'];assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(2276,2276,0)
    selected=[dict(file_path='/data/SC2.DK4',id=n) for n in ids];keys={(r['file_path'],r['id']) for r in fresh['record_keys']}
    assert not {(r['file_path'],r['id']) for r in selected}&keys
    assert {historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']}==keys
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==2279
    docs=[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    assert docs[0].read_text(encoding='utf-8').startswith('# Current editorial handoff - V2728')
    ROOT.mkdir(parents=True)
    for p in [lp,*docs]:copy2(p,ROOT/(p.name+'.before'))
    ledger['records_with_source_and_prose_pass']=ledger['records_with_source_prose_drafts']=2313
    ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4']=483
    ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4']=ids
    active=ledger['active_source_prose_drafts'];active['manuscripts'].append(str(DOC));active['route_record_subsets_pending'][str(DOC)]=ids
    active.update(status='3-reviewed-COMMON-incomplete;34-post-Seville-Egypt-warning-native-reviewed-pending-release',
        note='2310 fresh rereads:2276 integrated/reconciled and34 post-Seville/Egypt-warning drafts pending reference,representative and registered-release gates. Source/prose2313; marketCOMMON750-752 and all wider untouched prose remain open.')
    fresh['record_keys'].extend(selected);fresh['record_IDs'].extend(ids)
    pending=dict(id=FAMILY,file_path='/data/SC2.DK4',blocks=[30,31,132],records=34,record_keys=selected,manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        proposed_revisions=22,retentions=12,source_prose_reviews_added=34,completion_credit_added=0,native_font_proof=str(FONTS),
        pending='Complete relocation/reference census and all32 resized relative sites; final parity/pagination; whole-script loader/entry proofs; representative shared-rule reconciliation; optional registered cumulative stage afterV2724, exact clean patch and required startup.',
        new_emulator_runs=0)
    fresh.update(fresh_pass_records_explicitly_reread=2310,fresh_pass_records_integrated=2276,fresh_pass_records_pending_native_actual_release=34,
        pending_record_keys=selected,pending_contextual_families=[pending],latest_pending_contextual_family=FAMILY,latest_contextual_manuscript=str(DOC),latest_contextual_choice_draft=None,coverage_note=active['note'])
    for unit in ledger['coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=711,completed_route_records=677,next='Finish34 B30/B31/B132 reference/representative/release gates,then continue every untouched storyline/shared/town/random/player prose family.')
    ledger['coverage_units'].append(dict(**pending,status='source-prose-current-native-formatting-approved;references-representative-release-pending',full_goal_complete=False))
    ledger['formatting_watchlist']['lil_post_Seville_v2741']=dict(status='all34-current-native-fonts-and-full-QA-pass;reference-padding-and-release-pending',
        manuscript=str(DOC),source_context=str(SOURCE),control_contract=str(CONTROL),branch_proof=str(BRANCH),native_font_proof=str(FONTS),
        all5_sheets_viewed_or_exact_previously_viewed=True,four_phrase_flow_findings_resolved=True,narrow_line_count_notes=11,
        no_orphan_predicate_or_missing_glyph_waivers=True,reference_map_pending=True,representative_reconciliation_pending=True,actual_B30_B31_B132_IDs=[],new_emulator_runs=0)
    requirements=ROOT/'next_registered_integration_requirements.json'
    save(requirements,dict(parent_profile='all-routes-unified-v2724',parent_ROM=doc['current_ROM'],parent_ROM_sha256=doc['current_ROM_sha256'],
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),source_context=str(SOURCE),control_contract=str(CONTROL),branch_proof=str(BRANCH),native_fonts=str(FONTS),
        blocks=[30,31,132],speeches=34,choices=0,FE_panels=0,commands=91,relative_sites=32,
        next='Use complete native source/current command map to compile34 reviewed paragraphs, preserve each original complete preamble and record parity, adjust32 relative spans, and prove all opaque bytes via inverse restoration. Execute the original relocated branch cases, native all-block loader/parent/entry contract and shipped reference census; bind final parity-padded texts through current original macro/native fonts with no blank page. Reconcile established source-bound progressive shared rules from V2721b and current V2727 startup as representative evidence under the user sampling policy; inspect distinct concrete risks rather than requiring individual conditional/speaker visits. Add one optional guarded stage after the full V2724 stack, with source/runtime/config/negative guards, then build through build_integrated_release.py, verify complete ancestry496parent batches/114accepted layers plus the new manuscript, exact clean-input patch, all unrelated bytes and required current startup before completing34.',
        preserve_every_ROM_translation_profile_accepted114_and_V1492_promotion=True,
        no_actual_B30_B31_B132_or_individual_new_nameplate_claim=True,do_not_require_every_conditional_or_speaker_visit=True,
        current_COMMON_parser_unchanged='dk4tool.patch.surrender_advice_contextual_v1.current_entries',current_context='scripts/current_common_native_context_v2677.py',full_goal_complete=False))
    inventory=deepcopy(read(ledger['unfinished_editorial_scope_v2728']['path']))
    inventory.update(incomplete_route_source_prose_groups=[dict(family=FAMILY,file_path='/data/SC2.DK4',blocks=[30,31,132],count=34,record_IDs=ids)],incomplete_route_source_prose_count=34,
        next_focus='Finish34 reviewed B30/B31/B132 reference/representative/release gates;continue all untouched storyline/shared shop/town/random/player prose. Market750-752 callers,raw rejected-object coverage and five uncredited named-target leads remain open.')
    for unit in inventory['broader_coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=711,completed_route_records=677,source_prose_pending_records=34,source_prose_pending_family=FAMILY,next=inventory['next_focus'])
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
    ledger['unfinished_editorial_scope_v2741']=dict(path=str(inv),sha256=sha(inv.read_bytes()),incomplete_COMMON=3,incomplete_route_source_prose=34,full_goal_complete=False)
    proofpaths=[DOC,SOURCE,CONTROL,BRANCH,FONTS,APPROVAL,requirements,inv,previous,Path(__file__),Path(doc['scoped_profile_module']),
        Path('work/analysis/lil_post_Seville_phrase_review_v2738/refinement_receipt.json'),
        Path('work/analysis/lil_post_Seville_predicate_diagnostic_v2734b/original_expression_write_trace.json'),
        *[Path(s['path']) for s in font['review_sheets']]]
    evidence={str(p):sha(p.read_bytes()) for p in proofpaths}
    ledger['lil_post_Seville_source_prose_native_v2741']=dict(summary=SUMMARY,**pending,evidence=evidence,goal_turn_classification='progress',full_goal_complete=False)
    ledger['latest_checkpoint']=SUMMARY
    for key in ['completed_editorial_families','records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed','completed_editorial_record_counts_by_file',
        'current_integrated_candidate','reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal']:
        assert ledger[key]==before[key],key
    assert len(fresh['record_keys'])==len({(r['file_path'],r['id']) for r in fresh['record_keys']})==2310 and len(fresh['integrated_record_keys'])==2276
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete'];save(lp,ledger)
    section='## V2741:34 post-Seville and Egypt-warning reviews; reference and release pending\n\n'+SUMMARY+'\n\nManuscript: '+DOC.as_posix()+'. Source: '+SOURCE.as_posix()+'. Native proof: '+FONTS.as_posix()+'. Next integration: '+requirements.as_posix()+'. Unfinished scope: '+inv.as_posix()+'.\n\n'
    for i,p in enumerate(docs):
        first,rest=p.read_text(encoding='utf-8').split('\n',1)
        p.write_text(('# Current editorial handoff - V2741' if i==0 else first)+'\n\n'+section+rest,encoding='utf-8',newline='\n')
    candidate=ledger['current_integrated_candidate']
    save(ROOT/'checkpoint_receipt.json',dict(checkpoint='V2741',summary=SUMMARY,evidence=evidence,updated_files={str(p):sha(p.read_bytes()) for p in [lp,*docs]},
        new_completed_records=0,new_source_prose_reviews=34,proposed_revisions=22,justified_retentions=12,fresh_reread=2310,fresh_integrated=2276,fresh_pending=34,
        source_prose=2313,completed=2276,historical_revised=1592,historical_retained=684,incomplete_COMMON=3,incomplete_route=34,
        candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],
        next_requirements=str(requirements),actual_B30_B31_B132_IDs=[],new_emulator_runs=0,goal_turn_classification='progress',all_jobs_terminal=True,full_goal_complete=False))
    print('V2741:34new source/prose/native reviews;22revisions/12retentions.2310reread/2276integrated/34pending;source/prose2313. V2724unchanged;full goal active.')
