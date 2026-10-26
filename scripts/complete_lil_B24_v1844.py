"""Close13 individually observed lines only after registered patch/startup gates."""
from copy import deepcopy
import os
from pathlib import Path
from shutil import copy2
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B24_completion_v1844')
FINAL=Path('translations/lil_trade_routes_officers_final_review_v1.json')
DOC=Path('translations/lil_trade_routes_officers_editorial_manuscript_v4.json')
MAP=Path('translations/lil_trade_routes_editorial_relocation_map_v1.json')
REL=Path('work/analysis/lil_B24_release_v1840')
ACTUAL=Path('work/analysis/lil_B24_actual_v1838/complete_B24_scene_and_two_coordinate_fixture_audit.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
HANDOFF=Path('docs/editorial_handoff_current.md')
ROM=Path('out/all_routes_combined_v1841_candidate.nds')
GUIDE=Path('E:/Rota Nova translations/Guide screenshots/V1841 Lil trade routes and officers verified')

if __name__=='__main__':
    assert not ROOT.exists()and not FINAL.exists()and not GUIDE.exists()
    doc,mapping,release,startup,actual=map(read,(DOC,MAP,REL/'registered_release_verification.json',
        REL/'ordinary_startup_verification.json',ACTUAL))
    digest=sha(ROM.read_bytes())
    assert digest==release['candidate_sha256']==startup['candidate_sha256']==actual['candidate_sha256']
    assert release['complete_reconstruction_byte_exact']and release['registered_ROM_whole_file_byte_exact_to_actual_scene_research_ROM']
    assert startup['all8_complete_startup_title_NewGame_frames_exact']and startup['no_battery_save_savestate_or_fixtures']
    assert actual['all13_speeches26_actual_complete_native_independent_holds']and actual['all_readonly_callbacks_zero_errors_mismatches_host_restored']
    assert read(doc['actual_visual_review'])['both_actual_sheets_all13_panels_and_normal_Amsterdam_return_actually_viewed']
    assert sha(ROM.with_suffix('.manifest.json').read_bytes())==release['manifest_sha256']
    assert sha(Path(release['patch']).read_bytes())==release['patch_sha256']
    assert mapping['external_references_complete']
    block=IlnkContainer.parse(NdsImage.open(ROM).read_file('/data/SC2.DK4')).blocks[24]
    clean=IlnkContainer.parse(NdsImage.open('work/clean.nds').read_file('/data/SC2.DK4')).blocks[24]
    refs={r['id']:r for r in mapping['records']};observed={r['id']:r for r in actual['speeches']};rows=[]
    for draft in doc['records']:
        row=deepcopy(draft);ref=refs[row['id']];at=ref['new_offset'];raw=bytes.fromhex(ref['encoded_hex'])
        assert block[at:at+len(raw)]==raw and block[at+len(raw)]==0
        old=bytes.fromhex(row['source_hex']);ja=row['source_reference']['offset']
        assert clean[ja:ja+len(old)]==old and all(row['review'].values())
        row.update(previous_current_reference=row['current_reference'],previous_current_text_hex=row['current_text_hex'],
            current_reference={'offset':at,'bytes':len(raw),'header_offset':at-5,'record_index':block[:at].count(b'\0')},
            current_text_hex=raw.hex(),current_English=row['english'],completed_candidate_reference=str(ROM),
            completed_candidate_sha256=digest,reference_map=str(MAP),actual_proof=str(ACTUAL),
            individually_activated_in_current_build=True,
            actual_holds=observed[row['id']]['two_complete_actual_holds'],
            decision='revised-and-integrated'if row['editorial_decision']=='revise'else'retained-with-justification',
            status='complete-source-native-and-individual-original-gameplay')
        if row['editorial_decision']=='retain-wording':
            row['retained_wording_justification']='Huh. naturally preserves Lil\'s brief thoughtful ふーん response after the explanation; no demand for repetition or extra fact is added.'
        rows.append(row)
    assert len(rows)==13 and sum(r['editorial_decision']=='revise'for r in rows)==12
    ids={r['id']for r in rows};raw_ledger=LEDGER.read_bytes();ledger=read(LEDGER);before=deepcopy(ledger)
    assert(ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],
        ledger['retained_wordings_editorially_completed'],ledger['records_with_source_and_prose_pass'])==(1516,1146,370,1645)
    assert ids==set(ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4'])
    ROOT.mkdir(parents=True);(ROOT/'ledger_before.json').write_bytes(raw_ledger);(ROOT/'handoff_before.md').write_bytes(HANDOFF.read_bytes())
    scope=('All 13 Lil trade-route/officer speeches in SC2 B24 are complete:12 revised and one justified retained response. '
        'The clean Japanese and neighbors support the one-percent-per-town rule,officer/sailor distinction,Istanbul,hearsay and Camille\'s praise. '
        'All 13 complete native/independent font planes and104 original macro/catalog cases pass. '
        'The game naturally activates the scene after normal Amsterdam docking;all13 speeches were individually visited with26 full matching holds,all17 commands returned,and normal Amsterdam town UI resumed at47650. '
        'Two disclosed fixtures each own16 coordinate bytes only;all4MiB footprints,inputs,captures and read-only observer boundaries/host restoration pass. '
        'No battery save,savestate,RNG,event,message,health,actor or outcome override;no earned-travel,whole-route or hardware claim. '
        'Registered V1841 is whole-file identical to the observed research ROM. Only SC2 B24 grows136bytes relative to V1807;335 other blocks,every other ROM file/component,fonts,graphics,COMMON and123040 staged bytes remain exact. '
        'All478 manifest batches,114 accepted layers,previous profiles,seven invalid-release controls,eight fresh fixture-free startup frames and exact clean-input patch reconstruction pass. '
        'Full editorial goal remains active:116 reviewed-incomplete COMMON entries and broader untouched shared/routes/player prose remain. Separate graphics/all18 plaques and later older-record re-audit remain unfinished. V1492 stays promoted.')
    visual=ROOT/'registered_gameplay_and_visual_reconciliation.json'
    save(visual,{'registered_ROM_equals_entire_actual_research_ROM':True,'all13_actual_panels_both_sheets_and_normal_return_viewed':True,
        'all8_current_startup_controls_viewed':True,'no_completion_claim_for_other_prose_graphics_or_hardware':True,
        'proofs':{str(p):sha(p.read_bytes())for p in(DOC,MAP,ACTUAL,REL/'registered_release_verification.json',REL/'ordinary_startup_verification.json')},
        'full_goal_complete':False})
    save(FINAL,{'format':'dk4-editorial-final-family-review-v1','family':'Lil-trade-routes-officers13','file_path':'/data/SC2.DK4',
        'blocks':[24],'record_IDs':sorted(ids),'records':rows,'revised_count':12,'retained_count':1,
        'candidate':str(ROM),'candidate_sha256':digest,'actual_scope':scope,'reference_map':str(MAP),
        'source_native_and_all13_individual_actual_gates_passed':True,'final_proof':str(visual),'full_goal_complete':False})
    family='Lil-trade-routes-officers13'
    ledger['completed_editorial_families'].append({'id':family,'file_path':'/data/SC2.DK4','blocks':[24],
        'record_IDs':sorted(ids),'final_review':str(FINAL),'revised_count':12,'retained_count':1,
        'actual_verification_scope':scope,'records':rows})
    unit=next(u for u in ledger['coverage_units']if u['id']=='Lil-B24-trade-routes-officers13-source-prose')
    assert set(unit['record_IDs'])==ids
    unit.update(status='superseded-by-complete-family',completed_family=family,final_review=str(FINAL))
    ledger['coverage_units'].append({'id':family,'file_path':'/data/SC2.DK4','blocks':[24],
        'record_IDs':sorted(ids),'status':'complete-source-native-and-individual-original-gameplay',
        'final_review':str(FINAL),'actual_proofs':[str(ACTUAL),str(visual)],'completed_entries_added':13,'full_goal_complete':False})
    ledger['records_editorially_completed']+=13;ledger['records_revised_and_integrated']+=12
    ledger['retained_wordings_editorially_completed']+=1;ledger['completed_editorial_record_counts_by_file']['/data/SC2.DK4']+=13
    for file,pending in ledger['reviewed_but_incomplete_route_record_IDs'].items():
        ledger['reviewed_but_incomplete_route_record_IDs'][file]=[i for i in pending if i not in ids]
    drafts=ledger['active_source_prose_drafts']
    for name,pending in drafts['route_record_subsets_pending'].items():drafts['route_record_subsets_pending'][name]=[i for i in pending if i not in ids]
    drafts.update(status='116-reviewed-COMMON-and-broader-prose-open',note='Lil opening49,lessons64 andtrade-route/officer scene13 complete. Broader all-routes/player prose remains open.')
    ledger.setdefault('integrated_candidate_reference_history',[]).append(deepcopy(ledger['current_integrated_candidate']))
    ledger['current_integrated_candidate']={'path':str(ROM),'sha256':digest,'profile':release['profile'],
        'MESFILE_sha256':release['COMMON_sha256'],'ARM9_sha256':release['ARM9_sha256'],'SC2_sha256':release['SC2_sha256'],
        'patch':release['patch'],'patch_sha256':release['patch_sha256'],'manifest':str(ROM.with_suffix('.manifest.json')),
        'status':'experimental-verified-editorial-checkpoint-not-promoted','details':scope,'full_goal_complete':False}
    ledger.setdefault('native_completed_reference_history',[]).append(deepcopy(ledger['current_native_relocation_reference']))
    ledger['current_native_relocation_reference'].update(candidate=str(ROM),candidate_sha256=digest,
        COMMON_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'])
    ledger['latest_registered_editorial_candidate']={**release,'status':'experimental-verified-Lil-B24-13',
        'final_review':str(FINAL),'actual_proof':str(visual),'full_goal_complete':False}
    ledger['formatting_watchlist']['Lil_B24_trade_routes_officers13'].update(status='completed-in-V1841;broader-route-formatting-open',
        final_review=str(FINAL),all13_source_native_individual_actual_and_registered_gates_passed=True)
    ledger['next_route_scene_editorial_packet']={'file_path':'/data/SC2.DK4','candidate':str(ROM),
        'prior_reviewed_blocks':[22,120,23,24],'prior_blocks_editorially_complete':True,
        'next_source_scene_selection_pending':True,'normal_return_proof':str(ACTUAL),
        'next_available_source_context':'Original EV2 eligibility after normal Amsterdam return47650;do not assume B25. Alternatively advance116 pendingCOMMON whereoriginalcontexts available.'}
    summary='V1844 completes13 Lil B24 entries:1529 complete(1158 revised371 retained),1645 source/prose reviewed. '+scope
    ledger['latest_checkpoint']=summary
    ledger['research_checkpoints'].append({'id':'V1844-Lil-trade-routes-officers13-complete',
        'proof':str(ROOT/'completion_receipt.json'),'completed_entries_added':13,'source_prose_reviews_added':0,'full_goal_complete':False})
    for key in('unresolved_graphics_work','reviewed_but_incomplete_COMMON_IDs','source_prose_reviewed_counts_by_file',
        'records_with_source_and_prose_pass','older_record_reaudit_after_full_editorial_goal'):
        assert ledger[key]==before[key],key
    assert ledger['records_editorially_completed']==sum(ledger['completed_editorial_record_counts_by_file'].values())==1529
    assert ledger['records_revised_and_integrated']+ledger['retained_wordings_editorially_completed']==1529
    assert ledger['goal_status']=='active'and not ledger['full_goal_complete']
    assert not any(ledger['reviewed_but_incomplete_route_record_IDs'].values())
    pending=LEDGER.with_name('editorial_review_current_v1844_pending.json');assert not pending.exists()and LEDGER.read_bytes()==raw_ledger
    save(pending,ledger);os.replace(pending,LEDGER)
    GUIDE.mkdir(parents=True);guide=[]
    for row in rows:
        hold=row['actual_holds'][1];src=Path(hold['capture']);dst=GUIDE/(row['id']+'.png')
        copy2(src,dst);assert sha(dst.read_bytes())==hold['capture_sha256']
        guide.append({'id':row['id'],'path':str(dst),'sha256':sha(dst.read_bytes()),'source_capture':str(src)})
    for label,photo in [('Amsterdam_docking_prompt',actual['docking_prompt_capture']),('Amsterdam_normal_return',actual['terminal_capture'])]:
        src=Path(photo['path']);dst=GUIDE/(label+'.png');copy2(src,dst)
        assert sha(dst.read_bytes())==photo['PNG_sha256'];guide.append({'id':label,'path':str(dst),'sha256':sha(dst.read_bytes())})
    save(GUIDE/'provenance.json',{'candidate':str(ROM),'candidate_sha256':digest,'captures':guide,
        'targeted_actual_emulator_not_full_route_or_hardware':True,'two_each16_byte_coordinate_only_fixtures_disclosed':True,
        'source_proof':str(ACTUAL),'proof_sha256':sha(ACTUAL.read_bytes())})
    Path('docs/lil_B24_v1844_completion.md').write_text('# V1844 Lil trade-route and officer scene complete\n\n'+scope+
        f'\n\nCandidate: {ROM.as_posix()}\n\nSHA256: {digest}\n\nPatch SHA256: {release["patch_sha256"]}\n\nFinal review: {FINAL.as_posix()}\n',encoding='utf-8')
    for name in('translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md'):
        with(Path('docs')/name).open('a',encoding='utf-8')as f:
            f.write('\n\n## V1844 Lil B24 thirteen entries complete\n\n'+summary+'\n\nSee [completion](lil_B24_v1844_completion.md).\n')
    # Replace stale live-process advice with the proven terminal state.
    text=HANDOFF.read_text();text=text.replace('# Current editorial handoff - V1836','# Current editorial handoff - V1844',1)
    start=text.index('## Current coverage and registered release');end=text.index('## Immediate work:')
    current=f'''## Current coverage and registered release

- Ledger: translations/editorial_review_current_v1.json. **1529 complete =1158 revised +371 retained;1645 source/prose reviewed.**
- Completed per file1402 COMMON+127 SC2;reviewed1518 COMMON+127 SC2. No active reviewed-incomplete route drafts;116 reviewed-incomplete COMMON and broader untouched shared/routes/player prose remain.
- Latest registered experimental: {ROM.as_posix()},profile {release['profile']};478 manifest batches/114 accepted layers.
- Candidate SHA256: {digest}.
- Exact clean-input patch: {release['patch']};SHA256 {release['patch_sha256']}.
- Canonical out/raphael_natural_v2_accepted_base.nds SHA2563cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe.
- Clean work/clean.nds SHA256f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d.
- V1492 remains promoted(tag promoted-v1492),SHA25696d0eda08db4f6da69a936a44db1f41abcc1cd6ce202370a9edc5517eb5400fd. No new promotion/push performed.
- Last pushed53c0b58c4be456731024a1e594c3121360395296;branch codex/combined-routes-v89;origin https://github.com/CRSdefiance/Daik-kai_Jidai_IV_Rota_Nova_Translation.git.
- ARM9 {release['ARM9_sha256']};COMMON {release['COMMON_sha256']};SC2 {release['SC2_sha256']}. Staged payload123040bytes unchanged.

'''
    text=text[:start]+current+text[end:]
    start=text.index('## Immediate work:');end=text.index('## Completed work to avoid repeating')
    section=f'''## Latest completed scene: Lil trade routes and officers, SC2 B24

{scope}

- Final review: {FINAL.as_posix()}.
- Approved manuscript: {DOC.as_posix()};reference map: {MAP.as_posix()}.
- Actual proof: {ACTUAL.as_posix()};all13 actual panels,portraits,nameplates andnormal town return viewed.
- Native fonts/macro104: work/analysis/lil_B24_fonts_v1826/all13_native_macros_and_complete_font_planes.json;both sheets viewed.
- Original event/packed exclusion prefix: work/analysis/lil_B24_event_context_v1832b/original_full_event24_and_packed_set_prefix.json. Source flag27 word0x00FFFFFF(bytesFFFFFF00) excludes bit0. Original not-Bruges andCamille conditions mapped;natural Amsterdam activation verified.
- Fresh complete source entry/command census: work/analysis/lil_B24_reference_census_v1835/complete_shipped_entry_and17_mapped_command_census.json.336 loads/672 parent modes perROM in1830.
- Registered compiler dk4tool/patch/lil_trade_routes_editorial.py;config translations/lil_trade_routes_editorial_release_v1.json. Optional final stage afterV1807 stack,before final story-percent/art guards. Seven invalid releases rejected withoutpartialmutation.
- Registered exact patch/whole-ROM research identity: work/analysis/lil_B24_release_v1840/registered_release_verification.json.
- Fresh startup: work/analysis/lil_B24_release_v1840/ordinary_startup_verification.json;all8 full frames exactV1105 andviewed.
- Completion receipt: work/analysis/lil_B24_completion_v1844/completion_receipt.json. Guide screenshots: {GUIDE.as_posix()}.

### Process state and next action

All current jobs are **terminal**. Original1831 emulator(session21739) ended43800 normally withoutB24;successor1834(session67076) ended47650 aftercomplete B24. Navigation driver1837(session23008),builder1841 andboth startup tests also terminal. Do not rerun completed tests withoutconcrete risk. Frozen failed1832/1833/1833b producers preserved;successors1832b/1833c corrected offline assumptions beforelive edits.

Next: inventory original EV2 events/dependencies/complete predicates after actual Amsterdam town return47650. Latest snapshot E:/Rota Nova translations/Generated/work/emulation_v193/lil_B24_research_run_v1834_RESEARCH_ONLY/frame_047650_arm9_ram.bin. Original events22,23,24,120 complete;verify live state beforeusing. Do not infer next block25. Continue source-first prose review ofthe next original eligible scene,oradvance116 pendingCOMMON wherecontextsavailable. Preserve full all-routes/player-prose scope. Successful Lookout shot remains available with the level-preserving1798c fixture,described below.

'''
    text=text[:start]+section+text[end:]
    text=text.replace('Keepall184 outputROMs','Keep all185 output ROMs')
    text=text.replace('Refresh livehandle/frame beforehandoff toanotherthread.','All recorded jobs are terminal;refresh authoritative state before another thread starts testing.')
    HANDOFF.write_text(text,encoding='utf-8')
    save(ROOT/'completion_receipt.json',{'candidate':str(ROM),'candidate_sha256':digest,
        'patch':release['patch'],'patch_sha256':release['patch_sha256'],'final_review':str(FINAL),
        'completed_before_after':[1516,1529],'source_prose_reviewed_unchanged':1645,'revised_added':12,'retained_added':1,
        'ledger_sha256':sha(LEDGER.read_bytes()),'handoff_sha256':sha(HANDOFF.read_bytes()),'guide_captures':guide,
        'all_required_scene_native_actual_registered_patch_startup_visual_gates_passed':True,
        'full_goal_remains_active':True,'graphics_and_broader_editorial_remain_unfinished':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print({'complete':1529,'revised':1158,'retained':371,'source_prose_reviewed':1645,'B24_added':13,
           'guide_captures':len(guide),'full_goal_remains_active':True},flush=True)
