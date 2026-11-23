"""Verify all revised ruin dialogue, notices and captions in their native consumers."""

from inspect import getsource
from scripts import stage_ruins_clues_and_guides_20261118 as build
from scripts import verify_london_guild_assignments_20261118 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, native, stage, parent = build.base, build.native, build.stage, build.parent
ROOT = build.ROOT / "native_display_v1"
PROOF = ROOT / "native_display.json"
PRIOR = build.ROOT.with_name("research_v2") / ROOT.name / PROOF.name
MENU = PRIOR.parent.parent / "maria_native_menu"


def check_menu(prior, cmd):
    proof, = prior["menu_proofs"]
    assert proof["option_ids"] == cmd["record_ids"]
    assert base.digest(proof["menu_path"]) == proof["proof_sha256"]
    assert base.load(proof["menu_path"])["native_choice_object_hex"] == cmd["stored"]
    return proof | dict(candidate_menu_offset=cmd["stored_offset"], identical_native_object_reused=True)


source = getsource(previous.main)
verification = checked_text(source, {
    "rendered, styles, pictures, reused = [], [], [], []":
        "rendered, styles, pictures, reused, menus = [], [], [], [], []",
    "            if word == stage.STYLE:":
        """            if word in stage.MENU:
                menus.append(check_menu(previous, cmd))
                continue
            if word == stage.STYLE:""",
    "assert len(rendered) == 40 and len(styles) == 1": "assert len(rendered) == 77 and len(styles) == 8 and len(menus) == 1",
    '''k for k, row in rows.items() if row["decision"] == "revision"''':
        '''k for k, row in rows.items() if row["decision"] == "revision" and row["native_command_word"] not in stage.MENU''',
    'previous_sheets=previous["previous_sheets"] + previous["contact_sheets"]':
        'previous_sheets=previous["contact_sheets"], menu_proofs=menus',
})
scope = vars(previous) | globals()
exec(compile(verification, __file__ + "::unchanged-native-proof-and-menu-owner", "exec"), scope)

if __name__ == "__main__":
    scope["main"]()
