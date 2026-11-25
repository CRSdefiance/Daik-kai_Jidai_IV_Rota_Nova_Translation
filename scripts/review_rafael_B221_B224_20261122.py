"""Review Yukihisa's letter, the sword rumor, the swans, and the Three Kingdoms exchange."""

from collections import Counter
from types import FunctionType

from scripts import pair_rafael_B221_B240_20261122 as paired
from scripts import review_rafael_B177_B180_20261121 as precedent


base = paired.base
OUTPUT = paired.ROOT / "contextual_decisions_B221_B224_v4.json"
DECISIONS = {
    221: """
STYLE_8_0|||The crew member announces Yukihisa's letter and addresses the admiral directly. The concise delivery suits this voice.
STYLE_8_42|||Keep the more formal acknowledgment of a letter received. Preserve the distinction from the quicker announcements.
STYLE_8_84|||The same natural announcement serves the two original alias slots. Both point to the same stored body.
STYLE_8_122|Admiral, a letter for you from Yukihisa.|from Yukihisa.|Keep the polite wording in this distinct voice and keep the writer's name attached to the delivery.
STYLE_8_168|||You've got a letter gives this announcement the source's rougher, more familiar delivery.
STYLE_8_206|Here's a letter from Yukihisa, Admiral.|from Yukihisa, Admiral.|Keep the direct announcement and address in this voice and let the writer's name stay with the letter.
STYLE_8_244|||The excited summons and short announcement suit the source's lively voice.
27|I hear the fabled Muramasa blades are marked for destruction. They say the curse brings bad luck to Tokugawa, Japan's ruler.|the fabled Muramasa blades;marked for destruction.;the curse brings bad luck;Tokugawa, Japan's ruler.|Yukihisa writes formally about a rumor. Keep the famous blades, their reputation as Tokugawa's bane, his position and the attempt to destroy them.
30|A clan that bears Tokugawa a grudge seems to have hidden one blade somewhere in East Asia. I thought you should have word of it.|bears Tokugawa a grudge;somewhere in East Asia;you should have word of it.|Yukihisa says one blade appears to have been concealed by a clan with a grievance. The region is broad and the report is tentative.
33|||Keep Yukihisa's certainty that this is the blade he has sought for years and preserve the separate signed name.
STYLE_702_0|Not an easy read, is it? That's Yukihisa for you.|Not an easy read, is it?;That's Yukihisa for you.|The speaker shares their difficulty with the letter and gently recognizes Yukihisa's familiar style.
STYLE_702_38|||Keep the relatively formal judgment and the distinct brief comment on Yukihisa's personality.
STYLE_702_70|That was a tough read, huh? Just like Yukihisa.|That was a tough read, huh?;Just like Yukihisa.|The speaker uses a casual question tag and follows it with a familiar aside about Yukihisa.
STYLE_702_106|Hard to read, isn't it? It sounds just like Yukihisa.|Hard to read, isn't it?;It sounds just like Yukihisa.|Keep the gentler delivery and the recognition that the style sounds like Yukihisa.
STYLE_702_144|||Keep the rougher complaint that Yukihisa made it hard to read and the familiar final aside.
STYLE_702_188|||Keep the older voice's measured, colloquial judgment in both sentences.
STYLE_702_226|||This reply simply says the letter is too difficult to understand. It stays distinct from the variants that identify Yukihisa's style.
STYLE_702_270|||This more formal voice emphasizes that the difficulty is characteristic of Yukihisa. Keep the distinct emphasis.
65|||Jam has the same complaint in his own established voice. His quick second sentence keeps the teasing familiar.
71|||Rafael is interested and says the lead is worth pursuing. The promise stays at the level of looking for it.
""",
    222: """
5|||Al Shin asks for the admiral's attention and announces a lead. The urgency fits his eagerness to tell the story.
8|||Al Shin reports what he heard about a lord and a very sharp sword. Keep the rumor qualified.
11|||Rafael's brief response is intrigued and approving before he hears the unsettling part.
16|They say the blade is faintly red, like it's seen plenty of blood.|the blade is faintly red,;seen plenty of blood.|Al Shin repeats a description of the tint and the impression it gives. The line does not establish the blade's actual history.
20|||Rafael echoes the sword's color and considers the unusual detail.
25|||Al Shin retells the rumor that the lord feared the blade and sealed it away unused. Keep the separate judgment, delivered as his own insult.
28|But it's a fine sword, right? Seems like a waste to me.|But it's a fine sword, right?;Seems like a waste to me.|Rafael calls the blade good, checks that assessment with Al Shin, and regrets that it was put away.
32|||Al Shin calls the lord a fool and follows with a sarcastic question. His bluntness contrasts with Rafael's curiosity.
36|Seems like there's a story there. Where do you think he hid it?|there's a story there.;Where do you think he hid it?|Rafael agrees that the blade has a strange reputation and asks where it was hidden. Let the full location question land together.
40|||Al Shin admits he has no location and proposes searching if they get the chance.
""",
    223: """
5|||Cristina pauses to admire the square and gradually notices something in the little pond.
9|||A short speakerless swan call interrupts her first thought. Preserve the original distinction from Cristina's speech.
13|||Cristina recognizes the two swans and addresses them as fellow travelers. Her wondering tone keeps the comparison light.
17|||Preserve the original four calls and their cadence within the speakerless panel.
21|||Cristina chuckles and admits a little envy at the birds' closeness. No relationship between human characters is stated.
24|||The wingbeats mark the pair's departure and cue Cristina's alarm in the next panel.
28|Oh! Where are you off to? Wait, they're carrying something!|Where are you off to?;they're carrying something!|Cristina follows the swans with her eyes and spots that they are carrying something. Preserve the progression from question to surprise.
32|||Cristina starts identifying the direction before the exchange turns to Rafael.
36|||Rafael gets her attention with the established Cristina spelling.
40|Oh, Admiral FI! There was a pair of swans!|Admiral FI!;There was a pair of swans!|Cristina addresses the admiral with the original given-name substitution and eagerly tells him what she saw.
43|Really? In the square's pond? They must be used to people.|In the square's pond?;They must be used to people.|Rafael repeats the location in surprise and makes his own inference about how familiar the swans are with people.
47|||Cristina mentions the object's shape and shine, gives a tentative location near Amsterdam and asks whether Rafael wants to look.
""",
    224: """
5|||The guildmaster opens briskly by asking whether the group knows the novel. Keep the full approved title.
64_0|||The first caption tells him the player knows the book and leads to a question about favorite generals.
64_1|||The second caption says the player doesn't know the book and leads to his reading recommendation.
22|||The guildmaster recommends the novel in a friendly way on the unfamiliarity path and says it is enjoyable.
32|Oh, you do? I'm glad to hear it. Who's your favorite general?|Who's your favorite general?|He's delighted to meet someone who knows the novel. The next question invites the choice of a general.
242_0|||The first general's name remains Zhao Yun, the choice that leads to the guildmaster's own favorite and the spear rumor.
242_1|||The second general's name remains Guan Yu. Keep its distinct response branch.
242_2|||The third strategist's name remains Zhuge Liang, with the same name in his response.
51|||The guildmaster exclaims that Zhao Yun is his favorite too and expects that they will get along.
54|At Changban Bridge, he holds A Dou to his chest and rides straight through Cao Cao's army alone. That's my favorite part!|At Changban Bridge,;Cao Cao's army alone.;That's my favorite part!|The fan recalls his favorite moment in the novel. Preserve the bridge, A Dou, the enemy army and the lone ride.
58|||The guildmaster identifies the possible spear, qualifies the claim as a rumor, and limits the clue to a nearby peninsula.
62|I wanted it myself. I looked high and low and never found it. I thought you might have better luck.|looked high and low;never found it.;better luck.|He explains his own unsuccessful search and offers the group a reason to try without guaranteeing success.
72|||Keep the praise for Guan Yu's beard, bravery and cleverness, even though he isn't this reader's favorite.
78|Ah, Zhuge Liang, the strategist. His Memorial on the Expedition can bring you to tears, can't it? He's probably my second favorite.|Memorial on the Expedition;can't it?;my second favorite.|The admirer keeps the title of the memorial, its emotional effect and his tentative second-place ranking.
""",
}


