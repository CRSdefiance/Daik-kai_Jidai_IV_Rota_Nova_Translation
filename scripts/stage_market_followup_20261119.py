"""Review the Market investment and reward exchanges on the current ROM."""

from pathlib import Path
from types import FunctionType

from scripts import register_battle_dialogue_followup_20261119 as parent
from scripts import stage_market_reward_dialogue_20261115 as rewards
from scripts import stage_market_trade_dialogue_20261115 as trade
from scripts import stage_sea_hazard_dialogue_20261119 as shared
from scripts.stage_shared_notices_storage_v1 import relocate

base, native, workflow = parent.base, parent.native, shared.workflow
ARM, COMMON, CLEAN = shared.ARM, shared.COMMON, shared.CLEAN
ROOT = Path("work/market_followup_20261119")
ROM, PROOF = ROOT / "Market_Followup_RESEARCH_ONLY.nds", ROOT / "staged.json"
REVIEWS = tuple(Path(f"releases/all_routes_editorial_20261115_{kind}_candidate/verification/registered_review.json")
                for kind in ("market_trade_dialogue", "market_reward_dialogue"))
EDITS = {
    763: ("You're going to invest? I knew you weren't like the others! How much will you put in?",
          ("You're going to invest?", "I knew you weren't like the others!", "How much will you put in?")),
    765: ("I'll boost your market share a bit. Don't worry, I'll take care of it.",
          ("I'll boost your market share a bit.", "Don't worry, I'll take care of it.")),
    775: ("For all those popular goods, let me write you a letter of recommendation, too.",
          ("For all those popular goods,", "let me write you", "a letter of recommendation, too.")),
    782: ("Hmm... All right! For those popular goods, I'll throw in a little extra.",
          ("For those popular goods,", "I'll throw in a little extra.")),
}
REASONS = {
    745: "The brief follow-up fits the return to the same counter and invites the next request.",
    746: "'Just browsing?' carries the trader's mild disappointment after a zero amount.",
    747: "The trader accepts the investment, thanks the customer and says the money will be put to use.",
    748: "Keep the surprise and apology before the invitation to try again with more money.",
    749: "The full cargo warning leads directly to the practical suggestion to buy less.",
    753: "The short warning correctly identifies funds as the condition preventing the purchase.",
    761: "The apology and two steps match the refusal. The substituted facility identifies where to sign.",
    762: "The trader states why the offer is unexpected, appreciates it and asks for an amount in four distinct beats.",
    763: "Keep the surprised opening, a complete line for the trader's flattery and the amount question that follows.",
    764: "The lack of money, the blunt rebuke and the fee for viewing remain separate spoken beats.",
    765: "Put the modest increase and the trader's reassurance in two complete thoughts and keep the established market-share term.",
    766: "The invitation closes each benefit branch naturally and leaves the time of the next visit open.",
    774: "Keep the trader's sudden idea and the precise introduction title. The goods explain the favor.",
    775: "Thank the player for the large sale in the opening, then keep the writing offer and recommendation title intact.",
    776: "Keep the surprise and the greater sale quantity. The complete letter name distinguishes this favor.",
    777: "The trader notices what the player has and explains that adding words upgrades the existing letter.",
    778: "The enthusiastic offer names the recommendation, distinct from the introduction given in the other branch.",
    779: "The small-town restriction comes before the two possible offices and the expected share concession.",
    780: "The recommendation can be used more widely. 'Should' reflects the trader's degree of certainty.",
    781: "The parallel explanations make the different eligibility rules easy to compare and keep both letter names whole.",
    782: "Keep the trader's pause, the sale that prompts the favor and the deliberately unspecified extra.",
    783: "Keep the surprised question, the thanks and a familiar invitation to keep supplying the goods.",
}


