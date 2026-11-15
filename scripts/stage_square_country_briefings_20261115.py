"""Review ordinary Square replies and the complete country briefing family."""

from hashlib import sha256
from pathlib import Path
from types import FunctionType

from dk4tool.patch.country_editorial import compile_paragraph
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import register_square_samples_wraps_20261115 as parent
from scripts.prepare_country_editorial_v748 import MEANINGS
from scripts.prepare_shop_business_release_v745 import selectors
from scripts.preflight_shared_crew_notices_v1 import with_components
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools, glyph_codes
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.stage_square_samples_wraps_20261115 import (
    ARM, CLEAN, COMMON, GATES, compile_layouts, files, native_layout,
    owned_deployment, portrait_sheets, reference, render_portrait,
)


base = parent.base
ROOT = Path('work/square_country_briefings_20261115_v2')
ROM = ROOT / 'Square_Country_Briefings_RESEARCH_ONLY.nds'
STORED = ROOT / 'staged.json'
MANUSCRIPT = Path('translations/editorial_checkpoints/SharedText_20261110_v1/square_country_briefings_context_20261115_v2.json')
NUMBERS = (656, 657, 658, *range(688, 709))
PROSE = {
    657: "You're a sailor, aren't you? Try the trade house for bulk trade.",
    689: 'The Dutch just won independence from Spain after a long war.',
    690: 'The Hanseatic League ruled European trade. It faded after sailors found the sea route to India and reached the New World.',
    693: "Spain's thriving, isn't it? Abroad they call it 'the empire where the sun never sets.'",
    694: 'After the sea route to India opened, Genoa, Venice and other Italian city-states lost their eastern trading rights.',
    696: 'Istanbul was Constantinople, capital of the Byzantine Empire, or Eastern Rome.',
    702: "The kingdoms around here once bowed to the Ming Empire. Now there's nothing left of its former glory...",
    704: "The Ming dynasty once thrived. Now eunuchs do as they please, and the government sinks deeper into chaos. It's dreadful.",
    705: 'Under its founder, Yi Seong-gye, Korea united about 200 years ago.',
}
EXPECTED = {
    657: ("You're a sailor, aren't you?", 'Try the trade house for bulk trade.'),
    689: ('The Dutch just won independence', 'from Spain after a long war.'),
    705: ('Under its founder, Yi Seong-gye,', 'Korea united about 200 years ago.'),
}
MEANING = MEANINGS | {
    656: 'The shop specializes in retail sales.',
    657: 'The shopkeeper recognizes a sailor and directs them to the trade house for larger transactions.',
    658: 'Business has been passable, and the shopkeeper hopes for a good opportunity.',
}
NOTES = {
    656: 'The brief reply keeps the distinction between retail sales here and bulk trading at the trade house.',
    657: 'Retain the friendly question and make the referral a direct suggestion. The next line carries the whole referral.',
    658: 'Keep the speaker’s quick echo of Business?, modest assessment and private hope for a better deal.',
    688: 'Britain names the union of all three places. Keep the prediction of prosperity and the speaker’s cheer for the Queen.',
    689: 'The Dutch makes the conversational subject shorter while preserving the recent independence, Spain and the long war. The sentence now has two complete phrase groups.',
    690: 'Keep the League’s former dominance and later decline. Separate finding the sea route from reaching the New World, which also reads together on screen.',
    691: 'Keep Sweden’s recent independence from the Kalmar Union. Denmark and Norway remain together at the end.',
    692: 'Keep the shopkeeper’s questioning opening, the recent loss and the qualifier almost all.',
    693: 'Let the speaker ask for agreement, then attribute the nickname to people abroad as hearsay.',
    694: 'Restore the rights to trade with the East, along with both cities and the opening of the India route.',
    695: 'Keep the speaker’s categorical claim, the occupation and the change from churches to mosques.',
    696: 'Give Eastern Roman and Byzantine as two names for the same empire while keeping the earlier name Constantinople.',
    697: 'All preserves the shopkeeper’s claim about the cities, and seem retains the speaker’s uncertainty about the pirates.',
    698: 'The speaker explains the interest in trading rights by naming both ivory and gold. After all keeps the exchange conversational.',
    699: 'Keep the broad attribution to Muslim powers and the scope of this region. The speaker supplies no particular dynasty.',
    700: 'Keep the contempt in infidel and the pause before the speaker ends the conversation.',
    701: 'Keep the speaker’s moral advice and the stated attribution to karma from a past life.',
    702: 'Put the earlier submission and present decline in separate sentences. Keep the speaker’s emphatic judgment and trailing delivery.',
    703: 'Keep the kingdom, its former power in these waters and the stated pressure from Muslim powers.',
    704: 'Do as they please restores the criticism of arbitrary rule. Keep the worsening disorder in government and the speaker’s dismay.',
    705: 'Present Yi Seong-gye as founding ruler and keep the national unification and approximate two-century interval.',
    706: 'Keep the long warring era and the sense that a welcome end is finally approaching.',
    707: 'Keep the friendly opening question and the claim that European pirates come from many countries.',
    708: 'Keep the game’s title for Cortes, the Aztec kingdom and the wave of conquistadors that followed.',
}
SOURCE_RANGES = ((0x5F9B8, 0x5FB54),)


