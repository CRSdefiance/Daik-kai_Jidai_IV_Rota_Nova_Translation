"""Close the52-message ceremony family and one actual omitted cliff message."""

import copy
import shutil
from collections import Counter
from pathlib import Path

from PIL import Image,ImageDraw

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/cliff_editorial_v829')
LEDGER = Path('translations/editorial_review_current_v1.json')
DOC = Path('docs/editorial_v829_completion.md')
SUMMARY = (
    'V829 completes the52-entry ceremony editorial family:30 revised wordings and22 justified retentions, '
    'all52 clean-source/native contexts and126 actual full-font holds freshly rechecked against current code. '
    'Actual Lil site chant1224 now passes after the source-bound Cave Village Map164 transfer and original '
    'guide/fog events;the original192-tick return and two additional growth holds pass. '
    'One omitted Lil SC2 B294 R73 Japanese line is now localized through natural-dialogue-v2 with original94 '
    'speaker/header and48-byte slot intact. The actual corrected line and three following holds are complete '
    'and left-aligned at native x16;normal return and seven ordinary startup/New Game frames pass. '
    'Registered combined V829 and its exact clean-input patch preserve all471 batches,114 accepted layers, '
    'other scripts,all graphics,ARM9,COMMON and original command addresses. '
    'Ledger totals are603 completed (438 revised/165 retained),606 source-prose reviewed andthree older reviewed '
    'drafts pending. Of the completed entries,602 are COMMON andone is the new SC2 route review. '
    'Remaining shared1245+,older750-752 contexts,all remaining route/player prose and lossless raw-record '
    'coverage remain open. Graphics and all18 plaques remain separately unfinished;the full goal stays active.'
)


