"""Review Maria's ghost ship and naval alliances, with the queued opening wraps."""

from collections import Counter
from pathlib import Path

from scripts import register_maria_opening_hodram_wraps_20261122 as parent
from scripts import review_maria_B18_B20_20261122 as established


base,native=parent.base,parent.native
ROOT=Path("work/analysis/maria_B21_B32_followup_20261122")
PAIR=ROOT/"paired_source_registered_candidate.json"
EARLY=ROOT/"B21_B25_contextual_v1.json"
FOLLOW=parent.writer.review.ROOT/"maria_phrase_followups_v1.json"
FOLLOW_VISUAL=FOLLOW.with_name("maria_phrase_followups_visual_review.json")
PACKET,MANUSCRIPT,PLANS=[ROOT/name for name in ("combined_paired_source_v1.json","combined_manuscript_v1.json","combined_preflight_v1.json")]
CARRIED_BLOCKS=(0,14,17)
BLOCKS=((),(),(),(*CARRIED_BLOCKS,*range(21,33)))
ARCHIVE=established.ARCHIVE
CONTEXTS={
 26:"Defeated Hernan blusters that he let Maria win. She says the Athens guild will take him into custody and warns him against trying anything.",
 27:"The enemy disappears after the encounter. Xien, Ian and Manuel have distinct reactions across the possible speaker conditions. Maria cannot explain what she saw and sends the crew back to the Havana guild.",
 28:"The opponent addresses Maria by her epithet and threatens her with his iron-armored fleet. Xien addresses the fleet as a whole, Richard reacts in a separate branch, and Maria recognizes the iron cladding.",
 29:"Clifford's betrayal leaves Lil surrounded. The original player choice decides whether Maria intervenes. Across the intervention variants, Maria calls out the attackers, Lil bristles at being rescued, Camille asks for help, and the attacker turns his attention to the newcomers. The withdrawal variant gives Maria and Julian distinct closing replies.",
 30:"Clifford reveals why he used Maria's company and threatens her after they exceeded the role he gave them. Lil arrives to repay her debt and challenges him herself, prompting his patronizing warning.",
 31:"Kuhn sends an impostor fleet to attack Lil. Maria realizes the deception and joins the rescue. Camille and Hodram arrive, Lil apologizes, and Kuhn orders a retreat when his plan fails.",
 32:"Seven physical lookout replies share eight personality slots. Some identify the probable target and others only report an unusual ship. Maria reacts before the scene identifies it further.",
}
DECISIONS={
26:"""
8||Hernan stammers and insists he lost on purpose. The familiar boast follows his earlier confidence.
11|I'm turning you over to the guild in Athens. Try anything, and I make no promises about what happens to you.|Maria names who will take custody and says his life is at risk if he tries anything. Her warning stays measured.
""",
27:"""
5||Maria asks where the enemy ship went. The short question belongs to the sudden disappearance.
9||Xien's one-word reply leaves him sounding stunned.
13||Maria is unsure whether the disappearance means they won. Her question and pause carry that doubt.
23|Was that... really a ghost ship?|Xien gropes for an explanation. His hesitation works better in plain spoken language.
28||Ian asks the same question more formally than Xien. The measured existing wording works in his branch.
34|I don't know. I'm not usually superstitious, but what we just saw... I don't think we imagined it.|Maria leaves the identification open. She doubts that the sight can be dismissed as a mistake, and the pause keeps her shaken delivery.
44|Hmm. I can't make sense of it. I suppose we'll never know what it was.|Xien is puzzled and leaves the ship's identity unknown. His reply sounds like his conclusion to a conversation.
49||Manuel marvels at strange things and agrees the identity remains a mystery. His calm conclusion suits this alternate voice.
55||Maria sets the mystery aside, declares the assignment finished and names the Havana guild as their next stop.
""",
28:"""
5||Keep the approved Soaring Scarlet Orca epithet and the original surname substitution in the opening taunt.
8|Today's the day you die! You'll see what my iron-armored ships can do!|The challenger threatens Maria directly and boasts about the power of his iron-armored ships.
11||Xien reacts to the whole approaching fleet. Keep the distinction from Richard's question about a single ship.
22||Richard stammers over the sight of one unfamiliar ship. The clipped question captures his surprise.
31|Those ships... are they clad in iron?!|Maria recognizes iron plating but is still surprised enough to ask the question.
""",
29:"""
5||Maria's silent start belongs to the sudden attack.
9||Lil cries out before Camille asks how she is. Keep the sustained scream.
13||Camille calls Lil by name and checks on her immediately.
17|Clifford! How dare he turn on me?!|Lil names the man who betrayed her. The short outburst keeps her anger and personal sense of betrayal.
20|Ha ha ha! Give up already, little girl!|The attacker laughs and patronizes Lil while telling her to surrender. The taunt carries his condescension without giving her a new age or title.
23||Lil's blunt refusal answers his demand and suits her temper.
27||Camille says they're surrounded and cannot escape. His alarm has a concrete cause.
30||Lil curses when they run out of options.
SC3_B29_CHOICE_304_0||This choice commits Maria to helping the people under attack and reads as a direct action.
SC3_B29_CHOICE_304_1||This choice leaves the fight rather than intervening. Its wording matches Maria's withdrawal line.
45||Maria interrupts the attack before identifying herself.
49||The attacker reacts to a stranger intervening. The question is abrupt.
53|Does it matter? Hey, you there!|Maria dismisses the question of her identity, then singles someone out. The first beat sounds like a comeback.
56||The attacker initially wonders if Maria means him. Keep his short reply before her reprimand.
60||Maria rebukes grown men for ganging up on a girl. Her understatement keeps her control of the exchange.
72|Exactly. That's low. A man ought to treat women kindly. That's how a man should act.|Julian backs Maria up and makes the source's self-important declaration about gentlemanly behavior. Keep the final observation as part of his voice.
79|Huh?! Shut up! This is none of your business. If you don't know what's going on, stay out of it!|The attacker snaps at the newcomers and says people who do not know the situation should keep out.
88|I don't back down just because someone says so. Especially when a brute is picking on a helpless girl.|Maria refuses to leave. Her description sets up Lil's objection to being called helpless. The source refers to the brute and the girl's predicament.
91|W-wait. Did you just call me helpless?|Lil stammers as she interrupts and takes offense at Maria's exact word. Keep that callback.
94|You don't look all that tough from where I'm standing.|Maria judges how Lil looks in the immediate situation. The teasing reply leaves Lil room to object.
97||Lil starts to concede the point, then tries to defend herself before Camille cuts in.
100|Lil, not now! Don't pick a fight with someone offering to help us! Please, we need your help!|Camille switches from admonishing Lil to pleading with Maria. Both audiences and the urgency stay clear.
103||Lil objects that Camille has taken it upon himself to decide for her. Her irritation remains aimed at his interference.
107|Dunno what's going on, but this dull little rabbit hunt just turned up some tempting prey. Think I'll help myself!|The attacker uses hunting imagery and a predatory threat as he turns his attention to Maria. Keep the rough register and the new object of his interest.
111||This branch repeats Maria's refusal to be ordered out. Keep its separate entry and forceful delivery.
115||Lil recognizes Maria and calls her by the original given-name substitution.
119|With FI on our side, we're as good as a hundred strong!|Camille's confidence jumps when Maria joins. Keep the Japanese comparison to a hundred people as a boast and preserve the given-name substitution.
123|Tch. Dunno what's going on, but this dull little rabbit hunt just turned up some tempting prey.|The alternate branch uses the same hunting threat in its own first speech, before the speaker continues in the next panel.
127||The separate follow-up completes the attacker's threat. Preserve the division into two turns.
134||Lil reacts sharply to the predatory remark and demands to know what he means.
138||Maria warns that the attackers are coming. Keep the immediate call.
153||Maria says the fight is none of their business and orders the fleet to leave. The short pair matches the withdrawal choice.
164||Julian can scarcely believe Maria is leaving. Keep the stammer and trailing dismay.
""",
30:"""
5||Clifford greets the unexpected arrival with a short, knowing exclamation.
9||Maria immediately recognizes Clifford. Her surprised question needs no exposition.
13||Clifford gives Richard credit before saying he was outmatched. His phrasing acknowledges the work without changing the result.
16||Maria waits before Clifford discloses his scheme. Keep the silence.
20|Your job was to get the Ming government to drop that ridiculous policy of closing itself off. You did even better than I'd hoped.|Clifford says he assigned them to end the Ming government's policy of isolation. His smug praise makes it clear they exceeded his expectations.
23||Maria gives Clifford one short chance to finish. Her pause makes the challenge colder.
27|Richard was right about you. Beautiful, quick-tempered, and stubborn. In any case, you've meddled enough.|Clifford repeats Richard's description and says she has overstepped. Keep the distinct judgments of temperament and stubbornness.
30|What a waste. I'm going to have to kill you.|Clifford expresses regret before calmly announcing what he will do. The threat is personal and explicit in the source.
74||Lil calls out Maria's family name through the original substitution to announce her arrival.
78||Maria reacts with surprise before Lil explains.
82|I'm on your side whether you asked me or not! I can't stand owing anybody a favor!|Lil joins the fight on her own initiative and explains her debt. The affectionate defiance recalls Maria's earlier help without claiming a financial debt.
85||Clifford recognizes the Argot Company in surprise. Keep the approved faction name.
89|Clifford! Get ready for a fight!|Lil calls Clifford out with a direct threat of confrontation. The abrupt challenge follows her decision to intervene.
92||Clifford complains about the troublesome young woman and uses the source's fire warning. The established proverb fits his patronizing tone.
""",
31:"""
5||Lil is startled by the sudden attack and asks what is happening. The short cries fit the surprise.
8|Ships from FO have opened fire!|The sailor identifies the fleet by the original company substitution. The wording remains natural if the company calls itself a fleet.
11||Lil repeats the identified company and takes it as proof of Kuhn's claim. Keep the substitution and her sudden conclusion.
15|What is going on? We're not the ones attacking Lil! Whose fleet is that?|Maria denies responsibility for the attack and asks about the unidentified fleet. She knows Lil is under attack but has not yet identified the impostor.
18||Xien explains that Kuhn sent impostors to attack the Argot Company under Maria's colors. Keep both factions and the deception.
21||Maria connects the disguise with Kuhn's motives and calls for immediate help. The recognizable true-colors idiom fits this situation.
25||Xien interrupts with a stammer when another fleet approaches. He is still identifying it at the end of the line.
30||Hodram thinks they arrived in time. His quiet assessment precedes Camille's shout.
34||Camille draws out Lil's name as he calls to her. Keep the urgency of the shout.
38||Lil recognizes Camille and Hodram in turn, then asks why they are there. Preserve her surprise at both people.
42|FI told me you were in danger! It's Kuhn's fleet in disguise. They're the ones attacking you!|Camille credits Maria for the warning and explains that the attackers belong to Kuhn. Keep the given-name substitution and the overt correction.
45||Lil reacts in disbelief before Maria confirms the deceit.
49|Now you know what Kuhn's really like! We're joining the fight, too!|Maria answers Lil's shock by exposing Kuhn's character and says her own fleet will help as well.
52||Lil addresses Maria by name, admits her own mistake and apologizes. Her stammer carries embarrassment rather than a new confession.
56|It's all right. I'm glad we got here in time. Come on. Let's take down Kuhn!|Maria accepts the apology and is relieved it is not too late. Her final rally calls the group to deal with Kuhn.
60||Hodram calls the fleet into action and orders battle stations. The two familiar commands already sound natural.
63|Damn it. The plan failed!|Kuhn sees that his scheme did not work. The short, irritated realization leads to his aide's warning.
67||The subordinate addresses Kuhn respectfully and says the situation puts them at a disadvantage. The existing Sir adds no formal rank.
71|I know that! Damn it, we're pulling out!|Kuhn angrily says he knows they are at a disadvantage, then orders retreat in his own sharp voice.
""",
32:"""
SC3_B32_STYLE_8_0||Two styles share the measured report that this looks like the ship they were looking for. Preserve both aliases and its uncertainty.
SC3_B32_STYLE_8_28||The more excited voice sees a strange ship and guesses it could be the one. Keep both observations and the tentative link.
SC3_B32_STYLE_8_68||This lookout reports a strange ship at a distance without making the further identification. Her exclamation fits.
SC3_B32_STYLE_8_94||The rougher voice calls it weird. The informal wording distinguishes it from the measured lookouts.
SC3_B32_STYLE_8_120||The clipped sighting suits this voice and names only an odd ship.
SC3_B32_STYLE_8_150||The drawn-out Admiral call and excited report preserve the youthful delivery.
SC3_B32_STYLE_8_182||The formal lookout says he sighted an unusual ship without claiming to know which one it is.
24||Maria starts to recognize what she sees and falters. The unfinished question does not announce the answer early.
""",
}


