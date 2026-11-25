"""Reconcile24 freshly reread battle Chapel/Planning retentions with registered V2284."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/complete_battle_personal_context_v2386.py')
SUMMARY=(
 'V2411 reconciles24 historical COMMON battle Chapel18/Planning19 comments1645-1668 as fresh, individually justified retentions. Each clean Japanese comment was reread with native role, voice, actual protagonist, battle eligibility and ordinary-role contrasts. These are independent alternatives, not successive conversation turns. Chapel language preserves formal prayers, personal safety wishes, grief, rough preference for fighting, inclusive religious confidence, Rafael\'s named Claudio request, Hodram\'s own fleet, Lil\'s cheerful victory boast and Maria\'s gentle concern. Lord and God retain the Christian register supported by the explicit ordinary Father/Son/Holy Spirit invocation and Bible. No denomination, kinship, rank, divine effect or guaranteed battle result is added. Lost in1652 is explicitly documented as an inference from the unfinished battle-grief thought, not a native casualty count or named death. Claudio\'s familiar form is supported by clean1406; the old supplement\'s reference to1409 was erroneous because1409 concerns Xien. Planning preserves Schemes, naval-battle-only scope, idle-time humor, direct tactics, wishes and requests. It does not extend the limitation to all sailing. Marine Barracks and Strategy Room retain established help terms. Lil1667\'s implied futility is documented as a contextual inference from the role and related alternatives. All24 have new glosses and retention reasons. Existing full-name Hodram Joakim Bergstrom metadata is correct and retained. No English or speaker change is required. '
 'Current clean-exact code and150 direct battle/main battle/ordinary control cases pass for all21 NPCs and four genuinely captured protagonists. Captains are not substituted; actor health and mood are preserved. Twenty-five ordinary comments, including1406, have exact clean/current references as context only with no duplicate credit. The current ARM9 Schemes caption and established term-document hashes are bound. All24 full current native battle selectors, macro expanders, clears, fonts, first/final glyphs, complete words, guards, canaries, bounds and ABI pass under explicitly declared isolated CPU role/assignment/mode and initialized-widget controls. Forty-eight cold/warm COMMON copies pass with explicit host file-I/O contracts. The full252x96 bitmap fits the unchanged216x36 crop from native0,60 to screen16,112. One current ordinary initialized-parent projection binds shared geometry; it is not a current battle GPU visit. The registered battle-chapel-v914 compiler provides generated pair-safe36-column, at-most-three-row wrapping. Initial I1648, all three rows1663, the complete35-character Marine Barracks continuation1666 and full36-character final1665 row survive. Both font sheets were viewed. '
 'Eight historical V916 holds across1648/1654/1663/1666 are freshly bound to all current complete payloads, exact executed selector/Deck/role/macro code, independent bitmaps and actual216x36 RGB ink. They cover Cristina, Emilio and genuine Hodram. Observed0E04 flags and source low-byte4 LDRB instruction are preserved. Four historical returns pass through first Back and resumed battle time; assignments and funds remain unchanged. No world/ship/RNG freeze after resumed combat is asserted. Fourteen offline negative controls reject wrong format-low-byte headers and deleted initial/final glyphs or required continuations. The historical holds and return sheets were viewed. Original cold boots disclose two/three room/occupant bytes and source-terrain-checked coordinate approaches; no identity, health, money, battle-mode, text, code, enemy or outcome replacement is added. These remain historical gameplay with zero new current battle emulator runs or individual family visits. No earned travel, refit, recruitment or battle outcome is claimed. The misnamed native-proof output and failed missing-path authoring attempt are preserved; a successor binds the successful150-case proof. An overbroad authoring substitution mislabeled the Chapel context heading; a successor manuscript corrects role labels while preserving the first draft, all English, glosses, reasons and speakers. '
 'All24 reconcile through registered battle_chapel_planning_editorial and its18 historical revisions, with zero new prose revisions. Registered cumulative experimental V2284 remains493 batches and114 accepted layers with its exactly reconstructable clean-input patch. No ROM, runtime, geometry, registry, profile, manifest or patch change is needed. V1492 stays promoted, canonical/clean inputs are unchanged, and all ROMs and prior translations are preserved. Fresh coverage is1693 reread /1693 integrated-reconciled /zero pending. Historical completion remains2143(1498 revised,645 retained), source/prose2259 and incomplete COMMON116. Another450 historical completions need fresh review:449 COMMON plus SC2B294R73. All never-reviewed storylines, shared town/shop dialogue, random scenes and remaining player-facing prose remain in scope. Separate graphics/all18 plaques, SC3B109 classification and the later older-record technical re-audit remain open. The full objective remains active. All jobs are terminal.'
)
if __name__=='__main__':
 source=OLD.read_text();start=source.index('SUMMARY=(');end=source.index('\ndef historical_key(',start);source=source[:start]+'SUMMARY='+repr(SUMMARY)+'\n'+source[end:]
 changes={
 'battle_personal_completion_v2386':'battle_chapel_planning_completion_v2411',
 'translations/battle_personal_contextual_editorial_manuscript_v1.json':'translations/battle_chapel_planning_contextual_editorial_manuscript_v1b.json',
 'translations/battle_personal_contextual':'translations/battle_chapel_planning_contextual',
 'battle_personal_fonts_v2384/all25':'battle_chapel_planning_fonts_v2409/all24',
 'battle_personal_history_v2385':'battle_chapel_planning_history_v2410',
 'scripts.battle_personal_layout_v892':'scripts.battle_chapel_planning_layout_v914',
 'V2284 Battle personal25 contextual retentions verified':'V2284 Battle chapel planning24 contextual retentions verified',
 'IDS=list(range(1571,1596))':'IDS=list(range(1645,1669))',
 'Shared-Battle-personal25-contextual-retentions':'Shared-Battle-Chapel-Planning24-contextual-retentions',
 '(1595,1595,0)':'(1669,1669,0)',
 "d['speaker_metadata_corrections']==[1572]":"d['speaker_metadata_corrections']==[]",
 "d['fresh_hobby_context']":"d['fresh_ordinary_supplement']",
 "d['fresh_hobby_context_sha256']":"d['fresh_ordinary_supplement_sha256']",
 'all125_original_selector_and_discriminating_control_cases':'all150_battle_direct_main_and_ordinary_control_cases',
 '==125':'==150',
 'all25_complete_native_cases':'all24_complete_native_cases',
 'all50_native_cold_warm_copies':'all48_native_cold_warm_copies',
 '==50':'==48',
 'all25_native_battle_working':'all24_native_battle_working',
 "len(fonts['review_sheets'])==3":"len(fonts['review_sheets'])==2",
 "len(history['historical_holds'])==6":"len(history['historical_holds'])==8",
 '[1572,1577,1590]':'[1648,1654,1663,1666]',
 "len(history['scoped_historical_battle_returns_freshly_rechecked'])==3":"len(history['scoped_historical_battle_returns_freshly_rechecked'])==4",
 'five_negative_controls_current_reexecution_on_offline_clones':'fourteen_negative_controls_current_reexecution_on_offline_clones',
 "len(history['fourteen_negative_controls_current_reexecution_on_offline_clones'])==5":"len(history['fourteen_negative_controls_current_reexecution_on_offline_clones'])==14",
 "assert history['historical_ordinary_Carlo_control_current_bound']['frame']==36800 and ":'assert ',
 "['battle_personal_editorial']":"['battle_chapel_planning_editorial']",
 "stage='battle_personal_editorial'":"stage='battle_chapel_planning_editorial'",
 'historical_V893':'historical_V916',
 'battle-personal-v892':'battle-chapel-v914',
 '# Current editorial handoff - V2378':'# Current editorial handoff - V2404',
 'all25_current_native_previews_on3_sheets_viewed':'all24_current_native_previews_on2_sheets_viewed',
 'historical6_battle_holds_on1_labeled_sheet_viewed':'historical8_battle_holds_on1_labeled_sheet_viewed',
 'historical3_returns_and_ordinary_Carlo_control_on1_labeled_sheet_viewed':'historical4_returns_on1_labeled_sheet_viewed',
 'Carlo_odd19_first_row_leading_N_and_full_nodding_direction_complete':'I1648_three_rows1663_and_complete_Marine_Barracks1666_preserved',
 'source_music_break_drink_book_hobbies_and_flowers_preserved':'prayers_battle_only_tactics_nickname_and_documented_inferences_preserved',
 'battle_personal_editorial_v2383':'battle_chapel_planning_editorial_v2408b',
 'battle_personal_preflight_v2380/next25_preflight':'battle_chapel_planning_handoff_v2404/next24_preflight',
 'scripts/rebind_battle_personal_history_v2385.py':'scripts/rebind_battle_chapel_planning_history_v2410.py',
 'speaker_metadata_corrections=[1572]':'speaker_metadata_corrections=[]',
 'historical_actual_holds=6':'historical_actual_holds=8',
 'historical_returns_current_rechecked=3':'historical_returns_current_rechecked=4',
 'historical_ordinary_context_ID=1380,':'ordinary_context_reference_records=25,',
 'current_negative_control_cases=5':'current_negative_control_cases=14',
 'fresh_pass_records_explicitly_reread=1620':'fresh_pass_records_explicitly_reread=1693',
 'fresh_pass_records_integrated=1620':'fresh_pass_records_integrated=1693',
 '523':'450','522':'449','1620 file-qualified':'1693 file-qualified',
 'speaker_metadata_corrections=1':'speaker_metadata_corrections=0',
 'historical_actual_IDs=3':'historical_actual_IDs=4',
 'historical_current_pixel_rechecks=6':'historical_current_pixel_rechecks=8',
 'historical_ordinary_context_controls=1':'historical_ordinary_context_controls=0',
 'historical_returns_rechecked=3':'historical_returns_rechecked=4',
 'negative_controls=5':'negative_controls=14',
 'next_battle_personal_contextual_source_packet_v2380':'next_battle_chapel_planning_contextual_source_packet_v2404',
 'resolved_in_v2386':'resolved_in_v2411',
 'battle_personal_contextual_v2386':'battle_chapel_planning_contextual_v2411',
 'V2386 reconciles25 unchanged battle-personal comments and one speaker note':'V2411 reconciles24 unchanged battle Chapel/Planning comments',
 '==1620 and Counter':'==1693 and Counter',"':964":"':1037",
 'next_remaining_historical_inventory_v2386':'next_remaining_historical_inventory_v2411',
 '## V2386: Battle personal25 contextual retentions reconciled':'## V2411: Battle Chapel/Planning24 contextual retentions reconciled',
 '# Current editorial handoff - V2386':'# Current editorial handoff - V2411',
 'historical-only-V893-battle-ordinary-and-returns':'historical-only-V916-battle-and-returns',
 'ordinary1380_context_only=True,':'',"checkpoint='V2386'":"checkpoint='V2411'",
 'fresh_integrated=1620':'fresh_integrated=1693','speaker_metadata_corrected=1':'speaker_metadata_corrected=0',
 'all25_current_native_battle_font_proof':'all24_current_native_battle_font_proof',
 'all5_review_sheets_viewed':'all4_review_sheets_viewed','all5_sheets_viewed':'all4_sheets_viewed',
 'len(images)==5':'len(images)==4','guide_images=5':'guide_images=4',
 'current_native_copies=50':'current_native_copies=48','native_copies=50':'native_copies=48',
 'current_native_battle_fonts=25':'current_native_battle_fonts=24','native_fonts=25':'native_fonts=24',
 '25complete-current':'24complete-current','==25':'==24','records=25':'records=24','retained_count=25':'retained_count=24','justified_retentions=25':'justified_retentions=24','fresh_reconciliations=25':'fresh_reconciliations=24','retained=25':'retained=24',
 'paths=[DOC,NOTES,FONTS,HISTORY,RELEASE,visual,contextpath,hobby,':"paths=[DOC,NOTES,FONTS,HISTORY,RELEASE,visual,contextpath,hobby,Path('work/analysis/battle_chapel_planning_metadata_v2408c/context_metadata_corrections.json'),Path(d['context_metadata_successor_of']),"
 }
 for a,b in changes.items():assert a in source,a;source=source.replace(a,b)
 import ast
 ast.parse(source)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save('work/analysis/battle_chapel_planning_completion_v2411/producer_binding.json',dict(original=str(OLD),original_sha256=sha(OLD.read_bytes()),effective_source_sha256=sha(source.encode()),all_source_native_release_registry_and_coverage_assertions_preserved=True,corrected_context_metadata_successor_bound=True,full_goal_complete=False))
