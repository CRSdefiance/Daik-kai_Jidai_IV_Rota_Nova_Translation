"""Review Sakura's visits, the forest choices and Maria's inquiry in Macao."""

from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import prepare_sakura_expeditions_macau_20261118 as paired
from scripts import review_jungle_caves_20261118 as binder
from scripts.source_locked_derivation_v5118 import checked_text

base, parent = paired.paired.base, paired.parent
SOURCE = paired.ROOT / "paired_source.json"
SOURCE_SHA = "1603317e069b2272567e2b6ff4fec8e6619b8ac3e1cfcb817345695f1d74f10c"
FOLDER = Path("translations/editorial_checkpoints/SharedText_20261110_v1")
DECISIONS = FOLDER / "sakura_expeditions_macao_decisions_v4.txt"
OUTPUT = FOLDER / "sakura_expeditions_macao_20261118_prose_v4.json"
HISTORY = (
    ("rafael_B321_B342_integrated_final_review_v1.json",),
    ("hodram_B301_B310_integrated_final_review_v1.json", "hodram_B311_B324_integrated_final_review_v1.json"),
    ("lil254_B312_B319_integrated_final_review_v1.json",),
    ("maria349_B275_B285_integrated_final_review_v1.json",),
)
NOTES = {
    5: "Keep the association with India and the prestige of the cloth without specifying a textile fiber.",
    14: "Sakura appreciates the offer but considers the valuable chintz merchandise. Seeing it is enough for her.",
    19: "Keep sake as the drink Sakura knows and wine as the drink she has yet to try.",
    26: "The pause follows Sakura's agreement while she tastes the wine.",
    34: "Rafael is surprised by how quickly the two others finished his wine.",
    38: "Rafael reassures Sakura before reversing the storytelling roles.",
    40: "Keep Kyoto, the imperial capital and home of the emperor, as the destination Rafael wants to visit.",
    74: "Keep the practical distinction between scaring the wolf away and fighting. The route's displayed number remains consistent.",
    91: "Keep the exclusive given-name substitution and the injury notice.",
    107: "Rafael apologizes for losing his grip. His response contrasts with Lil's self-blame about how she fought.",
    117: "The narrator reports apparent crew fatigue after the escape or struggle.",
    132: "This is the speaker's practical judgment about foreign pressure and the rule, followed by a discreet exception.",
    151: "Keep the bat sound as a sound effect between two crew reactions.",
    152: "The detour avoids the bats and costs a day. The other choice presses on.",
    155: "The system records the same elapsed day as the other expeditions.",
    172: "The youthful voice is hungry while the others are catching their breath.",
    192: "The danger is a rock falling behind the party. The later choice still makes its route matter.",
    203: "Hodram calls for an emergency move into the brush after the dead end.",
    204: "The brush choice specifies left. It follows the original decision at the dead end.",
    205: "The brush choice specifies right. This preserves the available alternative.",
    206: "A deliberate silent reaction in this exchange.",
    227: "The speaker credits the party's escape to the rock rolling down the left path.",
    236: "Keep the discovery as hearsay, the map as illustrated and the ruins as an old kingdom near town.",
    244: "Lil explicitly blames herself for the outcome and regrets how she fought.",
    246: "Lil talks tough to the wolf while letting it go. Camille's aside undercuts her.",
    249: "Camille denies saying anything and privately remarks that Lil heard what he hoped she wouldn't.",
    261: "The narrator hedges about the injuries after the slope gives way.",
    271: "Maria tells the injured man to rest and promises to bring the ship's doctor.",
    278: "The former smuggler speaks roughly. Keep weapons, armor and the local lords he helped evade.",
    280: "Keep the source cultural term for the pirates with a plain English explanation, and the reference to the guns.",
    292: "The alleged delegation is Portuguese and the intended audience is with the Ming emperor. The speaker heard it secondhand.",
    309: "Restore the source currency and keep the price at 1,000 gold coins.",
    311: "The informant names Macao and tomorrow. The wrong port and week in his reply are hypothetical.",
    324: "The former smuggler recognizes Jacob from work and identifies his current rank in the ring.",
    329: "Maria tells him to stay calm and gives her provisional conclusion that the missionaries are impostors.",
    345: "This is Maria's forecast about what the smugglers may try to sell next, including people.",
    350: "The impostor claims Jesuit authority and a party of more than one hundred.",
    354: "The performance retains the historical title Son of Heaven and its accusation of deception.",
    361: "The supposed magistrate claims someone recognized and reported the impostors.",
    373: "The governor notices both Western and Japanese people among the supposed Ming troops.",
    379: "The former actor is deferential about portraying a magistrate. The crew hadn't acquired that rank.",
    384: "Sakura's worry introduces the calmer return exchange.",
    393: "Sakura offers to guide Maria only partway and says the map makes Kyoto easy to find.",
}
PHRASES = (
    "faraway places?", "have you heard of chintz?", "I hear it's fine cloth.",
    "it feels wonderful...", "something so valuable.", "It's for sale, isn't it?",
    "Seeing it is enough.", "What does wine taste like?", "different from sake, isn't it?",
    "I'd love to try it!", "It's your turn now.", "Would you tell me about Japan?",
    "map to the Proof.", "map to the Proof?", "the Proof's map", "before we forget,",
    "northeast of China.", "northeast of China, right?", "northeast of China, was it?",
    "northeast of China!", "without a map.", "Everyone, stay calm.", "if we treat it quickly.",
    "The wolves are gone, too.", "The wolves are gone.", "Thank goodness", "the wolf's gone.",
    "Your sailors look tired.", "closed-door policy", "in confidence.", "which way to go.",
    "One day has passed.", "I'm a little winded.", "Do you hear something?",
    "coming up behind us!", "into the brush!", "Is everyone all right?!",
    "down the left path!", "gave me a scare.", "slipped my mind.", "an old illustrated map.",
    "ruins of an old kingdom", "near town.", "where's the map now?", "looking for it?",
    "I-I'll manage.", "won't turn serious.", "out of the woods.", "This stays between us.",
    "It's my fault.", "let you go this time.", "(Of course she heard that.)",
    "a few people were hurt.", "Who's got it?", "You've got to stay still!",
    "try to rest.", "our ship's doctor.", "past the worst of it.", "weapons and armor",
    "the local lords' backs.", "for a laugh.", "what I did for a living.", "a secret of theirs.",
    "What port are they coming to?", "who might know more?", "at the tavern in Macao.",
    "The tavern in Macao?", "than in this town.", "Wouldn't you say, Admiral?",
    "1,000 gold coins?", "The fleet gets in tomorrow.", "Right here in Macao.",
    "why the boss told me to stay away.", "looks like a bodyguard!", "What's going on here?!",
    "pretending to be missionaries.", "an entire government.", "they'll make a fortune.",
    "that comes after them.", "at this a long time.", "drugs or enslaved people.",
    "stop them ourselves.", "The Society of Jesus sent us,", "more than a hundred in all.", "your audience.",
    "The Ming neglects its defenses.", "stand up to the great powers.", "the Son of Heaven himself!", "knew your faces", "cost me my head!",
    "without so much as a word", "in the Ming army?", "You had me convinced.",
    "Best mimic in town!", "Playing a magistrate...", "put on a disguise,",
    "that late already?", "at the temple.", "We'll be on our way.",
)


