"""Complete the reviewed64 lesson entries;retain the full editorial/graphics scope."""
from copy import deepcopy
import os
from pathlib import Path
from shutil import copy2
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_lessons_completion_v1779')
REL=Path('work/analysis/lil_lessons_release_v1774')
FINAL=Path('translations/lil_lessons_final_review_v1.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
HANDOFF=Path('docs/editorial_handoff_current.md')
GUIDE=Path('E:/Rota Nova translations/Guide screenshots/V1775 Lil sailing and crew lessons verified')
DOC=Path('translations/lil_lessons_editorial_manuscript_v5.json')
CHOICES=Path('translations/lil_lesson_choices_editorial_draft_v2.json')
MAP=Path('translations/lil_lessons_editorial_relocation_map_v1.json')

if __name__=='__main__':
    assert not ROOT.exists() and not FINAL.exists() and not GUIDE.exists()
    release,actual,doc,choices,mapping=map(read,(REL/'registered_release_verification.json',
        REL/'targeted_gameplay_and_startup_reconciliation.json',DOC,CHOICES,MAP))
    rom=Path(release['candidate']);digest=sha(rom.read_bytes())
    assert digest==release['candidate_sha256']==actual['candidate_sha256']=='6bc6b6bb01f9ea0e763ee1d6c4c3f2bcb1c7c8cca3be3dd54bd43903045cb55a'
    assert release['complete_reconstruction_byte_exact'] and release['all476_batches114_accepted_layers_and_prior_profiles_preserved']
    assert sha(Path(release['patch']).read_bytes())==release['patch_sha256']
    assert actual['all_four_original_response_paths_normal_type0_returns_verified']
    assert actual['all70_speech_visits140_complete_holds_and126_native_command_pairs']
    assert actual['all8_fixture_free_startup_controls_and_viewed_sheet_verified']
    assert actual['COMMON676_677_repaired_layout_preserved_without_new_shop_visit']
    assert mapping['external_references_complete'] and len(actual['individual_actual_speech_IDs'])==55
    assert len(doc['records'])==60 and len(choices['records'])==4
    all_prose=doc['records']+choices['records'];ids={r['id']for r in all_prose};assert len(ids)==64
    assert sum(r['editorial_decision']=='revise'for r in all_prose)==45
    assert sum(r['editorial_decision']=='retain-wording'for r in all_prose)==19
    clean=NdsImage.open('work/clean.nds');image=NdsImage.open(rom)
    source=IlnkContainer.parse(clean.read_file('/data/SC2.DK4')).blocks
    target=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
    refs={r['id']:r for b in mapping['blocks']for r in b['text_records']}
    used_choices={r['id']:r for r in release['stage']['changed_records']if 'option_index'in r}
    equivalents={r['id']:r for r in mapping['unvisited_conditional_records']}
    rows=[]
    for original in all_prose:
        row=deepcopy(original);ident=row['id'];number=row['block'];s=row['source_reference']
        raw=bytes.fromhex(row['source_hex']);assert source[number][s['offset']:s['offset']+len(raw)]==raw
        row['previous_current_reference']=row['current_reference'];row['previous_current_text_hex']=row['current_text_hex']
        if ident in refs:
            ref=refs[ident];value=bytes.fromhex(ref['target_hex']);offset=ref['new_offset']
            assert target[number][offset:offset+len(value)]==value
            assert target[number][offset-5:offset]==source[number][s['offset']-5:s['offset']]==b'\0\x40\xff\xff\0'
            assert raw[:1]==value[:1]
            target_index=next(i for i in range(len(target[number].split(b'\0')))if sum(len(v)+1 for v in target[number].split(b'\0')[:i])==offset)
            row['current_reference']={'file_path':'/data/SC2.DK4','block':number,'offset':offset,
                'bytes':len(value),'header_offset':offset-5,'record_index':target_index}
            row['current_text_hex']=value.hex()
            row['individually_activated_in_gameplay']=ident in actual['actual_holds_by_ID']
            if row['individually_activated_in_gameplay']:
                row['actual_samples']=actual['actual_holds_by_ID'][ident]
            else:
                assert ident in equivalents;row['native_equivalent_actual_sample']=equivalents[ident]
            row['actual_revised_gameplay_and_registered_release_pending']=False
        else:
            ref=used_choices[ident];offset=ref['new_offset'];value=row['english'].encode('ascii')
            assert target[number][offset:offset+len(value)+1]==value+b'\0'
            row['current_reference']={'file_path':'/data/SC2.DK4','block':number,'offset':offset,'bytes':len(value),
                'choice_command_offset':next(c['new_offset']for b in mapping['blocks']if b['block']==number for c in b['choice_commands']),
                'option_index':row['option_index']}
            row['current_text_hex']=value.hex();row['actual_original_choice_result_verified']=True
            row['actual_revised_choice_selection_and_release_pending']=False
        row.update(completed_candidate_reference=str(rom),completed_candidate_sha256=digest,
            decision='revised-and-integrated'if row['editorial_decision']=='revise'else'retained-after-source-native-review',
            status='complete-source-native-and-targeted-original-gameplay',reference_map=str(MAP),
            actual_proof=str(REL/'targeted_gameplay_and_startup_reconciliation.json'))
        rows.append(row)
    raw_ledger=LEDGER.read_bytes();ledger=read(LEDGER);before=deepcopy(ledger)
    assert (ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],
        ledger['retained_wordings_editorially_completed'],ledger['records_with_source_and_prose_pass'])==(1424,1076,348,1632)
    assert len(ledger['reviewed_but_incomplete_COMMON_IDs'])==144
    family='Lil-sailing-and-crew-lessons64'
    assert not any(f['id']==family for f in ledger['completed_editorial_families'])
    existing={str(i)for f in ledger['completed_editorial_families']for i in f.get('record_IDs',[])}
    assert not (ids&existing)
    scope=('All60 Lil sailing/crew speech and system objects plus4 choice labels in SC2 B120/B23 are source/context/prose/native reviewed. '
        'Both responses ofboth original lesson choices return normally;70 speech visits140 complete native/independent pixel holds and126 native command pairs pass. '
        '55 unique speech IDs were individually activated;five conditional IDs have exact encoded text,speaker andnative-consumer equivalents among activated IDs, '
        'and receive no individual actual-visit claim. All124 nested commands,36 relative operands and180 relocated native skip cases are mapped. '
        'B120 tests coldboot without input saves,savestates orfixtures;each successful crew test discloses one16-byte coordinate-only Bruges fixture. '
        'No event,choice outcome,RNG orcharacter fields were forced. Current V1761 research is whole-file byte-identical to registered V1775; '
        'older wind evidence inherits exact B120/runtime,not whole-ROM identity. Only SC2B120(+240) andB23(+284) differ from V1711. '
        'All334 other blocks,every other file/component,ARM9,COMMON,fonts,graphics and123040 staged bytes remain exact. '
        'All476 manifest batches114 accepted layers,all prior profiles,exact clean patch andeight fixture-free startup controls pass. '
        'Photographed COMMON676/677 layout fixes are inherited through exact COMMON/ARM9;no new shop visit. '
        'V1775 is experimental,V1492 remains promoted,andcanonical construction baseline is unchanged. '
        'Full editorial goal remains active;144 earlier reviewed COMMON entries,broader untouched routes/shared/player prose,separate graphics/all18 plaques andlater older-record re-audit remain open.')
    ROOT.mkdir(parents=True);(ROOT/'ledger_before.json').write_bytes(raw_ledger);(ROOT/'handoff_before.md').write_bytes(HANDOFF.read_bytes())
    proof_paths=[REL/'registered_release_verification.json',REL/'targeted_gameplay_and_startup_reconciliation.json',
        REL/'ordinary_startup_verification.json',REL/'registration_provenance.json',DOC,CHOICES,MAP,
        Path(doc['native_font_proof']),Path(doc['actual_context_FE_proof']),Path(doc['visual_review'])]
    proofs={str(p):sha(p.read_bytes())for p in proof_paths}
    save(FINAL,{'format':'dk4-editorial-family-final-review-v1','file_path':'/data/SC2.DK4','blocks':[120,23],
        'records':rows,'record_IDs':[r['id']for r in rows],'manuscripts':[str(DOC),str(CHOICES)],
        'candidate':str(rom),'candidate_sha256':digest,'proofs':proofs,'actual_verification_scope':scope,
        'completed_entries':64,'revised':45,'retained':19,'individual_actual_speech_IDs':actual['individual_actual_speech_IDs'],
        'unvisited_conditional_records':mapping['unvisited_conditional_records'],'full_goal_complete':False})
    ledger['completed_editorial_families'].append({'id':family,'file_path':'/data/SC2.DK4','blocks':[120,23],
        'record_IDs':[r['id']for r in rows],'records':rows,'final_review':str(FINAL),
        'documentation':'docs/lil_lessons_v1779_completion.md','actual_verification_scope':scope})
    unit=next(u for u in ledger['coverage_units']if u['id']=='Lil-sailing-lessons64-source-prose')
    assert set(unit['record_IDs'])==ids
    unit.update(status='superseded-by-complete-family',completed_family=family,final_review=str(FINAL),
        individually_actual_speech_IDs=actual['individual_actual_speech_IDs'],not_individually_actual_speech_IDs=sorted(equivalents))
    ledger['coverage_units'].append({'id':family,'file_path':'/data/SC2.DK4','blocks':[120,23],
        'record_IDs':[r['id']for r in rows],'status':'complete-source-native-and-targeted-original-gameplay',
        'final_review':str(FINAL),'actual_proofs':[str(REL/'targeted_gameplay_and_startup_reconciliation.json')],
        'completed_entries_added':64,'full_goal_complete':False})
    ledger['records_editorially_completed']+=64;ledger['records_revised_and_integrated']+=45
    ledger['retained_wordings_editorially_completed']+=19;ledger['completed_editorial_record_counts_by_file']['/data/SC2.DK4']+=64
    drafts=ledger['active_source_prose_drafts']
    for key,pending in drafts['route_record_subsets_pending'].items():drafts['route_record_subsets_pending'][key]=[i for i in pending if i not in ids]
    assert not any(drafts['route_record_subsets_pending'].values())
    drafts.update(status='144-reviewed-COMMON-and-broader-prose-open',note='Lil opening49 andsailing/crew lessons64 complete. Earlier144 reviewed COMMON andbroader shared/routes/player-facing prose remain.')
    stale_route=deepcopy(ledger['reviewed_but_incomplete_route_record_IDs'])
    completed_opening=set(read('translations/lil_opening_final_review_v1.json')['record_IDs'])
    for file,pending in ledger['reviewed_but_incomplete_route_record_IDs'].items():
        ledger['reviewed_but_incomplete_route_record_IDs'][file]=[i for i in pending if i not in ids|completed_opening]
    assert not any(ledger['reviewed_but_incomplete_route_record_IDs'].values())
    ledger.setdefault('integrated_candidate_reference_history',[]).append(deepcopy(ledger['current_integrated_candidate']))
    ledger['current_integrated_candidate']={'path':str(rom),'sha256':digest,'profile':release['profile'],
        'MESFILE_sha256':release['COMMON_sha256'],'ARM9_sha256':release['ARM9_sha256'],
        'patch':release['patch'],'patch_sha256':release['patch_sha256'],'manifest':str(rom.with_suffix('.manifest.json')),
        'status':'experimental-verified-editorial-checkpoint-not-promoted','details':scope,'full_goal_complete':False}
    ledger.setdefault('native_completed_reference_history',[]).append(deepcopy(ledger['current_native_relocation_reference']))
    ledger['current_native_relocation_reference'].update(candidate=str(rom),candidate_sha256=digest,
        COMMON_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'])
    ledger['latest_registered_editorial_candidate']={**release,'status':'experimental-verified-Lil-lessons64',
        'final_review':str(FINAL),'actual_proof':str(REL/'targeted_gameplay_and_startup_reconciliation.json'),'full_goal_complete':False}
    lesson=ledger['lil_lessons_editorial_v1720']
    for key in list(lesson):
        if key.endswith('_pending'):lesson[key]=False
    lesson.update(status='complete64-in-V1775',final_review=str(FINAL),registered_release=str(REL/'registered_release_verification.json'),
        individually_actual_speech_IDs=actual['individual_actual_speech_IDs'],unvisited_conditional_records=mapping['unvisited_conditional_records'])
    ledger['formatting_watchlist']['Lil_sailing_lessons64'].update(status='completed-in-V1775;broader-route-formatting-open',
        final_review=str(FINAL),all64_source_native_and_targeted_gameplay_gates_passed=True)
    ledger['next_route_scene_editorial_packet']={'file_path':'/data/SC2.DK4','candidate':str(rom),
        'prior_reviewed_blocks':[22,120,23],'prior_blocks_editorially_complete':True,
        'next_source_scene_selection_pending':True,
        'next_available_source_context':'Original EV2 events eligible after normal Bruges town return at41420;no next story block is assumed.',
        'normal_return_proof':'work/analysis/lil_crew_scene_v1763_final/complete_B23_scene_and_fixture_audit.json',
        'note':'Continue144 pending COMMON where contexts are available,or inventory next original Lil event/neighbor context before authoring. Broader all-routes/player-prose goal remains active.'}
    summary='V1779 completes64 Lil lesson entries(45 revised19 retained):1488 complete(1121 revised367 retained),1632 source/prose reviewed. '+scope
    ledger['latest_checkpoint']=summary
    ledger['research_checkpoints'].append({'id':'V1779-Lil-sailing-and-crew-lessons64-complete',
        'proof':str(ROOT/'completion_receipt.json'),'completed_entries_added':64,'source_prose_reviews_added':0,'full_goal_complete':False})
    for key in ('unresolved_graphics_work','reviewed_but_incomplete_COMMON_IDs','source_prose_reviewed_counts_by_file','records_with_source_and_prose_pass'):
        assert ledger[key]==before[key]
    assert ledger['goal_status']=='active' and ledger['full_goal_complete'] is False
    assert ledger['records_editorially_completed']==sum(ledger['completed_editorial_record_counts_by_file'].values())==1488
    assert ledger['records_revised_and_integrated']+ledger['retained_wordings_editorially_completed']==1488
    pending=LEDGER.with_name('editorial_review_current_v1779_pending.json');assert not pending.exists() and LEDGER.read_bytes()==raw_ledger
    save(pending,ledger);assert read(pending)==ledger and LEDGER.read_bytes()==raw_ledger;os.replace(pending,LEDGER)
    GUIDE.mkdir(parents=True);pictures=[]
    wanted=['DK4_MES_B120_R0039','DK4_MES_B120_R0134','DK4_MES_B120_R0137','DK4_MES_B23_R0030',
        'DK4_MES_B23_R0044','DK4_MES_B23_R0069','DK4_MES_B23_R0104','DK4_MES_B23_R0166']
    for index,ident in enumerate(wanted,1):
        samples=actual['actual_holds_by_ID'][ident]
        sample=next(s for s in samples if 'lil_revised_wind'not in s['proof'])
        hold=sample['holds'][1];src=Path(hold['capture']);dst=GUIDE/f'{index:02d}_{ident}.png'
        copy2(src,dst);assert sha(dst.read_bytes())==hold['capture_sha256']
        pictures.append({'guide':str(dst),'source':str(src),'sha256':hold['capture_sha256'],'record_ID':ident,
            'frame':hold['frame'],'fixture':'one16-byte coordinate-only Bruges fixture'if '_B23_'in ident else'none'})
    full=read('work/analysis/lil_crew_scene_v1763_final/complete_B23_scene_and_fixture_audit.json')
    for label,key in [('09_Crew_choice_menu','choice_menu_capture'),('10_Normal_Bruges_return','terminal_capture')]:
        photo=full[key];src=Path(photo['path']);dst=GUIDE/(label+'.png');copy2(src,dst)
        assert sha(dst.read_bytes())==photo['PNG_sha256']
        pictures.append({'guide':str(dst),'source':str(src),'sha256':photo['PNG_sha256'],'frame':photo['frame'],
            'fixture':'one16-byte coordinate-only Bruges fixture'})
    save(GUIDE/'capture_provenance.json',{'candidate':str(rom),'candidate_sha256':digest,'captures':pictures,
        'captured_current_research_ROM_whole_file_identical_to_registered_candidate':True,
        'original256x384_lossless_framebuffer_captures':True,'no_save_or_savestate_inputs':True,
        'B23_coordinate_fixture_disclosed_per_capture':True,'targeted_headless_DeSmuME_not_full_route_or_hardware':True,
        'verification':str(REL/'targeted_gameplay_and_startup_reconciliation.json')})
    checkpoint=Path('docs/lil_lessons_v1779_completion.md')
    checkpoint.write_text('# V1779 Lil sailing and crew lessons complete\n\n'+summary+'\n\n'
        '## Release files\n\nROM: '+str(rom)+'\n\nROM SHA256: '+digest+'\n\nPatch SHA256: '+release['patch_sha256']+
        '\n\nFinal review: '+str(FINAL)+'\n\nGuide captures: '+str(GUIDE)+'\n',encoding='utf-8')
    for name in ('translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md'):
        with (Path('docs')/name).open('a',encoding='utf-8')as f:
            f.write('\n\n## V1779 Lil sailing and crew lessons64 complete\n\n'+summary+'\n\nSee [completion](lil_lessons_v1779_completion.md).\n')
    handoff=f'''# Current editorial handoff - V1779

## Full active goal and constraints

Complete the scene-by-scene editorial review against clean Japanese: shared shops/towns, every route, and all remaining player-facing prose. Use natural, faithful American English and approved names Rafael, Joakim, Maria and Camille. Follow natural-dialogue-v2, exact source/current coverage, reviewed controls/macros, native formatting, targeted gameplay, registered cumulative builds and exact clean-input patches. Keep the full goal ACTIVE after this batch. No subagents authorized. sources/ is read-only. Preserve ALL generated ROMs; never prune.

The separate graphics audit and all18 plaques remain unfinished. Wood texture/borders are accepted only. Four low-resolution Online bodies remain excluded; preserve the two brown marks. The older-record re-audit follows the full editorial goal.

## Verified coverage

1488 complete =1121 revised +367 retained. 1632 source/prose reviewed. Completed per file:1374 COMMON +114 SC2 (Lil opening49, lessons64 and earlier B294 one). Earlier144 reviewed-incomplete COMMON entries and broader untouched shared/routes/player prose remain. No active reviewed-incomplete route drafts remain. A stale top-level list of49 already-completed B22 IDs was reconciled from its final review, with no additional credit; its prior contents are in the completion receipt.

Authoritative ledger: translations/editorial_review_current_v1.json. Final64 source/current offsets, updated current NUL indices, revision/retention reasons and actual/native scope: translations/lil_lessons_final_review_v1.json. Stable record IDs retain their original Japanese identity; typed choice resizing changes later current NUL indices.

## Latest registered cumulative build

- Candidate: out/all_routes_combined_v1775_candidate.nds. Physical file: E:/Rota Nova translations/Generated/out/all_routes_combined_v1775_candidate.nds.
- ROM SHA256: {digest}.
- Patch: out/all_routes_combined_v1775_candidate.xdelta;SHA256 {release['patch_sha256']}. Clean input work/clean.nds SHA256 f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d. Reconstruction matches every byte.
- Profile all-routes-unified-v1775 is experimental.476 final manifest batches and114 accepted layers. It retains the whole V1711 stack and adds lil_lessons_editorial after lil_opening_editorial, before final story-percent/plaque/art guards.
- Only SC2 B120 grows2076->2316(+240) and B23 grows2308->2592(+284) relative to V1711. All334 other SC2 blocks, every other file/component, runtime, font and graphic are exact. ARM9 SHA256 500b7d6cea559d7252ae4e67f94540e67739428823a17cf26842b6827712a41e;COMMON SHA256 {release['COMMON_sha256']};SC2 SHA256 {release['SC2_sha256']}. Staged payload stays123040 bytes.
- Canonical construction parent remains out/raphael_natural_v2_accepted_base.nds SHA256 3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe. V1492 remains promoted/tag promoted-v1492. Last pushed commit53c0b58c4be456731024a1e594c3121360395296, branch codex/combined-routes-v89. No fresh push/promotion authorization.

## Completed lesson evidence: do not repeat without a concrete risk

Current manuscripts: translations/lil_lessons_editorial_manuscript_v5.json (60 speeches/system panels) and translations/lil_lesson_choices_editorial_draft_v2.json (4 labels).45 revisions,19 retentions. Keep executed manuscripts/producers/proofs frozen; corrections require explicit successors.

Release proof folder: work/analysis/lil_lessons_release_v1774. Read registered_release_verification.json, targeted_gameplay_and_startup_reconciliation.json, ordinary_startup_verification.json and registration_provenance.json. Completion receipt: work/analysis/lil_lessons_completion_v1779/completion_receipt.json. Executed producers: register1774, verify1776, startup1777, reconcile1778, complete1779.

Approved reference map: translations/lil_lessons_editorial_relocation_map_v1.json, producer1773. Clean/current original code sections and overlays each have only direct interpreter call24070 and no2A510 literal aliases. Original loaders/cache/parents cover336 blocks and672 modes per ROM, entering payload+8. Fresh original-parser inventories cover all124 nested commands on clean/current/target. All36 relative operands have180 relocated native cases. This structural walk bridges opaque effects; it is not gameplay of every branch. Scope is the exact shipped B120/B23 and bound runtime, not arbitrary injected streams.

The production compiler rebuilds all60 paragraphs, four typed2100 choice labels,36 spans, CS length and parity. Inverse reconstruction restores every original logical byte. Never join NUL rows or copy research bins for this layer. Eight negative cases reject repeat application, wrong runtime/canonical source, incomplete map, wrong branch destination, unreviewed formatting, wrong speaker and changed choice. Global profiles/encoder/layout and old source guards remain exact. FE uses a local dataclass replacement under the exact runtime lock.

Actual response paths:

- B120 wind:1741/1744, terminal29930,41 commands,22 speeches/44 full holds.
- B120 default:1770/1771/1772c, terminal27850,30 commands,14 speeches/28 full holds.
- B23 full:1764/1763b-final, terminal41420,46 commands,30 speeches/60 full holds.
- B23 decline:1766/1767, terminal32940,9 commands,4 speeches/8 full holds.

Both responses of both original choices return normally. Total70 speech visits/140 complete native-independent-actual holds and126 scoped command pairs;55 unique speech IDs individually activated. Five conditional IDs have exact encoded text, speaker and consumer equivalents among actual IDs: B120 R62/R80/R109 match R186; B23 R91/R95 match B120 R155/R163. Do not claim individual activation of those five.

Current V1761 research ROM is whole-file identical to V1775. The older wind test inherits exact B120 and runtime, not whole-ROM identity (it has the older unrelated B23 instruction). B120 tests have no input save, savestate or fixture. Each successful B23 test discloses one16-byte coordinate-only Bruges fixture; original docking, choices, events and RNG evolve normally. All captured inputs, PNGs,4MiB snapshots, callback boundaries and host restoration are audited. Boundary snapshots do not exclude temporary write-restore. No full-route, hardware or earned-travel claim.

All64 native layouts and all actual sheets/menus/portraits/nameplates/ends were viewed. Eight fixture-free startup/title/New Game frames match V1105 and were viewed. COMMON676/677 fixes are inherited through exact COMMON/ARM9, with no new shop visit. Ten guide captures/provenance: {GUIDE}. Current research is whole-file identical to registered V1775; B23 fixture is disclosed per capture.

FE geometry: original mode1 context228x48, font6x12, logical12px rows composed to16px display through the independently documented V365 paper contract; no glyph stretching. All9 FE panels fit one native page. This is not an independent whole-GPU trace. Current proofs are work/analysis/lil_Deck_label_approval_v1758/all60_current_native_font_reconciliation.json and all9_current_FE_reconciliation.json. Preserve exact Deck View, Sail Handler, Half Open and Full Open terms. V1772/1772b failures were mistaken FE-count expectations only; original selectors R36/R39 had already passed full pixel checks. Successor1772c passes; preserve all three producers.

## Next work

Continue the earlier144 COMMON entries where original contexts can be activated, or inventory the next original eligible Lil event after normal Bruges town return41420 before authoring. Do not assume the next story block. Keep the full all-routes/player-prose scope. Do not repeat completed opening49, lessons64 or the hot-spring RNG campaign without a concrete risk.

Pending COMMON:614-628;750-752;1911-1930;1994-2010;2022-2037;2058-2081;2090-2105;2147-2178;2192.750-752 remain context-unmapped: production SC matches are CS lengths; alternate testdata SC3B164 CS0101 word750 remains unclassified. Do not claim unused. Close-sighting V1693 stopped at Syracuse Dock; an unloaded enemy null mobile does not prove inactivity (original eligibility returned1). Use original open-water context; never force seen flags. Vicinity/Armed Latina actual UI also remains pending.

For B23 trigger/fixture details, use source proof1751, native_lil_Bruges_location_v1754.py and prior docs/lil_crew_v1768_checkpoint.md; do not rediscover docking by guessing. Original EV2 event23/category5/action24 selects B23 after completed120, outside Amsterdam2, with Camille present. Town3 top-left20224,4320 plus16 gives docking center20240,4336; radius32. Fixture water20240,4312 is24 away. The earlier spawn-based target was outside the radius and failed legitimately. Normal sequence after wind: A30230 clears log; B30260/B30290 closes sails; fixture/wait30320; Down+B30620 anchors; Down+A30920 approaches; A31220 accepts original docking. Earlier failed four-fixture approach is audited1757, without arrival credit.

## Process and preservation

All current jobs are terminal: runner76609/27850, navigator4143/27850, builder95117, patch46914, startup9541, title and verification. No live emulator remains. Do not reuse terminal handles or restart solely after an observation timeout. Previous handoff/ledger are preserved in the completion folder. Prior archive V1769 remains available.

Before ROM changes, read AGENTS.md, build_continuity_protocol, release_stack and relevant known_issues. Before prose, read natural_dialogue_workflow/dialogue_delegation_protocol. Python C:/Python314/python.exe; PYTHONUTF8=1; PYTHONPATH=.;.deps. Default sandbox launcher fails on P-drive credentials; scoped escalation is needed. out and work/analysis are E-drive junctions; archive lexical absolute paths without resolve(). Preserve every generated ROM and all rejected producers.
'''
    HANDOFF.write_text(handoff,encoding='utf-8')
    save(ROOT/'completion_receipt.json',{'candidate':str(rom),'candidate_sha256':digest,'patch':release['patch'],
        'patch_sha256':release['patch_sha256'],'newly_completed':64,'newly_revised':45,'newly_retained':19,
        'completed':1488,'revised':1121,'retained':367,'source_prose':1632,'reviewed_incomplete_COMMON':144,
        'complete_COMMON':1374,'complete_SC2':114,'final_review':str(FINAL),'proofs':proofs,
        'guide':str(GUIDE),'screenshots':pictures,'all_current_jobs_terminal':True,
        'reconciled_stale_already_completed_B22_pending_list':stale_route,
        'no_additional_credit_for_prior_opening_reconciliation':True,
        'canonical_V1492_promotion_prior_profiles_graphics_and_all_ROMs_preserved':True,
        'ledger_sha256':sha(LEDGER.read_bytes()),'handoff_sha256':sha(HANDOFF.read_bytes()),
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print({'newly_completed':64,'complete':1488,'revised':1121,'retained':367,'source_prose':1632,
        'pending_reviewed_COMMON':144,'guide_captures':len(pictures),'full_goal':'active'},flush=True)
