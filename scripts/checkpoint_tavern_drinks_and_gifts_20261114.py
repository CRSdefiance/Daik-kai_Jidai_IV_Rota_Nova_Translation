"""Document the Tavern drink, rumor, and gift exchanges against clean Japanese."""

from pathlib import Path

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET,TABLE_OFFSET,common_message_entries
from scripts import stage_tavern_toast_and_gift_20261114 as stage
from scripts.review_sound_bgm_titles_v1 import reference

base=stage.base
OUT=Path("translations/editorial_checkpoints/SharedText_20261110_v1/tavern_drinks_rumors_gifts_20261114_v1.json")
TAVERN=Path("translations/tavern_exchanges_contextual_final_review_v1.json")
SERVICES=Path("translations/primary_town_services_contextual_final_review_v1.json")
CONTEXTS=(
    (range(51,63),"The barkeep opens the Tavern, quotes the first drink, calls the attendant, and handles the optional second drink. The attendant answers or greets the visitor; a direct question can start a separate branch."),
    (range(820,825),"Independent rumor replies after ordering a drink. The barkeep can distinguish local renown from influence, give a nearby-town tip, or have no news."),
    (range(825,828),"The player may briefly react to a tip, decline another drink and be teased, or hear a separate toast to the introduction after the paid-drink path."),
    (range(828,842),"A treasure rumor can introduce the subject, and a gift conversation branches by captain. The attendant notices the object, hears its name, admires it, responds to the captain’s question, and tentatively asks for it. Refusal draws an apology. Acceptance can use a generic or character-specific reply before the original transfer."),
)
COMMENTS={
 51:("The barkeep welcomes the customer and asks what they want.","The friendly direct question invites a drink order."),
 52:("The formal first-drink quote is ten gold coins.","That'll be gives the amount naturally before the player decides."),
 53:("The casual first-drink quote is five gold coins.","The terse price fits this barkeep and keeps the amount clear."),
 54:("The barkeep addresses the named attendant and tells them to pour for the guest.","The instruction is courteous to the visitor and keeps the supplied attendant name."),
 55:("The barkeep calls the named attendant to a customer.","The casual call and customer announcement keep the original energy and name order."),
 56:("The attendant promptly answers.","On it suits the brisk reply from elsewhere in the tavern."),
 57:("The attendant reacts to the guest and welcomes them.","The brief English greeting fits the arrival without overplaying the interjection."),
 58:("The attendant recognizes the named guest with a warmer greeting.","Oh and the original name keep the recognition distinct from the generic greeting."),
 59:("The attendant invites the player to have another cup.","The short offer sounds friendly and leads naturally into Yes or No."),
 60:("The polite follow-up quote asks for twenty gold coins.","The colloquial quote fits the second price branch and keeps the amount exact."),
 61:("The casual follow-up quote asks for ten gold coins.","The barkeep's short spoken amount contrasts naturally with the formal quote."),
 62:("The barkeep asks why the guest has come.","Need something is brisk and fits an ordinary inquiry."),
 820:("The named person associated with a town has become renowned in the stated role locally.","Famous around here gives the distinction from the power reported in 821."),
 821:("The named person associated with a town wields local influence in the stated role.","The registered real pull expresses influence in the barkeep's voice. It stays distinct from fame in 820."),
 822:("The speaker asks politely whether the guest has visited the named nearby town.","The complete English question keeps the visit and the nearby location."),
 823:("The barkeep asks whether the guest knows the named town and says it is nearby.","The conversational two sentences preserve the inquiry and proximity."),
 824:("The speaker has nothing noteworthy to report at the moment.","Right now keeps the reply limited to current news."),
 825:("The player gives a brief questioning reaction.","Hm keeps the momentary curiosity before the next turn."),
 826:("The barmaid is surprised at the refusal and teases the guest about their drinking tolerance.","The existing line relates the tease directly to the offered drink. It remains friendly after No."),
 828:("The attendant asks about a particular treasure whose whereabouts are uncertain and whose beauty is hearsay.","Out there somewhere keeps the uncertainty, and they say marks the reported praise."),
 829:("The attendant sees the object and asks what it is.","The single natural question carries both Japanese questions without repetition."),
 830:("Rafael echoes the question and names the item lightly.","The brief echo and naming answer suit Rafael and handle any supplied item name."),
 832:("Lil repeats the question and explains what the object is called.","The echoed question fits her light explanatory delivery before the attendant's compliment."),
 833:("Maria echoes the question and gives the object's name.","The existing phrasing is natural with both ordinary items and named treasures. Her interest question in the next turn gives this exchange its particular tone."),
 834:("The attendant admires the object.","How lovely preserves the delighted compliment."),
 835:("Rafael asks whether the attendant wants the object.","Would you like it is a warm offer and leads naturally to the tentative request."),
 836:("Hodram asks whether the object appeals to the attendant.","Do you like it invites a response without prematurely promising the gift."),
 837:("Lil reacts lightly and asks whether the attendant likes the object.","Oh preserves her reaction, and the question gives the attendant room to respond."),
 838:("Maria reacts lightly and asks whether the attendant is interested.","The existing English distinguishes interest from the simple liking question."),
 839:("The attendant tentatively asks whether the gift is meant for them.","The question keeps the uncertainty before the separately selected response."),
 840:("The attendant responds with delight, thanks the player and promises to cherish the gift.","The three short turns carry the emotional progression and the commitment to keep the gift."),
 841:("The attendant takes in the refusal and apologizes for having been selfish.","The pause and self-directed apology preserve disappointment without blaming the player."),
}


