"""Review the five installed opening captions against the clean artwork."""

from hashlib import sha256
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.graphics.fls import FlsArchive
from scripts import checkpoint_opening_display_scope_20261119 as scope
from scripts import observe_remaining_opening_shared_text_20261119 as replay
from scripts.verify_movie_playback_v302 import locations

base = replay.base
OUTPUT = replay.ROOT / "opening_captions_native.png"
PROOF = Path("translations/editorial_checkpoints/SharedText_20261110_v1/opening_movie_caption_retentions_20261119_v1.json")
PLAYBACK = Path("work/analysis/movie_viewport_v303/proof.json")
MANUSCRIPTS = {
    "rafael": Path("translations/opening_movie_m20_subtitle_v1.json"),
    "lil": Path("translations/m22_native_viewport_subtitles_v1.json"),
    "hodram": Path("translations/m24_native_viewport_subtitles_v1.json"),
}
NOTES = {
    ("rafael", 27): "Keep the familiar Clau and the two short questions. The second asks what Clau wanted to show and follows the first without changing the relationship.",
    ("lil", 1): "Keep the quick warning and its reason together. The two short calls suit the sudden objection.",
    ("lil", 2): "Keep Lil's repeated reassurance and confident offer to take charge. They answer the preceding warning in the same playful rhythm as the Japanese.",
    ("hodram", 3): "Keep the urgent announcement and the order to report to the captain. This is the initial sighting before the type of ship is inferred.",
    ("hodram", 4): "Keep the inference in 'Looks like' and the clipped, respectful call for orders. The dialogue advances from sighting the ship to identifying it and asking what to do.",
}
GATES = ["source", "context", "localization", "naturalness", "formatting"]


def main():
    assert not OUTPUT.exists() and not PROOF.exists()
    coverage, old = map(base.load, (scope.OUTPUT, PLAYBACK))
    release = base.load(replay.current.RELEASE)
    assert coverage["candidate_sha256"] == base.digest(replay.current.ROM) == release["candidate_sha256"]
    clean_path = replay.current.stage.CLEAN
    assert base.digest(clean_path) == release["clean_input_sha256"]
    clean, rom = map(base.NdsImage.open, (clean_path, replay.current.ROM))
    prior_cards = {(row["file_path"], row["texture_index"]): row for row in old["cards"]}
    rows = []
    sheet = Image.new("RGB", (1088, 5 * 90), "#2b3944")
    draw = ImageDraw.Draw(sheet)
    for name, path in MANUSCRIPTS.items():
        batch = base.load(path)
        asset = batch["file_path"]
        source_blob, current_blob = (im.read_file(asset) for im in (clean, rom))
        assert sha256(current_blob).hexdigest() == coverage["original_visible_asset_sha256"][asset]
        source, current = map(FlsArchive, (source_blob, current_blob))
        shots = []
        if name in replay.RUNS:
            report = base.load(replay.ROOT / name / "capture/capture_report.json")
            shots = [(row, scope.pixels(row, upper=True)) for row in report["frames_captured"]
                if row["frame"] in replay.RUNS[name]]
        for row in batch["records"]:
            i = row["asset_index"]
            previous = prior_cards[asset, i]
            orig, tex = source.texture(i), current.texture(i)
            source_sha = sha256(bytes(orig.indices)).hexdigest()
            tex_sha = sha256(bytes(tex.indices)).hexdigest()
            assert row.get("source_texture_sha256", source_sha) == source_sha
            assert previous["source_texture_sha256"] == tex_sha and previous["English"] == row["lines"]
            assert source.records[i][:4] == current.records[i][:4]
            visible = row["layout_width"]
            assert current.records[i][0] >> 16 == visible
            assert all(p % tex.width < visible for p, v in enumerate(tex.indices) if v)
            assert sum(bool(v) for v in tex.indices) == previous["source_opaque_pixels"]
            assert previous["matches"] and all(
                r["every_opaque_first_internal_final_letter_and_outline_pixel_exact"] for r in previous["matches"])
            holds = [
                dict(frame=shot["frame"], origin=hits[0], capture=shot["path"], capture_sha256=shot["PNG_sha256"])
                for shot, image in shots if len(hits := locations(tex, image.load())) == 1]
            y = len(rows) * 90
            draw.text((8, y + 2), f"{name.title()}   {asset} texture {i}   Clean Japanese", fill="white")
            draw.text((548, y + 2), "Installed English", fill="white")
            for x, image in ((8, orig), (548, tex)):
                art = image.render().crop((0, 0, visible, image.height))
                art = art.resize((art.width * 2, art.height * 2), Image.Resampling.NEAREST)
                sheet.paste(art, (x, y + 20), art)
            rows.append(dict(id=row["id"], file_path=asset, texture_index=i,
                source_reference=dict(file_sha256=sha256(source_blob).hexdigest(), texture_index_sha256=source_sha),
                current_reference=dict(file_sha256=sha256(current_blob).hexdigest(), texture_index_sha256=tex_sha),
                source_Japanese=row.get("Japanese"), source_meaning=row.get("source_meaning"),
                english=row["lines"], decision="retention", localization_note=NOTES[name, i],
                native_width=visible, opaque_glyph_and_outline_pixels=previous["source_opaque_pixels"],
                previous_render_evidence=dict(path=str(PLAYBACK), card=i, matched_frames=len(previous["matches"])),
                current_complete_masks=holds, review=dict.fromkeys(GATES, False)))
    assert len(rows) == 5
    sheet.save(OUTPUT)
    base.save(PROOF, dict(candidate_sha256=release["candidate_sha256"], records=rows,
        visual_review_pending=True, new_editorial_credit=0,
        evidence={str(p): base.digest(p) for p in (scope.OUTPUT, PLAYBACK, OUTPUT, *MANUSCRIPTS.values())}))
    print([(r["texture_index"], len(r["current_complete_masks"])) for r in rows])


if __name__ == "__main__":
    main()

