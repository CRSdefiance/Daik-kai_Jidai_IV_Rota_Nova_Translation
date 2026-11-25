"""Check complete mutiny panels and unchanged captions in paired story replays."""

from pathlib import Path

from PIL import Image, ImageChops, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import replay_aziza_mutiny_dialogue_20261115 as replay
from scripts import stage_aziza_mutiny_dialogue_20261115 as stage
from scripts.audit_lil_B221_English_paths_v7004 import body_masks
from scripts.replay_lil_ceramics_wrap_20261111 import masks
from scripts.replay_ritual_officiant_labels_20261115 import visible_name
from scripts.verify_captain_biographies_v1 import captured, shots


base, ROOT = stage.base, stage.ROOT
OUTPUT, SHEET = ROOT / 'playback_verification.json', ROOT / 'gameplay_comparison.png'


def load(route, side, sha):
    folder = ROOT / f'SC{route}_{side}'
    receipt = folder / 'fixture.json'
    fixture = base.load(receipt)
    report_path = Path(fixture['capture_report'])
    assert base.digest(report_path) == fixture['capture_sha256']
    report = base.load(report_path)
    assert fixture['candidate_sha256'] == sha and fixture['whole_candidate_inverse']
    assert report['ROM_sha256'] == fixture['fixture_sha256'] == base.digest(folder / 'initialized_dialogue_RESEARCH_ONLY.nds')
    assert report['frames'] == replay.END and report['cold_boot'] and not report['savestate_loaded']
    assert not report.get('battery_save_preloaded') and not report['callback_errors']
    assert not any(v for k, v in report.items() if k.startswith('synthetic_'))
    return fixture, report, {str(p): base.digest(p) for p in (receipt, report_path)}


def main():
    assert not OUTPUT.exists() and not SHEET.exists()
    staged, manuscript = map(base.load, (stage.STORED, stage.REVIEW))
    assert base.digest(stage.ROM) == staged['candidate_sha256']
    rows = {(row['route'], row['ordinal']): row for row in manuscript['records'] if row['decision'] == 'revision'}
    pictures, holds, unchanged, nameplates, evidence = [], [], {}, {}, {}
    font = GameAsciiFont.from_arm9(base.NdsImage.open(stage.ROM).read_file(stage.ARM))
    for route in (0, 1):
        before, old_r, old_e = load(route, 'before', staged['previous_sha256'])
        after, new_r, new_e = load(route, 'after', staged['candidate_sha256'])
        evidence.update(old_e | new_e)
        assert old_r['scripted_input_schedule'] == new_r['scripted_input_schedule']
        assert old_r['core_DLL_sha256'] == new_r['core_DLL_sha256'] and old_r['core_options'] == new_r['core_options']
        old, new = shots(old_r), shots(new_r)
        assert old.keys() == new.keys()
        selected = dict(zip(replay.HOLDS, replay.ORDINALS[route], strict=True))
        unchanged[route] = []
        for frame in old:
            a, b = captured(old[frame]), captured(new[frame])
            evidence.update({item['path']: item['PNG_sha256'] for item in (old[frame], new[frame])})
            diff = ImageChops.difference(a, b).getbbox()
            ordinal = selected.get(frame)
            if ordinal is not None:
                index = replay.ORDINALS[route].index(ordinal)
                ident = after['speech_rows'][index]['selector']
                if ident in stage.LABELS:
                    label = stage.LABELS[ident][0]
                    assert visible_name(font, a, label) and visible_name(font, b, label), (route, frame, label)
                    nameplates.setdefault(label, []).append({'route': route, 'frame': frame})
            if (route, ordinal) not in rows:
                assert diff is None, (route, frame, diff)
                unchanged[route].append(frame)
                continue
            row = rows[route, ordinal]
            assert before['speech_rows'][index] == row['current_reference']
            assert after['speech_rows'][index] == row['staged_reference']
            assert diff and 16 <= diff[0] < diff[2] <= 232 and 296 <= diff[1] < diff[3] <= 360
            for side, screen in (('before', a), ('after', b)):
                page, = row[side + '_native']['pages']
                expected = masks(bytes.fromhex(page['native_plane_hex']))
                assert body_masks(screen) == expected, (route, row['id'], frame, side)
            holds.append({'file_path': row['file_path'], 'record': row['id'], 'frame': frame,
                          'before': old[frame], 'after': new[frame], 'changed_bounds': diff})
            pictures.append((f"SC{route} {row['id'].split('_B')[1]}", a, b))
    assert len(holds) == len(pictures) == 3 and set(nameplates) == {'Angel', 'Snake'}
    sheet = Image.new('RGB', (1024, 265 * len(pictures)), '#263238')
    draw = ImageDraw.Draw(sheet)
    for row, (label, old, new) in enumerate(pictures):
        for column, page in enumerate((old, new)):
            x, y = column * 512, row * 265
            draw.text((x + 4, y + 4), f"{label} {'before' if column == 0 else 'after'}", fill='white')
            sheet.paste(page.crop((0, 264, 256, 384)).resize((512, 240), Image.Resampling.NEAREST), (x, y + 18))
    sheet.save(SHEET)
    base.save(OUTPUT, {'candidate_sha256': staged['candidate_sha256'], 'initialized_story_excerpts': True,
                       'holds': holds, 'unchanged_full_frames': unchanged, 'complete_nameplates': nameplates,
                       'new_natural_activation': False, 'hardware': False, 'sheet_sha256': base.digest(SHEET),
                       'evidence': evidence})
    print('Verified three changed story panels and complete Angel and Snake nameplates.')


if __name__ == '__main__':
    main()