def main():
    assert not ROOT.exists()
    release = base.load(parent.RELEASE)
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(CLEAN) == release["clean_input_sha256"]
    ctx = workflow.RegisteredRuntime(parent.RELEASE, release["own_registered_startup"], captain=3)
    clean = base.NdsImage.open(CLEAN)
    ja, arm, common = clean.read_file(ARM), ctx.arm, ctx.common
    source = workflow.common_message_entries(clean.read_file(COMMON), ja)
    directory = native.digest(arm[workflow.DIRECTORY_OFFSET:workflow.TABLE_OFFSET])
    current = workflow.owned_entries(common, arm, directory)
    context = trade.original_context(ja, arm)
    reward = rewards.original_branches(ja, arm)
    prior = {r["message_ID"]: r for path in REVIEWS for r in base.load(path)["records"]
             if r["message_ID"] in REASONS}
    assert prior.keys() == REASONS.keys()
    rows = {}
    for n, old in sorted(prior.items()):
        jp, installed = source[n], current[n]
        assert all(old["review"].values()) and jp.text.hex() == old["source_hex"]
        assert workflow.logical(installed.text) == old["english"]
        english, phrases = EDITS.get(n, (old["english"], ()))
        assert jp.text.count(b"%") == installed.text.count(b"%") == english.count("%s") == (n == 761)
        rows[n] = dict(id=old["id"], message_ID=n, file_path=COMMON, speaker=old["speaker"],
            context=old["context"], clean_Japanese=jp.text.decode("cp932"), source_meaning=old["source_meaning"],
            english=english, previous_English=old["english"], localization_note=REASONS[n],
            decision="revision" if n in EDITS else "retention", source_reference=workflow.reference(jp),
            current_reference=workflow.reference(installed), source_hex=jp.text.hex(), current_hex=installed.text.hex(),
            original_chains=old.get("original_chains", []), original_substitution_count=int(n == 761),
            protected_phrases=phrases, review=dict.fromkeys(workflow.parent.GATES, True) | {"formatting": False})

    wrap = FunctionType(rewards.compile_layouts.__code__, rewards.compile_layouts.__globals__ |
                        {"PHRASES": {n: p for n, (_, p) in EDITS.items()}})
    prepared = wrap({n: rows[n] for n in EDITS})
    repack = FunctionType(relocate.__code__, relocate.__globals__ | {"DIRECTORY": directory})
    new_common, new_arm, entries, allocation = repack(common, arm, rows, prepared)
    assert allocation["changed_visible_templates"] == list(EDITS)
    start, end = workflow.DIRECTORY_OFFSET, workflow.TABLE_OFFSET + len(current)*4
    assert new_arm[:start] == arm[:start] and new_arm[end:] == arm[end:]
    for stored in base.load(parent.env["PENDING"])["records"]:
        entry = entries[stored["message_ID"]]
        assert workflow.reference(entry) == stored["current_reference"] and entry.text.hex() == stored["current_hex"]

    new_ctx = rewards.with_components(ctx, new_arm, new_common)
    cpu, get, provider = new_ctx.machine(new_arm, new_common, new_ctx.raw, new_ctx.plan)
    painter, _, font = workflow.font_tools(ctx.image)
    kanji = ctx.image.read_file("/GRP/KANJI.FNT")
    pages = []
    for n, row in rows.items():
        template = entries[n].text
        ptr = get(0x5528C, n)
        assert bytes(cpu.mem_read(ptr, len(template)+1)) == template + b"\0"
        row.update(staged_reference=workflow.reference(entries[n]), staged_hex=template.hex(), native_displays=[])
        alternatives = [(item,) for item in context["facility_names"]] if n == 761 else [()]
        for values in alternatives:
            display, lines = rewards.native_layout(cpu, template, n, values, parent=0x02054014)
            expected = row["english"] % values if values else row["english"]
            assert " ".join(lines) == expected and 0 < len(lines) <= 4, (n, lines)
            assert all(0 < len(line) <= 36 for line in lines), (n, lines)
            assert all(any(phrase in line for line in lines) for phrase in (*row["protected_phrases"], *values))
            plane, glyphs = rewards.render_portrait(painter, new_arm, kanji, display)
            assert [g["code"] for g in glyphs] == workflow.glyph_codes(display)
            assert (glyphs[0]["code"], glyphs[-1]["code"]) == (ord(expected[0]), ord(expected[-1]))
            row["native_displays"].append(dict(arguments=values, display_hex=display.hex(), visible_lines=lines,
                glyph_count=len(glyphs), ink_sha256=native.digest(plane)))
            if n in EDITS:
                pages.append((n, plane))
    assert provider.reads and bytes(cpu.mem_read(ctx.actor_root, 0x1A04)) == ctx.actor_bytes
    image = base.NdsImage.open(parent.ROM)
    image.replace_file(ARM, new_arm)
    image.replace_file(COMMON, new_common)
    target = bytes(image.rom.save())
    image.replace_file(ARM, arm)
    image.replace_file(COMMON, common)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(target)
    base.save(PROOF, dict(candidate_sha256=base.digest(ROM), parent_sha256=base.digest(parent.ROM),
        previous_sha256=release["candidate_sha256"], clean_input_sha256=release["clean_input_sha256"],
        target_ARM9_sha256=native.digest(new_arm), target_COMMON_sha256=native.digest(new_common),
        entire_parent_inverse=True, allocation=allocation, market_bindings=context, reward_bindings=reward,
        source_proofs={p.as_posix(): base.digest(p) for p in REVIEWS},
        font=font, sheets=rewards.portrait_sheets(ROOT, pages), translation_policy="natural-dialogue-v2",
        encoder="dialogue-relocatable-v1", target_locale="en-US", review_gates=workflow.parent.GATES,
        records=list(rows.values())))
    print(f"Reviewed {len(rows)} Market records, including {len(pages)} revised pages.")


if __name__ == "__main__":
    main()
