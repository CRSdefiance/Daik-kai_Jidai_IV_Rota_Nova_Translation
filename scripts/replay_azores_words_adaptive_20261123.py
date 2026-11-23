"""Use the verified keyboard controls to finish the ordinary Azores visit."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from dk4tool.rom.nds import NdsImage
from scripts import observe_ordinary_azores_voyage_20261123 as voyage
from scripts.observe_azores_promised_words_20261123 import ANSWER, ANSWER_SOURCE, DONOR, OBSERVED, RELEASE, ROOT as PRIOR
from scripts.reconcile_editorial_acceptance_20261123 import ARM, digest, read
from scripts.run_village_development_v665 import Controller, LETTERS
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_regional_ui_v616 import glyphs


ROOT = PRIOR.with_name("azores_words_adaptive_store") / "live_qualified"
FIRST_PAUSE = 10120


class WordEntry(Controller):
    def main_editor(self):
        image = self.image()
        actual = {(x, y) for y in range(11) for x in range(84)
                  if image.getpixel((48 + x, 225 + y)) == (213, 214, 213)}
        return actual == glyphs(self.font, "Promised Words")

    def confirm_visible_entry(self, expected):
        value, receipt = self.entry()
        assert value == expected and self.main_editor(), (self.frame, expected, value)
        image = self.image()
        actual = {(x, y) for y in range(11) for x in range(108)
                  if image.getpixel((60 + x, 245 + y)) == (230, 230, 230)}
        assert actual == glyphs(self.font, expected)
        self.entries.append(receipt | {"complete108x11_input_foreground_and_blank_cells_exact": True})

    def navigate(self):
        self.phases["empty_editor"] = self.frame
        self.confirm_visible_entry("")
        typed = ""
        for letter in self.answer:
            index = LETTERS.index(letter)
            yield self.command(touch=[164, 134], frames=80)
            if self.main_editor():
                yield self.command(buttons=["A"], frames=80)
            assert not self.main_editor()
            yield self.command(touch=[62 + index % 10 * 14, 30 + index // 10 * 14], frames=80)
            if self.entry()[0] == typed:
                yield self.command(buttons=["A"], frames=80)
            typed += letter
            self.confirm_visible_entry(typed)
        self.phases["complete_entry"] = self.frame
        for action, phase in (("X", "confirmation"), ("A", "clue"), ("A", "facilities_notice"), ("A", "menu_return")):
            yield self.command(buttons=[action], frames=280)
            self.phases[phase] = self.frame


def main():
    assert not ROOT.exists() and ROOT.parent.is_dir()
    release = read(RELEASE)
    rom = Path(release["candidate"])
    assert digest(rom) == release["candidate_sha256"]
    assert digest(DONOR) == read(OBSERVED)["battery_save_preloaded"]["source_sha256"]
    assert ANSWER == next(row["english"] for row in read(ANSWER_SOURCE)["records"]
                          if row["kind"] == "ANSWER" and row["index"] == 13)
    controller = WordEntry(13, ROOT / "capture", NdsImage.open(rom).read_file(ARM), ANSWER)
    controller.frame = FIRST_PAUSE
    source = checked_text(getsource(voyage.main), {
        "native, original = harness.ct, sys.argv": "native, original, previous_stdin = harness.ct, sys.argv, sys.stdin",
        "        harness.ct = CoreLoader()": "        harness.ct = CoreLoader()\n        sys.stdin = controller",
        "        sys.argv, harness.ct = original, native": "        sys.argv, harness.ct, sys.stdin = original, native, previous_stdin",
    })
    current = SimpleNamespace(RELEASE=RELEASE, ROM=rom)
    scope = vars(voyage) | dict(ROOT=ROOT, HISTORY=OBSERVED, FIRST_PAUSE=FIRST_PAUSE, current=current,
                                controller=controller, __file__=__file__)
    exec(compile(source, __file__ + "::ordinary-keyboard-replay", "exec"), scope)
    scope["main"]()
    assert not controller.error, controller.error
    assert [row["entry"] for row in controller.entries] == [ANSWER[:i] for i in range(len(ANSWER) + 1)]


if __name__ == "__main__":
    main()
