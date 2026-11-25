"""Bind ordinary voyage and town holds to their clean and registered records."""

from pathlib import Path
from types import FunctionType, SimpleNamespace

from PIL import Image, ImageChops, ImageDraw

from scripts import checkpoint_regional_town_dialogue_20261115 as regional
from scripts import observe_lisbon_voyage_and_osaka_20261115 as observed
from scripts import stage_voyage_rat_and_search_dialogue_20261115 as stage
from scripts.stage_embedded_story_roles_20261115 import IlnkContainer, raw_speeches, scoped_inventory
from scripts.verify_captain_biographies_v1 import captured
from scripts.verify_london_stockholm_dialogue_20261115 import BODY, native_hold


base, ROOT = stage.base, stage.ROOT
OUTPUT, SHEET = ROOT / 'gameplay_verification.json', ROOT / 'voyage_comparison.png'
REGIONAL = Path('translations/editorial_checkpoints/SharedText_20261110_v1/lisbon_voyage_nagasaki_observation_20261115_v1.json')
RISK_HOLDS = {4075: 408, 4535: 2221}
LISBON = {5150: 656, 5950: 657, 6750: 685, 7550: 656, 8350: 657, 10350: 51}
LISBON_LINES = {
    51: (('Welcome! What will you have?',), 'Barkeep',
         'Keep the welcoming question as the bartender opens the drink menu.'),
    656: (('We only sell retail.',), 'Shopkeeper', 'Keep the direct limit on what this storefront sells.'),
    657: (("You're a sailor, aren't you?", 'Try the trade house for bulk trade.'), 'Shopkeeper',
          'Keep the spoken tag and the direct referral. Both thoughts occupy complete rows.'),
    685: (('Business? Just look around!', "I can't stop smiling."), 'Shopkeeper',
          'The shopkeeper answers with the bustle on display and their own delight. The break follows the change of thought.'),
}
NAGASAKI = {
    5360: (5, 'Sojin Kurushima', ("Well, Maria! Today we're settling", 'this once and for all!'),
           'The swaggering address and final challenge keep the familiar insult without implying family.'),
    5560: (15, 'Yukihisa Shiraki', ('Kurushima! End this folly!',),
           'Preserve the short, formal rebuke as he calls on Kurushima to stop the misconduct.'),
    5760: (18, 'Sojin Kurushima', ('A samurai siding with foreigners!', 'You shame every warrior!'),
           'Review “You shame every warrior!” against the sharper source charge that Yukihisa is unworthy of the warrior name.'),
    5960: (22, 'Yukihisa Shiraki', ('And is ravaging the mainland coast', 'and plundering defenseless people',
                                     'the conduct of a proud samurai?'),
           'The formal counterquestion points to the mainland coast and people who cannot fight back.'),
    6160: (26, 'Sojin Kurushima', ('Oh, listen to you.', 'So stiff and proper. Just the sort', "I can't stand."),
           'The rude dismissal keeps his contempt for Yukihisa’s upright attitude.'),
    6360: (32, 'Sojin Kurushima', ('Heh heh, Maria! Be my woman', 'and surrender. Your life alone', 'will be spared!'),
           'Review the explicit condition and Sojin’s personal promise to spare Maria alone. Keep the menace and the coerced proposal.'),
    6560: (35, 'Maria Li', ("Sojin Kurushima... Keep running", "your mouth, and I'll pluck out",
                           'that arrogant beard of yours.'),
           'Review the odd “arrogant beard” phrasing while keeping Maria’s mockery, her threat to pluck his beard and its conditional trigger.'),
    6760: (39, 'Sojin Kurushima', ("Ha ha ha! ...I'll kill you!",),
           'The laughter snaps into a direct threat as the exchange ends.'),
}
NAGASAKI_FOLLOWUPS = {18, 32, 35}


def check_run(root, case, sha):
    helper = FunctionType(regional.read_run.__code__, vars(regional) |
                          {'capture': SimpleNamespace(ROOT=root, schedule=observed.schedule)})
    return helper(case, sha)


def nameplate(font, image, label):
    pixels, bounds = regional.complete_mask(font, label, image, 16, 277, (98, 97, 98))
    return dict(text=label, pixels=pixels, bounds=bounds)


