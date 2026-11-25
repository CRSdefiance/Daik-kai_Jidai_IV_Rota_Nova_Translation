"""Resolve short contextual item references and verify the selected title fixes."""
from pathlib import Path
import re

from scripts import stage_current_item_story_terms_20261119 as build
from scripts.prepare_london_guild_assignments_20261118 import text_records

base, native = build.base, build.native
OUTPUT = build.review.ROOT / "item_term_dispositions.json"
ITEMS = {
    "Glassmaking Guide": (14, (0, 214, 61)),
    "Minotaur Axe": (41, (0, 219, 20)),
    "Thales Paper Map": (155, (2, 61, 238)),
    "Periander Stone Map": (157, (2, 61, 270)),
    "Solon Leaf Map": (158, (2, 61, 302)),
    "Cleobulus Cloth Map": (156, (2, 61, 334)),
    "Chiron Bamboo Map": (160, (2, 61, 366)),
    "Bias Coin Map": (159, (2, 61, 410)),
    "Kediri Talisman": (152, (2, 61, 425)),
    "Pittacus Blade Map": (161, (2, 61, 445)),
}
RETENTIONS = {
    (1, 172, 605): "The speaker mistakes rabbit droppings for a peppercorn and describes making spice. Keeping the fruit name preserves the botanical claim and the reveal.",
    (2, 168, 653): "The speaker calls the object a peppercorn and even advises where it might grow. The next reply reveals what it really is. Keep the object name in the joke.",
    (3, 139, 649): "The same joke needs the loose peppercorn that the speaker mistakes for a useful spice. The item catalogue's plant label would change the setup.",
    (1, 240, 381): "The previous question names Demon-Piercing Arrow. Cesare can say it while explaining the legend without repeating the full name.",
    (2, 136, 55): "Emilio and Lil are already looking at both halves. Upper and Lower Stone Tablets names the pair naturally.",
    (2, 268, 547): "The guildmaster passes on a rumor about a demon statue. The legend leaves the object's purpose unknown.",
    (2, 268, 609): "The companion echoes the description they just heard. Its eventual item title would give away more than the rumor.",
    (3, 238, 575): "The guildmaster repeats hearsay about a statue sealed in the ruins. The characters have yet to inspect it.",
    (3, 238, 637): "Keep the short questioning echo that follows the guildmaster's description.",
}


def speech_rows(image, archive_path, block, inventory):
    arm = image.read_file(native.ARM)
    bank = native.IlnkContainer.parse(image.read_file(archive_path)).blocks[block]
    return [(c["offset"] + offset, selector, body) for c in inventory(arm, bank)[0] if c["word"] == 0x4000
            for offset, selector, body, _ in text_records(bytes.fromhex(c["whole_command_hex"]), c["word"])]


def main():
    assert not OUTPUT.exists()
    scan_path = build.review.ROOT / "block_term_inventory.json"
    scan = base.load(scan_path)
    assert scan["candidate_sha256"] == base.digest(build.parent.ROM)
    clean, old, target = map(base.NdsImage.open, (native.CLEAN, build.parent.ROM, build.ROM))
    report, draft = map(base.load, (build.PROOF, build.review.OUTPUT))
    source = {(r["route"], r["block"], r["source_reference"]["record_index"]): r for r in draft["records"]}
    fixes = []
    for title, (id_, key) in ITEMS.items():
        row = source[key]
        group, = (g for g in report["groups"] if (g["route"], g["block"]) == key[:2])
        proof = scan["by_item"][str(id_)]
        binding, = (p for p in proof if p["file_path"] == row["file_path"] and p["block"] == row["block"])
        assert binding["English"] == title and binding["Japanese"] in row["Japanese"]
        assert title in row["english"]
        plan = group["plans"][row["id"]]
        assert any(title in text for text in plan["lines"])
        fixes.append(dict(id=row["id"], item_ID=id_, title=title, original_item_binding=binding,
                          native_complete_title_lines=plan["lines"]))

    keep = []
    inv, _, _ = native.scoped_inventory()
    for (route, block, offset), reason in RETENTIONS.items():
        path = f"/data/SC{route}.DK4"
        a, b, z = (speech_rows(im, path, block, inv) for im in (clean, old, target))
        assert b == z and [r[1] for r in a] == [r[1] for r in b]
        n, = (i for i, r in enumerate(a) if r[0] == offset)
        position, selector, body = b[n]
        keep.append(dict(file_path=path,block=block,source_body_offset=offset,current_body_offset=position,
                         selector=selector,source_hex=a[n][2].hex(),current_hex=body.hex(),
                         source_japanese=a[n][2].decode("cp932"),current_english=body.decode("ascii"),
                         reason=reason,exact_membership_of_surrounding_speech_source_and_current=True))
    crown = build.parent.VERIFY / "silla_crown_item_binding.json"
    assert base.load(crown)["all_sixty_literal_Japanese_mentions_accounted_for"]
    base.save(OUTPUT, dict(candidate_sha256=base.digest(build.ROM),revision_bindings=fixes,
        contextual_retentions=keep,earlier_exact_crown_terminology_receipt=str(crown),
        earlier_exact_crown_terminology_sha256=base.digest(crown),inventory_evidence_sha256=base.digest(scan_path),
        scope="Exact catalogue titles and deliberate shorthand in the selected exchanges",new_dialogue_credit=0))
    print("Bound ten corrected names, nine short or figurative references, and the existing Crown review.")


if __name__ == "__main__":
    main()