def main():
    packet, release = map(base.load, (paired.PAIRED, paired.parent.RELEASE))
    assert packet["release_proof_sha256"] == base.digest(paired.parent.RELEASE)
    assert packet["candidate_sha256"] == base.digest(paired.parent.ROM)
    names = {row["actor_ID"]: row["progressive_nameplate"] for row in
             base.load(precedent.prior.CATALOGUE)["source_and_current_default_name_fields"]}
    names[208] = "Runtime-selected crew voice"
    normalize = FunctionType(precedent.normalize.__code__, precedent.normalize.__globals__ | {"WRAPS": {}})
    records = []
    for group in packet["groups"]:
        block = group["block"]
        if block not in DECISIONS:
            continue
        decisions = [line.split("|", 3) for line in DECISIONS[block].strip().splitlines()]
        for row, (key, replacement, protected, note) in zip(group["records"], decisions, strict=True):
            ident = row["id"].removeprefix(f"SC0_B{block}_").removeprefix(f"DK4_MES_B{block}_")
            expected = ident.removeprefix("CHOICE_") if row["selector"] is None else ident
            if expected.startswith("R"):
                expected = str(int(expected[1:]))
            assert key == expected and note
            old = " ".join(row["current_English"].split())
            english = replacement or old
            phrases = protected.split(";") if protected else []
            assert all(phrase in english for phrase in phrases)
            entry = normalize(row | dict(previous_English=old, english=english,
                protected_phrases=phrases, localization_note=note,
                decision="revision" if english != old else "retention",
                review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False)), names)
            entry["contextual_speaker"] = row["earlier_speaker"]
            if row["native_command_word"] == 0x4100:
                entry.update(kind="actor-style", speaker="Runtime-selected crew voice",
                    source_hex=row["source_reference"]["exact_body_hex"], current_hex=row["current_reference"]["exact_body_hex"])
            records.append(entry)
    assert len(records) == 56 and len({row["id"] for row in records}) == 56
    assert sum(row["kind"] == "actor-style" for row in records) == 15
    assert sum(row["kind"] == "typed-choice-label" for row in records) == 5
    assert not OUTPUT.exists()
    counts = Counter(row["change_class"] for row in records)
    base.save(OUTPUT, dict(translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1", target_locale="en-US",
        review_gates=["source", "context", "localization", "naturalness", "formatting"],
        previous_sha256=packet["candidate_sha256"], previous_registry_sha256=release["registry_sha256"],
        source_packet=str(paired.PAIRED), source_packet_sha256=base.digest(paired.PAIRED),
        records=records, findings=dict(counts), new_editorial_credit=0,
        status="Contextual review complete. Stored formatting, gameplay and release checks pending."))
    print(f"Reviewed {len(records)} records. {dict(counts)}")


if __name__ == "__main__":
    main()
