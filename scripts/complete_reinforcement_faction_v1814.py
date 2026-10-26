"""Close only the six fully reviewed/rebuilt/current-gameplay reinforcement rows."""
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path
from shutil import copy2
import os
from dk4tool.rom.nds import NdsImage
from dk4tool.patch import reinforcement_faction_prose as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.script.common_message_table import common_message_entries
from scripts.reinforcement_sniping_layout_v1024 import compiled
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/reinforcement_completion_v1814')
FINAL=Path('translations/reinforcement_faction_final_review_v1.json')
DOC=Path('translations/reinforcement_sniping_editorial_manuscript_v4.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
HANDOFF=Path('docs/editorial_handoff_current.md')
ROM=Path('out/all_routes_combined_v1807_candidate.nds')
RELEASE=Path('work/analysis/reinforcement_faction_release_v1805/registered_release_verification.json')
ACTUAL=Path('work/analysis/reinforcement_faction_actual_v1813/actual_reinforcement_verification.json')
STARTUP=Path('work/analysis/reinforcement_faction_release_v1805/ordinary_startup_verification.json')
GUIDE=Path('E:/Rota Nova translations/Guide screenshots/V1807 Reinforcement announcement verified')

if __name__=='__main__':
    assert not ROOT.exists()and not FINAL.exists()and not GUIDE.exists()
    doc,release,actual,startup=map(read,(DOC,RELEASE,ACTUAL,STARTUP));digest=sha(ROM.read_bytes())
    assert digest==release['candidate_sha256']==actual['candidate_sha256']==startup['candidate_sha256']
    assert release['whole_reconstruction_byte_exact']and release['all477_batches114_accepted_layers_and_previous_profiles_preserved']
    assert sha(Path(release['patch']).read_bytes())==release['patch_sha256']
    assert sha(ROM.with_suffix('.manifest.json').read_bytes())==release['manifest_sha256']
    assert actual['normal_A_dismissal_enters_original_battle_without_blank_or_extra_page']
    assert len(actual['complete_actual_holds'])==2 and len(actual['exact_fixture_replays'])==1
    assert startup['all8_complete_startup_title_NewGame_frames_exact']
    assert sha(Path(startup['review_sheet']).read_bytes())==startup['review_sheet_sha256']
    visual=read(doc['successor_visual_review_proof']);assert visual['all120_new_native_printf_wraps_ABI_guards_full_font_planes_and_bounds_pass']
    image=NdsImage.open(ROM);arm=image.read_file('/__arm9__.bin');config=read(owned.CONFIG)
    entries=owned.entries(image.read_file(owned.PATH),arm,config['directory_sha256'])
    clean=NdsImage.open('work/clean.nds');jp=common_message_entries(clean.read_file(owned.PATH),clean.read_file('/__arm9__.bin'))
    ids=set(owned.IDS);rows=[]
    for previous in doc['records']:
        n=previous['message_id']
        if n not in ids:continue
        assert jp[n].text.hex()==previous['source_hex']and entries[n].text==compiled(previous)
        row=deepcopy(previous)
        row.update(previous_current_reference=row['current_reference'],previous_current_text_hex=row['current_text_hex'],
            current_reference={k:v for k,v in asdict(entries[n]).items()if k!='text'},
            current_text_hex=entries[n].text.hex(),current_English=row['english'],completed_candidate_reference=str(ROM),
            completed_candidate_sha256=digest,decision='revised-and-integrated',
            status='complete-source-native-and-representative-original-gameplay',actual_proof=str(ACTUAL),
            individually_activated_in_current_build=n==1911,
            actual_scope='Current original1911 with Charles18 fallback andfull Valdes faction label,complete holds5410/5510 andnormal battle return5610. Other five voice alternatives have full clean-source/context and20 native faction/font cases each;no individual actual-visit claim.')
        rows.append(row)
    assert len(rows)==6 and all(all(r['review'].values())for r in rows)
    ledger_raw=LEDGER.read_bytes();ledger=read(LEDGER);before=deepcopy(ledger)
    assert(ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'],ledger['records_with_source_and_prose_pass'])==(1503,1136,367,1632)
    assert ids<=set(ledger['reviewed_but_incomplete_COMMON_IDs'])
    family='Reinforcement-full-faction-voice-variants6'
    assert not any(f['id']==family for f in ledger['completed_editorial_families'])
    assert not any(set(f.get('native_message_IDs',[]))&ids for f in ledger['completed_editorial_families'])
    ROOT.mkdir(parents=True);(ROOT/'ledger_before.json').write_bytes(ledger_raw);(ROOT/'handoff_before.md').write_bytes(HANDOFF.read_bytes())
    scope=('Six COMMON reinforcement voice alternatives1911-1916 are complete in registered V1807. '
        'The clean Japanese assistance meanings and tones are preserved;ships from the complete faction label avoids a fleet from Bergstrom Fleet. '
        'All120 new original printf/wrap/full native-independent font cases andsix visual variants pass. '
        'Only those six paragraphs change in their existing allocations;all3668 native offsets/copy spans,41 block lengths,3662 other strings andall unowned bytes remain exact. '
        'All other ROM files/components,ARM9,fonts,graphics,stories and123040 staged bytes equal V1775. '
        'The new optional final layer preserves477 manifest batches,114 accepted layers,every prior profile andV1492 promotion. Seven invalid releases fail without partial mutation. '
        '54 native cold/warm copies and12 cache sequences pass full copied spans,NULs,output/input guards andABI. '
        'The clean-input patch reconstructs every ROM byte. Eight fixture-free startup/title/New Game frames match V1105 andwere viewed. '
        'Current original1911 has two complete native/independent/actual RGB holds,Charles18 portrait/name andfull Valdes label;normal A dismissal enters the original battle. '
        'One19-byte fixture sets16 own coordinates andthree original-method diplomatic prerequisite bytes. No source/disposable save,savestate,RNG,message,outcome,actor identity orship-stat override. '
        'This is a representative actual scene plus complete native voice/name coverage,not six individual visits,a full battle orhardware verification. '
        'Covering-fire1917-1923 remains pending final current-proof reconciliation;successful-shot1924-1930 remains pending actual success/dismissal/outcome. '
        'The separate V1775 Lookout pilot ended6471:206 exact whole4MiB fixture replays and12 original unsuccessful rolls;original level-up37->38/Aim166->168 explains its strict fixture stop. '
        'No shot completion credit. The successor fixture preserves naturally earned level/Aim andpasses three copied-state cases. '
        'Full editorial goal active;123 earlier reviewed-incomplete COMMON entries,broader shared/routes/player prose,separate graphics/all18 plaques andlater older-record re-audit remain open.')
    proofs=[DOC,RELEASE,ACTUAL,STARTUP,Path(doc['successor_native_format_proof']),Path(doc['successor_visual_review_proof']),
        Path(doc['unchanged14_current_format_proof']),Path('work/analysis/lookout_terminal_v1806/terminal_contact_roll_and_fixture_audit.json'),
        Path('work/analysis/lookout_level_successor_v1810/level_preserving_fixture_preflight.json')]
    save(FINAL,{'format':'dk4-editorial-family-final-review-v1','file_path':owned.PATH,'native_message_IDs':sorted(ids),
        'records':rows,'record_IDs':[r['id']for r in rows],'manuscript':str(DOC),'candidate':str(ROM),'candidate_sha256':digest,
        'proofs':{str(p):sha(p.read_bytes())for p in proofs},'actual_verification_scope':scope,
        'completed_entries':6,'revised':6,'retained':0,'full_goal_complete':False})
    ledger['completed_editorial_families'].append({'id':family,'file_path':owned.PATH,'native_message_IDs':sorted(ids),
        'record_IDs':[r['id']for r in rows],'records':rows,'final_review':str(FINAL),
        'documentation':'docs/reinforcement_v1814_completion.md','actual_verification_scope':scope})
    ledger['coverage_units'].append({'id':family,'file_path':owned.PATH,'native_message_IDs':sorted(ids),
        'status':'complete-source-native-and-representative-original-gameplay','final_review':str(FINAL),
        'completed_entries_added':6,'source_prose_reviews_added':0,'full_goal_complete':False})
    ledger['records_editorially_completed']+=6;ledger['records_revised_and_integrated']+=6
    ledger['completed_editorial_record_counts_by_file'][owned.PATH]+=6
    ledger['reviewed_but_incomplete_COMMON_IDs']=[n for n in ledger['reviewed_but_incomplete_COMMON_IDs']if n not in ids]
    drafts=ledger['active_source_prose_drafts'];drafts['native_message_IDs']=[n for n in drafts['native_message_IDs']if n not in ids]
    for key,pending in drafts['manuscript_record_subsets_pending'].items():drafts['manuscript_record_subsets_pending'][key]=[n for n in pending if n not in ids]
    drafts['manuscript_record_subsets_pending'][str(DOC)]=list(range(1917,1931))
    drafts['manuscripts'].append(str(DOC));drafts.update(status='123-reviewed-COMMON-and-broader-prose-open',
        note='Reinforcement6,fleet-sighting15 andLil opening/lessons complete. Remaining123 reviewed COMMON andbroader prose remain;covering-fire final reconciliation andsuccessful Lookout shot are open.')
    for unit in ledger['coverage_units']:
        if unit['id']=='all-route-scenes':
            unit.update(reviewed_route_records=114,completed_route_records=114,
                note='Earlier SC2 B294 one,Lil B22 opening49 andB120/B23 lessons64 are complete. All later Lil scenes andall other route scenes remain in scope.',
                next='Inventory the next original eligible Lil event after normal Bruges return;continue every route andremaining player prose.')
    ledger.setdefault('integrated_candidate_reference_history',[]).append(deepcopy(ledger['current_integrated_candidate']))
    ledger['current_integrated_candidate']={'path':str(ROM),'sha256':digest,'profile':'all-routes-unified-v1807',
        'MESFILE_sha256':release['COMMON_sha256'],'ARM9_sha256':release['ARM9_sha256'],
        'patch':release['patch'],'patch_sha256':release['patch_sha256'],'manifest':release['manifest'],
        'status':'experimental-verified-editorial-checkpoint-not-promoted','details':scope,'full_goal_complete':False}
    ledger['latest_registered_editorial_candidate']=deepcopy(ledger['current_integrated_candidate'])
    ledger['pending_registered_reinforcement_sniping_candidate'].update(
        completed_native_message_IDs=sorted(ids),pending_final_review_native_message_IDs=list(range(1917,1931)),
        latest_representative_reinforcement_actual_proof=str(ACTUAL),
        note='Historical V1034 artifact retained. Six reinforcement rows completed in current V1807;covering-fire final reconciliation andshot actual gate remain open.')
    ledger['lookout_contact_v1806']={'status':'bounded-negative-shot-test-native-rolls-observed',
        'proof':str(proofs[-2]),'native_rolls':12,'successful_shots':0,'terminal_frame':6471,
        'next_level_preserving_fixture_preflight':str(proofs[-1]),'completed_entries_added':0}
    ledger['formatting_watchlist'][family]={'final_review':str(FINAL),'native_faction_cases':120,'actual_holds':2,
        'source_native_offsets_and_complete_glyphs_preserved':True,'broader_formatting_audit_open':True}
    summary='V1814 completes six reinforcement entries:1509 complete(1142 revised367 retained),1632 source/prose reviewed;123 reviewed-incomplete COMMON andbroader prose remain. '+scope
    ledger['latest_checkpoint']=summary
    ledger['research_checkpoints'].append({'id':'V1814-reinforcement6-complete','proof':str(ROOT/'completion_receipt.json'),
        'completed_entries_added':6,'source_prose_reviews_added':0,
        'previous_goal_turn_classification':'no-progress:answered the thread/compaction question;current goal revalidated andadvanced this turn',
        'this_goal_turn_classification':'progress:six improved source-faithful paragraphs integrated,patched,native/startup/current-gameplay verified;12 native shot rolls andearned-level stop audited',
        'full_goal_complete':False})
    for key in('unresolved_graphics_work','source_prose_reviewed_counts_by_file','records_with_source_and_prose_pass',
        'reviewed_but_incomplete_route_record_IDs','newly_observed_armed_latina_followup','older_record_reaudit_after_full_editorial_goal'):
        assert ledger[key]==before[key],key
    assert ledger['goal_status']=='active'and ledger['full_goal_complete']is False
    assert ledger['records_editorially_completed']==sum(ledger['completed_editorial_record_counts_by_file'].values())==1509
    assert ledger['records_revised_and_integrated']+ledger['retained_wordings_editorially_completed']==1509
    assert len(ledger['reviewed_but_incomplete_COMMON_IDs'])==len(drafts['native_message_IDs'])==123
    pending=LEDGER.with_name('editorial_review_current_v1814_pending.json');assert not pending.exists()and LEDGER.read_bytes()==ledger_raw
    save(pending,ledger);os.replace(pending,LEDGER)
    guide=[];GUIDE.mkdir(parents=True)
    for name,source,frame in[('01_Original_reinforcement_announcement',Path(actual['complete_actual_holds'][1]['capture']),5510),
        ('02_Normal_battle_transition',Path(actual['actual_battle_entry_screenshot']),5610)]:
        target=GUIDE/(name+'.png');copy2(source,target);assert sha(target.read_bytes())==sha(source.read_bytes())
        guide.append({'guide':str(target),'source':str(source),'frame':frame,'sha256':sha(target.read_bytes())})
    save(GUIDE/'capture_provenance.json',{'candidate':str(ROM),'candidate_sha256':digest,'captures':guide,
        'original256x384_lossless_framebuffer_captures':True,'disclosed_fixture':'16 own coordinates plus3 original-method faction diplomatic prerequisite bytes;no earned progression claim.',
        'no_savestate_or_RNG_message_result_override':True,'actual_proof':str(ACTUAL),'actual_proof_sha256':sha(ACTUAL.read_bytes())})
    document=Path('docs/reinforcement_v1814_completion.md');document.write_text('# V1814 reinforcement6 complete\n\n'+summary+
        '\n\nFinal review: '+str(FINAL)+'\n\nLookout test: '+str(proofs[-2])+'\n\nNext Lookout fixture: scripts/native_lookout_contact_v1798c.py (offline validated only).\n',encoding='utf-8')
    for name in('translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md'):
        with(Path('docs')/name).open('a',encoding='utf-8')as f:f.write('\n\n## V1814 reinforcement6 complete\n\n'+summary+'\n\nSee [completion](reinforcement_v1814_completion.md).\n')
    handoff=HANDOFF.read_text();assert handoff.startswith('# Current editorial handoff - V1794')
    handoff=handoff.replace('# Current editorial handoff - V1794','# Current editorial handoff - V1814',1)
    handoff=handoff.replace('1503 complete =1136 revised +367 retained.','1509 complete =1142 revised +367 retained.')
    handoff=handoff.replace('Completed per file:1389 COMMON +114 SC2','Completed per file:1395 COMMON +114 SC2')
    handoff=handoff.replace('Earlier129 reviewed-incomplete COMMON','Earlier123 reviewed-incomplete COMMON')
    lo=handoff.index('## Latest registered cumulative build');hi=handoff.index('## Latest completed shared-dialogue work',lo)
    latest='## Latest registered cumulative build\n\n'+f'- Candidate: {ROM.as_posix()} (E:/Rota Nova translations/Generated/out/{ROM.name}).\n- ROM SHA256: {digest}.\n- Patch: {release["patch"]}; SHA256 {release["patch_sha256"]}. Exact clean-input reconstruction verified.\n- Profile all-routes-unified-v1807:477 batches/114 accepted layers,complete V1775 stack plus six exact-slot COMMON paragraphs. All other files/components/runtime/fonts/graphics/stories exact to V1775.\n- ARM9 SHA256: {release["ARM9_sha256"]}. COMMON SHA256: {release["COMMON_sha256"]}. SC2 SHA256: {release["SC2_sha256"]}.\n- Canonical base remains out/raphael_natural_v2_accepted_base.nds;V1492 remains promoted. Last pushed53c0b58c4be456731024a1e594c3121360395296. No fresh push/promotion authorization.\n\n## Latest completed family and next original-test evidence - V1814\n\n'+scope+'\n\n'+f'Final review: {FINAL.as_posix()}. Registered proof: {RELEASE.as_posix()}. Current actual proof: {ACTUAL.as_posix()}.\n\n'+'All jobs are terminal. Lookout runner61920 ended6471;both navigators40415/21673 areterminal. The last stop was a strict level37 fixture assumption;actual native level38/Aim168 is preserved by explicit successor1798c andthree offline source cases1810. Do not repeat the old fixed-level fixture. No successful shot,revival orRNG override. New current reinforcement runner14191 ended5810;startup89898/title areterminal. Do notrestart a live process solely on timeout.\n\n'+'Next: reconcile covering-fire1917-1923 using current exact text/native/runtime inheritance andhistorical actual proof;or use level-preserving1798c for a new bounded cold-load Lookout test after normal terminal6471. Both current shot actual andnormal outcome/dismissal remain open. New observer contract orrunner needs explicit whole-ARM9/target-template inheritance binding if it uses V1807 instead of source-bound V1775. All broader shared/routes/player prose remains in scope.\n\n'
    handoff=handoff[:lo]+latest+handoff[hi:]
    handoff=handoff.replace('earlier129 COMMON','earlier123 COMMON').replace('Pending COMMON:750-752;1911-1930;','Pending COMMON:750-752;1917-1930;')
    handoff=handoff.replace('Armed Latina actual name UI remains open separately. Successful Lookout shot1911-1930 also remains open.','Armed Latina actual name UI remains open separately. Reinforcement1911-1916 is nowcomplete;covering-fire1917-1923 final reconciliation andsuccessful Lookout shot1924-1930 remain open.')
    p0=handoff.index('All current jobs are terminal.');p1=handoff.index('\n\nBefore ROM changes',p0)
    handoff=handoff[:p0]+'All current jobs areterminal. Original Lookout1799 ended6471 andnew current reinforcement1812 ended5810;source/disposable saves arepreserved. All generated ROMs remain preserved,including newV1807. Never restart solely because observation timed out. Prior handoff/ledger arein the V1814 completion folder;archivesV1780/V1795 remain available.'+handoff[p1:]
    HANDOFF.write_text(handoff,encoding='utf-8')
    save(ROOT/'completion_receipt.json',{'candidate':str(ROM),'candidate_sha256':digest,'final_review':str(FINAL),
        'final_review_sha256':sha(FINAL.read_bytes()),'counts_before_after':[1503,1509],'revised_before_after':[1136,1142],
        'retained':367,'source_prose_reviewed':1632,'reviewed_incomplete_COMMON':123,
        'ledger_sha256':sha(LEDGER.read_bytes()),'handoff_sha256':sha(HANDOFF.read_bytes()),'guide_captures':guide,
        'all6_complete_source_native_registered_patch_startup_and_representative_actual_requirements_proven':True,
        'successful_shot_and14_other_family_rows_not_given_completion_credit':True,
        'full_editorial_goal_active_graphics_and_older_record_reaudit_separate':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Six reinforcement entries complete in V1807:1509 total(1142 revised367 retained),1632 source/prose,123 earlier pending COMMON. Goal active.',flush=True)
