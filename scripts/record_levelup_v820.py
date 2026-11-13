"""Record the scoped formatting repair without crediting the unfinished goal."""

import copy
import shutil
from pathlib import Path

from PIL import Image,ImageChops

from dk4tool.patch.grand_race_menu_release import sha
from scripts.levelup_format_runtime_v819 import ROOT
from scripts.verify_village_wrap_v608 import read,save

ROM=Path('out/all_routes_combined_v820_candidate.nds')
LEDGER=Path('translations/editorial_review_current_v1.json')
DOC=Path('docs/levelup_format_v820_checkpoint.md')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193')
SUMMARY=('V820 repairs the shared compound-stat level-up consumer:complete stat names and numbers occupy aligned rows;'
    'the maximum six-row notice uses the original four-plus-two pager without an extra blank page.'
    '634 header,4095 compound,48 full-parent contracts and63 full native font planes pass.'
    'Two actual ordinary stat holds,17 complete-screen controls and19 persistent-state/PRNG pairs pass;'
    'a separately labeled forced-growth ROM verifies four actual page holds and return.'
    'Neither test-only instruction is in V820. The registered ROM is byte-identical to the ordinary-scene tested ROM;'
    '470 inherited batches,114 accepted layers,all3668 COMMON messages and every route/graphics asset are preserved.'
    'Exact clean-input patch and seven ordinary startup/New Game frames pass.'
    'V818 four-row reflow failed the genuine six-stat case and was never integrated.'
    'The post-climb world-state mismatch,other protagonist reactions,older750-752 and wider editorial work remain open.'
    '550 completed/605 source-prose/55 pending unchanged;no prose completion credit;graphics audit separate;goal active.')


