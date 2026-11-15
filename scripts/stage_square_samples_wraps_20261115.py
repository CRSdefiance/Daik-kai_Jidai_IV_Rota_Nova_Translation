"""Review the Square giveaway exchange and its separate shop condition replies."""

from hashlib import sha256
from pathlib import Path
from types import FunctionType

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import register_town_market_wraps_20261115 as parent
from scripts.prepare_giveaway_editorial_v746 import table_selection
from scripts.prepare_product_pitches_v747 import native_layout
from scripts.prepare_shop_business_release_v745 import selectors as business_selectors
from scripts.preflight_shared_crew_notices_v1 import with_components
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools, glyph_codes
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.seal_shared_text_source_v1 import reference
from scripts.stage_expedition_report_wraps_20261115 import owned_deployment
from scripts.stage_mutiny_review_v1 import compile_layouts, portrait_sheets, render_portrait
from scripts.verify_release_baseline import files
from scripts.verify_tavern_queued_native_v626 import queued_wrap


base = parent.base
ARM, COMMON, CLEAN, GATES = parent.stage.ARM, parent.stage.COMMON, parent.stage.CLEAN, parent.stage.GATES
ROOT = Path('work/square_samples_wraps_20261115_v1')
ROM = ROOT / 'Square_Samples_Wraps_RESEARCH_ONLY.nds'
STORED = ROOT / 'staged.json'
MANUSCRIPT = Path('translations/editorial_checkpoints/SharedText_20261110_v1/square_samples_wraps_context_20261115_v1.json')
NUMBERS = (*range(659, 675), *range(682, 688))
PROSE = {
    659: 'Hand out the goods for free?',
    661: 'Give the goods out as samples?',
    665: "You'd like us to hand out the goods as free samples, then?",
    667: "Come and take one, everyone! They're free, so don't be shy.",
    672: 'Step right up! Free samples here! Try one now!',
    673: 'Help yourselves to a free sample!',
    687: "Business? The ship that makes the regular run sank. Everyone's in a bind.",
}
PHRASES = {
    683: ('from the epidemic!', 'Are you kidding me?'),
    684: ('Business? Food comes first.', 'People have to eat to survive.'),
    687: ('makes the regular run sank.', "Everyone's in a bind."),
}
EXPECTED_SPLITS = {665: ('as free samples, then?',), 667: ("They're free, so don't be shy.",),
                   672: ('Step right up! Free samples here!', 'Try one now!')}
SOURCE_RANGES = ((0x5ED34, 0x5EE08), (0x1184A0, 0x1184E0), (0x53F4C, 0x53F9C), (0x5F9B8, 0x5FB54))

