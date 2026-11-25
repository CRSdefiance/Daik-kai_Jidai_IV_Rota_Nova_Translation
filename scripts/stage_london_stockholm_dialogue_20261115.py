"""Review the ordinary London and Stockholm exchanges and stage three changes."""

from inspect import getsource
from pathlib import Path

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import observe_london_riga_towns_20261115 as capture
from scripts import probe_tavern_continuation_layout_v768 as old_formatter
from scripts.preflight_shared_crew_notices_v1 import with_components
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.review_sound_bgm_titles_v1 import reference
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_expedition_report_wraps_20261115 import owned_deployment
from scripts.stage_mutiny_review_v1 import portrait_sheets, render_portrait
from scripts.verify_release_baseline import files


base, parent = capture.base, capture.current
ARM, CLEAN, COMMON = parent.stage.ARM, parent.stage.CLEAN, '/COMMON/MESFILE.DK4'
ROOT = Path('work/london_stockholm_dialogue_20261115_v1')
ROM = ROOT / 'London_Stockholm_Dialogue_RESEARCH_ONLY.nds'
STORED = ROOT / 'staged.json'
MANUSCRIPT = Path('translations/editorial_checkpoints/SharedText_20261110_v1/london_stockholm_dialogue_20261115_v1.json')
GATES = ('source', 'context', 'localization', 'naturalness', 'formatting')
DISPATCH = 0x01FFCF3C
CHOICES = {858: "Would it be all right to spend about %s gold?",
           874: "Whoa! Really? Thanks for the round! Mighty generous of you!",
           1154: "Ah, %s! I hear you want to help defend our city."}
LONDON = 'Hodram orders a round for everyone. Manuel quotes the price. Hodram accepts, the barkeep calls the round, and a patron thanks him and shares a fleet rumor. A subsequent single drink leads to the nearby-town tip.'
PORT = 'Departing Riga, the port worker gives the run of crew readiness advice. Hodram sails to Stockholm and docks there.'
PALACE = 'Hodram opens the king’s military investment menu in Stockholm. The king greets him, then responds to cancelling or funding the investment.'
TAVERN = 'In Stockholm, Hodram orders a drink. The barkeep quotes the price, gives a regional rumor, and calls Francisca, who answers him.'
NOTES = {
    28: ('Port Worker', PORT, 'One ship is short of sailors. Review the formation before departing.',
         'Keep the distinction between one undermanned ship and the fleet as a whole.'),
    51: ('Barkeep', LONDON + ' ' + TAVERN, 'A casual welcome and invitation to order.',
         'The welcome naturally cues the menu and works in both taverns.'),
    53: ('Barkeep', LONDON + ' ' + TAVERN, 'The drink costs five gold coins.',
         'Keep the abrupt five-coin quote and the established local tender.'),
    55: ('Barkeep', TAVERN, 'The barkeep calls the named attendant about a customer.',
         'Hey and the contracted announcement sound natural when calling across the room.'),
    56: ('Francisca', TAVERN, 'A prompt affirmative answer to the barkeep’s call.',
         'On it! fits the quick acknowledgement before the attendant’s own greeting.'),
    65: ('Docking confirmation', PORT, 'Asks whether to call at the named port.',
         'Dock at is a clear confirmation and holds the substituted port name in the source position.'),
    85: ('Departure estimate', PORT, 'The supplies will last about the specified number of days at sea.',
         'Retain the forward-looking duration estimate and its native wide digits.'),
    814: ('Port Worker', PORT, 'The crew looks tired. The worker suggests resting at the inn.',
          'The question is a suggestion and leaves the decision to the player.'),
    821: ('Barkeep', TAVERN, 'Casually reports someone’s local influence, giving their name, origin, and role.',
          'Real pull suits the informal rumor and preserves all three arguments. This run shows Clifford.'),
    823: ('Barkeep', LONDON, 'Asks if the player knows the named town and says it is nearby.',
          'Keep the quick conversational question and the town’s proximity.'),
    858: ('Manuel Almeida', LONDON, 'Estimates the gold cost and asks courteously if it is acceptable.',
          'Frame the estimate as a courteous approval question. The formatter keeps the full amount with gold on the second line.'),
    865: ('Hodram', LONDON, 'Calls for drinks for everyone present.',
          'Keep the direct call and the energetic tone.'),
    872: ('Barkeep', LONDON, 'Announces the named patron is buying the round and urges everyone to enjoy it.',
          'Keep the public announcement. The installed translation uses the original patron label and leaves the second native address unused, as previously approved.'),
    874: ('Patron', LONDON, 'Greets the round with surprise and gratitude and praises the player’s generosity.',
          'Keep the boisterous thanks and give the generosity compliment once. The thanks and compliment each fit their own line.'),
    880: ('Patron', LONDON, 'Passes on hearsay that a company’s fleet is headed toward the named town.',
          'Word is fits a casual tip. The wording preserves the intended destination and does not imply arrival.'),
    1154: ('King', PALACE, 'Greets the player by the supplied name and says he hears they will help defend the city.',
           'Restore the hearsay in the king’s welcome and use the direct “help defend our city” before the player chooses an amount.'),
    1158: ('King', PALACE, 'Reacting to cancellation, he calls the player indecisive.',
           'Keep the gruff interjection and the short rebuke.'),
    1160: ('King', PALACE, 'The king acknowledges the display of good spirit and commends it.',
           'The deliberate second beat suits the king’s formal approval after an accepted donation.'),
}
NATIVE = {858: (0x02053D24, 0x02118400), 874: (0x02054014, 0), 1154: (0x02054014, 0)}


