"""Bind recent visible wrap issues and render their proposed fixes offline."""

from pathlib import Path
from types import FunctionType

from scripts import register_hodram_late_story_wraps_20261123 as active
from scripts import review_current_story_wraps_20261122 as native_review
from scripts import review_rafael_east_asia_followup_20261121 as pagination


base, native = active.base, active.native
CHECKPOINT = Path("translations/editorial_checkpoints/observed_wrap_followups_20261123")
MANUSCRIPT = CHECKPOINT / "working_review.md"
ROOT = Path(".codex-release-work/observed_wrap_followups_20261123/preflight_v2")
CASES = {
    (1, 167, 122): ("hodram_late_midroute_wraps", ["Keep using the fleet you have", "while you sign deals with new towns", "open trade routes.", "There's no need to buy more yet.", "With a one percent share,", "one to five units", "of trade goods."], 2),
    (1, 216, 78): ("hodram_late_story_wraps", ["Zhuge Liang. Brilliant strategist.", "His memorial before the campaign", "always moves me to tears.", "I'd say he's my second favorite."], 1),
    (0, 228, 31): ("rafael_remaining_wraps", ["Seek Excalibur, champion!", "The sacred sword", "on Avalon", "where the king sleeps."], 1),
    (0, 234, 35): ("rafael_remaining_wraps", ["the final sea battle", "across seven boats", "the enemy commander's ship", "Or so they say."], 1),
}


def preflight():
    release = base.load(active.RELEASE)
    candidate = base.digest(active.ROM)
    assert candidate == release["candidate_sha256"] and base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(native.CLEAN) == release["clean_input_sha256"]
    ctx = native.RegisteredRuntime(active.RELEASE, release["own_registered_startup"], captain=3)
    renderer = native_review.display.clipped_renderer(ctx)
    font = ctx.image.read_file("/GRP/KANJI.FNT")
    images = [base.NdsImage.open(p) for p in (native.CLEAN, active.ROM)]
    banks = {i: [native.IlnkContainer.parse(img.read_file(f"/data/SC{i}.DK4")).blocks for img in images]
             for i in (0, 1)}
    rows = [line.split("|") for line in MANUSCRIPT.read_text(encoding="utf8").splitlines()
            if line.startswith("| `/data/SC")]
    assert len(rows) == len(CASES)
    pictures, records = [], []
    for (key, (slug, phrases, pages)), columns in zip(CASES.items(), rows, strict=True):
        route, block, ordinal = key
        ident = f"DK4_MES_B{block}_R{ordinal:04d}"
        archive = f"/data/SC{route}.DK4"
        assert f"`{archive}` B{block} R{ordinal:04d}" in columns[1]
        english = columns[3].strip()
        assert english.isascii() and all(phrase in english for phrase in phrases)
        folder = Path(f"releases/all_routes_editorial_20261123_{slug}_candidate")
        ledger = folder / "verification/registered_review.json"
        digest = base.digest(ledger)
        assert digest == base.load(folder / "checksums.json")["verification/registered_review.json"]
        group = [r for r in base.load(ledger)["records"] if r["file_path"] == archive and r["block"] == block]
        owner, = [r for r in group if r["id"] == ident]
        for earlier in group:
            for bank, ref in zip(banks[route], (earlier["source_reference"], earlier["registered_reference"]), strict=True):
                payload = bank[block]
                at, raw = ref["command_offset"], bytes.fromhex(ref["exact_command_hex"])
                assert native.digest(payload) == ref["block_sha256"] and payload[at:at+len(raw)] == raw
        before, clean = (bytes.fromhex(owner[k]["exact_body_hex"]) for k in ("registered_reference", "source_reference"))
        row = dict(id=ident, english=english, protected_phrases=phrases)
        planner = pagination.company_scope["plan_progressive"]
        body, plan = planner(row, owner["source_selector"], before, clean)
        assert plan["expected_native_pages"] == pages, (ident, plan["lines"])
        expected = [native_review.display.display.expected(line, {}) for line in plan["lines"]]
        native_pages = native_review.display.display.raster(ctx, font, renderer, body, expected, pages)
        for i, page in enumerate(native_pages, 1):
            assert page["native_independent_plane_equal"]
            pictures.append((f"SC{route} {ident} / page {i}", bytes.fromhex(page["native_plane_hex"])))
        records.append(dict(file_path=archive, id=ident, prior_ledger=str(ledger), prior_ledger_sha256=digest,
            exchange_source_and_current_commands_verified=len(group), source_reference=owner["source_reference"],
            current_reference=owner["registered_reference"], english=english, plan=plan, native_pages=native_pages))
        print(ident, plan["lines"], flush=True)
    ROOT.mkdir(parents=True, exist_ok=True)
    contact = native_review.display.display.inherited.early.contact_sheets
    sheets = FunctionType(contact.__code__, contact.__globals__ | {"ROOT":ROOT})(pictures)
    base.save(ROOT / "native_preflight.json", dict(candidate_sha256=candidate, manuscript_sha256=base.digest(MANUSCRIPT),
        records=records, sheets=sheets, offline_native_only=True))


if __name__ == "__main__":
    preflight()