# Clean Japanese meaning and individual choices in the original alternative voices.
NOTES = {
    659: ('Confirms that the goods are to be distributed without charge.',
          'Hand out is the ordinary verb for an in-person giveaway, and for free preserves the explicit price.'),
    660: ('Politely checks that the player wants the trade goods distributed free.',
          'Retain the indirect phrasing and the confirmation tag. It sounds measured among the other voices.'),
    661: ('Confirms that the purpose of distributing the goods is to provide samples.',
          'Give out names distribution. Keep samples as this speaker’s stated purpose.'),
    662: ('Roughly asks whether the goods are to be given away at no cost.',
          'For nothing retains the rough emphasis and the final then fits the confirmation.'),
    663: ('Asks whether the trade goods go to the townspeople free of charge.',
          'The short question carries the older voice and names the townspeople as recipients.'),
    664: ('Casually confirms a free giveaway to local people.',
          'Right? fits the familiar register, and the wording retains both the recipients and the absence of a charge.'),
    665: ('Politely confirms that the goods are to be given away as free samples.',
          'Phrase the question as a request for confirmation. The party is about to distribute the goods, and free samples stays together.'),
    666: ('Invites people to help themselves to a sample and says today’s samples cost nothing.',
          'The polite pitch and the explicit today preserve the offer’s tone and timing.'),
    667: ('Invites everyone to take a sample freely and says there is no need to hold back because it costs nothing.',
          'Address everyone, then reassure them in one complete line. Keep the free offer and the reason they can help themselves.'),
    668: ('Calls people over to look and take a sample, treating the free giveaway as a special offer.',
          'Retain the quick promotional rhythm and the emphasis on doing something for the crowd.'),
    669: ('Invites people to try one and explains that the goods are samples.',
          'Both short exclamations fit the speaker’s polite invitation and identify the offer as a sample.'),
    670: ('Urges people to try it and take one while it is free.',
          'The brisk opening and invitation to take one preserve the rougher sales voice.'),
    671: ('Calls people over to try a sample for free right now.',
          'The friendly opening, the sample and the immediate free offer all remain explicit.'),
    672: ('A drawn-out pitch advertises samples and urges people to seize the chance to try one now.',
          'Use a recognizable market call and a separate invitation to try one now. Keep the speaker’s energy.'),
    673: ('Politely invites people to help themselves and try a sample for free.',
          'Help yourselves gives the invitation a courteous voice while announcing that the sample is free.'),
    674: ('Surprised that it is free, a customer decides to try it.',
          'Retain the surprised question and immediate decision, which follow the speaker’s free offer.'),
    682: ('The merchant says business is the least of their concerns and hopes for peace soon.',
          'The blunt change of subject and modest hope preserve the concern. Keep the existing related phrase break.'),
    683: ('People are collapsing from an epidemic, and the merchant takes the business question as an absurd joke.',
          'Keep the angry wording and put the entire rhetorical question on its own line.'),
    684: ('The merchant puts food first because people need it to survive.',
          'Each sentence makes a complete point. Keep the wording and break before the reason.'),
    685: ('The thriving town speaks for itself, and the merchant can hardly contain their delight.',
          'The invitation to look around and the smiling response keep the thriving market’s good humor.'),
    686: ('The merchant would rather the player did not ask and says trade is impossible in these conditions.',
          'The rhetorical question preserves frustration without specifying an unspoken cause.'),
    687: ('The regularly scheduled vessel sank, leaving everyone in trouble.',
          'Regular run is natural for the vessel’s route. Give the community’s predicament its own sentence.'),
}


def layout(arm, cpu, n, raw):
    if n < 674:
        parent_pc, table = (0x02053D24, 0x021184C0) if n < 666 else (0x02053DB8, 0x021184A0)
        display = queued_wrap(arm, raw, parent_pc, table)
        lines = [part.strip().decode('ascii') for part in display.split(b'\n')]
    else:
        parent_pc, table = 0x02054014, None
        display, lines = native_layout(cpu, raw, n, (), parent=parent_pc)
    assert 1 <= len(lines) <= 4 and all(0 < len(line) <= 36 for line in lines)
    assert b' '.join(raw.split()) == ' '.join(lines).encode('ascii')
    return parent_pc, table, display, lines