def digest(data):
    return parent.stage.digest(data)


def variant_values():
    yield 858, tuple((str(n).translate(str.maketrans('0123456789', '０１２３４５６７８９')),) for n in (
        1, 10, 303, 9999, 31275, 999999, 9999999, 99999999, 999999999, 2147483647))
    yield 874, ((),)
    yield 1154, tuple((n,) for n in ('Li', 'Castor', 'Argot', 'Bergstrom', 'ABCDEFGHIJKLMNOPQRSTUVW'))


def original_formatter():
    source = checked_text(getsource(old_formatter.format_case), {
        '    call(u, LITERAL - BASE, (wrapped, output, 0), instruction_limit=2000000)': '''    for at,value in ((0x264,row['parent']),(0x270,0),(0x274,row['message_id']),(0x27C,row['table'])):
        u.mem_write(STACK+at,struct.pack('<I',value))
    call(u, DISPATCH-BASE, (wrapped,output,0),instruction_limit=2000000)
    assert all(bytes(u.mem_read(p,len(value)+1)) == value + bytes(1) for p,value in zip(pointers,values))''',
    })
    namespace = vars(old_formatter) | dict(DISPATCH=DISPATCH)
    exec(compile(source, __file__ + '::installed-dispatch', 'exec'), namespace)
    return namespace['format_case']


