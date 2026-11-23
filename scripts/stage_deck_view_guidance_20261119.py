"""Clarify the room-assignment help observed in Rafael's Lisbon Deck View."""

from inspect import getsource
from pathlib import Path
from struct import unpack_from

from ndspy.code import MainCodeFile
from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.deck_filter_help import BASE, POOL, cache_plan, compiled
from scripts import observe_rafael_lisbon_return_20261119 as ordinary
from scripts import register_artifact_rumor_wraps_20261119 as parent
from scripts import verify_deck_filter_native_v263 as native_check
from scripts.prepare_all_routes_promotion_20261111 import verify_runtime
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_deck_filter_release_v263 import ink

base, native = parent.base, parent.native
ARM = native.ARM
ROOT = Path('work/deck_view_guidance_20261119/staged_v2')
ROM, PROOF = ROOT / 'Deck_View_Guidance_STAGED.nds', ROOT / 'stored_proof.json'
HISTORY = Path('translations/deck_filter_help_review_v2.json')
FRAME = 59380
ORIGINS = (33, 49, 81)
WORDS = {
    0x14F460: (None, 'Unassigned clearly filters navigators who have no station.'),
    0x14F490: (None, 'All contrasts with Unassigned and fits the existing filter.'),
    0x15594: (None, 'The instruction names the screen and its purpose in a single line.'),
    0x15598: ('Pick a navigator and assign them a room. Room type sets their duty.',
              'Describe the two actions and keep the relationship between room type and duty together on the next line.'),
    0x1559C: ('Each duty requires certain abilities. Navigators must meet them to qualify. Higher ability improves performance.',
              'State the ability threshold and the benefit of higher ability in complete statements, with a clear plural antecedent.'),
}


def screen_baseline(arm, rows):
    report_path = ordinary.CAPTURE / 'capture_report.json'
    report = base.load(report_path)
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['ROM_sha256'] == base.digest(ordinary.active.ROM)
    shot, = (r for r in report['frames_captured'] if r['frame'] == FRAME and r['path'].endswith('_navigation.png'))
    snapshot, = (r for r in report['read_only_pause_RAM_snapshots'] if r['frame'] == FRAME)
    assert base.digest(shot['path']) == shot['PNG_sha256'] and base.digest(snapshot['path']) == snapshot['sha256']
    live = Path(snapshot['path']).read_bytes()
    for row in rows:
        at = row['target_pointer'] - BASE
        assert unpack_from('<I', live, row['field'])[0] == row['target_pointer']
        assert live[at:at + len(row['current_bytes'])] == row['current_bytes']
    with Image.open(shot['path']) as frame:
        screen = frame.convert('RGB')
    font = GameAsciiFont.from_arm9(arm)
    expected = set()
    for row, y in zip(rows[2:], ORIGINS, strict=True):
        for k, text in enumerate(row['current_Compiled'].split('\n')):
            expected |= ink(font, text[1:] if k else text, 0, y + k * 16)
    observed = {(x, y) for y in range(30, 140) for x in range(256) if screen.getpixel((x, y)) == (230, 230, 230)}
    assert expected == observed
    return shot, snapshot, expected


def write_native_preview(arm, rows, frame):
    plan_path = ROOT / 'runtime_plan.json'
    base.save(plan_path, dict(records=rows, cache=cache_plan(arm)))
    recipe = checked_text(getsource(native_check.main), {
        'e["y"] + 11 <= 128': 'e["y"] + 12 <= 128',
        'expected[(e["y"] + y) * width + e["x"] + x]': 'expected[(e["y"] + y + 1) * width + e["x"] + x]',
        'boot_rom = NdsImage.open("out/all_routes_combined_v261_candidate.nds")': 'boot_rom = NdsImage.open(ROM)',
        '    (ROOT / "native_proof.json").write_text': '    save_preview(expected)\n    (ROOT / "native_proof.json").write_text',
    })

    def save_preview(expected):
        output = Image.new('RGB', (1024, 278), '#263238')
        labels = ImageDraw.Draw(output)
        labels.text((6, 5), 'Previous / ordinary Lisbon Deck View', fill='white')
        labels.text((518, 5), 'Revised / native preview', fill='white')
        with Image.open(frame['path']) as before:
            output.paste(before.convert('RGB').crop((0, 0, 256, 128)).resize((512, 256), Image.Resampling.NEAREST), (0, 20))
        after = Image.frombytes('L', (256, 128), bytes(232 if x else 46 for x in expected))
        output.paste(after.resize((512, 256), Image.Resampling.NEAREST), (512, 20))
        output.save(ROOT / 'deck_help_comparison.png')

    scope = vars(native_check) | dict(ROOT=ROOT, ROM=ROM, save_preview=save_preview)
    exec(compile(recipe, __file__ + '::native-deck-guidance', 'exec'), scope)
    scope['main']()


