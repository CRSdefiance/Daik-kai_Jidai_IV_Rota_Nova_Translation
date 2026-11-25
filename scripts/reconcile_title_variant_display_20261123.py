"""Bind the remaining title logo and transition labels to verified DS display families."""

from pathlib import Path
from types import FunctionType, SimpleNamespace

from PIL import Image, ImageDraw

from dk4tool.graphics.fls import FlsArchive
from scripts import observe_title_variant_display_20261123 as live
from scripts import reconcile_opening_label_dispositions_20261123 as opening
from scripts.reconcile_cartridge_header_check_20261123 import OUT as PREVIOUS
from scripts.reconcile_legacy_fleet_and_quit_paths_20261123 import (
    WORKLIST, base, common_message_entries, current, native, owned_entries, picture, stored_record,
    DIRECTORY_OFFSET, TABLE_OFFSET,
)


OUT = PREVIOUS.with_name("title_variant_display_20261123.json")
SHEET = OUT.with_suffix(".png")
TITLE, LOGO = opening.TITLE_PATH, "/FLS/logo.fls"
GROUPS = {
    "title_logo": (range(3598, 3601), (707, 807, 825, 987, 1005)),
    "title_transition": (range(3594, 3598), (579, 987, 1005, 1039, 5835, 5947, 5991, 6099, 6167,
                                             6179, 6191, 6231, 6435, 7211)),
    "separate_publisher_credits": ((), (6667, 6779, 6939, 7107, 7199)),
}
SAMPLES = {
    707: "Main logo appears", 825: "Complete title and subtitle", 1005: "Opening fade",
    1039: "Rafael sequence begins", 5835: "Dissolve from the night sea", 5991: "Sequence before dawn",
    6167: "Dawn transition", 6191: "White between scenes", 6231: "Complete closing tableau",
    6779: "Koei card", 6939: "Eiji Fukuzawa card", 7107: "Rekoeition card",
}


def draw_sheet(shots):
    sheet = Image.new("RGB", (768, 4 * 214), "#172630")
    draw = ImageDraw.Draw(sheet)
    for i, (frame, label) in enumerate(SAMPLES.items()):
        x, y = i % 3 * 256, i // 3 * 214
        draw.text((x + 5, y + 3), f"{frame}  {label}", fill="white")
        sheet.paste(picture(shots[frame]).crop((0, 0, 256, 192)), (x, y + 20))
    sheet.save(SHEET)


def composition(clean, active, shots, preceding):
    proof = base.load(opening.COMPOSITION_PROOF)
    results_path = Path(proof["results"])
    assert base.digest(results_path) == proof["results_sha256"]
    old = base.load(results_path)
    assert proof["all611_complete_upper_RGB_compositions_exact_without_exclusions"] and not old["failures"]
    by_frame = {row["display_frame"]: row for row in old["cases"]}
    assert len(by_frame) == 611
    groups = {}
    for label, (keys, frames) in GROUPS.items():
        path = LOGO if label == "separate_publisher_credits" else TITLE
        source, installed = (img.read_file(path) for img in (clean, active))
        original, current_archive = map(FlsArchive, (source, installed))
        assert original.count == current_archive.count == (4 if path == LOGO else 170)
        samples = []
        for frame in frames:
            row = by_frame[frame]
            assert row["source_movie"] == path and row["whole49152_RGB_pixels_exact_without_exclusions"]
            layers = [layer for layer in row["native_draws"] if layer["alpha"] and layer["drawn_pixels"]]
            ids = {layer["texture"] for layer in layers}
            assert all(index < current_archive.count for index in ids)
            for bind in row["source_VRAM_bindings"]:
                assert bind["native_source_index_cells_exact"] and bind["complete_original_palette_bytes_exact"]
            samples.append(dict(frame=frame, composed_texture_layers=[dict(texture=layer["texture"],
                alpha=layer["alpha"], drawn_pixels=layer["drawn_pixels"]) for layer in layers],
                capture=shots[frame]))
        used = {layer["texture"] for sample in samples for layer in sample["composed_texture_layers"]}
        if label == "title_logo":
            assert {4, 5} <= used
        elif label == "title_transition":
            assert {0, 6, 162, 163, 164, 165, 166, 168, 169} <= used
            assert all(original.texture(i) == current_archive.texture(i) for i in (0, 6, *range(162, 170)))
        else:
            assert used == set(range(4))
        if path == TITLE:
            assert preceding["title_asset_sha256"] == dict(clean=native.digest(source), installed=native.digest(installed))
        groups[label] = dict(archive=path, clean_sha256=native.digest(source), installed_sha256=native.digest(installed),
            associated_storage_keys=list(keys), historical_native_composition_samples_with_exact_current_RGB=samples)
    assert [r["texture"] for r in groups["title_transition"]["historical_native_composition_samples_with_exact_current_RGB"]
            if r["frame"] == 6191 for r in r["composed_texture_layers"]] == [6]
    white = picture(shots[6191]).crop((0, 0, 256, 192))
    assert white.getextrema() == ((255, 255),) * 3
    return groups


