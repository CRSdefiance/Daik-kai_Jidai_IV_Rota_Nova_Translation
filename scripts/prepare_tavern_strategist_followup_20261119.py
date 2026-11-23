"""Review the Tavern recruitment and Schemes exchanges against clean Japanese."""

from pathlib import Path

from dk4tool.patch.tavern_schemes_editorial import ARGUMENTS, compile_text
from scripts import register_hodram_early_confrontations_20261119 as parent
from scripts import stage_sea_hazard_dialogue_20261119 as shared

base, native, workflow = parent.base, parent.native, shared.workflow
ROOT = Path("work/tavern_strategist_followup_20261119")
OUTPUT = ROOT / "contextual_review_v3.json"
PRIOR = Path("translations/recruitment_schemes_contextual_final_review_v1.json")
CALLERS = Path("work/analysis/tavern_schemes_editorial_v774/native_context.json")
OWNERS = Path("work/analysis/tavern_schemes_integration_v776/input_contract.json")

EDITS = {
    908: ("It'll take about 1,000 gold coins to throw the enemy off balance. What do you have in mind?",
          "Spell out the original gold cost and retain the estimate and consultative tone."),
    909: ("For 1,000 gold coins, we can throw the enemy off balance. Which scheme shall we try?",
          "Keep the fixed gold cost and let the strategist ask about the plan in more natural English."),
    911: ("With 1,000 gold coins, we can shake them up. What's the plan?",
          "Keep the rough, confident voice and the explicit price."),
    915: ("%s, is that right? Which faction shall we target?",
          "Confirm the native scheme label before the courteous request for a faction."),
    918: ("All right, %s? Which faction shall it be?",
          "Keep the older voice distinct from the lively reaction with the same function."),
    927: ("Where shall we spread the rumors?",
          "The town selector supplies the place. Use the short natural question in this formal voice."),
    940: ("Lure a fleet under %s out to %s, correct?",
          "The first argument names the faction that owns the fleet. The second names its intended destination."),
    941: ("Lure a fleet under %s out to %s, then?",
          "Keep the ownership and destination clear in this courteous confirmation."),
    942: ("Draw a fleet under %s out to %s, right?",
          "Keep the younger voice's short confirmation and the sense of drawing the fleet out."),
    943: ("Bring a fleet under %s out to %s. Is that it?",
          "The speaker checks what the player wants. The faction names the fleet and the town names the destination."),
    944: ("Lure a fleet under %s out to %s, right?",
          "Keep the rough voice brief. It asks for confirmation of the target fleet and destination."),
    945: ("Draw a fleet under %s out to %s. Is that the plan?",
          "Retain the older voice's deliberate confirmation and the act of drawing a fleet out."),
    946: ("Get a fleet under %s to come out to %s?",
          "Keep the simple wording of the youthful voice and both original argument roles."),
    947: ("Lure a fleet under %s out to %s. Is that correct?",
          "Keep the mature voice formal and treat the faction as the target's owner."),
    957: ("In %s, shall we spread bad rumors about %s?",
          "Keep the town first and the faction second in a natural, courteous check before the scheme starts."),
}


def main():
    assert not OUTPUT.exists()
    release = base.load(parent.RELEASE)
    assert base.digest(parent.ROM) == release["candidate_sha256"] and base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(native.CLEAN) == release["clean_input_sha256"]
    clean, current = map(base.NdsImage.open, (native.CLEAN, parent.ROM))
    clean_arm, arm = (im.read_file(native.ARM) for im in (clean, current))
    assert native.digest(arm) == release["target_ARM9_sha256"]
    source = workflow.common_message_entries(clean.read_file(shared.COMMON), clean_arm)
    directory = native.digest(arm[workflow.DIRECTORY_OFFSET:workflow.TABLE_OFFSET])
    installed = workflow.owned_entries(current.read_file(shared.COMMON), arm, directory)
    prior = base.load(PRIOR)
    old = {r["message_ID"]: r for r in prior["records"]}
    assert old.keys() == set(range(883, 989))
    bindings, contract = map(base.load, (CALLERS, OWNERS))
    assert contract["editable_company_name_does_not_reach_these_original_scheme_consumers"]
    assert bindings["source_ARM9_sha256"] == native.digest(clean_arm)
    assert all(arm[lo:hi] == clean_arm[lo:hi] for lo, hi in bindings["source_current_executable_fragments_exact"])
    for location in bindings["original_voice_tables"]:
        at = int(location, 16) - 0x02000000
        assert arm[at:at + 32] == clean_arm[at:at + 32]
    records = []
    for ident, history in old.items():
        a, b = source[ident], installed[ident]
        assert a.text.hex() == history["source_hex"] and b.text.hex() == history["integrated_hex"], ident
        assert all(history["review"].values()), ident
        previous = workflow.logical(b.text)
        better, note = EDITS.get(ident, (previous, history["localization_note"]))
        revision = ident in EDITS
        record = dict(id=history["id"], message_ID=ident, message_id=ident, file_path=shared.COMMON,
            speaker=history["speaker"], context=history["context"].replace(";", ". "),
            source_meaning=history["source_meaning"], clean_Japanese=a.text.decode("cp932"),
            source_hex=a.text.hex(), current_hex=b.text.hex(), source_reference=workflow.reference(a),
            current_reference=workflow.reference(b), english=better, previous_English=previous,
            localization_note=note, decision="revision" if revision else "retention",
            original_voice_table=history["source_voice_table"], voice_slot=history["source_voice_slot"],
            source_native_arguments=ARGUMENTS.get(ident, []),
            English_argument_source_indices=list(range(len(ARGUMENTS.get(ident, [])))),
            original_substitution_count=a.text.count(b"%s"), review=dict(history["review"]) | {"formatting": not revision})
        if revision:
            assert b.text.startswith(b" ") and better.count("%s") == record["original_substitution_count"]
            record["encoded_hex"] = compile_text(record).hex()
        records.append(record)
    ROOT.mkdir(exist_ok=True)
    base.save(OUTPUT, dict(candidate_sha256=release["candidate_sha256"], registry_sha256=release["registry_sha256"],
        translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=list(workflow.parent.GATES), records=records,
        prior_evidence={p.as_posix(): base.digest(p) for p in (PRIOR, CALLERS, OWNERS)},
        no_duplicate_credit=True, registration_pending=True))
    print(f"Reviewed {len(records)} shared Tavern records, with {len(EDITS)} proposed revisions.")


if __name__ == "__main__":
    main()