def main():
    proof=read(ROOT/'registered_release_verification_v820.json')
    assert proof['candidate_sha256']==sha(ROM.read_bytes()) and proof['clean_input_reconstruction_byte_exact']
    a,b=[read(CAP/name/'capture_report.json') for name in ('ceremony_v809_newgame','levelup_v820_registered_newgame_matching_options')]
    assert b['ROM_sha256']==proof['candidate_sha256'] and b['frames']==4000
    assert a['scripted_input_schedule']==b['scripted_input_schedule'] and a['core_options']==b['core_options']
    assert b['cold_boot'] and not b['savestate_loaded'] and not b['callback_errors'] and not b.get('battery_save_preloaded')
    frames=[{r['frame']:r for r in d['frames_captured']} for d in (a,b)];pairs=[]
    for f in (1,60,180,1600,2000,3200,4000):
        x,y=[d[f] for d in frames]
        assert all(sha(Path(r['path']).read_bytes())==r['PNG_sha256'] for r in (x,y))
        assert ImageChops.difference(Image.open(x['path']).convert('RGB'),Image.open(y['path']).convert('RGB')).getbbox() is None
        pairs.append(dict(frame=f,whole_two_screen_pixels_equal_V809=True,capture=y))
    save(ROOT/'registered_newgame_verification_v820.json',dict(candidate_sha256=proof['candidate_sha256'],
        original_ROM=a['ROM'],capture_reports=[str(CAP/n/'capture_report.json') for n in ('ceremony_v809_newgame','levelup_v820_registered_newgame_matching_options')],
        seven_complete_frame_pairs=pairs,no_save_state_battery_or_fixture=True,
        targeted_emulator_startup_and_New_Game_not_hardware_or_route_completion=True))
    template='''# V820: level-up result alignment and pagination

{summary}

## Source and English

Clean COMMON335 is `%s、レベルアップ！！`; retained English is `%s leveled up!!`.
Clean336 is `%sが\\n%s上がりました！`; retained English is `%s increased by %s!`.
These are appropriate concise system notices; the source's emphatic double
exclamation is retained. No new prose, substitutions or stat names are introduced.
The separate97 popup header remains unchanged and is not newly approved editorially.

The original CActor builder0207E2E8 assembles the two possible growth groups in
native order0..5. All12 original class rows agree with clean source; the computed
gain range is0..3. Positive gains form up to six independently formatted stat rows,
each followed by a bare LF in the original768-byte local array. Actual V815/V816
captures showed split Agility/Luck despite intact source strings.

## Repair and boundaries

Only source-owned0207E3A8..0207E444 (156 bytes) and the four-byte call at0207E56C
change. The alternate97 header is instruction-set repacked, preserving its final
original ARM call and arguments. A private62-byte guard copies the raw result to
offset240 inside the same local array, adds the native first/continuation guards,
and removes the trailing LF. Maximum input/output is141/151 bytes; the copied
result ends at byte392, within768. No generic paragraph formatter changes.
Every staged section,123040-byte payload,cache,BSS,arena and allocation is exact.

V818's earlier balanced paragraph adapter could not handle all six rows within its
four-row cap. It remains failed research and is absent from the registered build.

## Verification

- 634 complete alternate-header instruction/rectangle/argument cases; external
 manager,bounds,name,COMMON97 and printf returns are declared I/O boundaries.
- 4095 nonempty gain combinations plus three empty/disabled source-tail controls.
 Complete words,numbers,ABI,PRNG and buffer guards pass;63 complete native fonts
 and seven two-page native font cases preserve full text and blank planes.
- 48 whole original CActor builder calls use original class growth,RNG,setters,
 fullwidth numbers,printf,strcat and post-growth effects. Both modal335 and popup97
 branches are covered with declared blocking-UI/audio boundaries. All8MiB outside
 the owned code and function/callee stack is exact, including persistent state.
- Ordinary Temple replay:two complete stat notices,17 whole-screen controls and19
 actor/town/items/goods/models/tasks/funds/calendar/PRNG pairs match V809. Only the
 two intended text bodies differ. A read-only native-state export reproduces the
 same6600-frame full4MiB and screenshot exactly.
- Separate synthetic display fixture:two test-only original instructions force six
 ID rows and gain3. Four actual holds show four rows then two for Hodram and Charles;
 A advances to the next actor and then town without blank pages. This does not
 establish earned levels or ordinary world outcomes. Both fixture instructions
 are absent from V820. Fixture screenshots are labeled as testing evidence.
- Registered V820 is byte-for-byte identical to the ordinary-scene tested repair
 ROM. Seven actual startup/New Game frames match V809, without saves or fixtures.
- 470 batches/114 accepted layers and prior profiles are exact. Every3668 COMMON
 entry,including repaired676/677,all route/help/graphics files and ARM7 is exact to
 V809. Only the permitted160-byte ARM9 code area can differ. The clean-input patch
 reconstructs every ROM byte. No hardware or full-playthrough claim is made.

## Candidate identity

- Candidate: `{rom}`
- SHA-256: `{rom_sha}`
- Profile: `all-routes-unified-v820` (experimental)
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`
- Canonical SHA-256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`
- Patch: `{patch}`
- Patch SHA-256: `{patch_sha}`
- Clean input SHA-256: `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`
- Internal delta from V809: `/__arm9__.bin` only; inherited canonical-base changes
 are recorded by the adjacent manifest.

## Remaining work

Continue from V820 so this formatting repair is retained. The V817 post-climb
world-state assertion is still failed; no claim of equivalence is made there.
The14 other-protagonist ceremony reactions and final family approval remain.
Older750-752,source-confirmed Angelo/sulfur wording findings,all-route and remaining
player-facing prose continue under the full editorial goal. Formatting remains an
ongoing per-consumer audit. The graphics audit and18 plaques remain incomplete.
No canonical promotion or additional editorial-completion credit is granted here.
'''
    DOC.write_text(template.format(summary=SUMMARY,rom=ROM,rom_sha=proof['candidate_sha256'],patch=proof['patch'],patch_sha=proof['patch_sha256']),encoding='utf-8')
    ledger=read(LEDGER)
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    assert (ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass'])==(550,605)
    backup=ROOT/'editorial_ledger_before_v820.json'
    if not backup.exists():shutil.copyfile(LEDGER,backup)
    detail=dict(status='registered-and-targeted-gameplay-verified;user-acceptance-pending',
        path=str(ROM),sha256=proof['candidate_sha256'],profile='all-routes-unified-v820',
        manifest=str(ROM.with_suffix('.manifest.json')),verification=str(ROM.with_suffix('.verification.json')),
        patch=proof['patch'],patch_sha256=proof['patch_sha256'],ARM9_sha256=proof['ARM9_sha256'],
        MESFILE_sha256=proof['COMMON_sha256'],documentation=str(DOC),new_editorial_completion_credit=0,
        broader_ceremony_world_state_failure_unresolved=True,full_goal_complete=False)
    ledger['latest_registered_formatting_candidate']=detail
    if 'previous_registered_ceremony_candidate_V809' not in ledger:
        ledger['previous_registered_ceremony_candidate_V809']=copy.deepcopy(ledger['pending_registered_ceremony_candidate'])
    ledger['pending_registered_ceremony_candidate'].update({k:v for k,v in detail.items() if k!='status'})
    ledger['pending_registered_ceremony_candidate']['status']='inherits-V809-ceremony-with-repaired-levelup-format;post-climb-state-gate-failed;whole-family-pending'
    ledger['next_ceremony_source_packet']['registered_candidate']=str(ROM)
    ledger['next_ceremony_source_packet']['registered_verification']=str(ROOT/'registered_release_verification_v820.json')
    ledger['next_integrated_profile_for_goal_continuation']='all-routes-unified-v820'
    for row in ledger['findings']:
        if row['id']=='COMMON335-336-compound-stat-word-splitting':
            row.update(status='scoped-consumer-repaired-integrated-and-targeted-gameplay-verified-V820',
                repair_proof=str(ROOT/'registered_release_verification_v820.json'),
                ordinary_gameplay=str(ROOT/'temple_gameplay_verification.json'),
                maximum_synthetic_display_proof=str(ROOT/'six_stat_actual_pagination.json'),
                no_completion_credit=True,
                detail='Aligned complete stat rows;original native four-plus-two pagination confirmed under separate six-stat testing fixture. Generic formatters unchanged;global audit remains open.')
            ledger['formatting_watchlist']['open_actual_levelup_word_split']=copy.deepcopy(row)
    ledger['formatting_watchlist']['latest_levelup_formatting_repair']=detail
    ledger['formatting_watchlist']['reference_case']+=' V820 preserves all676/677 text bytes;the separate level-up word-splitting consumer is now repaired and actual-display verified. The global formatting audit remains open.'
    ledger['latest_checkpoint']=SUMMARY
    ident='V819-V820-levelup-format-repair'
    if not any(r['id']==ident for r in ledger['research_checkpoints']):
        ledger['research_checkpoints'].append(dict(id=ident,documentation=str(DOC),new_ROM=True,
            new_source_prose_reviewed=0,new_editorially_completed=0,full_goal_complete=False))
    save(LEDGER,ledger)
    for name in ('translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md'):
        p=Path('docs')/name;s=p.read_text(encoding='utf-8');heading='## V820: shared level-up formatting repair verified'
        if heading not in s:p.write_text(s+'\n\n'+heading+'\n\n'+SUMMARY+' See [V820 evidence](levelup_format_v820_checkpoint.md).\n',encoding='utf-8')
    archive=Path('E:/Rota Nova translations/Editorial review/V820 Level-up formatting');archive.mkdir(parents=True,exist_ok=True)
    sources=[DOC,LEDGER,Path(__file__),Path('translations/levelup_stat_format_release_v1.json'),
        Path('dk4tool/patch/levelup_stat_format.py'),ROM.with_suffix('.manifest.json'),ROM.with_suffix('.verification.json'),
        *(Path('scripts')/name for name in ('levelup_format_runtime_v819.py','verify_levelup_runtime_v819.py',
            'verify_levelup_gameplay_v819.py','prepare_levelup_display_fixture_v819.py','verify_levelup_release_v820.py')),
        *ROOT.glob('*.json')]
    artifacts=[]
    for source in sources:
        sub='verification' if source.parent==ROOT else 'scripts' if source.parent==Path('scripts') else 'checkpoint'
        target=archive/sub/source.name;target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(source,target);assert sha(source.read_bytes())==sha(target.read_bytes())
        artifacts.append(dict(source=str(source),archived=str(target),sha256=sha(target.read_bytes())))
    pictures=Path('E:/Rota Nova translations/Screenshots/Test fixtures/V820 Level-up formatting');pictures.mkdir(parents=True,exist_ok=True)
    ordinary=read(ROOT/'temple_gameplay_verification.json')['complete_stat_holds']
    synthetic=read(ROOT/'six_stat_actual_pagination.json')['complete_actual_page_holds']
    images=[]
    for kind,rows in (('ordinary_scene',ordinary),('SYNTHETIC_six_stat_display',synthetic)):
        for row in rows:
            source=Path(row['capture']['path']);target=pictures/f'{kind}_{row["frame"]:06d}.png';shutil.copyfile(source,target)
            assert sha(source.read_bytes())==sha(target.read_bytes())
            images.append(dict(source=str(source),archived=str(target),sha256=sha(target.read_bytes()),test_scope=kind))
    save(pictures/'capture_manifest.json',dict(images=images,fixture_images_not_ordinary_campaign_or_final_guide_screenshots=True,
        ordinary_proof=str(ROOT/'temple_gameplay_verification.json'),synthetic_proof=str(ROOT/'six_stat_actual_pagination.json')))
    save(archive/'archive_manifest.json',dict(artifacts=artifacts,images=images,candidate=detail,
        full_goal_complete=False,canonical_baseline_not_promoted=True))
    print('V820 recorded and archived: scoped formatting finding repaired;550 complete/605 source-prose/55 pending unchanged. Goal active;climb state issue and graphics audit remain open.',flush=True)


if __name__=='__main__':main()
