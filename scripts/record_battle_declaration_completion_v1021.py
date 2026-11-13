"""Close the22-entry family after actual gates; keep the full editorial goal active."""
from copy import deepcopy
from collections import Counter
from pathlib import Path
from shutil import copy2
import struct

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.battle_declaration_editorial import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.battle_declaration_layout_v996 import compiled
from scripts.prepare_work_comments_v842 import reference
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/battle_declaration_v1021')
ROM=Path('out/all_routes_combined_v997_candidate.nds')
ACTUAL=Path('work/analysis/battle_declaration_v1020/actual_gameplay_verification.json')
DOC=Path('docs/battle_declaration_v1021_completion.md')
FINAL=Path('translations/battle_declaration_editorial_final_review_v1.json')
IDS=list(range(1889,1911))


def main():
    assert ROOT.exists() and not FINAL.exists() and not DOC.exists()
    assert not (ROOT/'registered_release_completion.json').exists()
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger=read(ledger_path)
    assert (ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],
            ledger['retained_wordings_editorially_completed'],ledger['records_with_source_and_prose_pass'])==(1174,878,296,1199)
    assert ledger['current_integrated_candidate']['sha256']=='bac5998ad942868c85d51d2a3f589e43ffced4dbc93659de7cc659a066c17078'
    assert ledger['reviewed_but_incomplete_COMMON_IDs']==[750,751,752,*IDS]
    before=deepcopy(ledger)
    save(ROOT/'editorial_ledger_before_completion.json',before)
    actual=read(ACTUAL);release=read('work/analysis/battle_declaration_v997b/registered_release_verification.json')
    startup=read('work/analysis/battle_declaration_v997b/ordinary_startup_verification.json')
    visual=read(ROOT/'completion_visual_review.json')
    assert actual['all_three_source_families_representatively_verified'] and visual['all7_whole_frames_visually_reviewed']
    assert len(actual['complete_actual_modal_holds'])==7 and len(actual['all_exact_fixture_replays'])==16
    assert len(actual['cancellations'])==3 and len(actual['known_and_unknown_Yes_paths'])==2
    assert actual['ready_dismissal_enters_original_battle_without_extra_page']
    rom=NdsImage.open(ROM);arm=rom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4')
    digest=sha(ROM.read_bytes())
    assert digest==actual['candidate_sha256']==release['candidate_sha256']==startup['candidate_sha256']
    assert sha(ROM.with_suffix('.xdelta').read_bytes())==release['patch_sha256']
    assert sha(Path(release['exact_clean_input_patch_reconstruction']).read_bytes())==digest
    assert release['complete_reconstruction_byte_exact'] and startup['all8_complete_startup_title_NewGame_frames_exact']
    assert release['all3646_unselected_message_strings_and_user676_677_repair_exact']
    clean=NdsImage.open('work/clean.nds');source_arm=clean.read_file('/__arm9__.bin')
    assert sha(Path('work/clean.nds').read_bytes())==before['source_pins']['japanese']['sha256']
    canonical=Path('out/raphael_natural_v2_accepted_base.nds')
    assert sha(canonical.read_bytes())=='3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    current=current_entries(common,arm)
    japanese=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),source_arm)
    manuscript=Path('translations/battle_declaration_editorial_manuscript_v3.json');doc=read(manuscript)
    assert Counter(r['editorial_decision'] for r in doc['records'])=={'revise':13,'retain':9}
    native_path=Path('work/analysis/battle_declaration_v995b/native_font_proof.json');native=read(native_path)
    assert len(native['cases'])==176 and read('work/analysis/battle_declaration_v996/visual_review.json')['all176_complete_previews_visually_reviewed_via8_full_canvas_sheets']
    rows=[]
    for original in doc['records']:
        row=deepcopy(original);n=row['message_id']
        assert n in IDS and japanese[n].text.hex()==row['source_hex']
        assert current[n].text==compiled(row)==bytes.fromhex(row['compiled_hex'])
        assert all(row['review'].values())
        row.update(before_reference=row['current_reference'],before_text_hex=row['current_text_hex'],
            current_reference=reference(current[n]),current_text_hex=current[n].text.hex(),
            completed_candidate_reference=str(ROM),
            decision='revised-and-integrated' if row['editorial_decision']=='revise' else 'retained-and-editorially-reviewed',
            complete_native_font_cases=[c for c in native['cases'] if c['message_id']==n],
            actual_holds=[h for h in actual['complete_actual_modal_holds'] if h['message_ID']==n],
            all_source_native_copy_font_and_family_actual_gates_pass=True,
            individual_actual_activation_not_claimed_when_actual_holds_empty=True)
        rows.append(row)
    assert sorted(r['message_id'] for r in rows)==IDS
    existing={n for f in ledger['completed_editorial_families'] for n in f.get('native_message_IDs',[])}
    assert not existing.intersection(IDS)
    supplement=ROOT/'source_context_supplement.json'
    source_spans=((0x2C1C4,0x2C1D8),(0x705F8,0x706A4),(0x8205C,0x820D8),(0x82B30,0x82B38))
    for lo,hi in source_spans:assert arm[lo:hi]==source_arm[lo:hi]
    save(supplement,{'candidate_sha256':digest,'clean_ROM_sha256':before['source_pins']['japanese']['sha256'],
        'exact_original_guard_spans':[{'start':a+0x02000000,'end':b+0x02000000,'sha256':sha(arm[a:b])} for a,b in source_spans],
        'fleet_position_getter_0202C1C4_reads_object34_38':True,
        'original_targeting_reads_cached_fleet_position_separately_from_live_ship_position':True,
        '705F8_unknown_input_flag_uses_original_empty_Lookout_and_state7_checks':True,
        'original_role7_maps_to_room_type1_Lookout':True,
        'qualified_Manuel23_observation_fixture_changes_only_occupants_no_ability_or_identity':True,
        'company9_default_fleet9_is_not_spawned_roaming_fleet28':True,
        'visible_fixture_binds_original_company_and_native_ship_to_roaming_fleet28':True,
        '367C8_terminology_erratum':'Original fallback speech actor getter, not a guarantee of the story captain. Prior dispatch proofs used the original returned actor and remain valid; genuine captain1 was never replaced.',
        'rejected_trials':'V1000 offline actor-pointer/ID assertion rejected before live application. Early Speyer proximity activates the original tutorial; stale cached coordinates and default faction fleet records do not prove selectable targets. Early already-war fixtures allow automatic combat before manual selection; those captures receive no readiness-text credit. The final readiness fixture applies only inside paused target selection before original manual activation.',
        'all_failed_or_detour_files_preserved_and_no_ROM_defect_or_scene_credit_inferred':True})
    scope=('Three terminal V997 cold boots,with seven whole modal holds for Janus unidentified1904,Emilio unidentified1909,Janus named1897/Pasha,and Emilio readiness1895. All22 receive source/context/prose and176 full native canvases;the remaining18 numeric IDs have family sample coverage rather than individual actual activations. Exact replay binds16 disclosed location,First Mate,qualified Lookout,relation and leader-branch fixtures to all4MiB RAM deltas. Three No paths preserve source companies,actors,goods,items,towns,own ship models,cash and clock and return to Declare War selection. Known and unknown Yes reach the original opponent response and native battle/duel state;readiness dismisses into original battle without an extra page. No savestate,numeric text/renderer injection,earned recruitment,travel,story unlock,victory,full-route or hardware claim.')
    save(FINAL,{'format':'dk4-editorial-family-final-review-v1','status':'22-source-context-prose-native-and-representative-gameplay-verified',
        'candidate':str(ROM),'candidate_sha256':digest,'source_manuscript':str(manuscript),'source_manuscript_sha256':sha(manuscript.read_bytes()),
        'registered_release_proof':'work/analysis/battle_declaration_v997b/registered_release_verification.json',
        'actual_gameplay_proof':str(ACTUAL),'native_font_proof':str(native_path),'source_context_supplement':str(supplement),
        'completion_visual_review':str(ROOT/'completion_visual_review.json'),'actual_scope':scope,'records':rows,
        'full_editorial_goal_complete':False,'separate_graphics_goal_complete':False})
    family={'id':'Shared-FirstMate-battle-readiness-declarations1889-1910','native_message_IDs':IDS,'records':rows,
        'final_review':str(FINAL),'documentation':str(DOC),'actual_verification_scope':scope}
    candidate=deepcopy(ledger['pending_registered_battle_declaration_candidate'])
    candidate.update(status='experimental-battle-declaration22-source-native-and-representative-gameplay-verified',details=str(DOC))
    ledger['previous_current_integrated_candidate_V987']=deepcopy(ledger['current_integrated_candidate'])
    ledger['native_relocation_reference_before_battle_declaration_completion']=deepcopy(ledger['current_native_relocation_reference'])
    ledger['current_integrated_candidate']=candidate;ledger['source_pins']['current']=deepcopy(candidate)
    ledger['current_native_relocation_reference']={'candidate':str(ROM),'COMMON_sha256':sha(common),'ARM9_sha256':sha(arm),
        'parser':'dk4tool.patch.battle_declaration_editorial.current_entries',
        'release_config':'translations/battle_declaration_editorial_release_v1.json',
        'source_locked_directory_and_all_other_strings_preserved':True,'requires_guarded_single8192_cache_policy':True}
    ledger['completed_editorial_families'].append(family)
    ledger['coverage_units'].append({'id':family['id'],'status':'complete-with-source-native-and-representative-gameplay-evidence',
        'native_message_IDs':IDS,'final_review':str(FINAL),'actual_proof':str(ACTUAL),'full_goal_complete':False})
    ledger['records_editorially_completed']+=22;ledger['records_revised_and_integrated']+=13
    ledger['retained_wordings_editorially_completed']+=9
    ledger['completed_editorial_record_counts_by_file']['/COMMON/MESFILE.DK4']+=22
    ledger['reviewed_but_incomplete_COMMON_IDs']=[750,751,752]
    ledger['active_source_prose_drafts']={'native_message_IDs':[750,751,752],
        'manuscripts':['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json'],
        'status':'three-older-source-prose-drafts-context-and-native-actual-gates-still-pending',
        'note':'These three reviewed drafts are not the full remaining shared,route,other player prose or raw-source scope.'}
    ledger['pending_registered_battle_declaration_candidate']=deepcopy(candidate)
    ledger['next_battle_declaration_actual_verification'].update(status='completed-representative-three-family-gates',
        actual_proof=str(ACTUAL),completion=str(DOC),no_live_process_left_by_this_checkpoint=True)
    ledger['battle_declaration_v1021']={'status':'22-source-context-prose-native-and-representative-actual-verified',
        'completed_entries_added':22,'revised':13,'retained':9,'native_message_IDs':IDS,
        'final_review':str(FINAL),'documentation':str(DOC),'proof':str(ROOT/'registered_release_completion.json'),
        'canonical_not_promoted':True}
    # Preserve the frozen preliminary inventory; add exact source/current references in a successor.
    next_packet=read('work/analysis/reinforcement_sniping_v1014/source_inventory.json')
    for row in next_packet['records']:
        n=row['message_id'];assert japanese[n].text.hex()==row['clean_hex'] and current[n].text.hex()==row['current_hex']
        row.update(source_reference=reference(japanese[n]),current_reference=reference(current[n]))
    next_packet.update(predecessor='work/analysis/reinforcement_sniping_v1014/source_inventory.json',
        predecessor_sha256=sha(Path('work/analysis/reinforcement_sniping_v1014/source_inventory.json').read_bytes()),
        original_callers_argument_objects_and_review_gates_still_pending=True,source_prose_reviews_added=0)
    next_path=ROOT/'next_reinforcement_sniping_source_packet.json';save(next_path,next_packet)
    ledger['next_reinforcement_sniping_source_packet']={'proof':str(next_path),'native_message_IDs':list(range(1911,1931)),
        'status':'exact-source-current-and-three-voice-tables-inventoried-context-prose-native-and-actual-pending',
        'source_prose_reviews_added':0,'completed_entries_added':0}
    ledger['formatting_watchlist']['latest_user_screenshot_recheck']={'proof':'work/analysis/battle_declaration_v997b/registered_release_verification.json',
        'candidate':str(ROM),'exact_repaired676_677_bytes_preserved':True,'new_actual_shop_activation_claimed':False}
    checkpoint=('V1021 closes22 First Mate battle/readiness/declaration entries1889-1910:13 revised,9 retained. Registered V997 and exact clean patch now have176 complete native-font cases,eight ordinary startup frames,three terminal actual scene runs,seven complete modal holds,16 exact fixture replays,three No returns and both named/unidentified Yes paths plus readiness dismissal. Literal I at1909 generated line end is actual-display verified. Totals1196 complete(891 revised,305 retained),1199 source/prose;older750-752 remain pending. Next1911-1930 reinforcement/covering-fire/admiral-shot inventory receives no review credit. Full shared/route/player prose/raw coverage,separate graphics/all18 plaques,Samwell header and later older-record re-audit remain open;goal active,canonical unchanged.')
    ledger['latest_checkpoint']=checkpoint
    ledger['research_checkpoints'].append({'id':'V1021-battle-declaration22-completed','proof':str(ROOT/'registered_release_completion.json'),
        'completed_entries_added':22,'source_prose_reviews_added':0,
        'previous_goal_turn_classification':'no progress toward new goal coverage: answered a formatting-status question using the earlier shop fix and existing preservation evidence',
        'this_goal_turn_classification':'progress:completed representative actual family gates,exact source-state fixture replays,all22 final records,and next20 exact source inventory',
        'full_goal_complete':False})
    assert ledger['approved_name_roles']==before['approved_name_roles'] and ledger['unresolved_graphics_work']==before['unresolved_graphics_work']
    assert (ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(1196,891,305)
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==1199
    assert len({n for f in ledger['completed_editorial_families'] for n in f.get('native_message_IDs',[])})==1195
    assert not ledger['full_goal_complete'] and ledger['goal_status']=='active'
    save(ledger_path,ledger);save('out/editorial_review_latest.json',candidate)
    text='''# V1021: battle declarations and readiness completed

COMMON1889-1910 now complete source,context,natural American English,native layout/copy and representative actual-scene gates:13 revised and9 retained wordings. Total1196 entries complete(891 revised,305 retained),1199 source/prose reviewed. This closes this family;the full editorial goal is active.

## Actual verification

Three terminal V997 cold boots provide seven full modal holds:Janus unidentified1904,Emilio unidentified1909,Janus named1897 with complete Pasha name,and Emilio readiness1895. Complete228x64 native/independent-font canvases match actual RGB,including blank ink regions,uniform left margins and every first/last letter. The literal I at the end of1909's first generated row and the following t are complete. All176 native cases and previous eight ordinary title/New Game frames remain pinned. Eighteen other numeric messages have complete source/native proof and family gameplay sampling,not individual actual activations.

Three No paths return to original Declare War selection with all20 company records,actors,towns,items,goods,own ship models,cash and clock unchanged. Both named and unidentified Yes paths show the original opponent reply,then source relation2 and original battle/duel context. Unknown acceptance also raises the original leader byte26 from0 to1. A separate late already-war fixture yields the ready announcement,whose normal dismissal enters battle without another page. No battle outcome or victory is claimed.

## Declared disposable fixtures and research corrections

Sixteen exact replays reproduce every declared fixture's complete4MiB before/after RAM and receipt. Source/disposable battery donors stay byte-exact. Fixtures cover location,First Mate,qualified Lookout,relationship and leader-branch state;they do not replace the captain,actor identity,renderer,text selector or outcomes. Qualified Manuel23 occupies the real Lookout;the original705F8 derives whether fleets are identified. A location fixture keeps the original fleet34/38 cached position consistent with live ship coordinates and approaches the actual spawned Pasha fleet28. The default faction fleet9 is a different object.

Early trials are preserved without credit:an offline actor-pointer versus numeric-ID assumption failed before live application;Speyer proximity activated Hodram's original tutorial;stale cached positions and inactive default fleet records did not prove selection;early war state allowed automatic combat before the readiness sample. The final readiness state is applied inside paused original selection. Original367C8 is a fallback speech actor getter,not a guarantee of story-captain identity;prior dispatch results used its real returned actor and remain valid. No ROM defect is inferred from these fixture failures.

## Release and coverage

The existing registered combined V997 is unchanged:all471 batches114 accepted layers,exact clean-input xdelta,7336 native copies178 cache sequences and owned fixed runtime footprints remain verified. No section,pool,cache,arena or123040-byte staged payload grows. Graphics,routes,names,fonts,ARM7/overlays,3646 other messages and repaired shop676/677 remain exact to V987. No new actual shop visit is claimed. Canonical promotion still requires explicit human cold-boot acceptance.

ROM:`out/all_routes_combined_v997_candidate.nds`,SHA256`0093915adb53c7c1034b696d54bf897079908aa598ea39bdced849107983660d`.
Patch:`out/all_routes_combined_v997_candidate.xdelta`,SHA256`4fcffaf2250277ed71d696bcad5c391ca3448a7f36d6aba3d3925ebe6ee99565`.

Next1911-1930 source/current records and three voice tables are inventoried;covering-fire specificity,compressed admiral-shot notices,old manual padding and substitution-object meaning require review. They receive zero source/prose or completion credit so far. Older750-752,all wider shared/route/player prose and raw native-source coverage,Samwell header,separate graphics/all18 plaques and the later older-record re-audit remain open.

Actual proof:`work/analysis/battle_declaration_v1020/actual_gameplay_verification.json`. Final review:`translations/battle_declaration_editorial_final_review_v1.json`. Seven full-frame visual sheet and final gate record are under`work/analysis/battle_declaration_v1021`. Evidence/guide candidates are retained on E. No savestate,earned progression,full-route or hardware verification claim is made.
'''
    DOC.write_text(text,encoding='utf-8')
    for p in map(Path,('docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md','docs/known_issues.md')):
        with p.open('a',encoding='utf-8') as f:f.write('\n\n## V1021: battle declarations and readiness completed\n\n'+checkpoint+' See [V1021 completion](battle_declaration_v1021_completion.md).\n')
    retention=Path('work/rom_retention/20261021T0513512620662Z.json');plan=read(retention)
    assert len(plan['roms'])==217 and all(Path(r['path']).exists() for r in plan['roms'])
    assert sha(Path('scripts/prune_generated_roms.ps1').read_bytes())=='aacaca07b50f1bafcfc5bb8579b609b0be2a8e79e3107f336405ba370a435f6f'
    save(ROOT/'registered_release_completion.json',{'candidate':candidate,'final_review':str(FINAL),'final_review_sha256':sha(FINAL.read_bytes()),
        'gameplay_proof':str(ACTUAL),'gameplay_proof_sha256':sha(ACTUAL.read_bytes()),
        'source_context_supplement':str(supplement),'source_context_supplement_sha256':sha(supplement.read_bytes()),
        'completed_entries_added':22,'revised':13,'retained':9,'records_editorially_completed':1196,
        'records_with_source_and_prose_pass':1199,'old750_752_still_incomplete':True,
        'new20_inventory_credit':0,'canonical_and_original_saves_unchanged':True,
        'retention_preview':str(retention),'retention_preview_only_no_ApplyPlan_or_deletion':True,
        'all217_ROMs_still_exist':True,'prior_auto_review_rejection_resolved_by_reading_default_preview_branch':True,
        'all_testing_processes_terminal_no_live_handle_left':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    guide=Path('E:/Rota Nova translations/Screenshots/Guide candidates/V1021 Battle declarations')
    archive=Path('E:/Rota Nova translations/Editorial review/V1021 Battle declaration gameplay')
    assert not guide.exists() and not archive.exists();guide.mkdir(parents=True)
    sources=[(actual['complete_actual_modal_holds'][0],'01_Unidentified_Janus.png'),
             (actual['complete_actual_modal_holds'][1],'02_Unidentified_Emilio.png'),
             (actual['complete_actual_modal_holds'][3],'03_Declare_War_Pasha.png'),
             (actual['complete_actual_modal_holds'][5],'04_Battle_Readiness_Emilio.png')]
    shots=[]
    for row,name in sources:
        p=Path(row['capture']);target=guide/name;copy2(p,target);assert sha(target.read_bytes())==row['capture_sha256']
        shots.append({'source':str(p),'target':str(target),'sha256':sha(target.read_bytes()),'unmodified_whole_native_frame':True})
    save(guide/'provenance.json',{'candidate_sha256':digest,'actual_proof':str(ACTUAL),'actual_proof_sha256':sha(ACTUAL.read_bytes()),
        'screenshots':shots,'disposable_crew_location_relationship_fixtures_disclosed':True,
        'earned_progression_or_guide_publication_not_claimed':True})
    copied=[]
    files=[FINAL,DOC,ledger_path,Path('out/editorial_review_latest.json'),ACTUAL,Path(__file__),
           Path('scripts/verify_battle_declaration_gameplay_v1020.py'),Path('scripts/verify_battle_declaration_modal_v1016.py')]
    files+=list(ROOT.glob('*.json'))+list(ROOT.glob('*.png'))
    files+=list(Path('scripts').glob('native_battle_declaration*1*.py'))
    files+=list(Path('scripts').glob('run_battle_declaration_live_v10*.py'))
    for p in dict.fromkeys(files):
        target=archive/p.absolute().relative_to(Path.cwd());target.parent.mkdir(parents=True,exist_ok=True);copy2(p,target)
        assert p.read_bytes()==target.read_bytes();copied.append({'source':str(p),'archive':str(target),'sha256':sha(target.read_bytes())})
    save(ROOT/'archive_manifest.json',{'files':copied,'all_hashes_verified':True,'no_ROM_or_save_duplicated':True,
        'guide_provenance':str(guide/'provenance.json')})
    print('22 complete:1196 total,891 revised305 retained;1199 source/prose;next20 inventory only. V997 latest experimental,exact patch/three actual families verified;full goal active.',flush=True)


if __name__=='__main__':main()
