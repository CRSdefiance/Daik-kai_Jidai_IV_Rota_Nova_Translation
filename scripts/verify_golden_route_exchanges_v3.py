"""Bind the observed Lisbon sale, Guild report and return to the reviewed candidate."""

from inspect import getsource
from json import dumps, loads
from types import SimpleNamespace

from scripts import verify_golden_route_exchanges_v1 as prior
from scripts import verify_golden_route_exchanges_v2 as layout
from scripts.source_locked_derivation_v5118 import checked_text


stage, base = layout.stage, layout.base
ROOT, ROM, PROOF = layout.ROOT, layout.ROM, layout.PROOF
BOOT, VISUAL, LIVE, CHECKPOINT, QA = layout.BOOT, layout.VISUAL, layout.LIVE, layout.CHECKPOINT, layout.QA
payout = SimpleNamespace(OUTPUT=layout.payout.OUTPUT, TABLE=prior.payout.TABLE)
HOLDS = {14000: 3324, 14300: 3328, 14600: 3336, 14900: 3344, 15200: 3348, 15500: 3356,
         15800: 3360, 20900: 3380, 21500: 3381, 21800: 3385}
FIXTURE_FRAME, DISCOVERY_FRAME, RETURN_FRAME, JULIO_FRAME = 12800, 21200, 22100, 17300


def verify_gameplay():
    source = checked_text(getsource(prior.verify_gameplay), {
        "assert report['frames'] == replay.END and not report['callback_errors']":
            "assert report['frames'] == RETURN_FRAME and not report['callback_errors']\n"
            "    assert terminal['original_save_unchanged']\n"
            "    donor = report['battery_save_preloaded']\n"
            "    assert donor['copied_byte_exact_before_cold_boot'] and base.digest(donor['source']) == donor['source_sha256']\n"
            "    journal = report_path.with_name('navigation_command_journal.json')\n"
            "    received = base.load(journal)['commands_received']\n"
            "    commands = Path(terminal['commands'])\n"
            "    assert all(row['validation_passed'] for row in received)\n"
            "    assert [row['command'] for row in received] == [loads(line) for line in commands.read_text(encoding='utf-8').splitlines()]",
        "report['read_only_capture_RAM_snapshots']": "report['read_only_pause_RAM_snapshots']",
        "row['path'].endswith('.png')": "row['path'].endswith('_navigation.png')",
        'replay.PAUSE': 'FIXTURE_FRAME',
        "[fixture | {'frame': replay.PAUSE}]": "[loads(dumps(fixture)) | {'frame': FIXTURE_FRAME}]",
        '(22600, 23200, 30400, 33100, 34000)': '(13400, 14000, 16100, 20900, 21800)',
        'payout.OUTPUT, terminal_path, report_path, Path(__file__))':
            'payout.OUTPUT, terminal_path, report_path, journal, commands, Path(__file__))',
        'discovery_view=frames[33400], guild_menu_return=frames[replay.END],':
            'discovery_view=frames[DISCOVERY_FRAME], guild_menu_return=frames[RETURN_FRAME],\n'
            '        inherited_Julio_First_glyph_and_reflow_observed=frames[JULIO_FRAME],',
    })
    environment = vars(prior) | vars(layout) | globals()
    exec(compile(source, __file__ + '::observed-lisbon-sale-and-guild', 'exec'), environment)
    environment['verify_gameplay']()


if __name__ == '__main__':
    verify_gameplay()