def make_records(packet):
    first=base.load(EARLY)
    assert first["candidate_sha256"]==packet["candidate_sha256"]
    assert first["source_packet_sha256"]==base.digest(PAIR)
    early={r["id"]:r for r in first["records"]}
    history={r["id"]:r for r in base.load(established.HISTORICAL)["records"]}
    rows=[]
    for group in packet["groups"]:
        block=group["block"]
        decisions={i:(wording,note) for i,wording,note in
                   (line.split("|",2) for line in DECISIONS.get(block,"").strip().splitlines())}
        for pair in group["records"]:
            ident,selector=pair["id"],pair["selector"]
            if block<=25:
                old=early.pop(ident)
                assert all(old[k]==v for k,v in pair.items())
                rows.append(old|{"change_class":"wording" if old["decision"]=="revision" else "retention"})
                continue
            old=history[ident]
            word=pair["native_command_word"]
            kind={0x4000:"progressive",0x4100:"actor-style",0x2100:"typed-choice-label"}[word]
            key=str(int(ident.rsplit("R",1)[1])) if word==0x4000 else ident
            english,note=decisions.pop(key)
            if ident=="DK4_MES_B26_R0011":
                english="I'm turning you over to the guild in Athens. Try anything, and I can't promise you'll make it out alive."
            now=" ".join(pair["current_English"].split())
            prefix=f"{selector:02x}" if word==0x4000 else ""
            source=prefix+pair["source_reference"]["exact_body_hex"]
            current=prefix+pair["current_reference"]["exact_body_hex"]
            assert old["source_hex"]==source and all(old["review"].values())
            assert old["source_reference"]["offset"]==pair["source_reference"]["offset"]
            assert not english or (english!=now and word==0x4000)
            rows.append(pair|dict(route=3,kind=kind,speaker=old["speaker"],source_selector=selector,
                native_slots=pair["slots"],source_hex=source,current_hex=current,previous_English=now,english=english or now,
                protected_phrases=[],source_meaning=note,context=CONTEXTS[block],localization_note=note,
                decision="revision" if english else "retention",change_class="wording" if english else "retention",
                review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False)))
        assert not decisions
    assert not early and len(rows)==112
    return rows


