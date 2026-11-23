"""Stage the contextual town-raid rephrase with the scoped Inn numeral patch."""

from pathlib import Path

from scripts import stage_inn_numerals_20261119 as previous

base,native,workflow = previous.base,previous.native,previous.workflow
parent,lead,patch = previous.parent,previous.lead,previous.patch
ARM,COMMON,CLEAN,PENDING,AFFECTED = previous.ARM,previous.COMMON,previous.CLEAN,previous.PENDING,previous.AFFECTED
ROOT = previous.ROOT.parent/"staged_v2"
ROM,PROOF,NATIVE_PROOF = ROOT/previous.ROM.name,ROOT/previous.PROOF.name,ROOT/previous.NATIVE_PROOF.name
REVISED = 1197
WORDS = "%s, %s attacked %s. What a rotten thing to do!"
NOTE = "The innkeeper first reports the attack and then voices personal disgust. Rotten keeps the familiar spoken register and the disapproval of the action itself. The reaction remains complete across the original date, attacker and town substitutions."


def main():
    assert not ROOT.exists()
    staged,release,ledger = map(base.load,(previous.PROOF,parent.RELEASE,base.LEDGER))
    assert base.digest(parent.ROM)==release["candidate_sha256"]==staged["parent_sha256"]==ledger["current_integrated_candidate"]["sha256"]
    assert base.digest(base.REGISTRY)==release["registry_sha256"]
    assert base.digest(previous.ROM)==staged["candidate_sha256"]
    image = base.NdsImage.open(previous.ROM)
    arm,common = image.read_file(ARM),image.read_file(COMMON)
    assert native.digest(common)==staged["target_COMMON_sha256"]
    directory = native.digest(arm[workflow.DIRECTORY_OFFSET:workflow.TABLE_OFFSET])
    before = workflow.owned_entries(common,arm,directory)
    initial = next(r for r in base.load(parent.REVIEW)["records"] if r["message_ID"]==REVISED)
    assert before[REVISED].text.hex()==initial["staged_hex"] and before[REVISED].text.count(b"%s")==WORDS.count("%s")==3
    after,installed,allocation = parent.stage.port.owned_deployment(common,arm,before,{REVISED:b" "+WORDS.encode("ascii")})
    assert all(workflow.reference(installed[r["message_ID"]])==r["current_reference"] and
        installed[r["message_ID"]].text.hex()==r["current_hex"] for r in base.load(PENDING)["records"])
    image.replace_file(COMMON,after)
    target = bytes(image.rom.save())
    image.replace_file(COMMON,common)
    assert bytes(image.rom.save())==previous.ROM.read_bytes()
    ROOT.mkdir(parents=True)
    ROM.write_bytes(target)
    base.save(PROOF,staged|dict(candidate_sha256=base.digest(ROM),target_COMMON_sha256=native.digest(after),
        text_changes=[dict(message_ID=REVISED,previous_hex=before[REVISED].text.hex(),staged_hex=installed[REVISED].text.hex(),
            current_reference=workflow.reference(before[REVISED]),staged_reference=workflow.reference(installed[REVISED]),
            previous_english=initial["english"],english=WORDS,note=NOTE)],allocation=allocation,
        source_proofs=staged["source_proofs"]|{str(p):base.digest(p) for p in (previous.PROOF,Path(__file__))}))
    print("Staged the Inn numeral correction with the contextual town-raid wording.")


if __name__=="__main__":
    main()