def main():
    assert not ROOT.exists() and not MANUSCRIPT.exists()
    release = base.load(parent.RELEASE)
    runtime = RegisteredRuntime(parent.RELEASE, release['own_registered_startup'], captain=3)
    arm, common = runtime.arm, runtime.common
    assert base.digest(CLEAN) == release['clean_input_sha256']
    assert sha256(arm).hexdigest() == release['target_ARM9_sha256']
    assert sha256(common).hexdigest() == release['target_COMMON_sha256']
    clean = base.NdsImage.open(CLEAN)
    clean_arm = clean.read_file(ARM)
    assert all(arm[a:b] == clean_arm[a:b] for a, b in SOURCE_RANGES)
    business = selectors(arm)
    assert len(business) == 13 and business == selectors(clean_arm)
    source = common_message_entries(clean.read_file(COMMON), clean_arm)
    old = owned_entries(common, arm, sha256(arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest())
    ledger = base.load(base.LEDGER)
    credited = {row['id'] for row in ledger[base.CONTEXT]['integrated_record_keys'] if row['file_path'] == COMMON}
    assert all(f'COMMON_MESSAGE_{n}' in credited for n in NUMBERS)
    guarded_wrap = FunctionType(compile_layouts.__code__, compile_layouts.__globals__ | dict(PHRASES={657: EXPECTED[657][1:]}))
    edited = guarded_wrap({657: dict(english=PROSE[657])})
    edited.update({n: compile_paragraph(PROSE[n]) for n in PROSE if n != 657})
    assert all(body != old[n].text for n, body in edited.items())
    deployed, rebound, slots = owned_deployment(common, arm, old, edited)
    isolated = with_components(runtime, arm, deployed)
    cpu, get, provider = isolated.machine(arm, deployed, isolated.raw, isolated.plan)
    renderer, _, font = font_tools(runtime.image)
    kanji = runtime.image.read_file('/GRP/KANJI.FNT')
    records, previews = [], []
    for n in NUMBERS:
        src, before, after = source[n], old[n], rebound[n]
        english = PROSE.get(n, ' '.join(before.text.decode('ascii').split()))
        assert b'%' not in src.text and b'%' not in after.text
        pointer = get(0x5528C, n)
        assert bytes(cpu.mem_read(pointer, len(after.text) + 1)) == after.text + b'\0'
        display, lines = native_layout(cpu, after.text, n, ())
        assert 1 <= len(lines) <= 4 and all(lines) and ' '.join(lines) == english
        if n in EXPECTED:
            assert tuple(lines) == EXPECTED[n]
        before_lines = lines
        if n in edited:
            old_display, before_lines = native_layout(cpu, before.text, n, ())
            assert before_lines != lines
            for title, body in (('before', old_display), ('after', display)):
                pixels, glyphs = render_portrait(renderer, arm, kanji, body)
                assert [g['code'] for g in glyphs] == glyph_codes(body)
                previews.append((f'{n} {title}', pixels))
        context = ('One of the independent regional briefings selected by the shopkeeper after the town share check.' if n >= 688
                   else {656: 'Shop specialism reply.', 657: 'Referral from the Square to bulk trading.',
                         658: 'Reply after the player asks how business is going in an ordinary town.'}[n])
        records.append(dict(id=f'COMMON_MESSAGE_{n}', message_ID=n, file_path=COMMON, speaker='Shopkeeper',
            context=context, source_meaning=MEANING[n], localization_note=NOTES[n],
            decision='revision' if n in edited else 'retention', english=english, previous_English=before.text.decode('ascii'),
            clean_Japanese=src.text.decode('cp932'), source_reference=reference(src), current_reference=reference(before),
            staged_reference=reference(after), source_hex=src.text.hex(), current_hex=before.text.hex(),
            staged_hex=after.text.hex(), formatter_parent=0x02054014, before_lines=before_lines, visible_lines=lines,
            preserved_runtime_arguments=0, review=dict.fromkeys(GATES, True) | {'formatting': False}))
    assert provider.reads and bytes(cpu.mem_read(isolated.actor_root, 0x1A04)) == isolated.actor_bytes
    ROOT.mkdir()
    image = base.NdsImage.open(parent.ROM)
    original_files = files(image)
    image.replace_file(COMMON, deployed)
    changed_files = files(image)
    assert original_files.keys() == changed_files.keys()
    assert {path for path in original_files if original_files[path] != changed_files[path]} == {COMMON}
    image.save(ROM)
    image.replace_file(COMMON, common)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    sheets = portrait_sheets(ROOT, previews)
    base.save(MANUSCRIPT, dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=list(GATES), previous_sha256=release['candidate_sha256'],
        clean_sha256=release['clean_input_sha256'], candidate_sha256=base.digest(ROM), source_exact_ranges=SOURCE_RANGES,
        original_shop_condition_selectors=business, records=records))
    base.save(STORED, dict(candidate_sha256=base.digest(ROM), previous_sha256=release['candidate_sha256'],
        target_ARM9_sha256=sha256(arm).hexdigest(), target_COMMON_sha256=sha256(deployed).hexdigest(),
        whole_parent_inverse=True, preserved_entries=len(rebound) - len(edited), allocations=slots, sheets=sheets,
        font=font, reviewed_records=len(records), changed_native_pages=len(previews) // 2,
        native_cache_file_reads=provider.reads, manuscript_sha256=base.digest(MANUSCRIPT)))
    print(f'{len(records)} exact source reviews and {len(edited)} revised native pages.')


if __name__ == '__main__':
    main()
