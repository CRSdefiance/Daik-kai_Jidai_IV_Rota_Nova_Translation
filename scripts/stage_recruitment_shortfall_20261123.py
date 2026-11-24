"""Reflow the two required-crew prompts identified by the capacity review."""

from inspect import getsource
from pathlib import Path

from scripts import register_recruitment_capacity_20261123 as parent
from scripts import stage_recruitment_capacity_wraps_20261123 as capacity
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = Path(".codex-release-work/recruitment_shortfall_20261123")
ROM, PROOF = ROOT / "Recruitment_Shortfall_STAGED.nds", ROOT / "stored_proof.json"
ARM, COMMON, CLEAN = capacity.ARM, capacity.COMMON, capacity.CLEAN
COUNTS = (1, 5, 9, 10, 12, 67, 99, 100, 324, 999, 1000, 9999, 10000, 65535)
DRAFTS = {
    1039: ("Still %s short on crew. Shall I round up more?",
           "The experienced officer gives the exact shortage and asks gently. The complete phrase round up stays together."),
    1041: ("We're %s short on crew. Shall I recruit more?",
           "Manuel's measured offer follows the exact staffing shortage. Recruit more stays together."),
}


def main():
    compare_code = checked_text(getsource(capacity.compare), {
        "range(1035, 1049)": "range(1035, 1042)",
        '        if key == 1039:\n            decision, note = "wrap lead", "The original voice is gentle. At common headcounts the current formatter splits round up."\n        elif key == 1041:\n            decision, note = "wrap lead", "The original offer is measured. At common headcounts recruiting? sits alone."\n': "",
        'assert len(lines) == 2 and len(lines[-1]) >= 15': 'assert len(lines) == 2 and len(lines[-1]) >= 13',
        'assert lines[0].endswith((".", "Want")) or value >= 10000, (key, value, lines)':
            'assert lines[0].endswith("Shall I") and lines[1] == ENDINGS[key], (key, value, lines)',
        '(1, 67, 65535)': '(1, 12, 65535)',
        '{key} / {value} spare': '{key} / {value} short',
    })
    main_code = checked_text(getsource(capacity.main), {
        'assert visit["ROM_sha256"] == base.load(parent.parent.RELEASE)["candidate_sha256"]':
            'assert visit["ROM_sha256"] == base.load(parent.parent.parent.RELEASE)["candidate_sha256"]',
        '''    proof_1048 = records[-1]["cases"][3]
    assert proof_1048["count"] == 67 and proof_1048["previous_lines"] == [
        "There's still room for 67 more", "aboard. Shall I try", "recruiting more?"]''':
            '''    observed = {r["message_id"]: r for r in records}
    assert observed[1039]["cases"][0]["previous_lines"][1] == "up some more?"
    assert observed[1041]["cases"][0]["previous_lines"][1] == "recruiting?"''',
        "original_voice_table=CAPACITY": "original_voice_table=SHORTFALL",
        "Staged seven capacity prompts": "Staged two shortfall prompts",
    })
    scope = vars(capacity) | dict(ROOT=ROOT, ROM=ROM, PROOF=PROOF, parent=parent, DRAFTS=DRAFTS, COUNTS=COUNTS,
                                  ENDINGS={1039: "round up more?", 1041: "recruit more?"})
    exec(compile(compare_code + "\n" + main_code, __file__ + "::shortfall", "exec"), scope)
    scope["main"]()


if __name__ == "__main__":
    main()