def record_observations():
    assert not REGIONAL.exists()
    prior = base.load(stage.parent.RELEASE)
    sha = prior['candidate_sha256']
    clean, image = map(base.NdsImage.open, (stage.CLEAN, stage.parent.ROM))
    clean_arm, arm = [rom.read_file(stage.ARM) for rom in (clean, image)]
    source = stage.common_message_entries(clean.read_file(stage.COMMON), clean_arm)
    installed = stage.owned_entries(image.read_file(stage.COMMON), arm,
                                    stage.digest(arm[stage.DIRECTORY_OFFSET:stage.TABLE_OFFSET]))
    font = regional.GameAsciiFont.from_arm9(arm)
    lisbon, lisbon_calls, evidence = check_run(observed.ROOT, 'lisbon', sha)
    assert [r['message_ID'] for r in lisbon_calls[::2]] == list(LISBON.values())
    holds = []
    for (frame, n), request in zip(LISBON.items(), lisbon_calls[::2], strict=True):
        assert request['frame'] < frame and request['message_ID'] == n
        actual = captured(lisbon[frame])
        lines, label, note = LISBON_LINES[n]
        assert ' '.join(installed[n].text.decode('ascii').split()) == ' '.join(lines)
        holds.append(dict(message_ID=n, frame=frame, source=stage.reference(source[n]),
            current=stage.reference(installed[n]), Japanese=source[n].text.decode('cp932'),
            English=' '.join(lines), original_request=request, decision='retention', localization_note=note,
            body=regional.body_mask(actual, font, lines), nameplate=nameplate(font, actual, label)))
        evidence[lisbon[frame]['path']] = lisbon[frame]['PNG_sha256']
    shots, calls, traces = check_run(observed.ROOT, 'osaka', sha)
    evidence.update(traces)
    assert [r['message_ID'] for r in calls[::2]] == [85, 86, 618]
    file, block = '/data/SC3.DK4', 3
    blobs = [IlnkContainer.parse(rom.read_file(file)).blocks[block] for rom in (clean, image)]
    inventory, _, _ = scoped_inventory()
    a, b = [raw_speeches(code, blob, inventory)[1] for code, blob in zip((clean_arm, arm), blobs, strict=True)]
    assert len(a) == len(b) == len(NAGASAKI)
    story = []
    for (frame, (n, label, lines, note)), ja, en in zip(NAGASAKI.items(), a, b, strict=True):
        assert ja['complete_preamble_hex'] == en['complete_preamble_hex']
        assert ja['record_index'] == en['record_index'] == n
        jp, stored = [bytes.fromhex(row['raw_hex'])[1:].decode('cp932') for row in (ja, en)]
        assert ' '.join(stored.replace('FI', 'Maria').split()) == ' '.join(lines)
        actual = captured(shots[frame])
        story.append(dict(id=f'DK4_MES_B{block}_R{n:04}', file_path=file, block=block, frame=frame,
            source_reference=ja, current_reference=en, Japanese=jp, English=' '.join(lines),
            body=regional.body_mask(actual, font, lines), nameplate=nameplate(font, actual, label),
            context='Sojin challenges Maria at sea. Yukihisa rebukes him and answers his samurai accusation. '
                    'Sojin ridicules Yukihisa, makes his demand, and answers Maria’s defiance with a threat.',
            localization_note=note, proposed_followup=n in NAGASAKI_FOLLOWUPS))
        evidence[shots[frame]['path']] = shots[frame]['PNG_sha256']
    shot = shots[5200]
    screen = captured(shot)
    lines = ("We've got company in the E! Those", "are Kurushima ships! Let's get", "ready for a fight!")
    assert installed[618].text.decode('ascii').strip() % ('E', 'Kurushima') == ' '.join(lines)
    alert = dict(message_ID=618, source=stage.reference(source[618]), current=stage.reference(installed[618]),
        Japanese=source[618].text.decode('cp932'), original_request=calls[-2], lines=lines,
        body=regional.body_mask(screen, font, lines), nameplate=nameplate(font, screen, 'Sailor'))
    evidence[shot['path']] = shot['PNG_sha256']
    base.save(REGIONAL, dict(candidate_sha256=sha, clean_sha256=prior['clean_input_sha256'],
        ordinary_saved_game=True, injected_location=False, reached_osaka=False, hardware=False,
        lisbon_holds=holds, nagasaki_encounter=story, preceding_ship_alert=alert,
        source_block_sha256=stage.digest(blobs[0]), current_block_sha256=stage.digest(blobs[1]),
        proof_scope='Lisbon shops and Tavern, and the Kurushima encounter following departure from Nagasaki.',
        evidence=evidence, new_editorial_credit=0))
    print('Verified six Lisbon holds, the sailing alert and all eight Kurushima fight speeches.')


