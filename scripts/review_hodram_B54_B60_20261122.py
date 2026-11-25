"""Review Sera's first words and the linked Espinosa and Sao Jorge scenes."""

from inspect import getsource
from types import SimpleNamespace

from scripts import register_hodram_B0_B23_20261122 as parent
from scripts import review_hodram_opening_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, native = parent.base, parent.native
ROOT = parent.writer.author.ROOT.with_name("hodram_B54_B70_followup_20261122")
SCOPE = tuple(range(54, 61))
paired = SimpleNamespace(PACKET=ROOT / "B54_B60_exact_current.json", CARRY=ROOT / "B54_B60_carried_decisions.json")
OUTPUT = ROOT / "B54_B60_contextual_v3.json"
ARCHIVE = "/data/SC1.DK4"

CONTEXTS = {
    54: "A local asks if Hodram is new in town, then laughs at his own encouragement. Hodram is left puzzled.",
    55: "The port worker recognizes Hodram as the officer he heard about and relays the Veracruz guildmaster's request.",
    56: "After the captives have a chance to leave, Hodram asks what the unidentified girl will do and proposes that the town look after her.",
    57: "Sera haltingly thanks Hodram with the few words she has learned. His surprise gives way to warmth and embarrassment.",
    58: "Espinosa's victims confront him. Sera's halting testimony leads to his admission, then Hodram leaves the decision to the townspeople. His exchange with Sera is followed by a request about a legendary weapon.",
    59: "The requester verifies the returned weapon, hands over Espinosa's map fragment, and links the search to his hopes for the region. Hodram accepts with reservations.",
    60: "Manuel explains why Sao Jorge is his second home, linking the townspeople's kindness and his faith to his pledge to fight slavers.",
}
DECISIONS = {
    54: """
6|||The local's casual question immediately marks Hodram as a newcomer.
10|||Hodram is surprised to be asked and confirms it without explaining himself.
18|?|?|Hodram's wordless puzzlement follows the man's laugh. Use the same regular question glyph as neighboring English dialogue.
""",
    55: """
6|You're that officer, FA, right? The guildmaster in Veracruz was asking for you.|The guildmaster in Veracruz;was asking for you.|The worker tentatively recognizes the officer by his surname and relays who was asking for him, with the original city.
""",
    56: """
7|||Hodram asks what the girl wants to do and whether she will go with the others. The two questions leave her the choice.
10|||The silent panel keeps her unidentified. Foreign Girl is the established caption tied to Hodram's perspective before he knows her name.
13|I see. You aren't from the same people as the other captives. The town can look after you for a while.|the other captives.;look after you for a while.|Hodram distinguishes her background from the other captives' and proposes temporary care in this town.
""",
    57: """
7|||Sera hesitates before speaking Hodram's given name. Preserve her small opening sound and the substitution.
11|||Hodram responds to his name and invites her to continue.
15|||The pauses in her first thank-you let the player hear how carefully she is putting the words together.
19|You can speak... Did you learn our language?|our language?|Hodram is startled to hear her speak intelligibly, then asks whether she has learned their language.
23|(Nods.) ...A little.|A little.|Keep both the nod and the halting admission that she knows only a little.
27|||Hodram's brief approval follows her modest answer. The line sounds natural and does not assume fluency.
31|||She repeats his name and the same hesitant thanks. Retain the pauses that link it to her first attempt.
35|A-ah... Don't mention it.|Don't mention it.|His small stammer and understated answer preserve his embarrassment and kindness.
""",
    58: """
6|||Espinosa stammers when the townspeople seize him. His frightened question starts the argument.
10|||The townsman's abrupt order pulls him into view without an invented threat.
14|||Hodram recognizes Espinosa with surprise. This line identifies him for the player.
18|Admiral FA! You beat the scoundrel. Thank you!|Admiral FA!;You beat the scoundrel.|The townsman addresses Hodram respectfully by his surname and thanks him for defeating Espinosa.
21|||Espinosa tries to intimidate them even as he stammers and loses control of the situation.
24|||The townsman cuts him off with the short, rough order.
28|Gah! I-it hurts!|I-it hurts!|Espinosa cries out and stammers in pain. Keep the reactiveness distinct from his earlier threat.
32|You've done whatever you pleased for long enough!|for long enough!|The townsman accuses Espinosa of a long history of doing as he likes.
35|||Espinosa stammers a denial by asking what the accusation is about.
39|Don't tell me you've forgotten! You swindled my father out of his home and farmland. Now my whole family's missing!|home and farmland.;my whole family's missing!|The townsman accuses him of taking his father's house and farmland by deception. His family is missing, with no claim that he knows their fate.
42|My friend tried to report your crimes back home. You killed them and made it look like an accident!|your crimes back home.;like an accident!|The witness says Espinosa killed a friend who meant to report the wrongdoing to the home country and disguised the death as an accident.
46|They took so many from my village. They make them work all over with barely a bite to eat!|from my village.;barely a bite to eat!|The woman accuses him of taking many villagers from her home and making them work with little food in several places.
58|||Manuel calls Espinosa a devil wearing a human guise. The existing image and quiet delivery fit his reaction.
64|I-I didn't know! My idiot underlings did it all on their own!|did it all on their own!|Espinosa pleads ignorance and blames his own subordinates.
68|Y-you bastard...!|Y-you bastard...!|The townsman stammers in anger after Espinosa puts the blame on others.
80|Rotten to the core... No reason to go easy on him.|Rotten to the core...;No reason to go easy on him.|This speaker sees no mitigating reason to show Espinosa leniency. Keep the contempt in the first phrase.
93|||Hodram sets the others aside and asks Sera a direct question about recognizing Espinosa.
97|||Sera's brief affirmative follows a pause. She answers without suddenly becoming fluent.
101|||The stammered recognition shows Espinosa is startled that she is here.
105|This man... He said sell me. High price. Send me... to his country.|He said sell me.;High price.;to his country.|Sera says he ordered them to send her to his country so she could be sold for a high price. Preserve her deliberate, limited speech.
108|||Espinosa can barely answer her first accusation.
112|||Hodram's silent response leaves Sera space to continue and Espinosa room to protest.
116|Wait! You've got the wrong man! She's making it up!|You've got the wrong man!;She's making it up!|Espinosa claims mistaken identity and calls the accusation fabricated.
120|This man... My little brother... the others... He killed them all! This man!|My little brother...;He killed them all!|Sera names her younger brother and the people with her as those Espinosa killed. Her broken phrases and repetition retain the emotion.
124|||Under pressure Espinosa admits what he did by saying he should have killed Sera along with the others. Keep the stammer and cutoff.
127|||Hodram concludes there is no plausible denial left. The existing quiet verdict fits his response to the admission.
137|You monster! Admiral FA, what will you do with him?|Admiral FA,;what will you do with him?|The townsman calls Espinosa inhuman and asks the admiral by surname how he will handle him.
141|I'll leave that decision to you.|leave that decision to you.|Hodram lets the people confronting Espinosa decide how to deal with him.
145|You heard him! Move! You'll pay for what you've done!|You heard him!;You'll pay for what you've done!|The townsman takes charge and promises to make Espinosa answer for his deeds. No specific punishment is supplied.
148|||Espinosa stammers as he begs for help, completing his fall from threats to pleading.
152|||Hodram remains silent as the townspeople take Espinosa away.
164|||Sera's silence follows the confrontation. Preserve the pause before Hodram addresses her.
168|Remember this, Sera. Even now, Westerners like him throw their weight around all over the world.|Remember this, Sera.;throw their weight around;all over the world.|He tells Sera to remember that people like Espinosa still exercise power widely. The observation leads into his reflection on his own conduct.
175|||Sera answers Hodram's self-doubt with simple words and his given name. Keep the original pauses and substitution.
179|||Hodram tells her not to put excessive trust in people, even after she distinguishes him from Espinosa.
186|Admiral FA.|Admiral FA.|The local addresses Hodram by surname before broaching a new request.
190|I hate to put you to the test, but I need you to find something for me.|put you to the test,;find something for me.|He acknowledges that the request may feel like a test and says he has something he needs them to find.
194|?|?|Hodram reacts silently to the unexpected request. Match the regular English question glyph.
198|Admiral, have you heard the stories about King Solomon?|about King Solomon?|The question asks whether Hodram knows the legends about Solomon.
202|They say that long ago, the great King Solomon could command even the demon king.|the great King Solomon;even the demon king.|Keep the story as legend, retain Solomon as the one wielding power, and keep the artifact's connection to the demon king clear.
206|They say a weapon tied to the demon king was sealed on an icy island, far to the northwest of here.|the demon king;an icy island,;far to the northwest of here.|The weapon's connection to the demon king and the location are rumor. The direction and distance remain explicit.
210|They say only someone worthy to rule can keep it. If you can bring it back...|worthy to rule;can keep it.;If you can bring it back...|The local describes a qualification for possessing the weapon and trails off after setting the condition for its return.
213|If I bring it back, then what?|then what?|Hodram deliberately echoes the condition and asks what follows.
217|||The local promises something in return while keeping what it is undisclosed.
220|||Hodram asks what the item is. The short question follows directly from the promise.
224|I can't tell you yet. You'll find out when you come back safely.|I can't tell you yet.;You'll find out;come back safely.|The local refuses to reveal the gift and keeps the original condition that Hodram return safely.
228|||Hodram mulls over the demon king's weapon. The pause leaves room for Manuel's geographical guess.
""",
    59: """
5|||The local is surprised that they found the object and asks to confirm it.
9|Yes, that's it. In that case, I'll leave this in your hands.|Yes, that's it.;leave this in your hands.|He identifies the returned object and decides to entrust another one to Hodram.
13|||He explicitly offers a piece of the map. The polite wording fits his request.
19|||Hodram asks what he has been given before the local explains Espinosa's connection.
23|Espinosa had it. He'd been after Africa's Proof of Conquest for a long time, too. We prayed he'd never get his hands on it...|Africa's Proof of Conquest;get his hands on it...|The fragment came from Espinosa, whose long search for the Proof worried the townspeople. Keep their hopes in the past.
26|You should rule these waters. May you find the treasure on the map soon and bring this land peace and prosperity.|rule these waters.;on the map soon;this land peace and prosperity.|The local hopes Hodram will find the marked treasure quickly and bring peace and prosperity to the region. Keep both outcomes as wishes and fit the closing thought on one page.
30|That's a lot to ask of me... Still, I'll take it. Thank you.|That's a lot to ask of me...;I'll take it.|Hodram is uneasy about the high expectations and accepts the map fragment graciously.
""",
    60: """
5|Admiral, I can't think of anyone worse than a slave trader.|worse than a slave trader.|Manuel expresses his own strong judgment about slavers, inviting Hodram to hear why.
8|?|?|Hodram's unspoken question leaves Manuel to explain himself. Use the regular question glyph.
12|I was a ship's carpenter with a Portuguese fleet bound for India. We put in at Sao Jorge. An illness was going around. I caught it and had to leave the ship.|a ship's carpenter;Portuguese fleet;bound for India.;at Sao Jorge.;going around.;leave the ship.|Manuel was serving as a ship's carpenter in the fleet bound for India. He stopped at Sao Jorge, caught an illness then going around, and left the ship.
15|The local people saved me. They took such good care of me.|The local people saved me.;good care of me.|Manuel credits his rescue to the residents and warmly remembers their exceptional care.
19|I heard the Portuguese had treated them terribly. But they saw a man who was sick and looked after me like family.|treated them terribly.;like family.|He reports what he heard about their mistreatment and makes clear that they still cared for him as they would for family.
22|||Hodram's quiet acknowledgment lets Manuel continue.
26|That's when the Lord's words, 'Love your neighbor,' truly sank in. This place has been my second home ever since.|'Love your neighbor,';my second home|Manuel connects what he experienced to the quoted commandment and says the town became his second home.
29|I swore that someday I'd fight the slavers who hunt people in Africa.|I swore that someday;hunt people in Africa.|Manuel recalls vowing to oppose the traders who carry out slave raids in Africa.
33|||Manuel urges Hodram to defeat Espinosa. The unqualified commitment follows his account.
36|||Hodram readily agrees. The short answer closes the account and the appeal.
""",
}


