"""Check ordinary store captions and shop transitions on the staged release."""

from PIL import ImageChops

from scripts import stage_square_shop_names_20261122 as stage
from scripts import verify_story_literal_names_20261122 as pictures


base, native, prior = stage.base,stage.native,stage.square.prior
LIVE = stage.ROOT/"ordinary_captions.json"
SHEET = stage.ROOT/"ordinary_square_captions.png"
ACTUAL = {
    "syracuse": (7150,("Delicacy Shop","Spice Shop","Jewelry Shop")),
    "lisbon": (4750,("Seasonings","Treats Shop","Textile Shop","Craft Shop")),
}


def verify():
    assert not LIVE.exists()
    stored, existing = map(base.load,(stage.PROOF,stage.parent.live.LIVE))
    candidate = base.digest(stage.ROM)
    assert candidate==stored["candidate_sha256"]
    assert existing["candidate_sha256"]==stored["predecessor_sha256"]==base.digest(stage.parent.ROM)
    revised = base.NdsImage.open(stage.ROM)
    font = prior.GameAsciiFont.from_arm9(revised.read_file(stage.ARM))
    evidence = {str(path):base.digest(path) for path in (stage.PROOF,stage.parent.live.LIVE)}
    thumbnails, observations = [], {}
    for city,(panel,names) in ACTUAL.items():
        path = stage.ROOT/city/"capture/capture_report.json"
        report = base.load(path)
        events,end,history,donor = stage.itinerary(city)
        assert report["ROM_sha256"]==candidate and report["frames"]==end
        assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
        assert not any(v for k,v in report.items() if k.startswith("synthetic_"))
        assert report["scripted_input_schedule"]==events
        loaded = report["battery_save_preloaded"]
        assert loaded["copied_byte_exact_before_cold_boot"] and loaded["source_sha256"]==donor["source_sha256"]==base.digest(donor["source"])
        evidence.update({str(p):base.digest(p) for p in (path,history)})
        frames = prior.shots(report)
        main = prior.captured(frames[panel]).convert("RGB")
        labels = [prior.live_caption(font,main,i,name) for i,name in enumerate(names)]
        controls = []
        if city=="syracuse":
            earlier = {row["frame"]["frame"]:row["frame"] for row in existing["observed"][city]}
            assert {6750,7150,7550,10350} <= earlier.keys()
            for frame in (6750,7150,7550,10350):
                old, new = [prior.captured(shot).convert("RGB") for shot in (earlier[frame],frames[frame])]
                diff = ImageChops.difference(old,new)
                changed = diff.getbbox()
                if frame==10350:
                    assert changed is None
                else:
                    assert changed is not None
                    diff.paste((0,0,0),prior.caption_box(1))
                    assert diff.getbbox() is None, (frame,changed)
                    prior.live_caption(font,old,1,"Spices Shop")
                    prior.live_caption(font,new,1,"Spice Shop")
                controls.append(dict(held_frame=frames[frame],predecessor_frame=earlier[frame],caption_only_difference=changed))
                for shot in (earlier[frame],frames[frame]):
                    assert base.digest(shot["path"])==shot["PNG_sha256"]
                    evidence[shot["path"]]=shot["PNG_sha256"]
            thumbnails.append(("Syracuse before / Spices Shop",prior.captured(earlier[panel]).convert("RGB")))
        selected = {n:frames[n] for n in stage.CAPTURES[city]}
        for frame,shot in selected.items():
            assert base.digest(shot["path"])==shot["PNG_sha256"]
            evidence[shot["path"]]=shot["PNG_sha256"]
            if frame!=4750 or city=="lisbon":
                thumbnails.append((f"{city.title()} / frame {frame}",prior.captured(shot).convert("RGB")))
        observations[city] = dict(revised_caption_frame=frames[panel],complete_caption_masks=labels,
            controls=controls,retained_frames=list(selected.values()),ordinary_saved_gameplay=True)
    assert len(observations["syracuse"]["controls"]) == 4
    path,sha = pictures.make_sheet(SHEET,thumbnails)
    base.save(LIVE,dict(candidate_sha256=candidate,predecessor_sha256=existing["candidate_sha256"],
        unchanged_syracuse_pixels_outside_spice_cell=True,observed=observations,actual_changed_categories=[3,7],
        offline_only_changed_categories=[10,12,14],sheets={path:sha},evidence=evidence,hardware=False))
    print("Ordinary Syracuse and Lisbon menus show the complete Spice Shop and Craft Shop captions.",flush=True)


if __name__=="__main__":
    verify()
