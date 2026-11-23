"""Review and bind the personal names and occupational labels in the ten exchanges."""

from contextlib import redirect_stdout
from inspect import getsource
from io import StringIO
from pathlib import Path
from struct import unpack_from

from scripts import reconcile_shared_speaker_labels_20261111 as precedent
from scripts import stage_rafael_east_asia_followup_20261121 as stage
from scripts import verify_rafael_east_asia_followup_20261121 as display
from scripts.review_barmaid_town_labels_20261115 import read_static
from scripts.source_locked_derivation_v5118 import checked_text


base, native = stage.base, stage.native
INVENTORY = Path("translations/editorial_checkpoints/SharedText_20261110_v1/default_actor_names_current_20261120_v1.json")
PROOF = stage.ROOT / "speaker_labels.json"
NOTES = {
    0: "Use approved Rafael Castor. Verify the same protagonist's given name and surname in the installed dialogue substitutions.",
    3: "Use approved Maria Li in the dialogue header. The catalogue's Huamei corresponds to the separate source field.",
    4: "Keep Janus Pasar. His hesitant question about Linares does not establish a title for Janus or Linares.",
    5: "Keep Claudio Manaus in the header and the established Clau nickname where Rafael speaks it.",
    6: "Keep Julio Erneco. His warning in the quarrel uses only the approved personal name in the header.",
    8: "Keep Arcadius Eudoxios in the public header. Rafael uses Eirene in private and the catalogue preserves the source middle field.",
    10: "Keep Xien Yan. His respectful transition to Admiral Li does not create a rank for him.",
    31: "Use Pedro Valdes in the dialogue and Pedro de Valdes in the catalogue, consistent with the source's separate middle particle.",
    34: "Keep the established Barbarossa Hayreddin in the header and the source's separate Fazul in the catalogue.",
    48: "Keep Simon Linares. The separate given name and surname match Valdes's address and Simon's claim about his Cordoban family.",
    83: "Shopkeeper suits the merchant who reports the fleet movements in town. Leave the source's background descriptor out of the speaking label.",
    104: "Trader identifies the trading-house worker who asks about the fight off Seville and warns Rafael.",
    106: "Trader also identifies the separate informant who points Rafael to Hangzhou. His casual voice and regional knowledge come from his dialogue.",
    113: "Port Worker fits the dock attendant who welcomes Rafael and relays the summons. The familiar Japanese form grants no office or kinship.",
    139: "Priest preserves the role that matters when he offers the object upon Rafael's Mediterranean victory.",
    147: "Guildmaster identifies the guild leader whose advice is to stay clear until the fleet is ready.",
    151: "Sailor suits the affiliated crew member cheering aboard. Keep the broader Retainer form for the catalogue.",
}


def main():
    assert not PROOF.exists()
    review, stage_proof, catalogue, rendered = map(base.load, (stage.OUTPUT, stage.PROOF, INVENTORY, display.PROOF))
    candidate = base.digest(stage.ROM)
    assert candidate == stage_proof["candidate_sha256"] == rendered["candidate_sha256"]
    dependencies = rendered["initialized_dependencies"]
    ctx = native.RegisteredRuntime(dependencies["release_proof"], dependencies["startup_proof"], captain=0)
    image = base.NdsImage.open(stage.ROM)
    assert all(ctx.image.read_file(path) == image.read_file(path) for path in display.display.ASSETS)
    clean_arm = base.NdsImage.open(native.CLEAN).read_file(native.ARM)
    assert native.digest(clean_arm) == base.load(precedent.INVENTORY)["clean_ARM9_sha256"]
    actors = {r["actor_ID"]: r for r in catalogue["source_and_current_default_name_fields"]}
    selectors = {r["source_selector"] for r in review["records"]}
    assert selectors == NOTES.keys()
    getter_template = precedent.original_names
    script = checked_text(getsource(getter_template.names), {
        'for ident in [2,4,13,23,109]:': f'for ident in {sorted(selectors)}:',
        'actor = root+4+32*ident': 'actor = root+0x19E4 if ident==0 else root+4+32*ident',
    })
    scope = vars(getter_template).copy()
    exec(compile(script, __file__ + "::scoped-native-name-getters", "exec"), scope)
    with redirect_stdout(StringIO()):
        executed = ctx.execute(scope["names"])
    assert len(executed["rows"]) == 2 * len(selectors)
    receipts = []
    for ident in sorted(selectors):
        known = actors[ident]
        fields = []
        for field in known["exact_fields"]:
            offset = field["offset"]
            original = read_static(clean_arm, offset) if unpack_from("<I", clean_arm, offset)[0] else None
            assert ctx.arm[offset:offset + 4] == ctx.raw[offset:offset + 4]
            pointer, = unpack_from("<I", ctx.raw, offset)
            current = None
            if pointer:
                at = pointer - precedent.BASE
                assert 0 <= at <= len(ctx.raw) - 96
                value = ctx.raw[at:ctx.raw.index(0, at, at + 96)]
                current = dict(pointer=pointer, offset=at, hex=value.hex(), text=value.decode("cp932"))
            assert original == field["clean"]
            fields.append(dict(field=field["field"], offset=offset, clean=original, current=current))
        getters = [row for row in executed["rows"] if row["actor_ID"] == ident]
        assert [r["consumer"] for r in getters] == ["progressive-nameplate", "full-catalogue"]
        assert [r["text"] for r in getters] == [known["progressive_nameplate"], known["full_catalogue"]]
        context = [r["id"] for r in review["records"] if r["source_selector"] == ident]
        assert {r["speaker"] for r in review["records"] if r["source_selector"] == ident} == {getters[0]["text"]}
        receipts.append(dict(actor_ID=ident, context_records=context, exact_ARM9_fields=fields,
                             native_getters=getters, decision="retention", localization_note=NOTES[ident]))
    base.save(PROOF, dict(candidate_sha256=candidate, runtime_dependencies=ctx.receipt(), records=receipts,
                         precedent={"path": str(INVENTORY), "sha256": base.digest(INVENTORY)},
                         offline_native_getters_only=True, new_editorial_credit=0))
    print(f"Reviewed {len(receipts)} names and roles and verified {len(executed['rows'])} native getters.")


if __name__ == "__main__":
    main()
