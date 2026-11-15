"""Review the traveling promoter, specialty, and Market exchanges on the current ROM."""

from hashlib import sha256
from pathlib import Path
from struct import unpack_from
from types import FunctionType

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import prepare_specialty_question_v752 as specialty
from scripts import register_expedition_report_wraps_20261115 as parent
from scripts.prepare_product_pitches_v747 import native_layout
from scripts.preflight_shared_crew_notices_v1 import with_components
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools, glyph_codes
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.seal_shared_text_source_v1 import reference
from scripts.stage_expedition_report_wraps_20261115 import owned_deployment
from scripts.stage_mutiny_review_v1 import compile_layouts, portrait_sheets, render_portrait
from scripts.verify_release_baseline import files


base = parent.base
ARM, COMMON, CLEAN, GATES = parent.stage.ARM, parent.stage.COMMON, parent.stage.CLEAN, parent.stage.GATES
ROOT = Path('work/town_market_wraps_20261115_v1')
ROM = ROOT / 'Town_Market_Wraps_RESEARCH_ONLY.nds'
STORED = ROOT / 'staged.json'
MANUSCRIPT = Path('translations/editorial_checkpoints/SharedText_20261110_v1/town_market_wraps_context_20261115_v1.json')
NUMBERS = range(738, 750)
PROSE = {
    739: "Hey, sailor! Could you take me to the square in another town? Any town will do...",
    748: "Huh? Sorry, that won't be enough. Come back when you've earned more.",
}
PHRASES = {
    739: ('Could you take me', 'to the square in another town?', 'Any town will do...'),
    743: ("Really? You're so kind!", "You're the best!"),
    748: ("Huh? Sorry, that won't be enough.", "Come back when you've earned more."),
    749: ('Your cargo holds are full!', "You'll have to buy less."),
}
DETAILS = {
    738: ('Traveling promoter', 'Arrival in a different town',
          'The promoter thanks the player, then says it is time to get to work.',
          'Retain the brisk thanks and the decision to start work as soon as they arrive.'),
    739: ('Traveling promoter', 'Request to travel to another town',
          'A passerby addresses a sailor and asks for a ride to the square in any other town.',
          'Make the favor a direct question. Keep the destination outside this town and the speaker’s openness about which town.'),
    740: ('Traveling promoter', 'Yes to the ride',
          'The promoter is surprised and grateful, then rallies to spread new trends to towns around the world.',
          'Keep the exuberant response, the personal obligation and the idea of starting new trends worldwide.'),
    741: ('Traveling promoter', 'No to the ride',
          'The promoter acknowledges the refusal and apologizes for asking too much.',
          'Sorry to impose is a natural apology after the player declines. Keep the turn brief.'),
    742: ('Local specialty requester', 'Offer to hand over an item',
          'The speaker asks for the offered item and thinks it could help make the named trade good a town specialty.',
          'Keep the item first and the prospective specialty second. I think preserves uncertainty and the opening question invites the player’s decision.'),
    743: ('Local specialty requester', 'Yes to the item request',
          'The speaker reacts with surprise and warmly praises the player’s kindness.',
          'Keep the two quick compliments. Move the wrap so “You’re the best!” reads together.'),
    744: ('Local specialty requester', 'No to the item request',
          'The speaker acknowledges the refusal and calls the player stingy.',
          'Keep the sharp turn from acknowledgment to “miser,” matching the comic reversal after the hopeful request.'),
    745: ('Trader', 'Another action after using the shop',
          'The trader asks whether the player still needs anything.',
          'Anything else? is a natural follow-up once the active transaction or inquiry is over.'),
    746: ('Trader', 'Leaves or declines without doing business',
          'The trader concludes that the player has only come to look around.',
          'The clipped question carries the seller’s disappointment and works in both source dismissal paths.'),
    747: ('Trader', 'Accepts an investment',
          'The trader appreciates the investment and promises to use it well.',
          'Keep the short thanks and the practical promise without specifying what the trader buys or builds.'),
    748: ('Trader', 'Cannot meet the requested investment amount',
          'The trader is surprised, apologizes that the amount will not suffice, and invites the player back after earning more.',
          'Keep the surprise, the apology and the invitation. “That won’t be enough” states the shortfall in a complete sentence.'),
    749: ('Trader', 'Purchase exceeds cargo capacity',
          'The trader says the holds are full and asks the player to reduce the purchase.',
          'Keep the reason and the instruction. Wrap at the sentence boundary so the instruction reads in full.'),
}
SOURCE_RANGES = ((0x5E458, 0x5E680), (0xBAB64, 0xBADC8), (0xBA48C, 0xBA490),
                 (0xBC92C, 0xBC948), (0xBC980, 0xBC98C), (0xC2B6C, 0xC2B74))


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
    assert all(arm[lo:hi] == clean_arm[lo:hi] for lo, hi in SOURCE_RANGES)
    source = common_message_entries(clean.read_file(COMMON), clean_arm)
    old = owned_entries(common, arm, sha256(arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest())
    ledger = base.load(base.LEDGER)
    credited = {row['id'] for row in ledger[base.CONTEXT]['integrated_record_keys'] if row['file_path'] == COMMON}
    assert all(f'COMMON_MESSAGE_{n}' in credited for n in NUMBERS)
    logical = {n: ' '.join(old[n].text.decode('ascii').split()) for n in NUMBERS}
    wrap = FunctionType(compile_layouts.__code__, compile_layouts.__globals__ | dict(PHRASES=PHRASES))
    edited = wrap({n: dict(english=PROSE.get(n, logical[n])) for n in PHRASES})
    assert all(body != old[n].text for n, body in edited.items())
    deployed, rebound, slots = owned_deployment(common, arm, old, edited)
    isolated = with_components(runtime, arm, deployed)
    cpu, get, provider = isolated.machine(arm, deployed, isolated.raw, isolated.plan)
    start = base.load(release['own_registered_startup'])
    read_names = FunctionType(specialty.catalog.__code__, specialty.catalog.__globals__ | dict(RAM=Path(start['read_only_snapshot']['path'])))
    names = read_names(arm)
    pairs = [(names['items'][p['prerequisite_item']]['name'], p['name']) for p in names['products'] if p['prerequisite_item'] < 20]
    assert len(pairs) == 25 and ('Baby Shark', 'Caviar') in pairs

    renderer, _, font = font_tools(runtime.image)
    kanji = runtime.image.read_file('/GRP/KANJI.FNT')
    records, preview, substitutions = [], [], []
    for n in NUMBERS:
        source_row, before, after = source[n], old[n], rebound[n]
        speaker, situation, meaning, note = DETAILS[n]
        assert source_row.text.decode('cp932').count('%s') == after.text.count(b'%s') == (2 if n == 742 else 0)
        pointer = get(0x5528C, n)
        assert bytes(cpu.mem_read(pointer, len(after.text) + 1)) == after.text + b'\0'
        # The two choices share the Yes/No builder and retain its original parent.
        parent_pc = 0x02053FCC if n in (739, 742) else 0x02054014
        if n == 742:
            variants = pairs
        else:
            variants = [()]
        for values in variants:
            display, lines = native_layout(cpu, after.text, n, values, parent=parent_pc)
            assert 1 <= len(lines) <= 4 and all(lines)
            if n == 742:
                substitutions.append(dict(values=values, lines=lines, native_output_hex=display.hex()))
        if n in edited:
            before_display, before_lines = native_layout(cpu, before.text, n, (), parent=parent_pc)
            assert before_lines != lines
            before_pixels, before_glyphs = render_portrait(renderer, arm, kanji, before_display)
            after_pixels, after_glyphs = render_portrait(renderer, arm, kanji, display)
            assert [g['code'] for g in before_glyphs] == glyph_codes(before_display)
            assert [g['code'] for g in after_glyphs] == glyph_codes(display)
            assert all(any(phrase in line for line in lines) for phrase in PHRASES[n])
            preview.extend(((f'{n} before', before_pixels), (f'{n} after', after_pixels)))
        else:
            before_lines = lines
        records.append(dict(id=f'COMMON_MESSAGE_{n}', message_ID=n, file_path=COMMON, speaker=speaker,
            context=situation, source_meaning=meaning, localization_note=note,
            decision='revision' if n in PROSE else 'wrap revision' if n in edited else 'retention',
            english=PROSE.get(n, logical[n]), previous_English=before.text.decode('ascii'),
            clean_Japanese=source_row.text.decode('cp932'), source_reference=reference(source_row),
            current_reference=reference(before), staged_reference=reference(after), source_hex=source_row.text.hex(),
            current_hex=before.text.hex(), staged_hex=after.text.hex(), formatter_parent=parent_pc,
            before_lines=before_lines if n != 742 else None, visible_lines=lines if n != 742 else None,
            preserved_runtime_arguments=after.text.count(b'%s'), review=dict.fromkeys(GATES, True) | {'formatting': False}))
    assert len(substitutions) == 25 and provider.reads
    assert bytes(cpu.mem_read(isolated.actor_root, 0x1A04)) == isolated.actor_bytes
    assert unpack_from('<I', arm, 0x5E678)[0] == 739
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
        source_exact_ranges=SOURCE_RANGES, specialty_title_arguments=substitutions, records=records))
    base.save(STORED, dict(candidate_sha256=base.digest(ROM), previous_sha256=release['candidate_sha256'],
        target_ARM9_sha256=sha256(arm).hexdigest(), target_COMMON_sha256=sha256(deployed).hexdigest(),
        whole_parent_inverse=True, preserved_entries=len(rebound) - len(edited), allocations=slots, sheets=sheets,
        font=font, reviewed_records=len(records), changed_native_pages=len(preview) // 2,
        native_cache_file_reads=provider.reads, manuscript_sha256=base.digest(MANUSCRIPT)))
    print(f'{len(records)} source reviews, {len(edited)} revised native pages, and {len(pairs)} specialty substitutions.')


if __name__ == '__main__':
    main()
