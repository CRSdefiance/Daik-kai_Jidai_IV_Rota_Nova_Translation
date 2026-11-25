"""Reconcile24 fresh Planning/Finance retentions in the unchanged cumulative release."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/complete_work_context_v2313.py')
SUMMARY=(
 'V2339 reconciles24 historical COMMON Planning19/Finance20 comments1447-1470 as fresh, individually justified retentions. Every clean Japanese comment was reread with its actual role, NPC voice, protagonist and consumer context. They are independent alternatives, not a sequential exchange. The scheming comments preserve tentative planning, study, acquired experience, confidence and the protagonists\' distinct attitudes. The source 練る/寝る devising/sleeping joke becomes dream up a plan followed by snoring and Wrong kind of dreaming, preserving its comic sequence through an English double meaning. The finance comments preserve multiport market prices, current demand, prospective profit, this month\'s accounting, uncertainty and Lil\'s overwhelmed reaction. They do not invent a plan, target, relationship, rank, price, commodity, completed trade, profit total or game effect. Each entry has a new source gloss and retention reason. Speaker metadata1456/1468 is normalized from Joakim to native actor1 Hodram; Joakim remains approved in Hodram Joakim Bergstrom. Older manuscripts and the historical JoakimPlanning case label are preserved. English and native names are unchanged. '
 'Clean-exact current source code and50 complete native helpers pass:42 NPC role selections cover all eight voice classes, and eight protagonist selections preserve four previously captured actual captain states without fresh captain-ID substitution or new current four-hero visits. Sera24 uses ordinary voices for roles19/20. All24 full native working-state selectors, macro expanders, clears, glyph/font requests, complete words, first/final letters, canaries, bounds and ABI pass under declared isolated CPU role/assignment and initialized-widget controls. Actor health, mood and captain records are not replaced. Independent whole252x96 pixels fit the unchanged216x36 body crop from native(0,60) to screen(16,112); one current initialized-parent projection binds that shared geometry. The registered planning-v860 formatter supplies36-column, three-row pair-safe wrapping, keeping market prices, clear picture, dream up and best shot together. Forty-eight cold/warm COMMON copies pass with explicit host file-I/O contracts. All24 current font previews were viewed on two sheets. The full35-character1466 continuation retains its final period. '
 'One new ordinary V2284 Copenhagen cold boot runs5401 frames using the inherited five-ship test battery. Original inputs move Gerhard from Survey slot7 to physical slot19, native Finance role20 and visible Purser label. Two complete1460 holds match the source whole12104 numeric selector, independent full bitmap and actual216x36 RGB foreground/blank-ink mask. Only the two assignment bytes change during preview; cancel restores all31. Funds, calendar, owned actor records, flagship and full ship models stay equal across four checkpoints. No new RAM, code, text, health, role, location, timing or RNG fixture or savestate is used. The inherited battery is not earned crew acquisition, statistics, fleet progress or campaign progress. Eight selection/return frames were viewed on one sheet. Other23 records have no new current individual visit claim. '
 'Eight historical V863 holds across1451/1456/1465/1466 are freshly rebound to exact current complete payloads, independent252x36 bitmaps and actual216x36 RGB foreground/blank-ink masks. They cover Claudio\'s dreaming pun, Hodram\'s direct-tactics reflection, Emilio\'s prospective sale question and Manuel\'s full profit-calculation continuation. One labeled historical sheet was viewed. Their disclosed two/three-byte room/occupant fixtures remain historical, with Claudio faction0 and Emilio faction21 unchanged and no earned recruitment claim. The four historical normal-return controls remain historical. No new current Planning, Claudio, Hodram, Emilio or Manuel visit is claimed. '
 'No English, ROM, runtime, geometry, registry, profile, manifest or patch change is required. All24 reconcile through the registered planning_finance_editorial stage; its17 historical revisions are not new revisions. Registered cumulative experimental V2284 remains493 batches and114 accepted layers with its exactly reconstructable clean-input patch. V1492 stays promoted, canonical/clean inputs are unchanged, and every ROM and earlier translation is preserved. Fresh coverage is1495 reread /1495 integrated-reconciled /zero pending. Historical completion remains2143(1498 revised,645 retained), source/prose2259 and incomplete COMMON116. Another648 historical completions require fresh review:647 COMMON plus SC2B294R73. All never-reviewed storylines, shared town/shop dialogue, random scenes and remaining player-facing prose remain in scope. Separate graphics/all18 plaques, SC3B109 classification and the later older-record technical re-audit remain open. The full objective is active. All jobs are terminal.'
)
if __name__=='__main__':
 source=OLD.read_text();start=source.index('SUMMARY=(');end=source.index('\ndef key(',start);source=source[:start]+'SUMMARY='+repr(SUMMARY)+'\n'+source[end:]
 changes={
 'work_completion_v2313':'planning_finance_completion_v2339',
 'translations/work_contextual':'translations/planning_finance_contextual',
 'scripts.work_comments_layout_v843':'scripts.planning_finance_layout_v860',
 'work_fonts_v2309':'planning_finance_fonts_v2336',
 'work_current_verification_v2311/ordinary_current_Shipwright_actual':'finance_current_verification_v2337/ordinary_current_Finance_actual',
 'work_history_v2312':'planning_finance_history_v2338',
 'V2284 Shipwright Doctor24 contextual retentions verified':'V2284 Planning Finance24 contextual retentions verified',
 'IDS=list(range(1386,1410))':'IDS=list(range(1447,1471))',
 'Shared-Shipwright-Doctor-work24-contextual-retentions':'Shared-Planning-Finance24-contextual-retentions',
 '(1410,1410,0)':'(1471,1471,0)',
 "['work_comments_editorial']":"['planning_finance_editorial']",
 "stage='work_comments_editorial'":"stage='planning_finance_editorial'",
 'len(changed)==21':'len(changed)==17',
 '[1387,1395,1398,1405]':'[1451,1456,1465,1466]',
 '1387':'1460',
 'historical_V845_current_bound_holds':'historical_V863_current_bound_holds',
 'work-v843 generated36-column3row pair-safe paragraph':'planning-v860 generated36-column3row pair-safe paragraph',
 'full36_cell1405_last_period_and_odd19_character1398_continuation_complete':'complete1451_dreaming_pun_and_full35_cell1466_continuation_and_period',
 'no_new_current_four_hero_or_Doctor_visits_claim':'no_new_current_four_hero_or_Planning_visits_claim',
 'work_editorial_v2308':'planning_finance_editorial_v2334',
 'work_context_v2307b/successor_provenance.json':'planning_finance_context_v2333/producer_binding.json',
 '1434':'1495',
 '709':'648',
 '708':'647',
 "':778":"':839",
 'next_work_contextual_source_packet_v2306':'next_planning_finance_contextual_source_packet_v2332',
 'resolved_in_v2313':'resolved_in_v2339',
 'work_contextual_v2313':'planning_finance_contextual_v2339',
 'next_remaining_historical_inventory_v2313':'next_remaining_historical_inventory_v2339',
 "l['next_planning_finance_contextual_source_packet_v2332']['resolved_in_v2339']":"l.setdefault('next_planning_finance_contextual_source_packet_v2332',{})['resolved_in_v2339']",
 'V2313 reconciles24 unchanged Shipwright/Doctor work comments':'V2339 reconciles24 unchanged Planning/Finance comments and two speaker metadata notes',
 '## V2313: Shipwright/Doctor24 contextual retentions reconciled':'## V2339: Planning/Finance24 contextual retentions reconciled',
 '# Current editorial handoff - V2306':'# Current editorial handoff - V2330c',
 '# Current editorial handoff - V2313':'# Current editorial handoff - V2339',
 'Current ordinary Shipwright gameplay':'Current ordinary Finance gameplay',
 'historical-only-V845':'historical-only-V863',
 "checkpoint='V2313'":"checkpoint='V2339'",
 'work-comment':'planning-finance-comment',
 'justified_retentions=24':'justified_retentions=24,speaker_metadata_corrections=2',
 'retained_count=24,historical_reconciliation_only':'retained_count=24,speaker_metadata_corrections=[1456,1468],historical_reconciliation_only'
 }
 for old,new in changes.items():assert old in source,old;source=source.replace(old,new)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save('work/analysis/planning_finance_completion_v2339/producer_binding.json',dict(original=str(OLD),original_sha256=sha(OLD.read_bytes()),effective_source_sha256=sha(source.encode()),all_original_source_native_release_registry_and_coverage_assertions_preserved=True,summary_fresh_for_Planning19_Finance20=True,metadata_corrections=[1456,1468],full_goal_complete=False))
