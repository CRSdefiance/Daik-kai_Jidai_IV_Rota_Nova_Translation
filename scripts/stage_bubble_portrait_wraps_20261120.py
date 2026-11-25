"""Review the Strange Bubbles encounter and its later ship-danger reports."""

from hashlib import sha256
from pathlib import Path
from types import FunctionType

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import checkpoint_sea_event_review_v1 as sea
from scripts import register_genoa_tomato_exchange_20261120 as parent
from scripts.preflight_shared_crew_notices_v1 import with_components
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools, glyph_codes
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.seal_shared_text_source_v1 import reference
from scripts.stage_expedition_report_wraps_20261115 import owned_deployment
from scripts.stage_mutiny_review_v1 import compile_layouts, portrait_case, portrait_sheets, render_portrait
from scripts.stage_sea_event_review_v1 import native_stored


base, CLEAN = parent.base, Path('work/clean.nds')
ARM, COMMON = '/__arm9__.bin', '/COMMON/MESFILE.DK4'
ROOT = Path('work/bubble_portrait_wraps_20261120')
ROM, PROOF = ROOT / 'Bubble_Portrait_Wraps_RESEARCH_ONLY.nds', ROOT / 'staged.json'
RELEASES = Path('releases')
EARLY = RELEASES / 'all_routes_editorial_20261118_sea_event_dialogue_candidate/verification/registered_review.json'
LATE = RELEASES / 'all_routes_editorial_20261111_sailing_hazards_and_dolphins_candidate/verification/registered_review.json'
HAZARD_UPDATE = RELEASES / 'all_routes_editorial_20261119_sea_hazard_dialogue_candidate/verification/registered_review.json'
BEATS = range(457, 481)
DANGER = range(2391, 2397)
GATES = ('source', 'context', 'localization', 'naturalness', 'formatting')
EDITS = {
    461: ('Admiral, over there! Suspicious bubbles on the water!',
          ('Admiral, over there!', 'Suspicious bubbles on the water!'),
          'The older lookout calls the admiral over to look at the suspicious bubbles. Use two complete exclamations.'),
    2392: ('These bubbles will swallow the ship!', (),
           'The officer sees an immediate threat and predicts what the bubbles will do. Keep the whole warning on one row.'),
    2395: ('Bubbles are engulfing the ship!', (),
           'The ship is already being surrounded. Give the older officer a whole, direct alarm without announcing that the ship has sunk.'),
}
RETENTIONS = {
    457: 'The formal request and the complete report give the older polite voice two clear beats.',
    458: 'The direct call to the admiral already identifies the strange bubbles and where they are.',
    459: '“I can see” keeps this voice’s immediate sighting and differentiates it from the general report.',
    460: 'The familiar call over and the mention of bubbles floating on the water preserve the rougher register.',
    462: 'The excited “look” and “weird” carry the original colloquial voice in two complete calls.',
    463: 'The speaker recognizes the shape of the rumor and trails off before explaining the danger.',
    464: 'The gulp and uncertain question preserve the hesitation before the explanation.',
    465: 'The gulp and unfinished question carry the shock without jumping ahead to name the hazard.',
    466: 'The tentative question refers back to what the crew has heard and fits its recognition beat.',
    467: 'The audible stammer keeps the speaker’s alarm within the tentative question.',
    468: 'The older voice opens with “Well now” and keeps the entire reference to the stories together.',
    469: 'The captain’s single question mark leaves the crewmate to explain the otherwise unfamiliar sight.',
    470: 'The story is attributed to sailors and states the danger without asserting it as fact.',
    471: '“A story going around” keeps the informal hearsay and the warning about ships.',
    472: 'The personal recollection and “whole ships” preserve this voice’s vivid retelling.',
    473: 'The sailor reports having heard the claim and keeps the object as a ship.',
    474: 'A pause before the remembered warning preserves the speaker’s unease and sudden recognition.',
    475: 'The older voice cites the old story and lets the threat of swallowing a ship whole stand intact.',
    476: 'The quick account and the trailing voice give the young sailor’s warning its worried cadence.',
    477: 'Rafael makes his alarm explicit, then orders evasion and sends everyone to their stations.',
    478: 'Hodram gives two clean, practical orders, preserving the original maneuver and crew response.',
    479: 'Lil’s shocked reaction gives way to the decision to steer clear and the command to the crew.',
    480: 'Maria’s first response is to keep the crew calm before giving the order and announcing the maneuver.',
    2391: 'The report already names the bubbles and the ship in one complete statement of ongoing danger.',
    2393: 'This voice predicts the imminent danger rather than reporting that the ship is already lost.',
    2394: 'The established wording preserves the direct statement and the crew member’s use of “our ship.”',
    2396: 'The younger voice keeps its startling image of the bubbles eating the ship.',
}


def unwrapped(raw):
    return ' '.join(raw.decode('ascii').split())


def annotate_groups(clean_arm, arm, late_review):
    original = {g['first_ID']: g for g in base.load(sea.OUTPUT)['exact_native_event_groups']}
    groups = {}
    for first, end, table, pool, pc, call, consumer, role, _ in sea.GROUPS:
        if first not in BEATS:
            continue
        group = original[first]
        if table:
            width = 16 if first == 477 else 32
            assert arm[table:table + width] == clean_arm[table:table + width]
        assert group['source_native_caller'] == sea.caller_binding(
            clean_arm, arm, pc, call, pool, sea.BASE + table if table else first, consumer)
        assert group['original_role_argument'] == role
        groups.update(dict.fromkeys(range(first, end), group))
    danger, = [g for g in late_review['native_context'] if g['first_ID'] == 2391]
    caller, = danger['native_callers']
    table = danger['table'] - sea.BASE
    for lo, hi in ((table, table + 32), (0x72DDC, 0x72DE4), (0x73114, 0x73118)):
        assert clean_arm[lo:hi] == arm[lo:hi]
    assert caller['consumer'] == 0x02053F0C
    return groups, danger | {'consumer': caller['consumer'], 'original_role_argument': None}


