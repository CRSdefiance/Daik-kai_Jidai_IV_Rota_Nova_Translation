"""Clear reproducible early-setup scratch and publish the current editorial checkpoint."""

from pathlib import Path

from scripts import review_rafael_deck_tutorial_followup_20261122 as lesson
from scripts import verify_early_setup_current_20261122 as setup


base = setup.base
ROOT = setup.ROOT
RECEIPT = ROOT / "checkpoint_cleanup.json"
DOC = Path("docs/editorial_early_setup_current_20261122.md")


def cleanup(review):
    assert not RECEIPT.exists()
    retained = {Path(p):sha for p,sha in review["reviewed_sheets"].items()}
    candidate = review["candidate_sha256"]
    frames = (review["character_editor"]["matches_prior_framebuffers"] +
              [row["capture"] for row in review["sound_setup"]["complete_current_title_masks"]] +
              [review["sound_setup"]["returned_to_options"]])
    retained.update({Path(row["path"]):row["PNG_sha256"] for row in frames})
    assert all(base.digest(p)==sha for p,sha in retained.items())
    keep = {p.resolve() for p in retained}
    discard = {}
    capture_root = ROOT.resolve()
    for case, expected in (("setup",6601),("options",8250)):
        capture = ROOT/case/"capture"
        report = base.load(capture/"capture_report.json")
        assert report["ROM_sha256"]==candidate and report["frames"]==expected
        assert report["cold_boot"] and not report.get("battery_save_preloaded")
        for row in report["frames_captured"]:
            path = Path(row["path"])
            assert path.resolve().parent==capture.resolve() and path.suffix==".png"
            # Keep distinct option/navigation screens as well as the proof holds.
            if row["frame"] in (1,60,180,expected) and path.resolve() not in keep:
                discard[path] = row["PNG_sha256"]
        save = capture/"saves"/setup.current.ROM.with_suffix(".dsv").name
        assert save.resolve().parent==(capture/"saves").resolve() and save.stat().st_size==262266
        discard[save] = base.digest(save)

    removed = []
    for path,sha in discard.items():
        assert path.resolve().is_relative_to(capture_root) and path.resolve() not in keep
        assert not path.is_symlink() and not path.is_junction() and base.digest(path)==sha
        removed.append(dict(path=str(path),sha256=sha,bytes=path.stat().st_size))
    for path in discard:
        path.unlink()
    assert all(base.digest(p)==sha for p,sha in retained.items())
    result = dict(candidate_sha256=candidate,removed=removed,bytes_reclaimed=sum(r["bytes"] for r in removed),
        retained_proof_witnesses=len(retained),only_generated_qa_scratch_removed=True)
    base.save(RECEIPT,result)
    return result


def publish(review, draft, glyphs, cleaned):
    assert not DOC.exists()
    candidate = review["candidate_sha256"]
    assert candidate == draft["previous_sha256"]==glyphs["candidate_sha256"]
    assert base.digest(setup.current.ROM)==candidate
    assert base.digest(base.REGISTRY)==draft["previous_registry_sha256"]
    report, notes, glyph_file, cleanup_file = (p.as_posix() for p in (
        setup.OUTPUT,lesson.OUTPUT,lesson.GLYPHS,RECEIPT))
    DOC.write_text(f"""# Current character setup, nameplates and Julio's Deck lesson

The registered testing ROM matched all 13 reviewed Rafael setup screens, including five edit headings, the birthday change, **Is everything OK?**, and the return after cancellation. The character editor requested COMMON 120. In Sound Setup, the existing **In High Spirits** title passed seven complete glyph checks. Its five requests used COMMON 3251. The 12 legacy setup, biography and Options entries have exact source and current references and remain open for other callers. None appeared in either tested flow. Audio and hardware were outside this check. [Coverage and observations](../{report})

Both default name getters match the earlier decisions for all 207 actors. The offline pass verified all 621 bound name fields and 414 results. Player-entered names and conditional or joined names have separate coverage. [Current name bindings and earlier decisions](../{report})

The Deck lesson now has six source-checked proposals and six justified retentions covering the full exchange with Julio and the following instruction panel. The current build already shows a regular ASCII F in the line the user reported. It still breaks after “where.” The proposed wording keeps “set a course on its own” together in the preliminary four-row plan, including a 16-character given name. Native rendering, direct visual checks and focused playback are pending before registration. [Full Deck lesson review](../{notes})

A current scan found no full-width Latin in 20,986 matched story bodies. COMMON 318 still contains the full-width I in “If you quit.” It remains a stored glyph lead with a source-checked proposal, pending a confirmed exhibition-data display owner. The scan covers the matched story form and mapped COMMON entries. [Exact glyph evidence](../{glyph_file})

The current ROM remains SHA-256 {candidate}. The checkpoint cleared {len(cleaned['removed'])} temporary captures and emulator saves, reclaiming {cleaned['bytes_reclaimed']:,} bytes. [Cleanup receipt](../{cleanup_file})
""",encoding="utf-8")
    summary = f"""# Current editorial checkpoint - 2026-11-22

Verified current New Game and Sound Setup display and all 207 default speaker-name decisions. Reviewed Julio's full Deck lesson, with six revisions drafted and six retentions. [Checkpoint]({DOC.name})

Continue with stored relocation and fresh native and visual checks for the six SC0 B43 proposals. Check Julio's full name substitution at representative and maximum supported sizes, the separate X-menu instruction panel and the return to Deck View. The 276 legacy display leads, broader town and random scenes, conditional and custom names, and other player-facing prose stay in scope. Graphics artwork and the later older-record technical re-audit remain separate. [Deck lesson exact source and current references](../{notes}) | [Current setup and name ledger](../{report})

""".encode("utf-8")
    for name in ("editorial_handoff_current.md","translation_progress.md"):
        path = DOC.with_name(name)
        base.replace_checked(path,summary+path.read_bytes())


def main():
    review,draft,glyphs = map(base.load,(setup.OUTPUT,lesson.OUTPUT,lesson.GLYPHS))
    assert not DOC.exists()
    result = cleanup(review)
    publish(review,draft,glyphs,result)
    print(f"Cleared {len(result['removed'])} generated files and reclaimed {result['bytes_reclaimed']:,} bytes.",flush=True)


if __name__ == "__main__":
    main()

