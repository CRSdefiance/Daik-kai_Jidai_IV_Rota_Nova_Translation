"""Review every source slot surrounding the observed ship assignment exchange."""

from collections import Counter
from pathlib import Path

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.compare_shared_text_source_v1 import DIRECTORY
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.seal_shared_text_source_v1 import reference
from scripts.seal_ship_loss_source_v1 import CLEAN, ROOT, SOURCE
from scripts.stage_ship_command_release_v1 import ARM, RELEASE, STARTUP


OUTPUT = ROOT/'current_contextual_review.json'
# None retains the exact logical current wording. The source-first drafts remain sealed.
DECISIONS = {
    338: (None, 'The concise system notice reports the same completed sinking.'),
    339: (None, 'The current neutral notice is clear in the actual exchange. Handle its stored blank row during formatting.'),
    2663: (None, 'The polite urgent report is concise and preserves the sinking.'),
    2664: (None, 'The short emphatic report matches the compressed source.'),
    2665: ('%s went down!', 'Use a more conversational verb for the casual contraction and abrupt reaction.'),
    2666: (None, 'The forceful short report preserves the blunt source ending.'),
    2667: (None, 'This slot repeats the same clean words as the neighboring forceful report. Keep both records and their shared wording.'),
    2668: ('Oh no, %s went down!', 'The longer ending expresses dismay that the flat current line misses.'),
    2669: (None, 'The current formal status preserves the emphatic fact without extra characterization.'),
    2670: (None, 'The existing complete warning naturally reports that no sailors remain.'),
    2671: (None, 'The current polite sentence reports the crew absence without inventing its cause.'),
    2672: ("%s doesn't have a single sailor left!", 'Restore the emphasis on not even one sailor and use a casual contraction.'),
    2673: ("%s hasn't got a sailor left!", 'Keep the rough informal voice and replace the stiff Not one sailor is aboard construction.'),
    2674: ("There's not a sailor left aboard %s!", 'The direct contraction and not a sailor preserve the blunt, emphatic voice.'),
    2675: ('Oh no, %s has no sailors left!', 'The drawn-out reaction conveys dismay. The revision keeps the empty-crew fact.'),
    2676: (None, 'The existing natural warning is accurate for the more formal report.'),
    2677: (None, 'The brief question checks assent, and the second sentence states the original action clearly.'),
    2678: ("It can't be helped. We'll abandon %s, then.", 'Express resignation without implying that the menu offers no choice.'),
    2679: (None, 'The current conversational question conveys the original emphasis and preserves the named ship.'),
    2680: (None, 'The natural question and its short tag match the observed Back confirmation.'),
    2681: ("Can't be helped. We'll abandon %s.", 'The clipped sentence keeps the resigned, gruff cadence without asserting that no other option exists.'),
    2682: (None, 'The short okay tag preserves the casual check and the planned action.'),
}


def main():
    assert not OUTPUT.exists()
    clean_drafts = load(SOURCE)
    ctx = RegisteredRuntime(RELEASE, STARTUP, captain=3)
    assert ctx.release['registered_manifest_entries'] == 732
    clean_arm = NdsImage.open(CLEAN).read_file(ARM)
    assert ctx.arm[0x2C1E0:0x2C65C] == clean_arm[0x2C1E0:0x2C65C]
    for table in clean_drafts['native_personality_tables']:
        at = table['pointer']-0x02000000
        assert ctx.arm[at:at+32].hex() == table['table_hex']
    current = owned_entries(ctx.common, ctx.arm, DIRECTORY)
    ledger = load('translations/editorial_review_current_v1.json')
    assert ctx.release['candidate_sha256'] == ledger['current_integrated_candidate']['sha256']
    keys = {(r['file_path'], r['id']) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['integrated_record_keys']}
    assert {r['message_ID'] for r in clean_drafts['records']} == set(DECISIONS)
    cpu, get, provider = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    rows = []
    for clean in clean_drafts['records']:
        n = clean['message_ID']
        assert (clean['file_path'], clean['id']) not in keys
        entry = current[n]
        at = get(0x5528C, n)
        assert bytes(cpu.mem_read(at, len(entry.text)+1)) == entry.text+b'\0'
        replacement, note = DECISIONS[n]
        current_english = entry.text.decode('cp932')
        english = current_english.strip() if replacement is None else replacement
        assert english.count('%s') == 1 and '\n' not in english and english.isascii()
        if n in (339,2680):
            assert english.replace('%s','Latina') in ('Latina has no sailors!', "So, we're abandoning Latina, right?")
        rows.append(dict(clean, current_reference=reference(entry), current_hex=entry.text.hex(),
            current_English=current_english, english=english, decision='retention' if replacement is None else 'revision',
            localization_note=note, source_native_substitution='%s ship name', speaker=('Speakerless fleet notice'
                if n in (338,339) else f"Original crew voice slot {clean['native_personality_slot']}"),
            context=clean_drafts['context'], source_meaning=clean['clean_source_meaning'],
            original_native_lookup_pass=True, source_and_current_caller_and_voice_tables_exact=True,
            representative_current_English_observed=n in (339,2680),
            current_template_comparison_pending=False,
            review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False), new_credit=0))
    assert bytes(cpu.mem_read(ctx.actor_root, 0x1A04)) == ctx.actor_bytes
    counts = dict(Counter(r['decision'] for r in rows))
    assert counts == dict(retention=14, revision=8)
    save(OUTPUT, dict(records=rows, counts=counts, runtime=ctx.receipt(), complete_original_voice_slots_preserved=True,
        current_native_lookups=22, all_original_caller_bytes_exact=True, original_ship_name_substitutions_preserved=True,
        earlier_incidental_observation_limited_to_two_current_messages=True,
        reviewed_current_gameplay_scope='The initialized run observed the Latina empty-crew and confirmation lines.',
        changed_dialogue_formatting_stored_andrepresentative_gameplay_pending=True, registered_integration_pending=True,
        evidence={str(p):digest(p) for p in [SOURCE, RELEASE, STARTUP, Path(__file__)]}, new_credit=0, full_goal_complete=False))
    print('All 22 original lookups pass. Eight revisions and 14 justified retentions are recorded.')


if __name__ == '__main__':
    main()