def opening_fixes():
    proposals,visible,registered=map(base.load,(FOLLOW,FOLLOW_VISUAL,parent.REVIEW))
    assert proposals["candidate_sha256"]==registered["candidate_sha256"]==base.digest(parent.ROM)
    assert proposals["review_sha256"]==base.digest(parent.REVIEW)
    assert visible=={row["path"]:row["sha256"] for row in proposals["sheets"]}
    assert all(base.digest(p)==h for p,h in visible.items())
    pairs=parent.writer.review.maria_packet.__globals__
    from inspect import getsource
    from scripts.source_locked_derivation_v5118 import checked_text
    source=checked_text(getsource(parent.writer.review.maria_packet),
                        {'return scope["source_and_current"](parent,range(18))':
                         'return scope["source_and_current"](parent,CARRIED_BLOCKS)'})
    env=pairs|{"parent":parent,"CARRIED_BLOCKS":CARRIED_BLOCKS}
    exec(compile(source,__file__+"::opening-pairs","exec"),env)
    groups=env["maria_packet"]()["groups"]
    changes={r["id"]:r for r in proposals["records"]}
    previous={r["id"]:r for r in registered["records"] if r["route"]==3 and r["block"] in CARRIED_BLOCKS}
    rows,plans=[],{}
    for group in groups:
        for pair in group["records"]:
            ident=pair["id"]
            row=previous.pop(ident)
            ref=row["registered_reference"]
            assert row["source_reference"]==pair["source_reference"] and all(row["review"].values())
            assert all(pair["current_reference"][k]==ref[k] for k in ("archive_sha256","block_sha256","command_offset","offset"))
            assert ref["exact_stored_hex"]==f'{pair["selector"]:02x}'+pair["current_reference"]["exact_body_hex"]
            old=row["english"]
            proposal=changes.pop(ident,None)
            if proposal:
                assert proposal["registered_reference"]==ref and proposal["current_English"]==old
                plans[ident]=proposal["native_layout_preflight"]
            english=proposal["proposed_English"] if proposal else old
            rows.append(pair|dict(route=3,kind=row["kind"],speaker=row["speaker"],source_selector=row["source_selector"],
                native_slots=row["native_slots"],source_hex=row["source_hex"],current_hex=ref["exact_stored_hex"],
                previous_English=old,english=english,protected_phrases=proposal["protected_phrases"] if proposal else [],
                source_meaning=row["source_meaning"],context=row["context"],
                localization_note=proposal["reason"] if proposal else row["localization_note"],
                previous_registered_reference=ref,decision_carried=not proposal,
                decision="revision" if proposal else "retention",
                change_class=("wording" if english!=old else "wrap-only") if proposal else "retention",
                review=row["review"]|{"formatting":not bool(proposal)}))
    assert not changes and not previous and len(rows)==20 and len(plans)==4
    return groups,rows,plans


