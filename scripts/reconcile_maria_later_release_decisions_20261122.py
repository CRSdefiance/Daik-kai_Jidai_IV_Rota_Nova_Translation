"""Restore applicable later release evidence for the Maria reconciliation leads."""

from pathlib import Path

from scripts import reconcile_maria_late_current_20261122 as scan


base,native,build=scan.base,scan.native,scan.build
ROOT=scan.OUT
SPECIAL=ROOT/"qualified_structural_pairing.json"
B109=ROOT/"special_group_binding_followup.json"
OUTPUT=ROOT/"exact_later_release_decisions.json"
GATES=("source","context","localization","naturalness","formatting")


def rows_to_bind(ordinary, special):
    needs={}
    for group in ordinary["groups"]:
        for row in group["records"]:
            if row["decision"]=="changed-since-reviewed":
                assert row["word"]==0x4000
                needs[row["id"]]=row | {"block":group["block"],"current_block_sha256":group["current_block_sha256"]}
    for row in special["records"]:
        if row["decision"]=="changed-since-reviewed":
            page,=row["native_pages"]
            assert page["command_word"]==0x4000
            needs[row["id"]]=row | page | {"source_offset":row["source_reference"]["offset"]}
    assert len(needs)==87
    return needs


def owned_body(span):
    command=span.get("exact_command_hex") or span.get("complete_command_hex")
    if command:
        raw=bytes.fromhex(command)
        assert raw[:5]==b"\0\x40\xff\xff\0" and raw[-1]==0
        return raw[5:].rstrip(b"\0").hex(), command
    return span.get("exact_stored_hex") or span.get("raw_hex") or span.get("exact_hex"),None


def historical_match(row, installed, command):
    if not all(row.get("review",{}).get(gate) for gate in GATES):
        return False
    there=row["source_reference"]
    source_hex=(row.get("source_hex") or owned_body(there)[0])
    if there.get("offset")!=installed["source_offset"] or source_hex!=installed["source_hex"]:
        return False
    reference=row["registered_reference"]
    pages=reference.get("pages")
    if pages and len(pages)!=1:
        return False
    stored, encoded=owned_body(pages[0] if pages else reference)
    return (stored==installed["current_hex"] and (encoded is None or encoded==command))


def main():
    assert not OUTPUT.exists()
    release=base.load(build.RELEASE)
    earlier,special,fallback=map(base.load,(scan.RESULT,SPECIAL,B109))
    assert release["candidate_sha256"]==base.digest(build.ROM)==earlier["candidate_sha256"]==special["candidate_sha256"]==fallback["candidate_sha256"]
    assert base.digest(scan.RESULT)==special["scan_sha256"]==fallback["base_reconciliation_sha256"]
    manifest=base.load(build.MANIFEST)
    assert manifest["candidate_sha256"]==release["candidate_sha256"]
    assert base.digest(build.MANIFEST)==release["manifest_sha256"]
    registered={Path(p).resolve() for p in manifest["batches"]}
    needs=rows_to_bind(earlier,special)
    current=base.NdsImage.open(build.ROM)
    bank=native.IlnkContainer.parse(current.read_file(scan.ARCHIVE)).blocks
    commands={}
    inventory,_,_=native.scoped_inventory()
    for n in {r["block"] for r in needs.values()}:
        commands[n]={c["offset"]:c["whole_command_hex"] for c in inventory(current.read_file(native.ARM),bank[n])[0]}
    checks={}
    for id,row in needs.items():
        command=commands[row["block"]][row["current_command_offset"]]
        assert owned_body({"exact_command_hex":command})[0]==row["current_hex"]
        checks[id]=command

    closed,proofs=[],{}
    paths=Path("releases").glob("*/verification/registered_review.json")
    for path in sorted(paths,reverse=True):
        if path.resolve() not in registered:
            continue
        manuscript=base.load(path)
        proof_path=path.with_name("registered_release_verification.json")
        for row in manuscript.get("records",[]):
            id=row.get("id")
            if id not in needs or row.get("file_path")!=scan.ARCHIVE or "registered_reference" not in row:
                continue
            match=needs[id]
            if not historical_match(row,match,checks[id]):
                continue
            if str(path) not in proofs:
                proof=base.load(proof_path)
                assert manuscript["candidate_sha256"]==proof["candidate_sha256"]
                assert proof["clean_input_sha256"]==release["clean_input_sha256"]
                assert proof["clean_input_patch_byte_exact"]
                proofs[str(path)]=dict(manuscript_hash=base.digest(path),release_path=str(proof_path),
                    release_hash=base.digest(proof_path),candidate_sha256=proof["candidate_sha256"])
            assert row["registered_reference"]["candidate_sha256"]==proofs[str(path)]["candidate_sha256"]
            closed.append(dict(id=id,block=match["block"],exact_previous_source_hex=match["source_hex"],
                original_source_reference=row["source_reference"],earlier_registered_reference=row["registered_reference"],
                prior_native_and_contextual_review=str(path),review=row["review"],
                installed_command_offset=match["current_command_offset"],installed_body_hex=match["current_hex"],
                installed_command_hex=checks[id],current_block_sha256=match["current_block_sha256"]))
            needs.pop(id)
    base.save(OUTPUT,dict(candidate_sha256=release["candidate_sha256"],scan_sha256=base.digest(scan.RESULT),
        structural_pairing_sha256=base.digest(SPECIAL),records=sorted(closed,key=lambda r:(r["block"],r["installed_command_offset"])),
        retained_later_release_count=len(closed),existing_exact_count=3752,
        latest_total_exact=3752+len(closed),pending=needs,qualified_release_receipts=proofs,
        gameplay_claimed=False,new_credit=0))
    print(f"{len(closed)} matched later registered decisions. Remaining: {', '.join(needs)}")


if __name__=="__main__":
    main()