def main():
    assert not OUT.exists()
    manifest=base.load(stage.STORED)
    release=base.load(stage.parent.RELEASE)
    assert base.digest(stage.parent.ROM)==release["candidate_sha256"]==manifest["previous_sha256"]
    assert base.digest(stage.CLEAN)==manifest["clean_sha256"] and base.digest(stage.ROM)==manifest["candidate_sha256"]
    rom,source=map(base.NdsImage.open,(stage.parent.ROM,stage.CLEAN))
    arm=rom.read_file(stage.ARM)
    digest=stage.parent.parent.source.current.assets.edit.digest
    current=owned_entries(rom.read_file(stage.COMMON),arm,digest(arm[DIRECTORY_OFFSET:TABLE_OFFSET]))
    japanese=common_message_entries(source.read_file(stage.COMMON),source.read_file(stage.ARM))
    revisions={r["message_id"]:r for r in manifest["records"]}
    previous={}
    for path in (SERVICES,TAVERN):
        for row in base.load(path)["records"]:
            if "message_id" in row:
                previous[row["message_id"]]=(path,row)
    ledger=base.load(base.LEDGER)
    credited={row["id"] for row in ledger[base.CONTEXT]["integrated_record_keys"] if row["file_path"]==stage.COMMON}
    records=[]
    for span,context in CONTEXTS:
        for n in span:
            assert f"COMMON_MESSAGE_{n}" in credited
            a,b=japanese[n],current[n]
            prior_path,past=previous[n]
            assert a.text.hex()==past["source_hex"]
            assert all(past["review"].values())
            prior_hex=past.get("integrated_hex",past["current_hex"])
            if n==821:
                prior_path=stage.parent.REVIEW
                earlier,=base.load(prior_path)["records"]
                prior_hex=earlier["registered_reference"]["exact_stored_hex"]
            assert b.text.hex()==prior_hex
            if n in revisions:
                row=revisions[n] | dict(exchange_context=context,formatting_status="fresh verification in separate release receipt")
            else:
                meaning,why=COMMENTS[n]
                row=dict(id=f"COMMON_MESSAGE_{n}",message_id=n,clean_reference=reference(a),current_reference=reference(b),
                    Japanese=a.text.decode("cp932"),English=b.text.decode("ascii"),clean_hex=a.text.hex(),current_hex=b.text.hex(),
                    exchange_context=context,source_meaning=meaning,localization_note=why,decision="retention",
                    review=dict.fromkeys(stage.GATES,True),formatting_status="inherited registered review and byte-exact retained text")
            row["prior_review"]=str(prior_path)
            records.append(row)
    accepted=sum(r["decision"]=="retention" for r in records)
    assert len(records)==34 and accepted==32
    base.save(OUT,dict(candidate_sha256=release["candidate_sha256"],clean_sha256=manifest["clean_sha256"],
        reviewed_source_keys=len(records),retentions=accepted,records=records,new_dialogue_credit=0,
        complete_paid_and_refused_gameplay_verified_separately=True,
        gift_context_historical_and_controlled=True,actual_gift_transfer_observed=False,full_goal_complete=False))
    print("Recorded 34 clean/current contextual comparisons with 32 justified retentions.")


if __name__=="__main__":
    main()