def main():
    assert not ROOT.exists()
    release = base.load(parent.RELEASE)
    assert base.digest(parent.ROM) == release['candidate_sha256'] and base.digest(base.REGISTRY) == release['registry_sha256']
    clean, rom = map(base.NdsImage.open, (native.CLEAN, parent.ROM))
    original, arm = (r.read_file(ARM) for r in (clean, rom))
    assert native.digest(arm) == release['target_ARM9_sha256']
    image = MainCodeFile(arm, BASE)
    pool = image.sections[3].data
    rows, spans = [], []
    for prior in base.load(HISTORY)['records']:
        field = prior['field']
        text, reason = WORDS[field]
        source, = unpack_from('<I', original, field)
        installed, = unpack_from('<I', arm, field)
        slot = installed - POOL
        assert source == prior['source_pointer'] and installed == prior['target_pointer']
        encoded = prior['source_Japanese'].encode('cp932') + b'\0'
        assert original[source-BASE:source-BASE + len(encoded)] == encoded
        current = prior['compiled'].encode('ascii') + b'\0'
        assert 0 <= slot < slot + len(current) <= len(pool) - 112
        assert pool[slot:slot + len(current)] == current
        english = text or prior['English']
        proposed = compiled(field, english, 2)
        assert len(proposed.split('\n')) == len(prior['compiled'].split('\n'))
        updated = proposed.encode('ascii') + b'\0'
        if text:
            assert len(updated) <= len(current), (hex(field), len(updated), len(current))
            spans.append((slot, current))
            pool[slot:slot + len(current)] = updated.ljust(len(current), b'\0')
        rows.append(prior | dict(English=english, compiled=proposed, decision='revision' if text else 'retention',
            localization_note=reason, current_bytes=current, current_Compiled=prior['compiled'], current_English=prior['English'],
            review=prior['review'] | {'formatting': not text}, exact_field=hex(BASE + field)))
    compiled_arm = bytes(image.save())
    assert len(spans) == 2 and cache_plan(compiled_arm) == cache_plan(arm)
    for offset, old in spans:
        pool[offset:offset + len(old)] = old
    assert bytes(image.save()) == arm
    verify_runtime(compiled_arm, release)
    shot, snapshot, baseline = screen_baseline(arm, rows)
    rom.replace_file(ARM, compiled_arm)
    target = bytes(rom.rom.save())
    rom.replace_file(ARM, arm)
    assert bytes(rom.rom.save()) == parent.ROM.read_bytes()
    for row in rows:
        row['current_hex'] = row.pop('current_bytes').hex()
    ROOT.mkdir(parents=True)
    ROM.write_bytes(target)
    (ROOT / 'research_arm9.bin').write_bytes(compiled_arm)
    write_native_preview(compiled_arm, rows, shot)
    preview = ROOT / 'deck_help_comparison.png'
    base.save(PROOF, dict(candidate_sha256=base.digest(ROM), predecessor_sha256=release['candidate_sha256'],
        clean_input_sha256=release['clean_input_sha256'], target_ARM9_sha256=native.digest(compiled_arm),
        whole_parent_inverse=True, records=rows, previous_live_hold=shot, previous_read_only_RAM=snapshot,
        previous_exact_help_pixels=len(baseline), proven_native_glyph_y_offset=1, native_proof=str(ROOT/'native_proof.json'),
        sheets=[dict(path=str(preview), sha256=base.digest(preview))],
        evidence={str(p): base.digest(p) for p in (HISTORY, parent.RELEASE, Path(__file__), ROOT/'native_proof.json')}))
    print('Staged two Deck help wording improvements and three retentions with intact six-line native layout.')


if __name__ == '__main__':
    main()
