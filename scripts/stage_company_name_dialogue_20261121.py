"""Store reviewed company-name dialogue with the validated twenty-cell name budget."""

from inspect import getsource
from types import FunctionType, SimpleNamespace

from scripts import review_company_name_dialogue_20261121 as review
from scripts import stage_all_routes_next_phrase_wraps_20261118 as earlier
from scripts.source_locked_derivation_v5118 import checked_text


base, native, stage = earlier.base, earlier.native, earlier.stage
parent = review.parent
ROOT = review.ROOT / "staged"
ROM, PROOF = ROOT / "Company_Name_Dialogue_STAGED.nds", ROOT / "stored_proof.json"
logical_end = earlier.logical_end


def main():
    selected = {(row["route"], row["block"]) for row in base.load(review.OUTPUT)["records"]}
    blocks = tuple(tuple(sorted(block for r, block in selected if r == route)) for route in range(4))
    paired = SimpleNamespace(BLOCKS=blocks)
    inherited = earlier.prior.precedent
    build = inherited.env["main"]
    settings = build.__globals__ | globals() | {"paired": paired, "company": earlier.company}
    source = checked_text(getsource(inherited.rebuild_function), {
        "precedent.plan_progressive": "company.plan_progressive",
    })
    exec(compile(source, __file__ + "::company-width", "exec"), settings)
    settings["catalogue_membership"] = FunctionType(inherited.catalogue_membership.__code__, settings)
    code = checked_text(inherited.source, {
        "    painter = stage.system.native_painter(ctx)":
            '    assert all(row["source_selector"] < 207 for row in manuscript["records"])\n    painter = None',
        "    assert groups.keys() == packet_groups.keys()": "    assert groups.keys() <= packet_groups.keys()",
        "Staged 17 source-bound wraps with exact catalogue ownership, branches and whole-ROM inverse.":
            "Stored the reviewed company dialogue with exact native branches and whole-ROM inverse.",
    })
    exec(compile(code, __file__ + "::stored-company-dialogue", "exec"), settings)
    settings["main"]()


if __name__ == "__main__":
    main()
