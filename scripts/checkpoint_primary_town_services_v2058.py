"""Checkpoint84 source/prose decisions; no formatting or integration credit."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/town_services_checkpoint_v2058')
DOC=Path('translations/primary_town_services_contextual_editorial_manuscript_v2.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
HANDOFF=Path('docs/editorial_handoff_current.md')
PROOF=Path('work/analysis/town_services_roles_v2056b/active_eight_requests_and_tribute_payment_direction.json')
LITERALS=Path('work/analysis/town_services_literals_v2055/all84_original_printf_shared_expander_and_literal_guards.json')
if __name__=='__main__':
 assert not ROOT.exists()
 doc,ledger,proof,literals=map(read,(DOC,LEDGER,PROOF,LITERALS));rows=doc['records'];ids=[r['message_id']for r in rows]
 assert ids==[n for n in range(85)if n!=64]
 assert len(rows)==84 and sum(r['editorial_decision']=='revise'for r in rows)==42
 assert all(all(r['review'][k]for k in('source','context','localization','naturalness'))and not r['review']['formatting']for r in rows)
 assert (ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(2059,1456,603)
 assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==2175
 f=ledger['contextual_story_natural_dialogue_pass_v1871']
 assert (f['fresh_pass_records_explicitly_reread'],f['fresh_pass_records_integrated'],f['fresh_pass_records_pending_native_actual_release'])==(656,656,0)
 assert len(ledger['reviewed_but_incomplete_COMMON_IDs'])==116 and not set(ids)&set(ledger['reviewed_but_incomplete_COMMON_IDs'])
 assert not literals['failures']and literals['original_native_printf_calls']==literals['original_shared_macro_calls']==488
 assert len(proof['full_town_RGB_pairs'])==20 and len(proof['tribute_branch_cases'])==3
 candidate=ledger['current_integrated_candidate'];assert sha(Path(candidate['path']).read_bytes())==candidate['sha256']==doc['current_ROM_sha256']
 ROOT.mkdir(parents=True)
 for path in(LEDGER,HANDOFF,Path('docs/translation_progress.md'),Path('docs/editorial_review_goal.md'),Path('docs/todo.md'),Path('docs/known_issues.md')):
  (ROOT/(path.name+'.before')).write_bytes(path.read_bytes())
 ledger['records_with_source_and_prose_pass']=ledger['records_with_source_prose_drafts']=2259
 ledger['source_prose_reviewed_counts_by_file']['/COMMON/MESFILE.DK4']=1602
 ledger['reviewed_but_incomplete_COMMON_IDs']=sorted(ledger['reviewed_but_incomplete_COMMON_IDs']+ids)
 active=ledger['active_source_prose_drafts'];active['native_message_IDs']=sorted(set(active['native_message_IDs'])|set(ids))
 active['manuscripts'] +=[str(DOC.with_name(DOC.name.replace('_v2','_v1'))),str(DOC)]
 active['manuscript_record_subsets_pending'][str(DOC)]=ids
 active['status']='200-reviewed-COMMON-incomplete;84fresh-town-services-drafts;0fresh-route-drafts;historical-manuscript-list-preserved'
 active['note']='Fresh740 explicitly reread:656 integrated/reconciled and84 new primary town-service drafts. Native format/cache/revised gameplay/release pending. Other1403 historical completions still need fresh reconciliation.'
 f['record_keys'] +=[dict(file_path='/COMMON/MESFILE.DK4',id=r['id'])for r in rows]
 f['record_IDs'] +=[r['id']for r in rows]
 assert len(f['record_keys'])==len({(r['file_path'],r['id'])for r in f['record_keys']})==740
 f.update(fresh_pass_records_explicitly_reread=740,fresh_pass_records_pending_native_actual_release=84,latest_contextual_manuscript=str(DOC))
 family=dict(id='Primary-town-services84',file_path='/COMMON/MESFILE.DK4',records=84,native_message_IDs=ids,manuscript=str(DOC),revisions=42,retentions=42,source_prose_reviewed=True,formatting_reference_actual_release_pending=True)
 f['pending_contextual_families'].append(family)
 f['coverage_note']='740 file-qualified entries explicitly reread:656 integrated/reconciled and84 primary town-service drafts pending native formatting/cache/revised gameplay/release. Historical2059 completions unchanged;1403 still outside the reconciled fresh pass. ID64 excluded for its complete ceremony exchange.'
 summary=('Reviewed84 primary town-service entries as complete clean-Japanese functional exchanges:42 proposed revisions and42 individually justified retentions. Covers crowd alerts,trader bargaining/price checks,crew/repair/supply warnings,resupply,tavern greeting-call-reply-drink-bill,docking/unassigned sailors,andtribute/rent. Separate previously completed ritual64 excluded for its own full exchange. '
 'Restores the named attendant as addressee in54,the customer announcement in55,per-view price fee18,zero-crew andrepair/supply distinctions,anditem rent84;variable quantities use number-neutral grammar. Native request trace binds8 actual IDs49,8,51,53,55,56,59,61;49/59 are Yes/No parents. Actual arguments are fullwidth600 andMihwa (4d69687761),correcting the earlier screenshot-based Miwa label. All20 post-opening town RGB pairs match the prior context. '
 'Original clean-exact caller and3 cloned native transfers prove monthly tribute76..82 credits the player anddebits the donor;these are offline native branch tests,not earned monthly-tribute gameplay. 488 originalprintf and488 originalshared-macro calls pass across all84 logical templates,typed supplied values and4 alignments,with exact native memory/ABI/canaries. '
 'No layout/cache/revised-gameplay orrelease approval yet. Allformatting gates remainfalse;English42/42 bodies unchanged innotes-only manuscriptv2. Historical2059 complete=1456revised603retained unchanged. Source/prose2259=1602COMMON429SC2117SC073SC138SC3. Fresh740 reread/656integrated/84pending;200COMMON incomplete and1403 historical completions need fresh reconciliation. '
 'RegisteredV2047 remains489batches114layers with its exact clean-input patch;no ROM/profile/registry mutation. All current emulator jobs terminal. Everyremaining storyline/shared shop/town/random/player prose,separategraphics/all18 plaques,SC3B109 classification andlater older-record technical re-audit stayopen. AllROMs andearlier translations preserved;V1492 promoted,canonicalunchanged,fullgoalactive.')
 evidence={str(p):sha(p.read_bytes())for p in(DOC,PROOF,LITERALS,Path('work/analysis/town_services_source_v2051/all84_clean_current_primary_town_service_exchanges.json'),Path('work/analysis/town_services_refinement_v2057/refinement_receipt.json'))}
 ledger['primary_town_services_contextual_v2058']=dict(summary=summary,manuscript=str(DOC),records=rows,evidence=evidence,formatting_complete=False,goal_turn_classification='progress',full_goal_complete=False)
 ledger['latest_checkpoint']='V2058 '+summary
 ledger['coverage_units'].append(dict(**family,status='source-prose-complete-native-format-cache-revised-gameplay-release-pending',source_prose_reviews_added=84,completed_entries_added=0,evidence=evidence,full_goal_complete=False))
 assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==2259 and len(ledger['reviewed_but_incomplete_COMMON_IDs'])==200
 assert len(active['native_message_IDs'])==200
 assert f['fresh_pass_records_integrated']==656 and f['historical_completed_records_outside_reconciled_fresh_pass']==1403
 assert ledger['goal_status']=='active'and not ledger['full_goal_complete'];save(LEDGER,ledger)
 h=HANDOFF.read_text(encoding='utf-8').replace('# Current editorial handoff - V2050','# Current editorial handoff - V2058',1)
 h=h.replace('603 retained; 2175 source/prose reviewed.','603 retained; 2259 source/prose reviewed.',1)
 h=h.replace('**656 explicitly reread and integrated/reconciled; 0 fresh route drafts.**','**740 explicitly reread:656 integrated/reconciled and84 primary town-service drafts pending.**',1)
 h=h.replace('Reviewed:1518 COMMON','Reviewed:1602 COMMON',1).replace('116 COMMON incomplete; all remaining','200 COMMON incomplete; all remaining',1)
 marker='## Maria Hangzhou opening38 integrated - V2050';assert marker in h
 section='## Primary town-services84 source/prose and native-role checkpoint - V2058\n\n'+summary+'\n\n'
 section+='- Manuscript: `'+str(DOC)+'`; all84 exact source/current references,full exchange IDs,glosses andindividual revision/retention reasons. V1 frozen;V2 corrects notes only.\n'
 section+='- Native request/role/payment proof: `'+str(PROOF)+'`. Actual38500-frame replay uses the existing isolated systemunlock,notearned;no savestate/story/location/RNG/funds/outcome fixture. No monthly tribute visit isclaimed. Eight actual requests and20 exact town RGB pairs.\n'
 section+='- Native literal proof: `'+str(LITERALS)+'`:488printf+488macro calls,0failures. Supplied typed stress arguments areoffline tests. These are not font/layout/cache or revised gameplay approval.\n'
 section+='- Correction: native attendant name bytes are **Mihwa**,not the earlier screenshot-based Miwa label inhistorical notes/guide filenames. Preserve old artifacts;game text wasnotrenamed. Failed2056 producer hasinvalid Python keyword names;explicit2056b successor passes.\n'
 section+='- Next: bind direct/Yes-No/portrait consumer geometry andcurrent post-expansion wrapper selection forIDs0..84;verify complete leading/trailing glyphs,whole words,bounds andpagination;source-locked single8KiB repack/all3668 copy preservation;representative revised town transitions;registered cumulative clean-input patch. Keep English asone paragraph before native macro expansion (literal I+LF isunsafe). Reuse passed story/release checks. Alljobs terminal.\n\n'
 HANDOFF.write_text(h.replace(marker,section+marker,1),encoding='utf-8',newline='\n')
 for name in('editorial_review_goal.md','translation_progress.md','todo.md','known_issues.md'):
  with(Path('docs')/name).open('a',encoding='utf-8',newline='\n')as out:out.write('\n\n## V2058 Primary town-services84 source/prose checkpoint\n\n'+summary+'\n')
 Path('docs/primary_town_services_v2058_checkpoint.md').write_text('# Primary town-services84 V2058\n\n'+section,encoding='utf-8',newline='\n')
 save(ROOT/'checkpoint_receipt.json',dict(summary=summary,evidence=evidence,ledger_sha256=sha(LEDGER.read_bytes()),handoff_sha256=sha(HANDOFF.read_bytes()),source_prose_reviews_added=84,completed_entries_added=0,source_prose=2259,fresh_reread=740,fresh_integrated=656,fresh_pending=84,historical_completed=2059,registered_candidate_unchanged=True,all_ROMs_preserved=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print(dict(source_prose=2259,fresh_reread=740,integrated=656,pending=84,historical_complete=2059,COMMON_incomplete=200))
