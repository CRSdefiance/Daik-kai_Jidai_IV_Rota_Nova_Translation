"""Verify ordinary Amsterdam Square replays and bind retained text to both ROMs."""

from hashlib import sha256
from pathlib import Path
from struct import unpack_from

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import observe_amsterdam_square_current_20261114 as capture
from scripts.review_sound_bgm_titles_v1 import reference
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_personal_gameplay_v841 import get_machine


base, current = capture.base, capture.current
ARM, COMMON, CLEAN, GATES = (
    current.stage.ARM, current.stage.COMMON, current.stage.CLEAN, current.stage.GATES)
OUTPUT = Path('translations/editorial_checkpoints/SharedText_20261110_v1/'
              'amsterdam_square_current_review_20261114_v1.json')
CASES = {
    'square': ((9701, 136), (10901, 658), (11701, 689), (12501, 657),
               (13301, 689), (14501, 657), (15301, 689)),
    'food': ((9701, 136), (10901, 658), (11701, 689), (12501, 657)),
}
DECISIONS = {
    136: (('Choose a shop sign to ask about', 'trends and other local news.'),
          'On entering the Square, the game explains what selecting a retailer’s sign does.',
          'The instruction names the exact action and preserves the request for trends and other information.'),
    657: (("You're a sailor, aren't you? For", 'bulk trade, try the trade house.'),
          'The shopkeeper recognizes a sailor and points them to the trade house for larger transactions.',
          'The question tag sounds conversational and stays together on the first line. The second line keeps the bulk-trade referral clear.'),
    658: (("Business? Oh, it's been all right.", "I'm hoping a good deal comes along."),
          'Asked how business is going, the shopkeeper gives a modest answer and hopes for a better opportunity.',
          'The quick echo and understated answer preserve the exchange’s casual rhythm and cautious optimism.'),
    689: (('The Netherlands only recently won', 'independence from Spain, after a', 'long war.'),
          'The shopkeeper explains the Netherlands’ recent independence from Spain after a long war.',
          'The matter-of-fact explanation retains both countries, the war’s length and the recency of independence.'),
}


def body_mask(image, font, lines):
    result = []
    for y in range(297, 345, 16):
        ink = {(x, row) for x in range(16, 244) for row in range(y, y + 16)
               if image.getpixel((x, row)) == (0, 8, 0)}
        index = (y - 297) // 16
        if index >= len(lines):
            assert not ink
            continue
        expected = {(6 * i + x, y + row) for i, character in enumerate(lines[index])
                    for glyph in (font.decode(character),)
                    for x in range(6) for row in range(11) if glyph.getpixel((x, row))}
        matches = [left for left in (16, 22) if {(left + x, row) for x, row in expected} == ink]
        assert len(matches) == 1, (lines[index], len(ink), len(expected))
        assert matches[0] + 6 * len(lines[index]) <= 244
        result.append(dict(text=lines[index], origin=[matches[0], y], complete_glyph_pixels=len(ink)))
    return result


def observed_panels(release, arm, evidence):
    font = GameAsciiFont.from_arm9(arm)
    result = {n: [] for n in DECISIONS}
    for case, panels in CASES.items():
        folder = capture.ROOT / case
        report_path, requests_path, terminal_path = (
            folder / path for path in ('capture/capture_report.json', 'requests.json', 'terminal.json'))
        report, trace, terminal = map(base.load, (report_path, requests_path, terminal_path))
        schedule, requested_frames, end, _, _ = capture.schedule(case)
        assert report['ROM_sha256'] == terminal['ROM_sha256'] == release['candidate_sha256']
        assert report['frames'] == terminal['completed_frames'] == end
        assert report['scripted_input_schedule'] == schedule
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert report.get('battery_save_preloaded') is None
        assert not any(value for key, value in report.items() if key.startswith('synthetic_'))
        assert trace['all_host_slots_restored_and_core_file_exact'] and not trace['errors'] and not trace['mismatches']
        evidence.update({str(path): base.digest(path) for path in (report_path, requests_path, terminal_path)})
        requests = trace['source_requests']
        assert terminal['COMMON_requests'] == len(requests)
        assert [row['message_ID'] for row in requests[::2]] == [120, 341, 341, 341, *(n for _, n in panels)]
        for direct, copy in zip(requests[::2], requests[1::2], strict=True):
            assert [direct['PC'], copy['PC']] == [0x0205528C, 0x020534F4]
            assert {key: value for key, value in direct.items() if key != 'PC'} == {
                key: value for key, value in copy.items() if key != 'PC'}
        captured = {row['frame']: row for row in report['frames_captured']}
        for (frame, n), request in zip(panels, requests[8::2], strict=True):
            assert frame in requested_frames and 0 < frame - request['frame'] < 160
            shot = captured[frame]
            path = shot['path']
            evidence[path] = base.digest(path)
            assert evidence[path] == shot['PNG_sha256']
            with Image.open(path) as opened:
                assert opened.size == (256, 384)
                image = opened.convert('RGB')
            body = body_mask(image, font, DECISIONS[n][0])
            panel = dict(replay=case, frame=frame, native_request=request, capture=path, lines=body)
            if n != 136:
                ink, bounds = complete_mask(font, 'Shopkeeper', image, 16, 277, (98, 97, 98))
                assert ink == 135
                panel['nameplate'] = dict(label='Shopkeeper', complete_glyph_pixels=ink, bounds=bounds)
            result[n].append(panel)
    return result


