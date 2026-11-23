"""Bind the ordinary Ceuta arrival, town dialogue and route lesson to clean records."""

from pathlib import Path

from dk4tool.dialogue.reviewed_choice_object_v2 import labels
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import check_rafael_voyage_ceuta_20261119 as display
from scripts import observe_rafael_ceuta_arrival_20261119 as run
from scripts import prepare_london_guild_assignments_20261118 as intake
from scripts.review_sound_bgm_titles_v1 import reference

base, native = run.base, run.native
COMMON = '/COMMON/MESFILE.DK4'
PAIR = Path('work/rafael_ceuta_contract_routes_20261119/paired_source.json')
OUTPUT = Path('translations/editorial_checkpoints/SharedText_20261110_v1/rafael_ceuta_arrival_20261119_v1.json')
SHARED_HOLDS = {
    8: (39605, 'Trader', 'Need help?'),
    49: (48485, 'Port Worker', 'Want to resupply for 90 gold?'),
    67: (36475, 'Sailor', 'Shall we dock at Ceuta?'),
    136: (41285, None, 'Choose a shop sign to ask about trends and other local news.'),
    657: (42005, 'Shopkeeper', "You're a sailor, aren't you? Try the Market for bulk trade."),
    658: (42965, 'Shopkeeper', "Business? Oh, it's been all right. I'm hoping a good deal comes along."),
    815: (49925, 'Port Worker', 'You have no cargo.'),
}


