"""Record actual Lil ceremony evidence without granting whole-family credit."""

import shutil
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_ceremony_lil_v826 import ROOT, CAP
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/ceremony_lil_v826_checkpoint.md')
LEDGER = Path('translations/editorial_review_current_v1.json')
SUMMARY = (
    'V826 verifies actual Lil temple chanting and Parthenon dancing in unchanged V820. '
    'All 14 dialogue holds match complete native and independently decoded font pixels, '
    'including blank paper, margins, first and final characters, and the original Lil/Parthenon substitutions. '
    'All 13 distinct source records match the clean Japanese exactly. '
    'Lil-specific 1206, 1209 and 1229 retain natural, faithful wording with her actual portrait. '
    'The original scenes return to Athens after 48 and 192 ticks. '
    'Calendar/access fixtures preserve all actors and the actual captain; donor saves remain unchanged. '
    '47 of 52 ceremony IDs now have actual display samples; 1211, 1213, 1214, 1217 and 1224 '
    'and the final family review remain. No whole-family completion credit is granted. '
    'V820 ROM, patch, registry and production text are unchanged; 550 complete/605 source-prose/55 pending '
    'remains the ledger total. The full editorial goal stays active and graphics remain separately unfinished.'
)


def main():
    proof_path = ROOT/'actual_Lil_temple_and_dance_verification.json'
    proof = read(proof_path)
    assert len(proof['complete_scene_holds']) == 14 and len(proof['source_context_reviews']) == 13
    assert proof['new_distinct_actual_reaction_IDs'] == [1206,1209,1229]
    assert [r['original_tick_increment'] for r in proof['native_time_and_return']] == [48,192]
    release = read('work/analysis/levelup_format_v819/registered_release_verification_v820.json')
    assert sha(Path(release['candidate']).read_bytes()) == release['candidate_sha256'] == proof['candidate_sha256']
    assert sha(Path(release['patch']).read_bytes()) == release['patch_sha256']
    assert read('out/all_routes_combined_v820_candidate.manifest.json')['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    for path, digest in read('translations/levelup_stat_format_release_v1.json')['dependencies'].items():
        assert sha(Path(path).read_bytes()) == digest, path
    ledger = read(LEDGER)
    assert ledger['goal_status'] == 'active' and not ledger['full_goal_complete']
    assert (ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass']) == (550,605)
    covered = set(ledger['actual_ceremony_hero_fasting_v825']['cumulative_distinct_actual_family_IDs'])
    covered |= {r['message_id'] for r in proof['complete_scene_holds']}
    family = {r['message_id'] for r in read('translations/ceremony_editorial_manuscript_v2.json')['records']}
    missing = family-covered
    assert len(covered) == 47 and missing == {1211,1213,1214,1217,1224}
    backup = ROOT/'editorial_ledger_before_v826.json'
    if not backup.exists():
        shutil.copyfile(LEDGER, backup)
    ledger['latest_checkpoint'] = SUMMARY
    ledger['actual_ceremony_Lil_v826'] = dict(
        proof=str(proof_path), candidate_sha256=proof['candidate_sha256'],
        complete_scene_holds=14, source_bound_distinct_records=13,
        new_distinct_actual_reaction_IDs=[1206,1209,1229],
        cumulative_distinct_actual_family_IDs=sorted(covered), remaining_actual_IDs=sorted(missing),
        whole52_family_pending=True, new_editorial_completion_credit=0,
        new_ROM=False, full_goal_complete=False)
    ledger['next_integrated_profile_for_goal_continuation'] = 'all-routes-unified-v820'
    save(LEDGER, ledger)
    DOC.write_text('''# V826: Lil temple chanting and Parthenon dancing

'''+SUMMARY+'''

## Source and wording

The same actual Lil save cold-boots in V820. The native getter returns captain 2,
Lil Argot, in Athens (town and fleet town 19) throughout. The clean Japanese
source matches every byte of all 13 distinct records in these two exchanges.
The frozen production manuscript is retained; no new prose or manual line breaks
are authored. In the actual context, Lil's reactions are natural and faithful:

| ID | Japanese | Current English | Reason to retain |
| --- | --- | --- | --- |
| 1206 | 何なの！？ | What was that?! | An immediate startled response to the officiant's loud vocalization. |
| 1209 | へ？？？ | Huh??? | Preserves her exaggerated, bewildered interjection. |
| 1229 | 踊りって何よ？ | What do you mean, dancing? | Natural skeptical response to being told to join the dancers. |

The remaining officiant instructions and result narration were read in sequence.
Their current wording preserves the ritual actions, tone and party experience.
Lil's portrait and caption appear with her reactions; the officiant remains the
original NPC. No protagonist, speaker, dialogue, outcome or random seed is replaced.

## Complete display checks

Seven holds cover temple chanting: 1201, 1203, 1204, 1206, 1207, 1209 and 290.
Seven cover dancing: 1219, 1220, 1227, 1229, 1230, 1231 and 290.
For every hold, the complete native raster equals independent font decoding and
all actual dark-ink and blank-paper pixels across the text body. Leading and
trailing characters, punctuation, row alignment, line breaks and bounds pass.
Native parent formatting, original substitutions, the resident template and its
whole COMMON block agree. The result uses Lil's real name and the guard uses
Parthenon. There is no manual text positioning or padding fix in this checkpoint.

The full hold contact sheet is `work/analysis/ceremony_lil_v826/complete_holds.png`.
Its tiles preserve the native screenshot pixels. No composite is inserted into
the ROM. The underlying captures are the emulator framebuffer output.

## Eligibility, time and transitions

Athens' feast is day 21. Role 9 on that exact odd feast day selects temple
chanting; role 11 on day 21 selects the original Parthenon dance branch. The
calendar and facility mask are isolated, authorized test inputs, not earned
campaign progress or a simulation of elapsed days. The site was already discovered.
Every fixture is recomputed against its actual pre-input RAM and agrees with the
emulator receipt. All 207 actors and the captain are unchanged by those writes.

After a facility change, the town menu is rebuilt by ordinary Port entry/return;
native menu selection and the visible tooltip identify the facility before entry.
The ordinary scenes then advance time by 48 ticks (temple) and 192 ticks (dance)
and return to town. The recorded advance sequence has no extra blank page.
Original ceremony code remains identical to the clean source in the ROM and all
actual RAM snapshots. These are targeted scene checks, not a complete route or
hardware test. They do not replace the earlier strict random-state investigations.

## Run and artifact provenance

The 14,800-frame run cold-boots a verified disposable copy of the V825 Lil Athens
save, without a savestate. The original donor and disposable input still match
SHA-256 `5516ebd26a405612880984c1a1722b0a92a4b0db5f970371dc00a6ce1a13bebb`.
The first exec response accidentally omitted its session identifier. Input was
recovered through that same process's console using the normal harness JSON
protocol. The original run continued and stopped normally; it was not restarted
or replaced. The final capture report records every gameplay input and both
fixture receipts. No live emulator remains.

The first verifier run passed its checks but failed to write its report because
the new output directory was missing. Creating that directory resolved the
reporting error; the unchanged scene assertions then passed on rerun.

Five ceremony IDs remain: 1211 (Rafael preparations), 1213/1217 (Lil preparations),
1214 (Maria preparations), and 1224 (Lil site chanting). Use their actual captains
and exact original eligibility conditions. Only after those contexts and the
final family review may the 52-entry ceremony family receive completion credit.
Older 750-752, route findings, all remaining routes/player prose, the separate
graphics audit and all 18 plaques remain unfinished.
''', encoding='utf-8')
    heading = '## V826: actual Lil chanting and dancing verified'
    for name in ('translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md'):
        path = Path('docs')/name
        text = path.read_text(encoding='utf-8')
        if heading not in text:
            path.write_text(text+'\n\n'+heading+'\n\n'+SUMMARY+' See [V826 scene evidence](ceremony_lil_v826_checkpoint.md).\n', encoding='utf-8')
    # A contact sheet for inspection only; original guide files stay byte exact.
    sheet = Image.new('RGB', (4*256,4*408), '#202830')
    draw = ImageDraw.Draw(sheet)
    for i, row in enumerate(proof['complete_scene_holds']):
        x,y = (i%4)*256,(i//4)*408
        draw.text((x+4,y+4), f'{row["frame"]}: COMMON {row["message_id"]}', fill='white')
        sheet.paste(Image.open(row['capture']['path']).convert('RGB'), (x,y+24))
    sheet.save(ROOT/'complete_holds.png')
    guide = Path('E:/Rota Nova translations/Screenshots/Guide candidates/V826 Lil temple and dancing')
    guide.mkdir(parents=True, exist_ok=True)
    images = []
    for row in proof['complete_scene_holds']:
        if row['message_id'] not in (1206,1209,1229,290):
            continue
        source = Path(row['capture']['path'])
        target = guide/f'Lil_{row["message_id"]}_{row["frame"]:06d}.png'
        shutil.copyfile(source,target)
        assert sha(source.read_bytes()) == sha(target.read_bytes())
        images.append(dict(frame=row['frame'], message_id=row['message_id'], source=str(source),
            archived=str(target), sha256=sha(target.read_bytes())))
    assert len(images) == 5
    save(guide/'capture_manifest.json',dict(images=images, proof=str(proof_path),
        actual_Lil_portrait_and_complete_native_glyphs_verified=True,
        authorized_calendar_access_fixtures_not_earned_campaign=True,
        original_pixels_no_rescaling_or_editing=True, full_goal_complete=False))
    archive = Path('E:/Rota Nova translations/Editorial review/V826 Lil temple and dancing')
    archive.mkdir(parents=True, exist_ok=True)
    artifacts = []
    for source in [DOC,LEDGER,proof_path,ROOT/'complete_holds.png',CAP/'capture_report.json',
                   Path(__file__),Path('scripts/verify_ceremony_lil_v826.py'),
                   Path('scripts/send_headless_console_command_v826.py')]:
        target = archive/source.name
        shutil.copyfile(source,target)
        assert sha(source.read_bytes()) == sha(target.read_bytes())
        artifacts.append(dict(source=str(source),archived=str(target),sha256=sha(target.read_bytes())))
    save(archive/'archive_manifest.json',dict(artifacts=artifacts, guide_candidates=images,
        candidate_sha256=proof['candidate_sha256'], candidate_patch_registry_and_frozen_dependencies_unchanged=True,
        cumulative_actual_family_IDs=47, remaining_actual_family_IDs=sorted(missing),
        whole_family_completion_credit=0, full_goal_complete=False))
    print('V826 recorded:14 holds,3 new reactions,47/52 IDs sampled;five remain. Five guide captures archived;V820 unchanged;goal active.', flush=True)


if __name__ == '__main__':
    main()