def retained_names(release, clean_arm, arm, evidence):
    startup_path = Path(release['own_registered_startup'])
    startup = base.load(startup_path)
    snapshot = startup['read_only_snapshot']
    raw = Path(snapshot['path']).read_bytes()
    assert snapshot['read_only_export'] and sha256(raw).hexdigest() == snapshot['sha256']
    evidence[str(startup_path)] = base.digest(startup_path)
    evidence[snapshot['path']] = snapshot['sha256']
    cpu, get = get_machine(arm, raw)
    table = get(0xCB184)
    ram_base = 0x02000000
    rows = []
    for actor, japanese, english, reason in (
        (82, '広場の店主', 'Shopkeeper', 'The Square location supplies the context while the title identifies the retailer.'),
        (83, '広場の店主', 'Shopkeeper', 'The Square location supplies the context while the title identifies the retailer.'),
        (91, '広場の店主', 'Shopkeeper', 'The Square location supplies the context while the title identifies the retailer.'),
        (164, 'カップル男', 'Man', 'His relationship comes through in the exchange. The nameplate can use a natural generic label.'),
        (165, 'カップル女', 'Woman', 'The tea request reads as a familiar exchange. The role label carries no unsupported age or marital title.'),
    ):
        source = 0x120B80 + actor * 32
        source_pointer, = unpack_from('<I', clean_arm, source)
        source_text = source_pointer - ram_base
        assert clean_arm[source_text:source_text + 32].split(b'\0', 1)[0].decode('cp932') == japanese
        runtime = table + 4 + actor * 32
        getters = {}
        for getter in (0x7EB0C, 0x7ED88):
            pointer = get(getter, runtime)
            assert ram_base <= pointer < ram_base + len(raw)
            assert bytes(cpu.mem_read(pointer, len(english) + 1)) == english.encode() + b'\0'
            getters[hex(ram_base + getter)] = pointer
        rows.append(dict(actor=actor, clean_ARM9_field=source, clean_ARM9_text_offset=source_text, clean_label=japanese,
                         current_label=english, current_runtime_actor=runtime, getter_returns=getters,
                         rationale=reason, scope='offline initialized name getters'))
    return rows


def main():
    assert not OUTPUT.exists()
    release = base.load(current.RELEASE)
    assert base.digest(current.ROM) == release['candidate_sha256']
    assert base.digest(CLEAN) == release['clean_input_sha256']
    clean, rom = map(base.NdsImage.open, (CLEAN, current.ROM))
    clean_arm, arm = clean.read_file(ARM), rom.read_file(ARM)
    common = rom.read_file(COMMON)
    assert sha256(arm).hexdigest() == release['target_ARM9_sha256']
    assert sha256(common).hexdigest() == release['target_COMMON_sha256']
    source = common_message_entries(clean.read_file(COMMON), clean_arm)
    stored = owned_entries(common, arm, sha256(arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest())
    ledger = base.load(base.LEDGER)
    credited = {row['id'] for row in ledger[base.CONTEXT]['integrated_record_keys'] if row['file_path'] == COMMON}
    evidence = {str(path): base.digest(path) for path in (current.RELEASE, Path(capture.__file__), Path(__file__))}
    observed = observed_panels(release, arm, evidence)
    retained = []
    for n, (lines, context, reason) in DECISIONS.items():
        id_key = f'COMMON_MESSAGE_{n}'
        assert id_key in credited
        english = stored[n].text.decode('ascii')
        assert ' '.join(english.split()) == ' '.join(lines)
        retained.append(dict(id=id_key, file_path=COMMON, clean_reference=reference(source[n]),
            current_reference=reference(stored[n]), clean_Japanese=source[n].text.decode('cp932'),
            current_English=english, clean_hex=source[n].text.hex(), current_hex=stored[n].text.hex(),
            context=context, decision='retain', rationale=reason, review=dict.fromkeys(GATES, True),
            existing_credit=True, ordinary_gameplay=observed[n]))
    names = retained_names(release, clean_arm, arm, evidence)
    base.save(OUTPUT, dict(candidate_sha256=release['candidate_sha256'], clean_sha256=release['clean_input_sha256'],
        actual_gameplay='Two Lil New Game replays, with Food, Liquor and Jewelry Shop visits.',
        panels=sum(map(len, observed.values())), shopkeeper_nameplates=sum(len(v) for n, v in observed.items() if n != 136),
        retained=retained, names=names, hardware=False, unvisited=['tea exchange'], new_editorial_credit=0,
        evidence=evidence))
    print('Verified 11 complete body masks, nine Shopkeeper nameplates and five offline name fields.')


if __name__ == '__main__':
    main()
