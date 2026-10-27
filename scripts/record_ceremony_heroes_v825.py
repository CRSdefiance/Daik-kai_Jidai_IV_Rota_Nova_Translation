"""Record six actual hero variants and retained64; whole family stays pending."""

import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/ceremony_heroes_v825')
LEDGER=Path('translations/editorial_review_current_v1.json')
DOC=Path('docs/ceremony_heroes_v825_checkpoint.md')
SUMMARY=('V825 verifies fasting with actual Rafael0,Maria3 and Lil2:24 complete scene/font holds,three unchanged64 refusal holds and allthree192-tick returns pass.'
    'Six previously outstanding reactions1233/1235/1236/1238/1240/1241 now have real captain portraits,native selected templates,full glyph/blank-plane and boundary evidence.'
    'A new Lil game reaches Amsterdam and saves normally without fixtures;its cold reload verifies Lil2.'
    'Allthree post-fast Athens games are saved and cold-reloaded with the correct captain,town19 and exact calendar ticks.'
    'Disposable copies protect all original donors;calendar/access/ship-coordinate fixtures preserve every actor and never replace speakers or dialogue.'
    'Temple assistance requires the exact feast day;the initial Athens22 preparation assumption is retracted.Off-day64 remains intact.'
    'Gate y165 was outside its native113..163 rectangle;verified234,140 hover is the navigation reference.'
    '44 of52 family message IDs now have actual display samples;8 variants and final family review remain.'
    'V820 ROM/patch/registry are unchanged;550 complete/605 source-prose/55 pending unchanged;editorial goal active and graphics audit separate.')


