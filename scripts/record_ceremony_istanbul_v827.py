"""Record four real preparation variants and the still-open cliff access lead."""

import shutil
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_ceremony_istanbul_v827 import ROOT, CAP
from scripts.verify_village_wrap_v608 import read, save

LEDGER = Path('translations/editorial_review_current_v1.json')
DOC = Path('docs/ceremony_istanbul_v827_checkpoint.md')
SUMMARY = (
    'V827 verifies the actual Rafael, Lil and Maria preparation scenes in unchanged V820: '
    '18 complete native/independent/actual font holds, nine clean-source records, four new '
    'reactions (1211/1213/1214/1217), three original 48-tick town returns and two additional '
    'complete Rafael level-up holds. Ceremony display coverage is 51/52 IDs. '
    'Lil site chant 1224 remains pending: the original Gate event requires a map after '
    'the rockfall/cliff briefing. The attempted entry is excluded from ceremony credit. '
    'An actual untranslated Japanese line is confirmed at SC2 B294 R73 with leading94; '
    'its raw bytes match clean source, and ordinary CP932 record enumeration skips it. '
    'Control-aware review and lossless raw-segment coverage remain necessary. '
    'Older Angelo wording and route indentation leads are retained. Reusable original-event '
    'Istanbul saves cold-reload correctly; no captain, dialogue, code or random state was substituted. '
    'V820 ROM/patch/registry and all production text remain unchanged. Ledger totals stay '
    '550 complete/605 source-prose/55 pending. Final ceremony review, the full editorial goal '
    'and the separate graphics audit remain unfinished.'
)


