"""Bind the 245 pending legacy records to their known independent display owners."""

from collections import Counter, defaultdict
from pathlib import Path
from struct import unpack_from
from unicodedata import normalize

from dk4tool.patch.gallery_caption_bounds import validate
from dk4tool.script.common_message_table import common_message_entries
from scripts import checkpoint_online_and_scene_consumers_v1 as prior
from scripts import register_about_extras_20261114 as current
from scripts.inventory_common_scene_caption_duplicates import captions as original_gallery


base=current.base
WORK=prior.OUTPUT.parent
OUT=WORK/"online_gallery_owner_reconciliation_20261114_v2.json"
ONLINE=Path("releases/all_routes_editorial_20261111_visible_online_captions_candidate/verification/registered_caption_review.json")
GALLERY=Path("releases/all_routes_editorial_20261111_visible_gallery_captions_candidate/verification/registered_caption_review.json")
ARM,COMMON=prior.ARM,prior.COMMON
GUIDE_COPY_GROUPS=(
    (3289,3290),(3291,3292,3293,3294),(3295,3296),(3297,3298),(3299,3300),(3301,3302),
    (3303,3304),(3305,3306),(3307,3308),(3309,3310),(3311,3312),(3313,3314),(3315,3316),
)


def main():
    assert not OUT.exists()
    release=base.load(current.RELEASE)
    assert base.digest(current.ROM)==release["candidate_sha256"]
    clean_path=current.parent.parent.stage.CLEAN
    assert base.digest(clean_path)==release["clean_input_sha256"]
    now,clean=map(base.NdsImage.open,(current.ROM,clean_path))
    arm,ja=[i.read_file(ARM) for i in (now,clean)]
    digest=current.source.current.assets.edit.digest
    assert digest(arm)==release["target_ARM9_sha256"]
    active=prior.review.owned_entries(now.read_file(COMMON),arm,digest(arm[prior.review.DIRECTORY_OFFSET:prior.review.TABLE_OFFSET]))
    original=common_message_entries(clean.read_file(COMMON),ja)
    online=base.load(ONLINE)["records"]
    gallery=base.load(GALLERY)["records"]
    exact_duplicate=defaultdict(list)
    compiled=validate(arm)
    clean_gallery=original_gallery(ja)
    for source,caption,proof in zip(clean_gallery,compiled,gallery,strict=True):
        assert caption["route"]==source["route_index"]==proof["route"]
        assert caption["position"]==source["index"]==proof["position"]
        item=proof["registered_reference"]
        assert caption["pointer"]==item["pointer"] and caption["field"]==item["field"]
        assert caption["English"]==proof["english"] and all(proof["review"].values())
        assert bytes.fromhex(item["stored_hex"])==caption["English"].encode("ascii")+b"\0"
        assert source["japanese"]==proof["source_Japanese"]
        exact_duplicate[source["source_hex"]].append(dict(source_Japanese=source["japanese"],
            exact_clean_ARM9_offset=source["offset"],current_field_offset=caption["field"],
            current_text=caption["English"],current_pointer=caption["pointer"],bounds=caption["bounds"],
            route=caption["route"],position=caption["position"]))
    assert len(compiled)==164

    topics={}
    for p,common_ids in zip(online,GUIDE_COPY_GROUPS,strict=True):
        own=p["registered_reference"]
        payload=bytes.fromhex(own["stored_hex"])
        off=own["offset"]
        assert arm[off:off+len(payload)]==payload
        assert ja[off:].split(b"\0",1)[0].decode("cp932")==p["source_Japanese"]
        assert all(p["review"].values())
        for n in common_ids:
            assert n not in topics
            topics[n]=dict(owner="Online Version ARM9 caption",category=p["original_category"],page=p["original_page"],
                ARM9_offset=off,Japanese=p["source_Japanese"],displayed_English=p["english"],same_source_topic=True)
    tie_in=base.load(current.REVIEW)
    assert len(tie_in["records"])==6 and not tie_in["actual_COMMON_requests"]
    for row in tie_in["records"]:
        ref=row["registered_reference"]
        at=ref["ARM9_offset"]
        assert unpack_from("<I",arm,ref["pointer_field"])[0]==0x02000000+at
        payload=bytes.fromhex(ref["exact_stored_hex"])
        assert arm[at:at+len(payload)]==payload
    tie_roles={3317:[1],3318:[1],3319:[2,3,4]}
    prior_rows=base.load(prior.OUTPUT)["exact_native_records"]
    rows=[]
    variants=defaultdict(list)
    for group in exact_duplicate.values():
        for item in group:
            variants[normalize("NFKC",item["source_Japanese"])].append(item)
    for row in prior_rows:
        ident=row["message_ID"]
        a,b=original[ident],active[ident]
        assert a.text==b.text==bytes.fromhex(row["clean_hex"])
        related=exact_duplicate.get(a.text.hex(),[])
        assert related==[] or len(related)==len(row["independent_gallery_captions"])
        loose=[]
        normalized=normalize("NFKC",row["clean_Japanese"])
        if not related and normalized.endswith("(大)"):
            loose=variants.get(normalized.removesuffix("(大)"),[])
        if ident in tie_roles:
            owner=dict(owner="About Extras ARM9 page sequence",visible_related_pages=tie_roles[ident],same_source_topic=True)
        else:
            owner=topics.get(ident)
        rows.append(dict(message_ID=ident,source_family=row["family"],source_Japanese=row["clean_Japanese"],
            stored_hex=b.text.hex(),source_reference=prior.review.reference(a),current_reference=prior.review.reference(b),
            independent_exact_Gallery_captions=related,related_large_variant_Gallery_candidates=loose,
            independently_displayed_Online_or_Extras_owner=owner,legacy_COMMON_caller_search_pending=True))
    assert len(rows)==245 and sum(bool(row["independent_exact_Gallery_captions"]) for row in rows)==123
    assert sum(bool(row["independently_displayed_Online_or_Extras_owner"]) for row in rows)==31
    base.save(OUT,dict(candidate_sha256=release["candidate_sha256"],maps=rows,
        verified_current_Gallery_titles=164,verified_current_Online_guide_captions=13,verified_current_About_Extras_pages=6,
        exact_COMMON_bytes_rebound=len(rows),exact_independent_Gallery_rows=123,large_variant_candidates=sum(bool(row["related_large_variant_Gallery_candidates"]) for row in rows),
        other_common_use_active=True,earlier_actual_Online_and_Gallery_capture=str(WORK/"online_and_gallery_observed_consumers_v1.json"),
        evidence={str(p):base.digest(p) for p in (ONLINE,GALLERY,prior.OUTPUT,current.REVIEW,current.RELEASE)},
        new_dialogue_credit=0,full_goal_complete=False))
    print("Reconciled 245 exact COMMON entries to current Gallery, Online guide and About Extras ownership.")


if __name__=="__main__":
    main()

