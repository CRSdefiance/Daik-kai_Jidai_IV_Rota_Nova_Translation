"""Keep short phrases together in the guild and survey dialogue."""

from types import FunctionType

from scripts import stage_guild_search_and_survey_20261118 as prior


base, native, parent, precedent = prior.base, prior.native, prior.parent, prior.precedent
ROOT = prior.ROOT.with_name("guild_search_and_survey_20261118_v3")
ROM, STORED = ROOT / prior.ROM.name, ROOT / prior.STORED.name
MANUSCRIPT = prior.MANUSCRIPT.with_name("guild_search_and_survey_20261118_v3.json")
PHRASES = {
    (0, 266, 37): ("It looks like", "making money"),
    (0, 266, 56): ("We're going",),
    (0, 269, 14): ("He's a slippery one",),
    (1, 259, 86): ("A strange bunch", "hanging around there"),
    (2, 247, 9): ("I'd like you",),
    (3, 230, 52): ("It's over.",),
}
EDITS = prior.EDITS.copy()
for key, protected in PHRASES.items():
    text, earlier, note = EDITS[key]
    EDITS[key] = (text, earlier + protected, note)


def validate_native(ctx, revised):
    old = base.load(prior.STORED)
    assert old["candidate_sha256"] == base.digest(prior.ROM)
    assert old["manuscript_sha256"] == base.digest(prior.MANUSCRIPT)
    assert old["previous_sha256"] == ctx.release["candidate_sha256"]
    prior_image = base.NdsImage.open(prior.ROM)
    for path in (native.ARM, "/GRP/KANJI.FNT"):
        assert ctx.image.read_file(path) == prior_image.read_file(path)
    approved = {(r["route"], r["id"]): r for r in base.load(prior.MANUSCRIPT)["records"] if r["decision"] == "revision"}
    fresh = []
    for row in revised:
        earlier = approved.pop((row["route"], row["id"]))
        turn = row["source_reference"]["record_index"]
        if (row["route"], row["block"], turn) in PHRASES:
            fresh.append(row)
            continue
        for field in ("source_reference", "current_reference", "english", "target_hex"):
            assert earlier[field] == row[field]
        for key, value in row["staged_reference"].items():
            if key != "block_sha256":
                assert earlier["staged_reference"][key] == value
        for page in earlier["after_native"]["pages"]:
            assert native.digest(bytes.fromhex(page["native_plane_hex"])) == page["plane_sha256"]
        row["after_native"] = earlier["after_native"]
    assert not approved and len(fresh) == len(PHRASES)
    precedent.validate_native(ctx, fresh)
    return [(f"SC{row['route']} {row['id'].split('_B')[1]} {page['page']}/{len(row['after_native']['pages'])}",
             bytes.fromhex(page["native_plane_hex"]))
            for row in revised for page in row["after_native"]["pages"]]


scope = prior.scope | globals()
for name in ("historical", "review_exchange", "collect", "main"):
    scope[name] = FunctionType(prior.scope[name].__code__, scope)


if __name__ == "__main__":
    scope["main"]()