def main():
    assert not OUTPUT.exists()
    report_path = run.CAPTURE / 'capture_report.json'
    trace_path = run.ROOT / 'observer/commands.json'
    journal_path = run.CAPTURE / 'navigation_command_journal.json'
    report, trace, journal, prefix, packet, release = map(base.load,
        (report_path, trace_path, journal_path, run.PREFIX, PAIR, run.active.RELEASE))
    candidate = base.digest(run.active.ROM)
    assert candidate == report['ROM_sha256'] == packet['candidate_sha256'] == release['candidate_sha256']
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    tail = []
    for event in journal['commands_received']:
        key = event['command']
        if key.get('buttons') or key.get('touch'):
            recorded = dict(start=event['frame']+1, duration=key['duration'], buttons=key['buttons'])
            if 'touch' in key:
                recorded['touch'] = key['touch']
            tail.append(recorded)
    assert report['scripted_input_schedule'] == prefix['scripted_input_schedule'] + tail
    assert not any(value for key, value in report.items() if key.startswith('synthetic_'))
    assert report['frames'] == journal['last_command_frame'] == 50165
    assert journal['ROM_sha256'] == candidate and all(r['validation_passed'] for r in journal['commands_received'])
    assert journal['commands_received'][-1]['command'] == {'stop': True}
    assert not trace['errors'] and not trace['mismatches'] and not trace['unreturned_at_capture_end']
    assert trace['all_host_slots_restored_and_core_file_exact']
    donor = report['battery_save_preloaded']
    assert donor['copied_byte_exact_before_cold_boot'] and base.digest(donor['source']) == donor['source_sha256']
    evidence = {str(p):base.digest(p) for p in (report_path, trace_path, journal_path, run.JOURNAL, run.PREFIX,
        PAIR, run.ROOT/'source_contract.json', run.active.RELEASE, Path(run.__file__), Path(__file__))}
    clean, current = map(base.NdsImage.open, (native.CLEAN,run.active.ROM))
    arm = current.read_file(native.ARM)
    banks = [native.IlnkContainer.parse(image.read_file('/data/SC0.DK4')).blocks for image in (clean,current)]
    names = display.deck.GameAsciiFont.from_arm9(arm)
    ctx = native.RegisteredRuntime(run.active.RELEASE, release['own_registered_startup'], captain=3)
    system_paint = display.stage.workflow.stage.system.native_painter(ctx)
    _, paint = display.offline.workflow.early.prior.precedent.planners(arm)
    painters = (arm, current.read_file(display.deck.FONT), paint, system_paint)
    shots = display.deck.shots(report)

    def witnessed(frame):
        photo = shots[frame]
        assert base.digest(photo['path']) == photo['PNG_sha256']
        evidence[photo['path']] = photo['PNG_sha256']
        return photo

    story, menu, unvisited = [], [], []
    for group, count in zip(packet['groups'], (22,27), strict=True):
        block = group['block']
        assert native.digest(banks[0][block]) == group['source_block_sha256']
        assert native.digest(banks[1][block]) == group['current_block_sha256']
        commands = intake.native.scoped_inventory()[0](arm,banks[1][block])[0]
        sizes = {c['offset']:c for c in commands}
        records = {}
        for row in group['records']:
            records.setdefault(row['current_command_offset'], []).append(row)
        calls = display.tavern.observed_commands(trace,block,group['current_block_sha256'])
        assert len(calls) == count, (block,len(calls))
        assert calls[-1][1]['result_words'] == [0,1 if block == 45 else 0]
        for entered, returned in calls:
            at, word = entered['source']['instruction_offset'], entered['source']['first_word']
            assert sizes[at]['word'] == word
            if at not in records:
                continue
            raw = bytes.fromhex(sizes[at]['whole_command_hex'])
            selected = records.pop(at)
            if word == 0x2100:
                assert block == 139 and returned['result_words'] == [2,0]
                assert tuple(labels(raw)) == (b'Yes, please.',b'No, thanks. Got it.')
                menu.append(dict(block=block, source_records=selected, native_result=returned['result_words'], hold=witnessed(44405)))
                continue
            row, = selected
            body = raw[6:raw.index(0,6)]
            assert word == 0x4000 and body.hex() == row['current_body_hex'] and raw[5] == row['selector']
            expanded = body.replace(b'FI',b'Rafael').replace(b'FO',b'Castor Co.')
            selector, plane, mask = display.expected_page(painters,raw[:6]+expanded+b'\0','ordinary Ceuta')
            hold, _ = display.hold_with_mask(entered,returned,shots,names,selector,mask)
            witnessed(hold['frame'])
            story.append(dict(id=f"DK4_MES_B{block}_R{row['source_record_index']:04}",
                block=block, source_current=row, hold=hold, native_plane_sha256=native.digest(plane),
                complete_body_and_nameplate_masks=True, actual_runtime_name_substitution=expanded != body))
        unvisited.extend(r for remaining in records.values() for r in remaining)
    assert len(story) == 29 and len(menu) == 1
    assert [(r['block'],r['source_record_index']) for r in unvisited] == [(139,102)]

    current_entries = owned_entries(current.read_file(COMMON),arm,native.digest(arm[DIRECTORY_OFFSET:TABLE_OFFSET]))
    clean_entries = common_message_entries(clean.read_file(COMMON),clean.read_file(native.ARM))
    focus = {r['message_ID'] for r in base.load(run.active.parent.parent.parent.stage.PENDING)['records']}
    assert len(focus) == 276
    after = [r for r in trace['COMMON_requests'] if r['frame'] >= run.START]
    assert len(after) == 20 and len({r['message_ID'] for r in after}) == 8
    assert not focus.intersection(r['message_ID'] for r in after)
    shared = []
    for mid in sorted({r['message_ID'] for r in after}):
        orig, present = clean_entries[mid],current_entries[mid]
        row = dict(message_ID=mid, original_Japanese=orig.text.decode('cp932'), current_English=present.text.decode('cp932'),
            clean_reference=reference(orig), current_reference=reference(present),
            native_calls=[r for r in after if r['message_ID']==mid])
        if mid in SHARED_HOLDS:
            frame, speaker, text = SHARED_HOLDS[mid]
            row.update(human_read_gameplay_text=text,speaker=speaker,hold=witnessed(frame))
        shared.append(row)
    base.save(OUTPUT,dict(candidate_sha256=candidate, ordinary_Rafael_Lisbon_to_Ceuta=True,
        preserved_donor=donor['source_sha256'], hardware=False, story_panels=story, original_choices=menu,
        unvisited_story_records=unvisited, town_and_sea_shared_requests=shared, pending_shared_keys_requested=[],
        Trade_UI_holds=[witnessed(40085),witnessed(40325)], returned_to_Port_hold=witnessed(50165),
        register_changed=False, new_contextual_credit=0, full_goal_complete=False, evidence=evidence))
    print('Ordinary Ceuta replay verified 29 story panels, both route choices and eight distinct shared requests.')


if __name__ == '__main__':
    main()
