"""Bind complete observed regional dialogue panels to their clean and current records."""

from hashlib import sha256
from pathlib import Path

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import observe_regional_town_dialogue_20261115 as capture
from scripts.checkpoint_amsterdam_square_current_20261114 import body_mask
from scripts.review_sound_bgm_titles_v1 import reference
from scripts.verify_captain_biographies_v1 import captured, shots
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask


base, current = capture.base, capture.current
OUTPUT = Path('translations/editorial_checkpoints/SharedText_20261110_v1/regional_town_dialogue_20261115_v1.json')
TOWNS = {
    'tunis': ((3200, 0), (5150, 654), (5950, 654), (6750, 732), (7550, 654), (8350, 732), (10350, 51)),
    'valencia': ((5150, 658), (5950, 658), (6750, 656), (7950, 658), (8750, 656), (10750, 714)),
    'syracuse': ((5150, 656), (5950, 658), (6750, 657), (7550, 657), (8350, 715), (10350, 51)),
}
TEXT = {
    0: (('Admiral, people seem to be', 'gathering in the square.'), 'Charles Rochefort',
        'Keep his cautious hint about the crowd before the player chooses to enter the square.'),
    51: (('Welcome! What will you have?',), 'Barkeep', 'Keep the friendly welcome and immediate question before the drink menu.'),
    654: (("If you've brought Whale Meat, be", 'sure to sell your stock', 'at the Market soon!'), 'Shopkeeper',
          'The shopkeeper urges prompt sale if the player brought the in-demand good. The live wrap separates be sure.'),
    656: (('We only sell retail.',), 'Shopkeeper', 'Keep the direct explanation that the shop sells at retail.'),
    657: (("You're a sailor, aren't you?", 'Try the trade house for bulk trade.'), 'Shopkeeper',
          'Keep the question tag intact and the practical referral as its own line.'),
    658: (("Business? Oh, it's been all right.", "I'm hoping a good deal comes along."), 'Shopkeeper',
          'Keep the casual echo, modest report and hope for a better opportunity.'),
    714: (("Admiral Valdes's Spanish navy has", "such formidable ships that it's", 'called the Invincible Armada.'), 'Shopkeeper',
          'Keep the navy, its admiral and the nickname as the shopkeeper’s reported local knowledge.'),
    715: (('The Centurione Company once traded', 'far and wide, as if the', 'Mediterranean belonged to it.'), 'Shopkeeper',
          'Keep the company’s past reach and the shopkeeper’s comparison, which leaves territorial ownership figurative.'),
    732: (("This trend looks like it'll last a", 'while yet.'), 'Shopkeeper',
          'The forecast stays tentative. The live first line strands the article from a while.'),
}
WRAP_LEADS = {654: ('be sure', 'at the Market soon'), 732: ('a while yet',)}


def read_run(city, sha):
    folder = capture.ROOT / city
    paths = [folder / p for p in ('capture/capture_report.json', 'requests.json', 'terminal.json')]
    report, trace, terminal = map(base.load, paths)
    events, _, end, _, donor = capture.schedule(city)
    assert report['ROM_sha256'] == terminal['ROM_sha256'] == sha and report['frames'] == end
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['scripted_input_schedule'] == events and not any(v for k, v in report.items() if k.startswith('synthetic_'))
    assert report['battery_save_preloaded']['source_sha256'] == donor['source_sha256'] == base.digest(donor['source'])
    assert trace['all_host_slots_restored_and_core_file_exact'] and not trace['mismatches'] and not trace['errors']
    assert terminal['target_COMMON_calls'] == trace['source_requests']
    evidence = {str(p): base.digest(p) for p in paths}
    assert all(base.digest(p) == digest for p, digest in terminal['evidence'].items())
    return shots(report), trace['source_requests'], evidence


def main():
    assert not OUTPUT.exists()
    release = base.load(current.RELEASE)
    assert base.digest(current.ROM) == release['candidate_sha256'] and base.digest(current.stage.CLEAN) == release['clean_input_sha256']
    clean, rom = map(base.NdsImage.open, (current.stage.CLEAN, current.ROM))
    common, arm = current.stage.COMMON, current.stage.ARM
    source = common_message_entries(clean.read_file(common), clean.read_file(arm))
    code = rom.read_file(arm)
    installed = owned_entries(rom.read_file(common), code, sha256(code[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest())
    font = GameAsciiFont.from_arm9(code)
    results, evidence = {}, {}
    for city, panels in TOWNS.items():
        frames, calls, dependencies = read_run(city, release['candidate_sha256'])
        evidence.update(dependencies)
        assert [n for _, n in panels] == [row['message_ID'] for row in calls[::2]]
        actual = []
        for (frame, n), first, second in zip(panels, calls[::2], calls[1::2], strict=True):
            assert [first['PC'], second['PC']] == [0x0205528C, 0x020534F4] and first['frame'] == second['frame'] < frame
            assert n == first['message_ID'] == second['message_ID']
            shot = frames[frame]
            image = captured(shot)
            lines, role, note = TEXT[n]
            body = body_mask(image, font, lines)
            pixels, bounds = complete_mask(font, role, image, 16, 277, (98, 97, 98))
            evidence[shot['path']] = shot['PNG_sha256']
            s, t = source[n], installed[n]
            expanded = t.text.decode('cp932').replace('%s', 'Whale Meat') if n == 654 else t.text.decode('cp932')
            assert ' '.join(expanded.split()) == ' '.join(lines)
            actual.append(dict(message_ID=n, frame=frame, source_reference=reference(s), current_reference=reference(t),
                Japanese=s.text.decode('cp932'), installed_English=t.text.decode('cp932'), source_hex=s.text.hex(),
                current_hex=t.text.hex(), body=body, original_request=first, capture=shot,
                nameplate=dict(text=role, complete_pixels=pixels, bounds=bounds), localization_note=note,
                decision='layout follow-up' if n in WRAP_LEADS else 'retention', phrase_wrap_leads=WRAP_LEADS.get(n, ())))
        results[city] = actual
    assert sum(map(len, results.values())) == 19
    base.save(OUTPUT, dict(candidate_sha256=release['candidate_sha256'], clean_sha256=release['clean_input_sha256'],
        original_town_dialogue=results, observed_variants=sorted(TEXT), layout_followups=sorted(WRAP_LEADS),
        actual_cold_boot_saved_gameplay=True, hardware=False, new_editorial_credit=0, evidence=evidence))
    print('Verified 19 complete regional dialogue and nameplate holds across nine distinct records.')


if __name__ == '__main__':
    main()