def main():
    assert not any(p.exists() for p in (PACKET,MANUSCRIPT,PLANS))
    paired,release=map(base.load,(PAIR,parent.RELEASE))
    assert paired["candidate_sha256"]==release["candidate_sha256"]==base.digest(parent.ROM)
    assert paired["release_proof_sha256"]==base.digest(parent.RELEASE)
    assert release["registry_sha256"]==base.digest(base.REGISTRY)
    rows=make_records(paired)
    groups,opening,expected=opening_fixes()
    all_rows=opening+rows
    plans=established.preflight(all_rows)
    assert all(plans[i]["encoded_hex"]==q["encoded_hex"] for i,q in expected.items())
    base.save(PACKET,paired|{"groups":groups+paired["groups"]})
    labels={}
    for row in all_rows:
        if row["kind"]=="progressive":
            assert labels.setdefault(row["source_selector"],row["speaker"])==row["speaker"]
    findings=dict(Counter(r["change_class"] for r in all_rows))
    base.save(MANUSCRIPT,dict(translation_policy="natural-dialogue-v2",target_locale="en-US",encoder="dialogue-relocatable-v1",
        previous_sha256=release["candidate_sha256"],previous_registry_sha256=release["registry_sha256"],planned_FE={},
        source_packet=str(PACKET),source_packet_sha256=base.digest(PACKET),records=all_rows,findings=findings,
        Maria_names_and_roles=labels,contextual_records_revisited=116,contextual_decisions_reused=16,
        new_editorial_credit=0,evidence={str(p):base.digest(p) for p in (PAIR,EARLY,FOLLOW,FOLLOW_VISUAL,established.HISTORICAL)},
        status="Contextual records compared and layouts planned. Stored, visual and gameplay review pending."))
    base.save(PLANS,dict(candidate_sha256=release["candidate_sha256"],draft_sha256=base.digest(MANUSCRIPT),plans=plans))
    print(findings, "across",len(all_rows),"exact records and four opening wrap fixes.")


if __name__=="__main__":
    main()

