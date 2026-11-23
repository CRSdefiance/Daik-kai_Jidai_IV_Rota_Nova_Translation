"""Reconcile later Maria dialogue against exact registered editorial decisions in one pass."""

from collections import Counter, defaultdict
from pathlib import Path

from scripts import register_maria_B51_B70_20261122 as build
from scripts import review_maria_B18_B20_20261122 as census_scope


base,native=build.base,build.native
ARCHIVE="/data/SC3.DK4"
CENSUS=census_scope.CENSUS
OUT=build.writer.review.ROOT.parent/"maria_B71_B302_current_20261122"
RESULT=OUT/"exact_current_dialogue_reconciliation.json"
RANGE=range(71,303)


def stored_refs(row):
    for field in ("registered_reference","integrated_reference","planned_integrated_reference"):
        ref=row.get(field)
        if ref and isinstance(ref,dict):
            value=ref.get("exact_stored_hex") or ref.get("stored_hex") or ref.get("raw_hex")
            if value:
                yield value,ref


def load_editorial_history():
    paths=set(Path("translations").glob("maria*integrated_final_review_v1.json"))
    paths.update(Path("translations").glob("maria*contextual_final_review_v1.json"))
    paths.update(Path("releases").glob("*/verification/registered_review.json"))
    paths.update(Path("releases").glob("*/verification/registered_editorial_review.json"))
    known,proofs=defaultdict(list),{}
    for path in sorted(paths):
        used=False
        for row in base.load(path).get("records",[]):
            if row.get("file_path")!=ARCHIVE or row.get("block") not in RANGE:
                continue
            source=row.get("source_hex")
            gates=row.get("review") or {}
            if not source or not all(gates.get(k) is True for k in ("source","context","localization","naturalness","formatting")):
                continue
            ref=row["source_reference"]
            if "offset" not in ref:
                continue
            for body,target in stored_refs(row):
                used=True
                key=(row["block"],ref["offset"],source)
                known[key].append(dict(id=row["id"],review_path=str(path),historical_reference=target,stored_hex=body))
        if used:
            proofs[str(path)]=base.digest(path)
    return known,proofs


def clean_body(source, current, word, positions):
    source_bytes,current_bytes=[bytes.fromhex(row["whole_command_hex"]) for row in (source,current)]
    if word in (0x4000,0x4100):
        assert source_bytes[:6]==current_bytes[:6] if word==0x4000 else source_bytes[18:20]==current_bytes[18:20]
    text=census_scope.pairing.text_records
    for a,b in zip(text(source_bytes,word),text(current_bytes,word),strict=True):
        source_at,current_at=source["offset"]+a[0],current["offset"]+b[0]
        assert (a[1],a[3])==(b[1],b[3])
        prefix=f"{a[1]:02x}" if word==0x4000 else ""
        owner=positions[source_at]
        source_hex,installed_hex=prefix+a[2].hex(),prefix+b[2].hex()
        assert owner["source_hex"]==source_hex and owner["covered"]
        yield dict(id=owner["id"],word=word,source_offset=source_at,source_command_offset=source["offset"],
                   current_offset=current_at,current_command_offset=current["offset"],source_hex=source_hex,
                   current_hex=installed_hex,selector=a[1],slots=a[3])


def main():
    assert not RESULT.exists()
    release,census=map(base.load,(build.RELEASE,CENSUS))
    assert release["candidate_sha256"]==base.digest(build.ROM) and release["registry_sha256"]==base.digest(base.REGISTRY)
    assert census["source_ROM_sha256"]==release["clean_input_sha256"]==base.digest(native.CLEAN)
    assert not census["missing"] and not census["inventory_failures"] and not census["legacy_source_bindings_not_exact"]
    clean,installed=map(base.NdsImage.open,(native.CLEAN,build.ROM))
    archives=[image.read_file(ARCHIVE) for image in (clean,installed)]
    hashes=list(map(native.digest,archives))
    assert hashes==[census["source_archive_sha256"],release["target_SC3_sha256"]]
    arms=[image.read_file(native.ARM) for image in (clean,installed)]
    assert native.digest(arms[1])==release["target_ARM9_sha256"]
    banks=[native.IlnkContainer.parse(raw).blocks for raw in archives]
    inputs=defaultdict(dict)
    for row in census["records"]:
        block=row["block"]
        if block in RANGE:
            inputs[block][row["source_reference"]["offset"]]=row
    known,history=load_editorial_history()
    inventory,_,_=native.scoped_inventory()
    results,exceptions=[],[]
    status=Counter()
    for n in RANGE:
        positions=inputs[n]
        if not positions:
            continue
        bodies=[bank[n] for bank in banks]
        reference=dict(block=n,source_block_sha256=native.digest(bodies[0]),current_block_sha256=native.digest(bodies[1]))
        try:
            cmd=[inventory(a,b)[0] for a,b in zip(arms,bodies,strict=True)]
            rows=[body for original,cur in zip(*cmd,strict=True)
                  for word in (original["word"],)
                  if word in census_scope.pairing.TEXT_WORDS
                  for body in clean_body(original,cur,word,positions)]
            assert [r["word"] for r in cmd[0]]==[r["word"] for r in cmd[1]]
            assert len(rows)==len(positions) and {r["source_offset"] for r in rows}==positions.keys()
        except (ValueError, KeyError, AssertionError) as error:
            exceptions.append(reference|dict(records=[r["id"] for r in positions.values()],reason=repr(error)))
            status["requires-structural-pairing"]+=len(positions)
            continue
        for row in rows:
            prior=known[n,row["source_offset"],row["source_hex"]]
            same=next((proof for proof in prior if proof["stored_hex"]==row["current_hex"]),None)
            verdict="exact-stored" if same else "changed-since-reviewed" if prior else "prior-exact-reference-needed"
            status[verdict]+=1
            row.update(decision=verdict,prior_review=same or (prior[0] if prior else None))
        results.append(reference|dict(records=rows))
    assert sum(status.values())==sum(map(len,inputs.values()))
    OUT.mkdir(exist_ok=True)
    base.save(RESULT,dict(candidate_sha256=release["candidate_sha256"],registered_release=str(build.RELEASE),
        certificate_sha256=base.digest(build.RELEASE),archive=ARCHIVE,archive_sha256=hashes[1],clean_archive_sha256=hashes[0],
        clean_census=str(CENSUS),clean_census_sha256=base.digest(CENSUS),earlier_reviews=history,
        results=dict(status),groups=results,exceptions=exceptions,added_credit=0,actual_gameplay=False))
    print(dict(status),[row["block"] for row in exceptions])


if __name__=="__main__":
    main()