def main():
    proof=read(ROOT/'actual_hero_fast_and_retained64_verification.json')
    reload=read(ROOT/'normal_save_reload_verification.json')
    assert len(proof['complete_scene_holds'])==24 and len(proof['retained_refusal_holds'])==3
    assert len(proof['new_distinct_protagonist_reactions'])==6 and len(reload['rows'])==3
    assert all(r['native_four_day192_tick_advance'] for r in proof['original_time_and_return'])
    release=read('work/analysis/levelup_format_v819/registered_release_verification_v820.json')
    assert sha(Path(release['candidate']).read_bytes())==proof['sha256']==release['candidate_sha256']
    assert sha(Path(release['patch']).read_bytes())==release['patch_sha256']
    assert read('out/all_routes_combined_v820_candidate.manifest.json')['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    for p,h in read('translations/levelup_stat_format_release_v1.json')['dependencies'].items():assert sha(Path(p).read_bytes())==h,p
    ledger=read(LEDGER);assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    assert (ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass'])==(550,605)
    prior=set(ledger['actual_ceremony_Athens_v817']['cumulative_distinct_actual_IDs'])
    covered=prior|{r['message_id'] for r in proof['complete_scene_holds']}|{64}
    source=read('translations/ceremony_editorial_manuscript_v2.json')
    missing={r['message_id'] for r in source['records']}-covered
    assert len(covered)==44 and missing=={1206,1209,1211,1213,1214,1217,1224,1229}
    source_rows={r['message_id']:r for r in source['records']}
    reviewed=[]
    for n in proof['new_distinct_protagonist_reactions']:
        row=source_rows[n]
        reviewed.append(dict(message_id=n,Japanese=row['japanese'],English=row['english'],
            source_meaning=row['source_meaning'],localization_note=row['localization_note'],
            actual_hero_context_and_complete_native_display_now_verified=True,
            wording_retained_from_frozen_production_manuscript_not_reauthored=True))
    save(ROOT/'six_reaction_context_review.json',dict(records=reviewed,
        retained64_source_meaning=source_rows[64]['source_meaning'],
        retained64_English=source_rows[64]['english'],
        retained64_stern_terse_conditional_command_fits_off_day_officiant_context=True,
        native_single_row_origin0_verified_not_a_multiline_alignment_exception=True,
        new_whole_family_completion_credit=0))
    DOC.write_text('''# V825: actual Rafael, Maria and Lil fasting reactions

'''+SUMMARY+'''

## Actual protagonists and protected saves

The original native getter0207F244 verifies Rafael0,Maria3,Lil2. Original current
captain virtual names and notice names agree in every selected hold. Their actual
portraits and captions were visually inspected. No captain,actor,dialogue,speaker,
random seed or source code is replaced by the runtime fixtures.

Lil starts through the ordinary V820 New Game UI. The complete original opening
plays before a normal Amsterdam save. Its DSV has42840 non-FF cartridge bytes;
an ordinary cold reload returns captain2,Lil Argot,town2. Earlier V537 Lil files
were entirely FF and were not used as donors. Maria's older donor has documented
New Game/Hangzhou provenance through the previously authorized selection bypass;
that bypass is absent from the current ROM. Rafael's donor is likewise loaded
normally. All emulator inputs name verified disposable copies.

Automatic approval review initially rejected commands naming original Rafael and
Maria donor paths. No emulator started for those rejected commands. Explicit
byte-identical disposable copies resolved the concern. Original donor hashes are
checked again after testing;the harness also makes a separate working copy before
cold boot. New source saves are preserved separately from future disposable copies.

The only runtime fixture inputs are the original calendar word,Athens facility
mask,site7 discovery bit and active ship's eight coordinate bytes. Private native
preflights prove all207 actors and the current captain remain exact and confirm
the actual captain IDs before/after those inputs. Docking,introductory events,
NPC conversations,rite selection,results,growth and time then run in the game.
Access and the calendar jump are isolated testing inputs,not earned travel or
the simulation of elapsed days. No savestates are loaded.

## Display and English checks

Each captain has eight full fasting holds:1219,1220,1232,its first reaction,
1237,1230,its hunger reaction,and294 with the original captain-name argument.

| Captain | First reaction | Hunger reaction |
| --- | --- | --- |
| Rafael |1233: What?!|1238: (Stomach rumbles...)|
| Maria |1236: ... I suppose I have no choice.|1241: ...|
| Lil |1235: Whaaat?!|1240: (I'm so hungry...)|

Clean-source glosses and frozen production wording are retained;the new actual
contexts support the distinct youthful,exasperated and restrained reactions.
No source fact or voice is changed to simplify layout. All24 native font planes
equal independent decoding and actual full dark-ink/blank-paper planes. Native
parent dispatch,real substitutions,resident COMMON templates and whole decoded
blocks match. Leading/trailing letters,punctuation,spaces,rows and bounds pass.

The original unchanged64 refusal is also checked for allthree captains. Its raw
`No business? Leave now.` is a terse natural command matching用のない者は、即刻立ち去られよ.
It has one native row at origin0,without authored padding or an extra multiline
alignment rule. Complete source/native font and actual pixel planes agree.

## Time,return and durable checkpoints

Each accepted fast advances192 original ticks (four days). The actual captain,
native notice name,town19 and fleet town19 remain correct after the return.
The save UI then writes normally. Fresh fixture-free cold boots verify:

| Saved captain | Native captain | Town | Saved/reloaded ticks |
| --- | --- | --- | --- |
| Rafael |0|19|1202|
| Maria |3|19|4064|
| Lil |2|19|1202|

These are separate campaigns and their random results are not compared with one
another. The source-RNG investigation at V824 remains the reference for qualified
matching-input simulation checks. This checkpoint does not claim a full route,
hardware verification,or ordinary earned access.

Files under `E:/Rota Nova translations/Saves/Test fixtures`:

- `V825 Lil Amsterdam ordinary New Game.dsv` preserves the new unmodified start.
- `V825 Rafael Athens after fasting.dsv`
- `V825 Maria Athens after fasting.dsv`
- `V825 Lil Athens after fasting.dsv`

Adjacent evidence records every SHA-256,source report,disposable copy and cold
reload. Guide candidates retain native pixels and carry a fixture-scope manifest.

## Corrected navigation and eligibility assumptions

Temple020619A0 first compares the actual day with the feast day. Only equality
offers assistance;parity then selects preparation or chanting. Athens22 was an
incorrect preparation target and correctly produced64. Istanbul's exact even
feast24 supplies preparation;Athens' exact odd feast21 supplies chanting. The
source-case packet maps each outstanding ID explicitly. No failed/off-target
visit is counted as a ritual preparation.

The Gate button's original method020B8C8C verifies role11. Its native rectangle
is212,113..256,163. The earlier165-row touch was outside it and left another
facility selected.234,140 is the verified Gate hover before confirming. Initial
clicks during a facility rebuild are not assumed executed. Wrong Inn/Temple
visits remain navigation evidence only;all counted holds come after the Guard's
actual Parthenon offer and original yes input.

## Remaining scope

44 distinct IDs in the52-entry ceremony family now have actual display samples.
Eight variants remain:1206,1209,1211,1213,1214,1217,1224,1229. In particular,Lil's
1206/1209 can be reached by the original Temple chanting branch;they do not both
require a separate prayer route. Preparations and the remaining Lil chant/dance
contexts still need their exact original conditions and actual display checks.
Finish these and the final family review before granting52-entry completion.

The current ROM remainsV820,SHA-256`'''+release['candidate_sha256']+'''`.
Its patch,registry,all text and graphics are unchanged. No new production
translation is authored here.550 completed/605 source-prose/55 pending stays
unchanged. Older750-752,Angelo/sulfur,all remaining routes and player-facing prose
remain in the full editorial goal. Graphics and all18 plaques remain unfinished.
''',encoding='utf-8')
    backup=ROOT/'editorial_ledger_before_v825.json'
    if not backup.exists():shutil.copyfile(LEDGER,backup)
    detail=dict(documentation=str(DOC),proof=str(ROOT/'actual_hero_fast_and_retained64_verification.json'),
        normal_saves=str(ROOT/'after_fast_normal_save_provenance.json'),
        normal_reloads=str(ROOT/'normal_save_reload_verification.json'),
        new_distinct_reaction_IDs=proof['new_distinct_protagonist_reactions'],
        retained64_actual_display_verified=True,complete_scene_holds=24,complete_retained_refusal_holds=3,
        cumulative_distinct_actual_family_IDs=sorted(covered),remaining_actual_IDs=sorted(missing),
        whole52_family_pending=True,new_editorial_completion_credit=0,new_ROM=False,full_goal_complete=False)
    ledger['actual_ceremony_hero_fasting_v825']=detail
    ledger['pending_registered_ceremony_candidate'].update(
        status='44-of52-IDs-actual-display-sampled;source-RNG-cause-mapped;eight-hero-reactions-and-final-family-pending',
        actual_protagonist_verification_v825=detail)
    ledger['next_ceremony_source_packet'].update(
        status='44-distinct-family-IDs-with-actual-display-samples;eight-variants-and-final-review-pending',
        actual_protagonist_verification_v825=detail,
        next='Verify remaining1206/1209/1211/1213/1214/1217/1224/1229 under actual heroes. Use source-verified exact feast days:Temple chanting Athens21;preparations Istanbul24;remaining Lil site chant/dance source conditions. Then final52 review and older750-752/remaining prose.')
    ledger['active_source_prose_drafts']['note']=('51 production ceremony paragraphs retain201 native layouts/fonts.44 of52 family IDs now have actual display samples,including unchanged64;'
        'six real-captain fasting variants and allthree192-tick returns pass. Eight reaction variants and final whole52 review remain. Three older750-752 drafts stay open.')
    ledger['latest_checkpoint']=SUMMARY
    ident='V825-six-real-protagonist-fasting-reactions-and-normal-saves'
    if not any(r['id']==ident for r in ledger['research_checkpoints']):
        ledger['research_checkpoints'].append(dict(id=ident,documentation=str(DOC),new_ROM=False,
            new_source_prose_reviewed=0,new_editorially_completed=0,full_goal_complete=False))
    assert ledger['next_integrated_profile_for_goal_continuation']=='all-routes-unified-v820'
    save(LEDGER,ledger)
    for name in ('translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md'):
        p=Path('docs')/name;s=p.read_text(encoding='utf-8');heading='## V825: six real-protagonist fasting variants verified'
        if heading not in s:p.write_text(s+'\n\n'+heading+'\n\n'+SUMMARY+' See [actual hero and save evidence](ceremony_heroes_v825_checkpoint.md).\n',encoding='utf-8')
    # These are guide candidates with explicit isolated-access provenance.
    pics=Path('E:/Rota Nova translations/Screenshots/Guide candidates/V825 Ceremony captain reactions')
    pics.mkdir(parents=True,exist_ok=True);images=[]
    ids=set(proof['new_distinct_protagonist_reactions'])|{294}
    for row in proof['complete_scene_holds']:
        if row['message_id'] not in ids:continue
        source=Path(row['capture']['path']);target=pics/f'{row["hero"]}_{row["message_id"]}_{row["frame"]:06d}.png'
        shutil.copyfile(source,target);assert sha(source.read_bytes())==sha(target.read_bytes())
        images.append(dict(hero=row['hero'],message_id=row['message_id'],source=str(source),archived=str(target),sha256=sha(target.read_bytes())))
    assert len(images)==9
    save(pics/'capture_manifest.json',dict(images=images,actual_captain_portraits_and_complete_glyphs_verified=True,
        calendar_access_and_location_fixtures_explicit_not_earned_campaign=True,
        no_image_editing_or_rescaling=True,proof=detail['proof'],whole_graphics_audit_not_approved=True))
    archive=Path('E:/Rota Nova translations/Editorial review/V825 Actual captain ceremony reactions');archive.mkdir(parents=True,exist_ok=True)
    sources=[DOC,LEDGER,Path(__file__),*ROOT.glob('*.json'),
        *(Path('scripts')/n for n in ('native_ceremony_hero_fixture_v825.py','run_ceremony_hero_capture_v825.py','verify_ceremony_heroes_v825.py'))]
    artifacts=[]
    for source in sources:
        sub='scripts' if source.parent==Path('scripts') else 'verification' if source.parent==ROOT else 'checkpoint'
        target=archive/sub/source.name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
        assert sha(source.read_bytes())==sha(target.read_bytes())
        artifacts.append(dict(source=str(source),archived=str(target),sha256=sha(target.read_bytes())))
    save(archive/'archive_manifest.json',dict(artifacts=artifacts,guide_candidates=images,
        candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],no_ROM_patch_registry_or_frozen_dependency_changes=True,
        original_donors_unchanged=True,new_whole_family_credit=0,full_goal_complete=False))
    print('V825 recorded:6 new reactions+retained64;44/52 family IDs sampled,eight variants remain. Archived9 guide candidates and verified saves;goal active,no ROM changes.',flush=True)


if __name__=='__main__':main()
