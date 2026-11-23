"""Bind the next thirteen complete Hodram exchanges to the current Rafael release."""

from collections import Counter
from inspect import getsource
from pathlib import Path

from scripts import cleanup_rafael_midroute_exchanges_20261122 as checkpoint
from scripts import pair_hodram_early_and_midroute_wraps_20261122 as prior
from scripts import register_rafael_midroute_exchanges_20261122 as release
from scripts.source_locked_derivation_v5118 import checked_text

base, native, ARCHIVE = prior.base, prior.native, prior.ARCHIVE
INTERVALS = {
    "B91_B110": (97, 100, 101, 102, 110),
    "B111_B130": (123, 124, 129),
    "B131_B150": (132, 135, 136, 137, 140),
}
OUTPUT = Path("translations/editorial_checkpoints/hodram_midroute_followups_20261123/paired_source.json")


bind_source = checked_text(getsource(prior.bind_block), {
    'prefix = bytes([selector]) if selector is not None else b""':
        'prefix = bytes([selector]) if word == 0x4000 else b""',
    'assert (prefix + current_body).hex() == registered["exact_stored_hex"]':
        'assert (prefix + current_body).hex() == registered["exact_stored_hex"], (number, entry["id"], hex(word))',
})
binding = vars(prior).copy()
exec(compile(bind_source, __file__ + "::mixed-consumer-source-binding", "exec"), binding)

def main():
    registered, queue = (base.load(p) for p in (release.RELEASE, checkpoint.QUEUE))
    candidate = base.digest(release.ROM)
    assert candidate == registered["candidate_sha256"] == queue["candidate_sha256"]
    assert base.digest(native.CLEAN) == registered["clean_input_sha256"]
    assert base.digest(base.REGISTRY) == registered["registry_sha256"]
    images = [base.NdsImage.open(p) for p in (native.CLEAN, release.ROM)]
    arms = [i.read_file(native.ARM) for i in images]
    archives = [i.read_file(ARCHIVE) for i in images]
    hashes = [native.digest(data) for data in archives]
    assert hashes[1] == registered["target_SC1_sha256"]
    banks = [native.IlnkContainer.parse(data).blocks for data in archives]
    references, groups = {}, []
    for interval, blocks in INTERVALS.items():
        ref = Path(f"releases/all_routes_editorial_20261122_hodram_{interval}_candidate/verification/registered_review.json")
        installed = base.load(ref)["records"]
        references[str(ref)] = base.digest(ref)
        for block in blocks:
            records = [r for r in installed if r["block"] == block]
            leads = {r["offset"]: r for r in queue["records"] if r["file_path"] == ARCHIVE
                     and r["block"] == block and "reviewed" not in r}
            assert records and leads
            groups.append(binding["bind_block"](block, records, [b[block] for b in banks], hashes, arms, leads))
    count = Counter(r["native_command_word"] for g in groups for r in g["records"])
    wraps = sum(len(g["open_wrap_leads"]) for g in groups)
    assert sum(count.values()) == 306 and wraps == 17 and count[0x4100] == 5 and count[0x2100] == 8
    assert not OUTPUT.exists()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    base.save(OUTPUT, dict(candidate_sha256=candidate, clean_sha256=registered["clean_input_sha256"],
        groups=groups, earlier_reviews=references, contextual_review_pending=True, new_review_credit=0))
    print(f"Bound {sum(count.values())} texts in {len(groups)} Hodram exchanges with {wraps} open wraps, "
          f"{count[0x4100]} style variants and {count[0x2100]} choice labels.", flush=True)


if __name__ == "__main__":
    main()