def main():
    assert base.digest(SOURCE) == SOURCE_SHA and not OUTPUT.exists()
    packet, release = map(base.load, (SOURCE, parent.RELEASE))
    assert packet["candidate_sha256"] == release["candidate_sha256"] and packet["complete_source_current_binding"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    edit_list = [line.split("|", 2) for line in DECISIONS.read_text(encoding="utf-8-sig").splitlines() if line]
    chosen = {(int(route), int(pos)): english for route, pos, english in edit_list}
    assert len(chosen) == len(edit_list)
    history_paths = [[Path("translations") / name for name in names] for names in HISTORY]
    history = [{k: (p, row) for p in paths for k, row in binder.binder.index_history(p).items()}
               for paths in history_paths]
    hashes = {p: base.digest(p) for paths in history_paths for p in paths}
    scope = vars(binder).copy()
    script = checked_text(getsource(binder.review_one), {
        "if word == 0x2100:": "if word in (0x2100, 0x2200):",
        "if word == 0x2100 else": "if word in (0x2100, 0x2200) else",
    })
    exec(compile(script, __file__ + "::two-and-three-choice-source-binder", "exec"), scope)
    sequence, done, records = {}, set(), []
    for group in packet["groups"]:
        route, block = group["route"], group["block"]
        for raw in group["records"]:
            key = raw["native_command_word"], raw["Japanese"]
            ordinal = sequence.setdefault(key, len(sequence)+1)
            path, prior = history[route][block, raw["source_offset"]]
            gloss = prior["source_meaning"]
            note = NOTES.get(ordinal, gloss)
            if 43 <= ordinal <= 50:
                note = f"Keep the individual companion's register and the map's distinction from the Proof. {gloss}"
            proposed = chosen.get((route, ordinal))
            edit = {(1, route): proposed} if proposed is not None else {}
            review = FunctionType(scope["review_one"].__code__,
                                  scope | {"NOTES": (note,), "EDITS": edit, "PHRASES": PHRASES})
            item = review(raw, group, prior, 1, path, hashes[path])
            item["source_meaning"] = gloss
            item["context"] = prior["context"]
            item["packet_ordinal"] = ordinal
            if item["decision"] == "revision":
                done.add((route, ordinal))
            else:
                item["localization_note"] = f"Current wording preserves this beat in the exchange. {note}"
            records.append(item)
    assert done == chosen.keys(), chosen.keys() - done
    assert len(records) == len({(r["file_path"], r["id"]) for r in records}) == 527
    base.save(OUTPUT, dict(translation_policy="natural-dialogue-v2", target_locale="en-US",
        source_packet=str(SOURCE), source_packet_sha256=SOURCE_SHA, previous_sha256=release["candidate_sha256"],
        previous_registry_sha256=release["registry_sha256"], clean_input_sha256=release["clean_input_sha256"],
        formatting_and_registration_pending=True, additional_review_credit=0, records=records))
    print(binder.binder.Counter((r["kind"], r["decision"]) for r in records))


if __name__ == "__main__":
    main()