def stage():
    assert not ROOT.exists() and not MANUSCRIPT.exists()
    release = base.load(parent.RELEASE)
    assert base.digest(base.REGISTRY) == release['registry_sha256'] and base.digest(CLEAN) == release['clean_input_sha256']
    runtime = RegisteredRuntime(parent.RELEASE, release['own_registered_startup'], captain=3)
    source = base.NdsImage.open(CLEAN)
    clean_arm = source.read_file(ARM)
    arm, common = runtime.arm, runtime.common
    assert digest(arm) == release['target_ARM9_sha256'] and digest(common) == release['target_COMMON_sha256']
    assert all(clean_arm[lo:hi] == arm[lo:hi] for lo, hi in ((0x53CB0,0x53D44),(0x53FE4,0x54058),(0x58350,0x5839C)))
    original = common_message_entries(source.read_file(COMMON), clean_arm)
    old = owned_entries(common, arm, digest(arm[DIRECTORY_OFFSET:TABLE_OFFSET]))
    ledger = base.load(base.LEDGER)
    credited = {row['id'] for row in ledger[base.CONTEXT]['integrated_record_keys'] if row['file_path'] == COMMON}
    raw = {ident: b' ' + text.encode('ascii') for ident, text in CHOICES.items()}
    patched, installed, slots = owned_deployment(common, arm, old, raw)
    isolated = with_components(runtime, arm, patched)
    cpu, get, _ = isolated.machine(arm, patched, isolated.raw, isolated.plan)
    raster, _, font = font_tools(runtime.image)
    kanji = runtime.image.read_file('/GRP/KANJI.FNT')
    actual, evidence = {}, {}
    for case in capture.HISTORY:
        path = capture.ROOT / case / 'terminal.json'
        receipt = base.load(path)
        assert receipt['ROM_sha256'] == release['candidate_sha256']
        assert all(base.digest(p) == sha for p, sha in receipt['evidence'].items())
        evidence[str(path)] = base.digest(path)
        actual[case] = [r for r in receipt['target_COMMON_calls'] if r['PC'] == 0x0205528C]
    assert set(NOTES) == {r['message_ID'] for results in actual.values() for r in results}

    records, variants, pages = [], [], []
    format_case = original_formatter()
    for ident, values in variant_values():
        parent_call, table = NATIVE[ident]
        ptr = get(0x5528C, ident)
        body = raw[ident]
        assert bytes(cpu.mem_read(ptr, len(body)+1)) == body + b'\0'
        assert old[ident].text.count(b'%s') == original[ident].text.count(b'%s') == body.count(b'%s')
        for args in values:
            text = tuple(value.encode('cp932') for value in args)
            result = format_case(cpu, dict(message_id=ident, english=CHOICES[ident],
                parent=parent_call, table=table, English_argument_source_indices=list(range(len(text)))), text)
            assert not result['findings'] and len(result['lines']) <= (3 if ident == 858 else 4)
            if ident == 858:
                assert result['lines'] == ['Would it be all right to spend', f'about {args[0]} gold?']
            if ident == 874:
                assert result['lines'] == ['Whoa! Really? Thanks for the round!', 'Mighty generous of you!']
            pixels, glyphs = render_portrait(raster, arm, kanji, bytes.fromhex(result['formatted_hex']))
            variants.append(result | dict(arguments=list(args), native_ink_sha256=digest(pixels), complete_glyphs=len(glyphs)))
            pages.append((f'{ident} {" / ".join(args)}', pixels))
    assert len(variants) == 16 and bytes(cpu.mem_read(isolated.actor_root, 0x1A04)) == isolated.actor_bytes

    for ident, (speaker, context, meaning, note) in NOTES.items():
        s, p, t = (entries[ident] for entries in (original, old, installed))
        key = f'COMMON_MESSAGE_{ident}'
        assert key in credited
        records.append(dict(id=key, file_path=COMMON, message_ID=ident, speaker=speaker, context=context,
            Japanese=s.text.decode('cp932'), source_meaning=meaning, localization_note=note,
            english=CHOICES.get(ident, ' '.join(t.text.decode('ascii').split())), previous_English=p.text.decode('ascii'),
            decision='revision' if ident in CHOICES else 'retention', review=dict.fromkeys(GATES, True),
            source_reference=reference(s), current_reference=reference(p), staged_reference=reference(t),
            source_hex=s.text.hex(), current_hex=p.text.hex(), staged_hex=t.text.hex(),
            original_calls={city:[r for r in calls if r['message_ID'] == ident] for city,calls in actual.items()},
            substitutions=dict(source=s.text.count(b'%s'), current=p.text.count(b'%s'), staged=t.text.count(b'%s'))))
    doc = dict(translation_policy='natural-dialogue-v2', encoder='dialogue-relocatable-v1', target_locale='en-US',
        review_gates=list(GATES), records=records, focused_native_cases=variants, additional_dialogue_credit=0,
        actual_current_source_hashes=evidence)
    ROOT.mkdir()
    image = base.NdsImage.open(parent.ROM)
    prior = files(image)
    image.replace_file(COMMON, patched)
    after = files(image)
    assert prior.keys() == after.keys() and {p for p in prior if prior[p] != after[p]} == {COMMON}
    image.save(ROM)
    image.replace_file(COMMON, common)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    base.save(MANUSCRIPT, doc)
    base.save(STORED, dict(previous_sha256=release['candidate_sha256'], candidate_sha256=base.digest(ROM),
        target_ARM9_sha256=digest(arm), target_COMMON_sha256=digest(patched), allocations=slots,
        preserved_entries=len(installed)-len(CHOICES), manuscript_sha256=base.digest(MANUSCRIPT),
        sheets=portrait_sheets(ROOT, pages), font=font, whole_parent_inverse=True))
    print(f'{len(records)} contextual decisions, {len(CHOICES)} staged revisions, and {len(variants)} complete native pages.')


if __name__ == '__main__':
    stage()