def main():
    assert not ROOT.exists()
    release, early, late = map(base.load, (parent.RELEASE, EARLY, LATE))
    assert base.digest(base.REGISTRY) == release['registry_sha256']
    assert base.digest(parent.ROM) == release['candidate_sha256']
    assert base.digest(CLEAN) == release['clean_input_sha256']
    ctx = RegisteredRuntime(parent.RELEASE, release['own_registered_startup'], captain=3)
    clean = base.NdsImage.open(CLEAN)
    clean_arm = clean.read_file(ARM)
    ja = common_message_entries(clean.read_file(COMMON), clean_arm)
    entries = owned_entries(ctx.common, ctx.arm, sha256(ctx.arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest())
    groups, danger = annotate_groups(clean_arm, ctx.arm, late)
    earlier = {r['message_ID']: r for report, keys in ((early, BEATS), (late, DANGER))
               for r in report['records'] if r['message_ID'] in keys}
    refreshed, = [r for r in base.load(HAZARD_UPDATE)['records'] if r['message_ID'] == 2393]
    earlier[2393] = refreshed
    assert set(earlier) == EDITS.keys() | RETENTIONS.keys()
    rows = {}
    for n, orig in sorted(earlier.items()):
        source, installed = ja[n], entries[n]
        assert orig['source_hex'] == source.text.hex() and unwrapped(installed.text) == orig['english'], n
        english, phrases, note = EDITS.get(n, (orig['english'], (), RETENTIONS.get(n)))
        rows[n] = dict(id=orig['id'], file_path=COMMON, message_ID=n, speaker=orig['speaker'], context=orig['context'],
                       source_meaning=orig['source_meaning'], clean_Japanese=source.text.decode('cp932'),
                       source_reference=reference(source), current_reference=reference(installed),
                       English_before=orig['english'], english=english, localization_note=note, protected_phrases=phrases,
                       current_hex=installed.text.hex(), source_hex=source.text.hex(),
                       decision='revision' if n in EDITS else 'retention',
                       review=dict.fromkeys(GATES, True) | {'formatting': n not in EDITS})
    compiler = FunctionType(compile_layouts.__code__, compile_layouts.__globals__ |
                            {'PHRASES': {n: phrases for n, (_, phrases, _) in EDITS.items() if phrases}})
    replacements = compiler({n: rows[n] for n in EDITS})
    common, target_rows, allocation = owned_deployment(ctx.common, ctx.arm, entries, replacements)
    target = with_components(ctx, ctx.arm, common)
    painter, _, font = font_tools(ctx.image)
    kanji = ctx.image.read_file('/GRP/KANJI.FNT')

    def display(context, n, payload):
        row = rows[n]
        if n in groups:
            return native_stored(context, row, groups[n], payload)
        actor = next(a for a, _, key in danger['original_voice_choices'] if key == n)
        return portrait_case(context, row, danger, payload, actor)

    pages = []
    for n, row in rows.items():
        payload = target_rows[n].text
        row.update(staged_hex=payload.hex(), staged_reference=reference(target_rows[n]))
        row['native_consumer'] = display(target, n, payload)
        visible = row['native_consumer'].pop('display')
        lines = [part.strip() for part in visible.decode('ascii').splitlines()]
        assert unwrapped(visible) == row['english'] and 1 <= len(lines) <= 4
        assert all(any(phrase in line for line in lines) for phrase in row['protected_phrases'])
        ink, glyphs = render_portrait(painter, ctx.arm, kanji, visible)
        codes = [g['code'] for g in glyphs]
        assert codes == glyph_codes(visible)
        assert codes[0] == ord(row['english'][0]) and codes[-1] == ord(row['english'][-1])
        row.update(visible_lines=lines, display_hex=visible.hex(), glyph_count=len(glyphs),
                   mask_sha256=sha256(ink).hexdigest(), expected_pages=1)
        if n in EDITS:
            before = display(ctx, n, entries[n].text).pop('display')
            old_ink, _ = render_portrait(painter, ctx.arm, kanji, before)
            assert old_ink != ink and (len(lines) == 2 if n == 461 else len(lines) == 1)
            pages.extend([(f'{n} before', old_ink), (f'{n} revised', ink)])
    image = base.NdsImage.open(parent.ROM)
    image.replace_file(COMMON, common)
    ROM.parent.mkdir()
    image.save(ROM)
    image.replace_file(COMMON, ctx.common)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    base.save(PROOF, dict(candidate_sha256=base.digest(ROM), parent_sha256=release['candidate_sha256'],
        clean_input_sha256=release['clean_input_sha256'], target_ARM9_sha256=release['target_ARM9_sha256'],
        target_COMMON_sha256=sha256(common).hexdigest(), full_parent_inverse=True, allocation=allocation,
        translation_policy='natural-dialogue-v2', encoder='dialogue-relocatable-v1', target_locale='en-US',
        review_gates=list(GATES), records=list(rows.values()), sheets=portrait_sheets(ROOT, pages), font=font,
        gameplay_pending=True, new_contextual_credit=0,
        evidence={str(p): base.digest(p) for p in (parent.RELEASE, EARLY, LATE, HAZARD_UPDATE, sea.OUTPUT, Path(__file__))}))
    print('Thirty complete portrait checks, three revised warnings, and 27 individual retentions.')


if __name__ == '__main__':
    main()