def verify():
    assert not OUTPUT.exists() and not SHEET.exists()
    staged = base.load(stage.STORED)
    prior = base.load(stage.parent.RELEASE)
    assert base.digest(stage.parent.ROM) == prior['candidate_sha256'] == staged['previous_sha256']
    assert base.digest(stage.ROM) == staged['candidate_sha256'] and REGIONAL.exists()
    old, requests_before, evidence = check_run(observed.ROOT, 'voyage', prior['candidate_sha256'])
    new, requests_after, dependencies = check_run(stage.ROOT, 'voyage', staged['candidate_sha256'])
    assert old.keys() == new.keys()
    evidence.update(dependencies | {str(REGIONAL): base.digest(REGIONAL)})
    image = base.NdsImage.open(stage.ROM)
    arm, kanji = (image.read_file(path) for path in (stage.ARM, '/GRP/KANJI.FNT'))
    raster, _, _ = stage.font_tools(image)
    font = regional.GameAsciiFont.from_arm9(arm)
    cases = {row['message_ID']: row for row in staged['native_cases']}
    matches, controls = [], []
    sheet = Image.new('RGB', (1024, 468), '#263238')
    draw = ImageDraw.Draw(sheet)
    for i, (frame, n) in enumerate(RISK_HOLDS.items()):
        case = cases[n]
        a, b = captured(old[frame]), captured(new[frame])
        diff = ImageChops.difference(a, b).getbbox()
        assert diff and BODY[0] <= diff[0] < diff[2] <= BODY[2] and BODY[1] <= diff[1] < diff[3] <= BODY[3]
        actor = nameplate(font, b, 'Manuel Almeida')
        assert actor == nameplate(font, a, 'Manuel Almeida')
        for j, (shot, screen, description, text_key, hash_key) in enumerate((
            (old[frame], a, 'Before', 'old_display_hex', 'old_plane_sha256'),
            (new[frame], b, 'Revised', 'display_hex', 'plane_sha256'))):
            plane, _ = stage.render_portrait(raster, arm, kanji, bytes.fromhex(case[text_key]))
            assert stage.digest(plane) == case[hash_key]
            native_hold(screen, plane)
            evidence[shot['path']] = shot['PNG_sha256']
            x, y = j * 512, i * 234
            draw.text((x + 4, y + 3), f'{n} {description}', fill='white')
            sheet.paste(screen.crop((0, 271, 256, 378)).resize((512, 214), Image.Resampling.NEAREST), (x, y + 17))
        selected = [[row for row in calls if row['message_ID'] == n and 0 < frame - row['frame'] <= 300]
                    for calls in (requests_before, requests_after)]
        assert all(len(pair) == 2 and {row['PC'] for row in pair} == {0x0205528C, 0x020534F4}
                   and all(row['caller_LR'] == 0x02053DA4 for row in pair) for pair in selected), selected
        matches.append(dict(frame=frame, message_ID=n, display=case['lines'], actor=actor,
                            changed_bounds=diff, before_calls=selected[0], after_calls=selected[1]))
    for frame, item in ((4735, 'Food'), (4955, 'Water')):
        a, b = captured(old[frame]), captured(new[frame])
        assert a.tobytes() == b.tobytes()
        lines = (f"We've run out of {item}!",)
        controls.append(dict(frame=frame, body=regional.body_mask(b, font, lines), nameplate=nameplate(font, b, 'Manuel Almeida')))
        evidence.update({shot[frame]['path']: shot[frame]['PNG_sha256'] for shot in (old, new)})
    for frame in (3200, 3855):
        assert captured(old[frame]).tobytes() == captured(new[frame]).tobytes()
        controls.append(dict(frame=frame, whole_frame_exact=True))
        evidence.update({shot[frame]['path']: shot[frame]['PNG_sha256'] for shot in (old, new)})
    assert all(row['message_ID'] != 405 for row in (*requests_before, *requests_after))
    sheet.save(SHEET)
    base.save(OUTPUT, dict(candidate_sha256=staged['candidate_sha256'], comparison_ROM_sha256=prior['candidate_sha256'],
        ordinary_saved_game=True, hardware=False, revised_holds=matches, exact_control_frames=controls,
        later_voyage_frames_after_sample_not_claimed_equivalent=True,
        native_only_revisions=sorted(set(stage.REVISIONS) - set(RISK_HOLDS.values())),
        sheet_sha256=base.digest(SHEET), evidence=evidence))
    print('Verified the two revised voyage holds and four exact controls.')


if __name__ == '__main__':
    import sys
    assert sys.argv[1:] in (['observation'], ['verify'])
    (record_observations if sys.argv[1] == 'observation' else verify)()