def bind_packet():
    original, prior, inherited = [ROOT / name for name in (
        "paired_source_registered_candidate.json", "prior_contextual_decisions.json", "opening_successor_exact_binding.json")]
    packet, carry, receipt, release = map(base.load, (original, prior, inherited, parent.RELEASE))
    assert receipt["successor_sha256"] == release["candidate_sha256"] == base.digest(parent.ROM)
    assert receipt["source_packet_sha256"] == carry["source_packet_sha256"] == base.digest(original)
    assert receipt["prior_contextual_receipt_sha256"] == base.digest(prior)
    assert release["registry_sha256"] == base.digest(base.REGISTRY)
    image = base.NdsImage.open(parent.ROM)
    archive = image.read_file(ARCHIVE)
    current_hash = native.digest(archive)
    blocks = native.IlnkContainer.parse(archive).blocks
    assert current_hash == release["target_SC1_sha256"]
    assert all(native.digest(image.read_file(path)) == digest for path, digest in receipt["verified_unchanged_assets"].items())
    groups = [group for group in packet["groups"] if group["block"] in SCOPE]
    for group in groups:
        block = group["block"]
        assert native.digest(blocks[block]) == group["current_block_sha256"] == receipt["installed_group_hashes"][str(block)]
        group["current_archive_sha256"] = current_hash
        for row in group["records"]:
            row["current_reference"]["archive_sha256"] = current_hash
    candidate = release["candidate_sha256"]
    packet.update(groups=groups, candidate_sha256=candidate, profile=release["profile"], release_proof=str(parent.RELEASE),
                  release_proof_sha256=base.digest(parent.RELEASE), carried_binding=str(inherited), carried_binding_sha256=base.digest(inherited))
    for pool in ("pending_records", "reused_records"):
        carry[pool] = [row for row in carry[pool] if row["block"] in SCOPE]
        for row in carry[pool]:
            row["current_reference"]["archive_sha256"] = current_hash
    assert sum(len(g["records"]) for g in groups) == 82
    assert len(carry["pending_records"]) == 79 and len(carry["reused_records"]) == 3
    if paired.PACKET.exists():
        assert base.load(paired.PACKET) == packet
    else:
        base.save(paired.PACKET, packet)
    carry.update(candidate_sha256=candidate, source_packet=str(paired.PACKET), source_packet_sha256=base.digest(paired.PACKET))
    if paired.CARRY.exists():
        assert base.load(paired.CARRY) == carry
    else:
        base.save(paired.CARRY, carry)


GLYPHS = {"DK4_MES_B54_R0018", "DK4_MES_B58_R0194", "DK4_MES_B60_R0008"}
source = checked_text(getsource(previous.main), {
    "len(records) == 118": "len(records) == 79",
    'change_class="wording" if replacement else "wrap-only" if phrases else "retention"':
        'change_class="glyph" if row["id"] in GLYPHS else "wording" if replacement else "wrap-only" if phrases else "retention"',
})
scope = vars(previous) | globals()
exec(compile(source, __file__ + "::linked-dialogue", "exec"), scope)


if __name__ == "__main__":
    bind_packet()
    scope["main"]()
