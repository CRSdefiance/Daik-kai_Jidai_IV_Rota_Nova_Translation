"""Develop villages through actual typed passwords, using coordinates only for approach."""

import argparse
import io
import json
import struct
import sys
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import headless_desmume_v193 as harness
from scripts import native_location_fixture_v519 as location
from scripts.native_village_visits_v664 import relocate
from scripts.run_village_visits_v664 import CAP
from scripts.verify_regional_ui_v616 import glyphs
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/village_development_v665')
PREVIOUS = Path('work/analysis/village_visits_v664')
LETTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


class Controller(io.TextIOBase):
    """Read only exported pause images/RAM; issue ordinary input commands."""

    def __init__(self, village, folder, arm, answer):
        self.village, self.folder, self.arm, self.answer = village, folder, arm, answer
        self.font = GameAsciiFont.from_arm9(arm)
        self.frame, self.parent, self.error = 5200, None, None
        self.journal, self.phases, self.entries = [], {}, []
        self.generator = self.navigate()

    def readline(self, size=-1):
        try:
            command = next(self.generator)
        except StopIteration:
            command = {'stop': True}
        except (AssertionError, ValueError, OSError, KeyError, struct.error) as error:
            self.error = repr(error)
            command = {'stop': True}
        self.journal.append({'frame': self.frame, 'command': command})
        save(self.folder / 'controller_progress.json', {'village': self.village, 'answer': self.answer,
            'commands': self.journal, 'phases': self.phases, 'entered_character_states': self.entries,
            'error': self.error, 'controller_source_sha256': sha(Path(__file__).read_bytes())})
        self.frame = command.get('until', self.frame)
        return json.dumps(command) + '\n'

    def command(self, *, buttons=None, touch=None, frames=40):
        command = {'until': self.frame + frames, 'duration': 8, 'buttons': buttons or []}
        if touch is not None:
            command['touch'] = touch
        return command

    def image(self):
        return Image.open(self.folder / f'frame_{self.frame:06d}_navigation.png').convert('RGB')

    def main_editor(self):
        image = self.image()
        expected = glyphs(self.font, 'Promised Words')
        actual = {(x, y) for y in range(11) for x in range(84)
                  if image.getpixel((48 + x, 224 + y)) == (213, 214, 213)}
        return actual == expected

    def entry(self):
        path = self.folder / f'frame_{self.frame:06d}_arm9_ram.bin'
        raw = path.read_bytes()
        assert len(raw) == 0x400000
        marker = read('work/analysis/village_promised_words_plan.json')['keyboard_wrapper']['provider_vtable']
        needle = struct.pack('<I', marker)
        if self.parent is None:
            owners = [i - 4 for i in range(0x170000, len(raw) - 4, 4) if raw[i:i + 4] == needle]
            assert len(owners) == 1
            self.parent = owners[0]
        p = self.parent
        assert raw[p + 4:p + 8] == needle and struct.unpack_from('<I', raw, p + 0xD8)[0] == 18
        value = raw[p + 0xB4:p + 0xB4 + 19].split(b'\0', 1)[0].decode('ascii')
        assert struct.unpack_from('<I', raw, p + 0x78)[0] == len(value)
        return value, {'frame': self.frame, 'parent': p + 0x02000000, 'entry': value,
                       'RAM': str(path), 'RAM_sha256': sha(raw)}

    def confirm_visible_entry(self, expected):
        value, receipt = self.entry()
        assert value == expected and self.main_editor(), (self.frame, expected, value)
        image = self.image()
        actual = {(x, y) for y in range(11) for x in range(108)
                  if image.getpixel((60 + x, 244 + y)) == (230, 230, 230)}
        assert actual == glyphs(self.font, expected), (self.frame, 'complete visible entry differs', expected)
        receipt['complete108x11_input_foreground_and_blank_cells_exact'] = True
        self.entries.append(receipt)

    def navigate(self):
        if self.village == 18:
            commands = [json.loads(s) for s in (PREVIOUS / 'commands_Ezo_chief.jsonl').read_text(encoding='utf-8').splitlines()]
        else:
            commands = [json.loads(s) for s in (PREVIOUS / f'commands_chief_{self.village:02d}.jsonl').read_text(encoding='utf-8').splitlines()]
        for command in commands:
            if not command.get('stop'):
                yield command
        self.phases['chief_request'] = self.frame
        yield self.command(buttons=['A'], frames=400)
        self.phases['input_prompt'] = self.frame
        yield self.command(buttons=['A'], frames=400)
        self.phases['empty_keyboard'] = self.frame
        self.confirm_visible_entry('')
        prefix = ''
        for character in self.answer:
            # Original groups50/51 contain full-width Latin and symbols. The
            # village-specific insertion hook normalizes those keys to ASCII.
            group, index = (51, 10) if character == ' ' else (50, LETTERS.index(character))
            assert self.main_editor()
            yield self.command(touch=[168 if group == 50 else 182, 134])
            if self.main_editor():
                yield self.command(buttons=['A'])
            assert not self.main_editor()
            yield self.command(touch=[62 + index % 10 * 14, 30 + index // 10 * 14])
            value, _ = self.entry()
            if value == prefix:
                yield self.command(buttons=['A'])
            prefix += character
            self.confirm_visible_entry(prefix)
            print(f'V665 village{self.village}: entered {prefix!r}', flush=True)
        self.phases['complete_password_before_submission'] = self.frame
        yield self.command(buttons=['X'], frames=400)
        self.phases['answer_confirmation'] = self.frame
        yield self.command(buttons=['A'], frames=400)
        self.phases['accepted_clue'] = self.frame
        yield self.command(buttons=['A'], frames=400)
        self.phases['facilities_notice'] = self.frame
        yield self.command(buttons=['A'], frames=400)
        self.phases['developed_village_menu'] = self.frame
        count = 3 + int(self.village % 2 == 0) + int(self.village % 3 == 0) + int(self.village % 5 == 0)
        for _ in range(count - 2):
            yield self.command(buttons=['DOWN'], frames=100)
        yield self.command(buttons=['A'], frames=400)
        self.phases['departure'] = self.frame
        yield self.command(buttons=['A'], frames=400)
        self.phases['return_docking_prompt'] = self.frame
        yield self.command(buttons=['A'], frames=400)
        self.phases['developed_town_return'] = self.frame


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('village', type=int)
    parser.add_argument('--tag', default='first')
    parser.add_argument('--prepare-only', action='store_true')
    args = parser.parse_args()
    assert 0 <= args.village < 24 and args.tag.replace('_', '').isalnum()
    ROOT.mkdir(exist_ok=True)
    if not (ROOT / 'preflight.json').exists():
        old = read(PREVIOUS / 'preflight.json')
        frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
        save(ROOT / 'preflight.json', {k: old[k] for k in
            ('candidate', 'candidate_sha256', 'donor', 'donor_sha256', 'release_hashes')} | {
            'previous_goal_turn_classification': 'progress: V664 all24 initial village branches verified and archived',
            'all_original_audits_before': {n: read(Path('translations') / n) for n in frozen}})
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert sha(Path(pre['donor']).read_bytes()) == pre['donor_sha256']
    if args.prepare_only:
        return
    answer = next(r['english'] for r in read('translations/village_promised_words_manuscript_v1.json')['records']
                  if r['kind'] == 'ANSWER' and r['index'] == args.village)
    folder = CAP / f'village_development_v665_{args.village:02d}_{args.tag}'
    assert not folder.exists(), 'Retain previous evidence; use a fresh tag for a new run'
    folder.mkdir()
    arm = NdsImage.open(pre['candidate']).read_file('/__arm9__.bin')
    controller = Controller(args.village, folder, arm, answer)
    inputs = PREVIOUS / ('inputs_Ezo_chief.json' if args.village == 18 else f'inputs_chief_{args.village:02d}.json')
    old, stdin = location.relocate, sys.stdin
    location.relocate, sys.stdin = relocate, controller
    sys.argv = ['headless_desmume_v193.py', '--rom', pre['candidate'], '--out', str(folder),
        '--frames', '30000', '--inputs-json', str(inputs), '--battery-save', pre['donor'],
        '--pause-at', '5200', '--allow-location-fixtures', '--touchscreen', '--capture-every', '999999',
        '--dump-pause-ram', '--dump-ram', '--dump-native-state']
    try:
        harness.main()
    finally:
        location.relocate, sys.stdin = old, stdin
    if controller.error:
        raise RuntimeError('Controller stopped with retained evidence: ' + controller.error)
    print(f'V665 village{args.village} development/return run terminal at{controller.frame}.', flush=True)


if __name__ == '__main__':
    main()