def main():
    proof_path = ROOT/'four_preparation_variants_actual_verification.json'
    proof = read(proof_path)
    assert len(proof['complete_scene_holds']) == 18 and len(proof['source_context_reviews']) == 9
    assert proof['new_actual_variant_IDs'] == [1211,1213,1214,1217]
    assert len(proof['cumulative_distinct_actual_family_IDs']) == 51
    release = read('work/analysis/levelup_format_v819/registered_release_verification_v820.json')
    assert sha(Path(release['candidate']).read_bytes()) == release['candidate_sha256'] == proof['candidate_sha256']
    assert sha(Path(release['patch']).read_bytes()) == release['patch_sha256']
    assert read('out/all_routes_combined_v820_candidate.manifest.json')['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    for path,digest in read('translations/levelup_stat_format_release_v1.json')['dependencies'].items():
        assert sha(Path(path).read_bytes()) == digest, path
    assert read(ROOT/'Maria_normal_reload_verification.json')['ordinary_cold_boot_no_fixtures_or_savestate']
    assert read(ROOT/'Lil_cliff_normal_reload_verification.json')['ordinary_cold_boot_no_fixtures_or_savestate']
    # Both pre-ceremony reloads start normally, before the later Lil-only fixture.
    reloads = read(ROOT/'Rafael_Lil_normal_reload_identity_stage.json')['rows']
    for row in reloads:
        report = read(CAP/f'ceremony_{row["hero"]}_final_variants_v827'/'capture_report.json')
        assert report['cold_boot'] and not report['savestate_loaded']
        assert all(r['frame'] > 4000 for r in report.get('synthetic_condition_fixtures',[]))
        save_row = row['source_save']
        assert sha(Path(save_row['normal_save']).read_bytes()) == save_row['sha256']
        assert sha(Path(save_row['disposable_copy']).read_bytes()) == save_row['sha256']
    lead = read(ROOT/'actual_untranslated_cliff_event_lead.json')
    pair = [r for r in lead['exact_raw_current_and_clean_candidates'] if r['file'] == '/data/SC2.DK4']
    assert len(pair) == 2 and {r['image'] for r in pair} == {'clean','current'}
    assert pair[0]['raw_hex'] == pair[1]['raw_hex'] and all(r['prefix_hex'] == '94' for r in pair)
    ledger = read(LEDGER)
    assert ledger['goal_status'] == 'active' and not ledger['full_goal_complete']
    assert (ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass']) == (550,605)
    if not (ROOT/'editorial_ledger_before_v827.json').exists():
        shutil.copyfile(LEDGER,ROOT/'editorial_ledger_before_v827.json')
    ledger['latest_checkpoint'] = SUMMARY
    ledger['actual_ceremony_preparations_v827'] = dict(proof=str(proof_path),
        complete_scene_holds=18,extra_growth_holds=2,source_bound_records=9,
        new_actual_variant_IDs=proof['new_actual_variant_IDs'],
        cumulative_distinct_actual_family_IDs=proof['cumulative_distinct_actual_family_IDs'],
        remaining_actual_IDs=[1224],original_map_prerequisite_pending=True,
        whole52_family_pending=True,new_editorial_completion_credit=0,new_ROM=False,full_goal_complete=False)
    ledger['additional_editorial_findings_v827'] = [
        dict(id='SC2-B294-R73-untranslated-cliff-line',status='open-source-control-context-and-localization-review',
             proof=str(ROOT/'actual_untranslated_cliff_event_lead.json'),
             exact_current_and_clean_raw_record_equal=True,
             ordinary_CP932_record_enumerator_skips_segment=True,
             source94_presentation_state_must_be_mapped_before_authoring=True),
        dict(id='Angelo-and-Cappadocia-older-route-prose',status='open-natural-dialogue-v2-and-layout-review',
             proof=str(ROOT/'encountered_route_editorial_leads.json'),
             clean_same_ordinal_links_provisional_until_context_and_control_review=True),
    ]
    ledger['next_integrated_profile_for_goal_continuation'] = 'all-routes-unified-v820'
    save(LEDGER,ledger)
    DOC.write_text('''# V827: actual preparation variants and newly exposed route text

'''+SUMMARY+'''

## What was verified

| Captain | New preparation reaction | Subsequent reaction |
| --- | --- | --- |
| Rafael | 1211: Help? | 1216: ... (already sampled) |
| Lil | 1213: You mean help with the preparations? | 1217: (Ugh, what is this all about?) |
| Maria | 1214: Help out? | 1216: ... (already sampled) |

The clean Japanese for 1201,1210,1211,1213,1214,1215,1216,1217,291 matches the
frozen source references exactly. The current wording is retained after reading
each actual scene: Rafael and Maria ask tersely for clarification; Lil is more
expressive and then privately exasperated. No new prose, line breaks or padding
are authored. All 18 native font planes equal independently decoded fonts and
every actual dark-ink/blank-paper pixel in the complete text area. First/final
letters, punctuation, substitutions, line alignment, page bounds, resident
templates and full COMMON blocks pass. Actual original portraits and captions
are preserved. The result names the actual captain, never the old Hodram donor.

Each preparation scene returns normally after 48 ticks. Rafael also levels up:
his complete header and three aligned stat rows are checked against actual
pixels. Stamina rises by 2, Agility by 1, and Charm by 1, with no trailing blank
row or split words. Original ceremony code remains exact in the ROM and tested
RAM. The source-owned V820 stat fix remains unchanged.

## Actual access and saves

The three actual captains depart Athens normally. Authorized isolated calendar,
Istanbul facility/site-access and active-ship coordinate inputs then allow the
original docking and events. Each executed fixture receipt is recomputed against
its actual pre-input RAM. Only declared data bytes leave the private native
simulation; all 207 actors and the actual captain remain exact. No source code,
dialogue, speaker, random seed or ritual result is supplied. Earned travel or
elapsed daily simulation is not claimed.

The original Cappadocia arrival/Brass Lamp event plays. Rafael and Lil also play
Angelo's original recruitment event. Navigation uses ordinary buttons; fast B
pulses at the end receive no route text or full-glyph completion credit. All
original/disposable input donors retain their hashes. New original-event
Istanbul checkpoints are saved normally and cold-reloaded with the correct
captain, town 22 and native calendar. Maria reloads at 5506 ticks; Rafael/Lil
pre-ceremony reloads at 2596 ticks. Lil's later cliff-briefing save reloads at
3940 ticks. The dates include disclosed calendar test inputs.

## Remaining ceremony variant

The expected Lil site-chant sequence did not occur at frames 9200-15400. The
original Gate scene first reports a rockfall, introduces a cliff path, then asks
for a map. On re-entry the Guildmaster says he cannot guide Lil without one.
These are original route events and are excluded from ceremony coverage. The
last COMMON 1224 (Lil's Huh?) needs its actual site-chant context. Identify the
original map/access predicate, obtain the map normally or through the already
authorized isolated inventory fixture, then test the ordinary ceremony branch.
Do not replace the speaker, skip the predicate or manufacture a matching hold.
The normal cliff-briefing save is ready for this next step.

Display coverage is 51/52 ceremony IDs. No whole-family credit is granted until
1224 and the final source/prose/layout/eligibility/outcome review are complete.
Earlier strict random-state findings retain their original scope and failures.

## Actual untranslated Japanese and older route findings

Lil's cliff event displays Japanese at current `/data/SC2.DK4`, block 294,
NUL-segment 73, raw block offset 641 (the Japanese itself begins at 642). The
leading byte is 94; the following Japanese reads 決意はかたいようだな / 他でもねえ。あんたのためだ.
The complete raw current record equals the clean source record at the same
location. `/testdata/SC2.DK4` has the corresponding source variant at B295 R72.
This is an untranslated source record, not a new V827 ROM change.

The ordinary `iter_mesfile_records` parser skips this whole segment after its
CP932 decode fails. Its leading94 presentation/speaker state must be mapped
against the original consumer before authoring English. Do not strip an arbitrary
byte or treat that state as Japanese text. Record-only coverage based on decoded
rows is insufficient here. The full editorial audit must also account for raw
segments rejected by the decoder, classifying text versus technical data with
source/control evidence. This is added to the older record-check revisit work.

Exact raw source/current bytes, neighboring segments and the actual screenshot
are in `actual_untranslated_cliff_event_lead.json`. Separate exact current
references capture older Angelo and arrival dialogue, including the unnatural
Rafael response These aren't looks! and uneven route continuation indentation.
Their clean same-ordinal links are leads until full context/control review;
none is granted editorial completion credit or rewritten in this checkpoint.

## Artifact and completion scope

All screenshots and evidence stay on E:. The contact sheet is an inspection
composite; guide candidates retain byte-exact native screenshots. The Japanese
defect capture is audit evidence, not a finalized guide image. The ROM remains
V820, SHA-256 b8126bf14fd3aa0236c03ee48492a40eb0f2b50e77df5a16c3d6f92ea6bb2251.
Its exact patch, registry and frozen dependencies remain unchanged. The ledger
stays 550 completed / 605 source-prose reviewed / 55 pending, with no new whole
family credit. Remaining shared prose, all routes/player-facing text, older
750-752, the graphics audit and all 18 plaques remain open. These targeted
emulator checks do not establish a full route or hardware playthrough.
''',encoding='utf-8')
    heading = '## V827: four actual preparation variants and untranslated cliff finding'
    for name in ('translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md'):
        path = Path('docs')/name
        text = path.read_text(encoding='utf-8')
        if heading not in text:
            path.write_text(text+'\n\n'+heading+'\n\n'+SUMMARY+' See [V827 evidence](ceremony_istanbul_v827_checkpoint.md).\n',encoding='utf-8')
    pictures = proof['complete_scene_holds']+proof['extra_real_growth_holds']
    sheet = Image.new('RGB',(1024,5*408),'#202830')
    draw = ImageDraw.Draw(sheet)
    for i,row in enumerate(pictures):
        x,y = i%4*256,i//4*408
        draw.text((x+4,y+4),f'{row.get("hero","Rafael")} {row["frame"]} ID {row.get("message_id","growth")}',fill='white')
        sheet.paste(Image.open(row['capture']['path']).convert('RGB'),(x,y+24))
    sheet.save(ROOT/'complete_preparation_holds.png')
    guide = Path('E:/Rota Nova translations/Screenshots/Guide candidates/V827 Preparation scenes')
    guide.mkdir(parents=True,exist_ok=True)
    images = []
    for row in proof['complete_scene_holds']:
        if row['message_id'] not in (1211,1213,1214,1217,291):
            continue
        source = Path(row['capture']['path'])
        target = guide/f'{row["hero"]}_{row["message_id"]}_{row["frame"]:06d}.png'
        shutil.copyfile(source,target)
        assert sha(source.read_bytes()) == sha(target.read_bytes())
        images.append(dict(source=str(source),archived=str(target),sha256=sha(target.read_bytes())))
    row = proof['extra_real_growth_holds'][1]
    source = Path(row['capture']['path'])
    target = guide/'Rafael_three_aligned_stat_rows_007400.png'
    shutil.copyfile(source,target)
    assert sha(source.read_bytes()) == sha(target.read_bytes())
    images.append(dict(source=str(source),archived=str(target),sha256=sha(target.read_bytes())))
    assert len(images) == 8
    save(guide/'capture_manifest.json',dict(images=images,proof=str(proof_path),
        original_pixels_no_rescaling_or_editing=True,access_calendar_and_location_fixtures_disclosed=True,
        no_earned_campaign_or_full_graphics_approval_claim=True))
    archive = Path('E:/Rota Nova translations/Editorial review/V827 Preparation variants and cliff findings')
    archive.mkdir(parents=True,exist_ok=True)
    sources = [DOC,LEDGER,Path(__file__),ROOT/'complete_preparation_holds.png',*ROOT.glob('*.json'),
               Path('scripts/verify_ceremony_istanbul_v827.py'),Path('scripts/run_ceremony_capture_v827.py'),
               Path('scripts/native_ceremony_istanbul_fixture_v827.py')]
    sources += [CAP/f'ceremony_{h}_Istanbul_v827'/'capture_report.json' for h in ('Rafael','Lil','Maria')]
    sources += [CAP/f'ceremony_{h}_final_variants_v827'/'capture_report.json' for h in ('Rafael','Lil')]
    # Reports have the same filename; retain their source directory in the archive.
    artifacts = []
    for source in sources:
        sub = source.parent.name if source.name == 'capture_report.json' else 'checkpoint'
        target = archive/sub/source.name
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(source,target)
        assert sha(source.read_bytes()) == sha(target.read_bytes())
        artifacts.append(dict(source=str(source),archived=str(target),sha256=sha(target.read_bytes())))
    save(archive/'archive_manifest.json',dict(artifacts=artifacts,guide_candidates=images,
        candidate_sha256=proof['candidate_sha256'],production_ROM_patch_registry_unchanged=True,
        cumulative_actual_family_IDs=51,remaining_actual_family_IDs=[1224],
        whole_family_completion_credit=0,full_goal_complete=False))
    print('V827 recorded:51/52 ceremony IDs,4 new reactions,untranslated94 record retained as open work;8 guide captures archived;goal active.',flush=True)


if __name__ == '__main__':
    main()