def main():
    final_path = Path('translations/ceremony_editorial_final_review_v1.json')
    family = read(final_path)
    release = read(ROOT/'registered_binary_and_patch_verification.json')
    scene = read(ROOT/'actual_cliff_scene_and_transition_verification.json')
    startup = read(ROOT/'ordinary_New_Game_verification.json')
    chant = read(ROOT/'last_Lil_ceremony_variant_v828.json')
    assert family['ceremony_family_editorial_complete'] and family['complete_actual_hold_rechecks'] == 126
    assert family['prose_revisions'] == 30 and family['retained_wordings'] == 22
    assert len(family['records']) == 52 and len(scene['complete_holds']) == 4
    assert len(startup['seven_complete_frame_pairs']) == 7 and len(chant['complete_scene_holds']) == 8
    assert family['candidate_sha256'] == scene['candidate_sha256'] == startup['candidate_sha256'] == release['candidate_sha256']
    assert sha(Path(release['candidate']).read_bytes()) == release['candidate_sha256']
    assert sha(Path(release['patch']).read_bytes()) == release['patch_sha256']
    for path,digest in read('translations/lil_cliff_editorial_release_v1.json')['dependencies'].items():
        assert sha(Path(path).read_bytes()) == digest
    ledger = read(LEDGER)
    if not (ROOT/'editorial_ledger_before_v829.json').exists():
        shutil.copyfile(LEDGER,ROOT/'editorial_ledger_before_v829.json')
    ceremony_id = 'Religious-ceremonies-64-289-295-1200-1244-final'
    if not any(f['id'] == ceremony_id for f in ledger['completed_editorial_families']):
        existing = {n for f in ledger['completed_editorial_families'] for n in f['native_message_IDs']}
        ids = {r['message_id'] for r in family['records']}
        assert len(existing) == 550 and not existing & ids
        ledger['completed_editorial_families'].append(dict(id=ceremony_id,native_message_IDs=sorted(ids),
            records=family['records'],final_review=str(final_path),family_editorial_complete=True,
            whole_game_or_route_completion=False))
    cliff_id = 'Lil-SC2-B294-R73-previously-omitted-native-message'
    if not any(f['id'] == cliff_id for f in ledger['completed_editorial_families']):
        row = copy.deepcopy(read('translations/lil_cliff_editorial_v1.json')['records'][0])
        row.update(decision='revised-and-integrated',file_path='/data/SC2.DK4',
            completed_candidate_reference=release['candidate'],actual_scene_proof=str(ROOT/'actual_cliff_scene_and_transition_verification.json'))
        ledger['completed_editorial_families'].append(dict(id=cliff_id,native_message_IDs=[],
            route_record_IDs=['SC2:B294:R73'],records=[row],whole_B293_B294_editorial_complete=False))
    all_records = [r for f in ledger['completed_editorial_families'] for r in f['records']]
    decisions = Counter(r['decision'] for r in all_records)
    revised = sum(n for name,n in decisions.items() if name in ('revise','revised-and-integrated'))
    retained = sum(n for name,n in decisions.items() if name.startswith('retain'))
    assert (len(all_records),revised,retained) == (603,438,165)
    ledger['records_editorially_completed'] = 603
    ledger['records_revised_and_integrated'] = revised
    ledger['retained_wordings_editorially_completed'] = retained
    ledger['records_with_source_and_prose_pass'] = 606
    ledger['records_with_source_prose_drafts'] = 606
    ledger['completed_editorial_record_counts_by_file'] = {'/COMMON/MESFILE.DK4':602,'/data/SC2.DK4':1}
    ledger['source_prose_reviewed_counts_by_file'] = {'/COMMON/MESFILE.DK4':605,'/data/SC2.DK4':1}
    ledger['reviewed_but_incomplete_COMMON_IDs'] = [750,751,752]
    ledger['latest_checkpoint'] = SUMMARY
    ledger['goal_status'] = 'active'
    ledger['full_goal_complete'] = False
    ledger.setdefault('previous_current_integrated_candidate_V803',copy.deepcopy(ledger['current_integrated_candidate']))
    current = dict(path=release['candidate'],sha256=release['candidate_sha256'],profile='all-routes-unified-v829',
        MESFILE_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],patch=release['patch'],
        patch_sha256=release['patch_sha256'],manifest='out/all_routes_combined_v829_candidate.manifest.json',
        status='experimental-Ceremony52-and-one-cliff-record-editorially-verified',details=str(DOC),
        full_goal_complete=False)
    ledger['current_integrated_candidate'] = current
    ledger['next_integrated_profile_for_goal_continuation'] = 'all-routes-unified-v829'
    ledger['source_pins'].setdefault('initial_review_target',copy.deepcopy(ledger['source_pins']['current']))
    ledger['source_pins']['current'] = {k:current[k] for k in ('path','sha256','MESFILE_sha256','ARM9_sha256')}
    pending = ledger['pending_registered_ceremony_candidate']
    pending['status'] = 'completed-at-V829;all52-source-and-actual-message-review-gates-complete'
    pending['completion_proof'] = str(final_path)
    pending['new_editorial_completion_credit'] = 52
    pending['completed_candidate'] = current
    for finding in ledger.get('additional_editorial_findings_v827',[]):
        if finding['id'] == 'SC2-B294-R73-untranslated-cliff-line':
            finding['status'] = 'completed-V829'
            finding['resolution'] = 'Exact raw source resolution,original94 mapping and natural-dialogue-v2 repair;actual aligned glyphs and normal transitions verified.'
            finding['completion_proof'] = str(ROOT/'actual_cliff_scene_and_transition_verification.json')
    ledger['raw_source_coverage_revisit'] = dict(status='open-before-whole-goal-completion',
        reason='The old B293-B294 complete-scope claim counted only decoded CSV rows and missed a real native94 speech record.',
        next_action='Inventory raw native story objects and decoder-rejected segments;classify text/controls from source consumers before claiming route completeness.',
        do_not_globally_strip_ambiguous_Shift_JIS_leading_bytes=True)
    save(LEDGER,ledger)
    DOC.write_text('''# V829: ceremony family complete and missing cliff dialogue repaired

'''+SUMMARY+'''

## Completed editorial work

The ceremony family covers COMMON 64,289,290,291,293,294,295 and1200-1244.
All52 clean Japanese source records, meanings, speaker contexts, approved names,
runtime substitutions and English paragraphs were reviewed. Thirty wordings were
revised and22 retained. Fifty-one records were re-encoded in the earlier V809
production layer; that storage count is not the prose-revision count. Unchanged64
retains its original single-row rendering. Frozen production manuscripts remain
intact; `translations/ceremony_editorial_final_review_v1.json` supersedes their
historical pending-playback status with per-record final evidence.

All126 actual dialogue holds were freshly checked against V829's unchanged
COMMON, native formatter and game font. Every complete native and independently
decoded font plane equals the actual dark-ink and blank-paper pixels; templates,
resident blocks, margins, first/final letters, names and bounds agree. All52
unique message IDs have an actual sample, including distinct real-captain
reactions. These are targeted scenes and native branch/context contracts, not
every possible input sequence or complete route playthroughs.

Lil's last site chant is reached through original gameplay after granting the
source-verified Cave Village Map164 through its original inventory transfer.
The original guide and fog events run; a disclosed calendar input places the
ceremony on its actual feast day. No speaker, captain, script, random seed,
quest outcome or ceremony text is supplied by a fixture. All eight dialogue
holds, the original192-tick return, and two additional Lil growth holds pass.
Earlier original scheduler-RNG timing findings remain documented in
`ceremony_random_cause_v824_checkpoint.md`; the strict all-frame trace failures
are retained with their actual scope and are not relabelled as passes.

## The omitted cliff record

Current and clean SC2 B294 R73 have a48-byte native message beginning with94.
The old whole-record CP932 decoder rejects it, so the V110 CSV-derived claim of
complete B293-B294 translation omitted a real line. The original live resident
block and wrapped text establish the one-byte presentation prefix, and the
existing Lil route profile already maps94 to the guide state. The Guildmaster
portrait/caption remains intact.

Japanese: 決意はかたいようだな / 他でもねえ。あんたのためだ

English: You're set on it, huh? Just for you, then.

This is one logical natural-dialogue-v2 paragraph with an automatic protected
break and four padding bytes. It preserves firm resolve and the personal favor
without inventing a promise to do Lil's climb. The actual two rows share native
x16; every letter and punctuation mark is present. The repaired hold and the
following three original dialogue holds have exact complete native/independent
font planes. A single A advances to the original next record, with no blank page,
and the scene returns to town with its calendar unchanged. The static preview's
conservative continuation indent is not an instruction to add alignment spaces;
the live progressive consumer correctly consumes its guard.

## Source safety and combined build

The new raw source resolver is explicit opt-in: exact file/record bytes, one
already mapped route speaker prefix, fixed natural-dialogue-v2, decodable
Japanese body, no unmapped embedded controls and explicit retained speaker.
Normally decodable rows keep the ordinary resolver. Thirteen focused tests pass,
including real Shift-JIS94 text leads and negative source/prefix/control cases.
All98 original V110 materialized rows remain identical.

Adding this row before the frozen historical transforms initially failed the
original complete-route source guard. That failure is preserved in `build.log`.
The final registered profile builds the historical470 batches and all114 accepted
layers unchanged, then applies the reviewed fixed message through a late stage.
That stage repeats normal dialogue QA, locks complete current/target files and
runtime components, preserves the original native header and actor, and rejects
every change outside the selected body. Source, record and target negative cases
all fail without partial mutation. No historical guard is removed or waived.
Immutable feature modules remain hash dependencies; the evolving generic builder
and materializer are archived as provenance instead of preventing later features.

Compared with V820, only body bytes inside this48-byte SC2 message slot change.
Every other file/component, all existing translations and graphics, the native
actor byte, all following command addresses, ARM9 and COMMON are exact. The
late batch is listed in the final471-batch manifest. Seven ordinary cold-boot
startup/New Game screens match V820 pixel-for-pixel with the same options and
input schedule, without a save, savestate or fixture.

ROM: `out/all_routes_combined_v829_candidate.nds`

SHA-256: `641d4a9dfd4dee5ca66fc89fe242cc36f9f3373d773510011b6f5898af45e66d`

Patch: `out/all_routes_combined_v829_candidate.xdelta`

The patch reconstructs that ROM byte-exactly from the hash-pinned clean source.
The ROM remains experimental; the user-accepted canonical baseline is unchanged.

## Progress and remaining scope

The ledger now has603 completed entries:602 COMMON entries plus the new SC2
route review. The438 revised and165 retained counts are wording decisions.
606 entries have source/prose review; older COMMON750-752 are the three reviewed
drafts still awaiting completion. This is not the denominator for the whole game.

Next work includes those older contexts, remaining shared1245+ prose and every
remaining route/player-facing editorial review. Raw/native-object coverage must
account for decoder-rejected records before any whole-route completeness claim.
The previously found Angelo/sulfur wording and route indentation leads remain
open. The graphics audit, all18 plaques, earlier Online-body exclusion and retained
brown marks are unchanged. The full editorial goal remains active.

The first final-family counter check incorrectly expected51 wording revisions;
the frozen source manuscript proves30 revisions and22 retentions. That bookkeeping
assumption was corrected, and all source and126 actual display checks then passed.
An earlier release-check assertion also needed normal Windows path normalization;
it did not expose a ROM defect. Final binary, negative-guard, patch, scene and
ordinary-startup evidence is recorded separately and archived on E:.
''',encoding='utf-8')
    heading = '## V829: ceremony52 complete;omitted cliff dialogue repaired'
    for name in ('translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md'):
        path = Path('docs')/name
        text = path.read_text(encoding='utf-8')
        if heading not in text:
            path.write_text(text+'\n\n'+heading+'\n\n'+SUMMARY+' See [V829 completion evidence](editorial_v829_completion.md).\n',encoding='utf-8')
    for name in ('lil_sc2_b293_b294_control_note.md','all_routes_unified_lil_v110_checkpoint.md'):
        path = Path('docs')/name
        text = path.read_text(encoding='utf-8')
        heading = '## Coverage correction from V829 actual playback'
        if heading not in text:
            path.write_text(text+'\n\n'+heading+'\n\nThe historical complete-scope claim counted exported decodable rows. A real native speech record,SC2 B294 R73 with presentation94,was omitted by whole-record CP932 decoding and remained Japanese. V829 repairs it with exact source controls and actual display/transition verification. Further raw/native-object coverage is required before broader completeness claims. See [V829 evidence](editorial_v829_completion.md).\n',encoding='utf-8')
    path = Path('docs/natural_dialogue_workflow.md')
    text = path.read_text(encoding='utf-8')
    heading = '## Decoder-rejected native speech and late editorial layers'
    if heading not in text:
        path.write_text(text+'\n\n'+heading+'''

Decoded CSV counts alone do not prove source coverage. V829 actual playback found
SC2 B294 R73,whose mapped94 presentation byte makes whole-record CP932 decoding
fail. Inventory raw native objects and rejected segments;classify text versus
technical data from original consumers. Never globally strip a Shift-JIS lead.
For a proven otherwise-missing fixed native message,a v2 record may declare
`raw_source` with its complete exact `hex` and one `presentation_prefix_hex`.
The route profile and actual preamble effect must already be mapped. Ordinary
decodable records stay on the normal resolver;do not reinterpret genuine Japanese
leading glyphs as state. The resolver fails on unmatched bytes,unknown prefixes
and embedded unmapped controls. Speaker markup remains explicit and preserved.

Frozen complete-route transforms retain their original inputs. A registered
`late_story_editorial_release` can apply source-reviewed fixed native messages
after those transforms,with normal natural-dialogue QA,complete current/target
hash locks,original message headers/actors and all other bytes/command addresses
preserved. Its batch is listed in the final manifest. Do not weaken an old source
guard to force a new dialogue batch into an earlier stage. See V829 for the exact
source/control,negative-case and actual rendering evidence.
''',encoding='utf-8')
    # Finalized native screenshots are copied byte-exactly for later guide use.
    guide = Path('E:/Rota Nova translations/Screenshots/Guide candidates/V829 Ceremony completion and cliff repair')
    guide.mkdir(parents=True,exist_ok=True)
    selected = [(r,f'Ceremony_{r["message_id"]}_{r["frame"]:06d}.png') for r in chant['complete_scene_holds'] if r['message_id'] in (1224,1225,290)]
    growth = chant['extra_growth_holds'][1]
    selected.append((growth,'Lil_Wits_growth_016800.png'))
    selected += [(r,f'Cliff_SC2_R{r["record"]:04d}_{r["frame"]:06d}.png') for r in scene['complete_holds'] if r['record'] in (73,76)]
    return_path = Path(scene['complete_holds'][0]['capture']['path']).parent/'frame_011400_navigation.png'
    selected.append((dict(capture=dict(path=str(return_path))),'Cliff_normal_town_return_011400.png'))
    images = []
    for row,name in selected:
        source = Path(row['capture']['path'])
        target = guide/name
        shutil.copyfile(source,target)
        assert sha(source.read_bytes()) == sha(target.read_bytes())
        images.append(dict(source=str(source),archived=str(target),sha256=sha(target.read_bytes())))
    assert len(images) == 7
    save(guide/'capture_manifest.json',dict(images=images,
        ceremony_capture_source_ROM='V820;ceremony bytes,native code,font and assets exact inV829',
        cliff_capture_source_ROM='Registered V829',map_calendar_access_fixtures_disclosed_not_earned_campaign=True,
        original_pixels_no_rescaling_or_editing=True,graphics_audit_not_completed=True))
    sheet = Image.new('RGB',(3*256,3*408),'#202830')
    draw = ImageDraw.Draw(sheet)
    for i,row in enumerate(images):
        x,y = i%3*256,i//3*408
        draw.text((x+4,y+4),Path(row['archived']).stem[:35],fill='white')
        sheet.paste(Image.open(row['source']).convert('RGB'),(x,y+24))
    sheet.save(ROOT/'final_native_capture_review.png')
    source_programs = [Path(p) for p in (
        'scripts/build_integrated_release.py','dk4tool/patch/late_story_editorial.py',
        'dk4tool/script/raw_dialogue_source.py','dk4tool/script/translation_batch.py',
        'scripts/verify_cliff_release_v829.py','scripts/verify_ceremony_and_cliff_v829.py',
        'scripts/final_review_ceremony_v829.py','scripts/native_ceremony_map_fixture_v828.py',
        'scripts/run_ceremony_capture_v828.py','tests/test_raw_dialogue_source.py')]
    save(ROOT/'source_program_manifest.json',dict(programs=[dict(path=str(p),sha256=sha(p.read_bytes())) for p in source_programs],
        old_frozen_production_modules_and_manuscripts_unmodified=True,full_goal_complete=False))
    archive = Path('E:/Rota Nova translations/Editorial review/V829 Ceremony completion and cliff repair')
    archive.mkdir(parents=True,exist_ok=True)
    sources = [DOC,LEDGER,final_path,Path(__file__),Path('translations/lil_cliff_editorial_v1.json'),
        Path('translations/lil_cliff_editorial_release_v1.json'),Path('translations/release_stack.json'),
        Path('out/all_routes_combined_v829_candidate.manifest.json'),*source_programs,*ROOT.glob('*.json'),ROOT/'final_native_capture_review.png']
    artifacts = []
    for source in sources:
        sub = 'programs' if source.suffix == '.py' else 'verification' if source.parent == ROOT else 'checkpoint'
        target = archive/sub/source.name
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(source,target)
        assert sha(source.read_bytes()) == sha(target.read_bytes())
        artifacts.append(dict(source=str(source),archived=str(target),sha256=sha(target.read_bytes())))
    save(archive/'archive_manifest.json',dict(artifacts=artifacts,guide_candidates=images,
        candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],patch=release['patch'],
        patch_sha256=release['patch_sha256'],completed_ceremony_records=52,completed_cliff_records=1,
        total_completed=603,revised=438,retained=165,source_prose_reviewed=606,reviewed_pending_COMMON_IDs=[750,751,752],
        full_goal_complete=False))
    print('V829 recorded:ceremony52 complete+one repaired cliff record;603 completed/606 reviewed;full goal active. Archived7 guide captures.',flush=True)


if __name__ == '__main__':
    main()