def main():
    release, review, prior, inventory, preceding = map(base.load,
        (current.RELEASE, current.REVIEW, PREVIOUS, WORKLIST, opening.OUT))
    assert base.digest(current.ROM) == release["candidate_sha256"] == review["candidate_sha256"] == prior["candidate_sha256"]
    assert base.digest(native.CLEAN) == release["clean_input_sha256"] == preceding["clean_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    remaining = set(prior["remaining_without_scoped_disposition"])
    assert len(remaining) == 21 and opening.VARIANTS_OPEN <= remaining
    observer = SimpleNamespace(ROOT=live.ROOT, schedule=live.schedule, trace=live.TRACE)
    check_run = FunctionType(opening.checked_run.__code__, vars(opening) | {"live": observer})
    observed, report = check_run("title", release, remaining)
    assert not observed["COMMON_requests"] and observed["completed_frames"] == 7400
    shots = opening.frames(report)
    _, pixels = opening.title_pixels(report)
    assert set(live.FRAMES) <= set(map(int, pixels["matched_frames"]))

    clean, active = map(base.NdsImage.open, (native.CLEAN, current.ROM))
    ja, en = (img.read_file(current.ARM) for img in (clean, active))
    common = active.read_file(current.COMMON)
    assert native.digest(en) == release["target_ARM9_sha256"] and native.digest(common) == release["target_COMMON_sha256"]
    source = common_message_entries(clean.read_file(current.COMMON), ja)
    installed = owned_entries(common, en, native.digest(en[DIRECTORY_OFFSET:TABLE_OFFSET]))
    stored = {r["message_ID"]: r for r in inventory["records"]}
    binding = {r["message_ID"]: r for r in review["shared_consumer_binding"]["records"]}
    groups = composition(clean, active, shots, preceding)
    rows = []
    for label in ("title_transition", "title_logo"):
        for key in groups[label]["associated_storage_keys"]:
            record = stored_record(key, source, installed, stored, binding)
            record.update(verified_title_display_family=label, exact_label_to_texture_pointer_proven=False,
                disposition="Separate movie composition during the observed DS title cycle. The archive retains this variant's source label.")
            rows.append(record)
    bound = {row["message_ID"] for row in rows}
    assert len(bound) == 7 and bound == (opening.VARIANTS_OPEN - {3577, 3578})
    draw_sheet(shots)
    base.save(OUT, dict(candidate_sha256=release["candidate_sha256"], source_storage_inventory=len(stored),
        reviewed_entries=rows, remaining_without_scoped_disposition=sorted(remaining - bound),
        fresh_unattended_title_replay=observed, exact_complete_RGB_frames=pixels, title_display_groups=groups,
        still_missing_exact_story_or_title_image_labels=[3401, 3490, 3577, 3578],
        direct_COMMON_display_elsewhere_unverified=True, actual_hardware=False, new_ROM=False,
        sheet=dict(path=str(SHEET), sha256=base.digest(SHEET)),
        evidence={str(path): base.digest(path) for path in (PREVIOUS, WORKLIST, opening.OUT, opening.COMPOSITION_PROOF,
            opening.live.COMPOSITION, current.RELEASE, current.REVIEW, Path(__file__), Path(live.__file__))}))
    print(f"Verified seven title display scopes and {len(live.FRAMES)} requested framebuffer holds; {len(remaining - bound)} remain.")


if __name__ == "__main__":
    main()