def main():
    assert not ROOT.exists() and not MANUSCRIPT.exists()
    release = base.load(parent.RELEASE)
    runtime = RegisteredRuntime(parent.RELEASE, release['own_registered_startup'], captain=3)
    assert base.digest(CLEAN) == release['clean_input_sha256']
    clean = base.NdsImage.open(CLEAN)
    arm, common = runtime.arm, runtime.common
    clean_arm = clean.read_file(ARM)
    assert sha256(arm).hexdigest() == release['target_ARM9_sha256']
    assert sha256(common).hexdigest() == release['target_COMMON_sha256']
    assert all(arm[a:b] == clean_arm[a:b] for a, b in SOURCE_RANGES)
    assert len(table_selection(arm)) == 16 and table_selection(arm) == table_selection(clean_arm)
    business = business_selectors(arm)
    assert len(business) == 13 and business == business_selectors(clean_arm)
    source = common_message_entries(clean.read_file(COMMON), clean_arm)
    old = owned_entries(common, arm, sha256(arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest())
    ledger = base.load(base.LEDGER)
    credited = {row['id'] for row in ledger[base.CONTEXT]['integrated_record_keys'] if row['file_path'] == COMMON}
    assert all(f'COMMON_MESSAGE_{n}' in credited for n in NUMBERS)
    logical = {n: ' '.join(old[n].text.decode('ascii').split()) for n in NUMBERS}
    wrap = FunctionType(compile_layouts.__code__, compile_layouts.__globals__ | dict(PHRASES=PHRASES))
    edited = {n: text.encode('ascii') for n, text in PROSE.items() if n < 674}
    edited.update(wrap({n: dict(english=PROSE.get(n, logical[n])) for n in PHRASES}))
    deployed, rebound, slots = owned_deployment(common, arm, old, edited)
    isolated = with_components(runtime, arm, deployed)
    cpu, get, provider = isolated.machine(arm, deployed, isolated.raw, isolated.plan)
    renderer, _, font = font_tools(runtime.image)
    kanji = runtime.image.read_file('/GRP/KANJI.FNT')
    records, preview = [], []
    for n in NUMBERS:
        source_row, before, after = source[n], old[n], rebound[n]
        assert b'%' not in source_row.text and b'%' not in after.text
        pointer = get(0x5528C, n)
        assert bytes(cpu.mem_read(pointer, len(after.text) + 1)) == after.text + b'\0'
        parent_pc, table, display, lines = layout(arm, cpu, n, after.text)
        before_lines = lines
        if n in edited:
            _, _, before_display, before_lines = layout(arm, cpu, n, before.text)
            assert before_lines != lines and before.text != after.text
            for title, body in (('before', before_display), ('after', display)):
                pixels, glyphs = render_portrait(renderer, arm, kanji, body)
                assert [g['code'] for g in glyphs] == glyph_codes(body)
                preview.append((f'{n} {title}', pixels))
            assert all(any(phrase in line for line in lines) for phrase in PHRASES.get(n, EXPECTED_SPLITS.get(n, ())))
        speaker = 'Assigned Missionary' if n < 674 else 'Customer' if n == 674 else 'Shopkeeper'
        context = ('Ask before offering the goods.' if n < 666 else 'Pitch after the player confirms the giveaway.' if n < 674 else
                   'Response after the announcement.' if n == 674 else 'Reply to the question about business in this town condition.')
        meaning, note = NOTES[n]
        records.append(dict(id=f'COMMON_MESSAGE_{n}', message_ID=n, file_path=COMMON, speaker=speaker,
            context=context, source_meaning=meaning, localization_note=note,
            decision='revision' if n in PROSE else 'wrap revision' if n in edited else 'retention',
            english=PROSE.get(n, logical[n]), previous_English=before.text.decode('ascii'),
            clean_Japanese=source_row.text.decode('cp932'), source_reference=reference(source_row),
            current_reference=reference(before), staged_reference=reference(after), source_hex=source_row.text.hex(),
            current_hex=before.text.hex(), staged_hex=after.text.hex(), formatter_parent=parent_pc, voice_table=table,
            before_lines=before_lines, visible_lines=lines, review=dict.fromkeys(GATES, True) | {'formatting': False}))
    assert provider.reads and bytes(cpu.mem_read(isolated.actor_root, 0x1A04)) == isolated.actor_bytes
    ROOT.mkdir()
    image = base.NdsImage.open(parent.ROM)
    original_files = files(image)
    image.replace_file(COMMON, deployed)
    changed_files = files(image)
    assert original_files.keys() == changed_files.keys()
    assert {path for path in original_files if changed_files[path] != original_files[path]} == {COMMON}
    image.save(ROM)
    image.replace_file(COMMON, common)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    sheets = portrait_sheets(ROOT, preview)
    base.save(MANUSCRIPT, dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=list(GATES), previous_sha256=release['candidate_sha256'],
        clean_sha256=release['clean_input_sha256'], candidate_sha256=base.digest(ROM),
        source_exact_ranges=SOURCE_RANGES, original_shop_condition_selectors=business, records=records))
    base.save(STORED, dict(candidate_sha256=base.digest(ROM), previous_sha256=release['candidate_sha256'],
        target_ARM9_sha256=sha256(arm).hexdigest(), target_COMMON_sha256=sha256(deployed).hexdigest(),
        whole_parent_inverse=True, preserved_entries=len(rebound) - len(edited), allocations=slots, sheets=sheets,
        font=font, reviewed_records=len(records), changed_native_pages=len(preview) // 2,
        native_cache_file_reads=provider.reads, manuscript_sha256=base.digest(MANUSCRIPT)))
    print(f'{len(records)} source reviews and {len(edited)} revised full native pages.')


if __name__ == '__main__':
    main()
