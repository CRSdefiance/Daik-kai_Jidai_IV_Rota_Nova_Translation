"""Bind complete captured menus to their own dialogue interval and ordinary A return."""
import argparse
from pathlib import Path

from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('fixture', 'terminal', 'body-proof', 'menu-proof', 'live-menus', 'out'):
        parser.add_argument('--' + name, type=Path, required=True)
    args = parser.parse_args()
    assert not args.out.exists()
    fixture, terminal, body, native, live = map(load, (
        args.fixture, args.terminal, args.body_proof, args.menu_proof, args.live_menus))
    assert terminal['terminal'] and terminal['frames'] == fixture['frames'] == body['frames'] == live['frames']
    assert body['all_selected_pages_observed_in_exact_fixture_order']
    assert live['all_declared_native_menus_have_complete_pixel_centering_bounds_andbackground_matches']
    assert body['evidence'][str(args.fixture)] == live['fixture_sha256'] == digest(args.fixture)
    assert body['evidence'][str(args.terminal)] == live['terminal_sha256'] == digest(args.terminal)
    assert digest(fixture['inputs']) == fixture['inputs_sha256']
    controls = load(fixture['inputs'])
    expected = {(row['block'], row['source_command_offset']): row for row in fixture['menus']}
    proven = {(row['block'], row['source_command_offset']): row for row in native['menus']}
    actual = {(row['block'], row['source_command_offset']): row for row in live['menus']}
    assert len(expected) == len(proven) == len(actual) and expected.keys() == proven.keys() == actual.keys()
    assert len({key[1] for key in expected}) == len(expected), 'Capture samples require unique source offsets in this receipt.'
    ordered = body['ordered_selected_source_calls']
    speech = fixture['selected_records']
    rows = []
    for key, menu in actual.items():
        declared, exact = expected[key], proven[key]
        assert declared['command_hex'] == exact['target_object_hex']
        assert Path(menu['proof']) == Path(exact['native_receipt'])
        assert digest(menu['proof']) == menu['proof_sha256'] == exact['native_receipt_sha256']
        previous = next(row for row in reversed(speech) if row['fixture_offset'] < declared['fixture_offset'])
        following = next(row for row in speech if row['fixture_offset'] > declared['fixture_offset'])
        left = max(row['frame'] for row in ordered if row['id'] == previous['id'])
        right = next(row['frame'] for row in ordered if row['id'] == following['id'] and row['page'] == 1)
        assert right > left
        samples = [row for row in live['menu_samples'] if row['source_command_offset'] == key[1]]
        assert len(samples) == menu['complete_live_samples'] and all(left < row['frame'] < right for row in samples)
        selected = [row for row in samples if row['visible_selected_option'] is not None]
        assert selected and {row['visible_selected_option'] for row in selected} == set(menu['observed_selected_options'])
        final_frame = max(row['frame'] for row in selected)
        presses = [row['start'] for row in controls if row['buttons'] == ['A'] and final_frame < row['start'] <= right]
        assert len(presses) == 1, (key, final_frame, right, presses)
        rows.append({**menu, 'preceding_speech': previous['id'], 'following_speech': following['id'],
                     'preceding_speech_frame': left, 'following_speech_frame': right,
                     'observed_default_return_A_input': presses[0]})
    args.out.parent.mkdir(parents=True, exist_ok=True)
    save(args.out, {**live, 'menus': rows, 'body_proof': str(args.body_proof),
                    'body_proof_sha256': digest(args.body_proof),
                    'ordinary_A_return_to_next_fixture_speech_observed': True,
                    'observed_each_menu_between_its_own_exact_preceding_and_following_speech': True,
                    'complete_live_menu_receipt': str(args.live_menus),
                    'complete_live_menu_receipt_sha256': digest(args.live_menus),
                    'return_binding_evidence': {str(path): digest(path) for path in (
                        args.fixture, args.terminal, args.body_proof, args.menu_proof,
                        args.live_menus, Path(fixture['inputs']), Path(__file__))}})
    print(f'Bound {len(rows)} captured menus to their own dialogue intervals and ordinary A returns.')


if __name__ == '__main__':
    main()
