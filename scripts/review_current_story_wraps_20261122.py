"""Bind and review current wrap leads against complete early and tutorial exchanges."""

from collections import Counter
from pathlib import Path
from types import FunctionType

from scripts import register_square_rumor_wraps_20261122 as parent
from scripts import scan_current_progressive_wrap_leads_20261111 as scanner
from scripts import stage_late_trade_exchanges_20261118 as layout
from scripts import verify_all_routes_next_phrase_wraps_20261118 as display


base,native = parent.base,parent.native
ROOT = Path("work/analysis/current_story_wraps_20261122")
TRIAGE,REVIEW,PREFLIGHT = (ROOT/n for n in ("current_triage.json","contextual_review.json","native_preflight.json"))
CATALOGUE = Path("translations/editorial_checkpoints/SharedText_20261110_v1/default_actor_names_current_20261120_v1.json")
CONTEXT = {
    (0,42):"Clau wants to fight pirates. His companions react, and Rafael argues for gaining experience in other ports before taking that risk.",
    (0,46):"From the possibility of hostile fleets, the instructor turns to the available sailing actions and explains targets and coastal Search.",
    (0,48):"The crew welcomes a young scholar and his mentor. The older man's assessment, the young man's humility and Clau's teasing play against one another.",
    (0,84):"Clau explains Gerhard's former rank and the seizure of Vels. Gerhard recognizes Clau by his family name, takes over the account and invites Rafael's party inside.",
    (1,3):"Aziza rallies the crew as the rival fleet approaches. She gives Snake, Angel and Dandy separate orders, throws down a challenge and draws a measured reaction from Hodram and Gerhard.",
    (1,42):"Hodram levels with his crew about the country's finances and nominal navy before challenging them to build a fleet of their own.",
    (2,26):"Lil is embarrassed at failing to recognize Clifford and Camille calls out. Clifford dismisses the offense and checks her name before explaining how he knows about the company.",
    (2,164):"The ship-buying lesson moves from limited purchases and increasing market share to matching hull size and staffing to what the fleet can carry.",
    (3,18):"The crew talks about the poetry and appeal of the sea. A crewmate's jubilant victory interjection prompts a dry exception before the group returns to the theme.",
    (3,31):"Camille and Hodram arrive when Lil is in danger, expose Kuhn's disguise and join her side. Kuhn realizes the plan has failed and orders a retreat on the affected branch.",
    (3,135):"The ship-buying lesson explains when buying ships makes sense, how limited one-percent shares are, and why hull size and price must match the buyer's trade.",
}

# Blank revisions preserve the installed words. Protected groups inform the native formatter.
DECISIONS = {
    (0,42):"""
47|||Clau boasts he can board pirate ships and knock down their crews one at a time. The almost gleeful exaggeration sets up Rafael's caution.
50|||Julio's brief exasperation lets Clau's proposal hang before Rafael answers it.
54||We're nowhere near ready for that.;We wouldn't make it out alive.|Rafael takes Clau's suggestion seriously enough to explain why it would get them killed. Keep the two complete sentences together after his initial pause.
59|||The response endorses Rafael's concern and suggests the named waters as a first step. The further destinations remain open.
63|||The lesson promises experience in both sailing and trade by visiting ports. The conversational future tense suits the advice.
""",
    (0,46):"""
23|||The risk is a fleet picking a fight sooner than expected, not an order for the player to attack.
27|||His brief transition frames the three actions that follow.
41||what's nearby,;start a battle,|The list teaches the three separate actions. Keep the contraction with nearby so the first action reads as one instruction.
44|||Choosing a town or fleet is required for information or to start a battle. The existing order conveys the selection step before the reason.
47|||The advice names the coast and keeps the result uncertain.
""",
    (0,48):"""
236|||The quiet aside gently ribs his crewmate before conceding the comparison. Keep the parentheses and speaker.
239|||The cough interrupts the banter.
247||dedication to learning.;He's a promising... young man.|The speaker compliments the young man's attitude and then his general promise. Keep the hesitation within young man and attach He's to the second thought.
250|||The scholar admits his navigation experience is limited and expects to learn from the crew. His modest register works.
254|||Rafael reassures him by admitting that the crew is also starting out.
262|||The older speaker's enthusiasm lifts the mood as the voyage begins.
273|||The anticipation is a brief answer to the preceding celebration.
280||Aren't you, Clau?|Rafael values having a learned crewmate and seeks Clau's agreement. Keep their conversational tag intact while using more of the opening row.
284|||The response sounds grudging for a beat, then wishes the doctor and his assistant well. The final afterthought carries the tease.
288|||The confident short reply fits the mood at the end of the exchange.
""",
    (0,84):"""
147|||Clau explains that Vels was among the pirates taken by Gerhard's fleet. The two sentences set up Julio's surprise.
151|||The short question gives Gerhard an opening to take over the story.
155|That's enough. Mr. Manaus, is it? I'll tell the rest. Come in, Admiral. The rest of you, too.|Mr. Manaus, is it?;Come in, Admiral.;The rest of you, too.|Gerhard recognizes the person he calls Manaus before taking over from Clau. The address translates 君 in context and separates it from the explicit Admiral invitation.
160|||Gerhard saw potential in Vels while the pirate was young and took him in to train him. The existing sequence keeps his motive and choice distinct.
""",
    (1,3):"""
6||They're the ones;our waters!|Aziza points out the rival company and accuses it of intruding in her waters. Keep FO, plus the forceful follow-up without stranding They're.
9|||The short shout answers her accusation.
13|||Aziza orders battle stations and assigns command to Snake. Neither order needs added details.
16|||Snake's quick answer suits the tactical exchange.
20|Angel! Bring us around to their starboard quarter!|their starboard quarter!|Aziza orders the ship into the enemy's right-rear quarter. The active command makes the direction clear and matches her parallel original order.
23|||Angel's exuberance and acknowledgment distinguish him from the others.
26|||Aziza asks Dandy about gunnery readiness immediately after assigning the maneuver.
29|||The concise confirmation gives Dandy a distinct disciplined voice.
33|||Aziza's excitement gives way to a rough call for the crew's attention. The short bursts fit her.
36|||The challenge to the named company asks who deserves these waters. Keep the original company substitution.
39|||The second cheer answers the battle challenge.
43|||Hodram's understated recognition contrasts with Aziza's theatrics.
47|||Gerhard tentatively identifies the opposing leader as a woman. Keep the unfinished observation.
51|||Hodram treats the opposing fleet as pirates and orders preparations. Keep his blunt decision after Gerhard's uncertainty.
55|||Gerhard accepts the command without further argument.
""",
    (1,42):"""
76|||Keep the full phrase a navy in name only together on the next row. The shorter first row belongs to Hodram's direct appeal to what his crew already knows.
79|||The description of a stopgap patrol fleet explains exactly how their superiors see them.
82||Aiding the Protestants;it's one reason money's tight.|Keep the political policy and the qualifier that it is one reason for the budget difficulty. Put the explanation's final clause together.
86|||The two- or three-year horizon makes clear that Hodram expects a long undertaking.
90|||The climax keeps the Baltic, the king and the people in his appeal for effort.
""",
    (2,26):"""
156|||Lil's stammer and final interruption convey both embarrassment and the sudden recognition of what she has said.
168|||Camille's interjection uses the original given-name token.
175|||Clifford dismisses the offense before checking Lil's full name. Reserve the second line for both substitutions and the question mark at maximum name width.
179|||Lil asks naturally whether he knows the group.
183|||Clifford's restrained reply explains why information comes his way.
""",
    (2,164):"""
140|||The distinction between adding trading ports and buying a ship stays clear. Retain the percentage and the exact one-to-five units.
143||it's time to buy a ship.|The lesson reaches a practical conclusion when the company can buy more goods. Keep that conclusion intact and match the parallel lesson.
147|||Size and cost are the first things to consider. The short direct instruction segues into the budget example.
150|||The example makes clear that additional sailors do not help a fleet that cannot fill its cargo space.
163|||The first sentence is too long for a single native row. Retain the existing subject lead and keep two or three masts together before the separate tradeoff.
166|||The five-hold maximum and the conditional advice about marine quarters and guns stay factual.
""",
    (3,18):"""
49|||Her surprise at a man she thought cared only about ships gives the next reflection a reason to begin.
53|||Keep the original given name and the old sailor's general claim about poetry.
64||Ha ha! We won!;Time for a victory feast!|The victory yell comically interrupts the reflection. His invitation to feast becomes a complete second thought without dividing Time for.
68|||The dry exception lands immediately after the celebratory interruption.
75|||The reflection returns in a quieter tone and preserves the sea's acceptance as the speaker's image.
""",
    (3,31):"""
34|||The cry announces Camille's alarm and stretches Lil's name as in the Japanese.
38|||Lil is startled to find Camille and Hodram here. The two questions keep her surprise before the explanation.
42||That's Kuhn's fleet in disguise.;They're the ones attacking you!|Camille quotes the warning and identifies the attackers. Keep the original given-name substitution and let each revelation occupy a complete thought.
45|||Lil's shocked question follows the revelation directly.
49|||Maria validates the accusation and volunteers to join the fight. The declaration works as an immediate response.
63|||Kuhn's terse frustration acknowledges that his plan failed.
67|||The aide's formal warning about disadvantage prepares Kuhn's retaliation.
71||we're pulling out!|Preserve Kuhn's irritation and put the retreat order together.
""",
    (3,135):"""
325|||The compact example preserves the route expansion, one percent and one-to-five-unit limits.
328||it's time to buy a ship.|Keep the conclusion together across both versions of this tutorial. The cue remains growth in market share and buying power.
332|||The instructor moves from when to buy a ship to deciding which ship to buy.
335|||The example retains the tradeoff between increased staffing needs and unused cargo space.
""",
}


def indexed(arm,block,inventory):
    return inventory(arm,block)[0]


def bind(arm,clean_arm,inventory,route,n,source,current,owners):
    a,b = indexed(clean_arm,source,inventory),indexed(arm,current,inventory)
    if (route,n)==(0,84):
        assert len(b)==len(a)+2
        a,b=a[:67],b[:67]
    assert [x["word"] for x in a]==[x["word"] for x in b]
    sa,ca = ({x["offset"]:i for i,x in enumerate(m)} for m in (a,b))
    results = []
    for x,y in zip(a,b,strict=True):
        if x["word"]!=0x4000:
            continue
        o,q=x["offset"],y["offset"]
        k=source[:o+5].count(b"\0")
        if k not in owners:
            continue
        left,right=[bytes.fromhex(z["whole_command_hex"]) for z in (x,y)]
        assert left[:6]==right[:6] and left[:5]==b"\0\x40\xff\xff\0" and left[5]<207
        assert [sa[p] for p in x["ancestor_0100_offsets"]]==[ca[p] for p in y["ancestor_0100_offsets"]]
        bodies=[v[5:v.index(0,6)] for v in (left,right)]
        refs=[dict(command_offset=at,offset=at+5,exact_body_hex=raw[1:].hex(),exact_command_hex=cmd.hex())
              for at,raw,cmd in zip((o,q),bodies,(left,right),strict=True)]
        results.append((k,left[5],bodies,refs))
    assert {r[0] for r in results}==owners.keys()
    return results,len(a),len(b)


def main():
    assert not ROOT.exists()
    current = base.load(parent.RELEASE)
    candidate=base.digest(parent.ROM)
    assert candidate==current["candidate_sha256"]
    assert base.digest(base.REGISTRY)==current["registry_sha256"] and base.digest(parent.MANIFEST)==current["manifest_sha256"]
    assert base.digest(native.CLEAN)==current["clean_input_sha256"]
    images=list(map(base.NdsImage.open,(native.CLEAN,parent.ROM)))
    clean_arm,arm=[x.read_file(native.ARM) for x in images]
    actors={r["actor_ID"]:r["progressive_nameplate"] for r in base.load(CATALOGUE)["source_and_current_default_name_fields"]}
    inventory,_,_=native.scoped_inventory()
    triage,totals,groups,rows=[],{},[],[]
    for route in range(4):
        path=f"/data/SC{route}.DK4"
        clean,current_archive=[x.read_file(path) for x in images]
        assert native.digest(current_archive)==current[f"target_SC{route}_sha256"]
        stats,leads=scanner.scan(path,current_archive)
        totals[path]=dict(stats)|dict(marked=len(leads),archive_sha256=native.digest(current_archive))
        triage.extend(leads)
        source_bank,active_bank=[native.IlnkContainer.parse(a).blocks for a in (clean,current_archive)]
        for (owner,n),text in DECISIONS.items():
            if owner!=route:
                continue
            decisions={}
            for line in text.strip().splitlines():
                i,revised,protection,note=line.split("|",3)
                decisions[int(i)]=(revised,protection,note)
            source,active=source_bank[n],active_bank[n]
            found,count_a,count_b=bind(arm,clean_arm,inventory,route,n,source,active,decisions)
            ids=[]
            for i,actor,(jp,en),(sr,cr) in found:
                replacement,protection,note=decisions[i]
                previous=" ".join(en[1:].decode("ascii").split())
                english=replacement or previous
                phrases=protection.split(";") if protection else []
                assert all(p in english for p in phrases)
                ident=f"DK4_MES_B{n}_R{i:04}"
                ids.append(ident)
                sr.update(file_path=path,block=n,block_sha256=native.digest(source),archive_sha256=native.digest(clean))
                cr.update(file_path=path,block=n,block_sha256=native.digest(active),archive_sha256=native.digest(current_archive),
                          candidate_sha256=candidate)
                changed=bool(phrases or replacement)
                rows.append(dict(id=ident,route=route,block=n,file_path=path,kind="progressive",source_selector=actor,
                    speaker=actors[actor],source_reference=sr,current_reference=cr,source_hex=jp.hex(),current_hex=en.hex(),
                    Japanese=jp[1:].decode("cp932"),previous_English=previous,english=english,protected_phrases=phrases,
                    context=CONTEXT[route,n],localization_note=note,decision="revision" if changed else "retention",
                    change_class="prose" if replacement else "wrap_only" if changed else "retention",
                    review=dict(source=True,context=True,localization=True,naturalness=True,formatting=not changed)))
            groups.append(dict(route=route,file_path=path,block=n,source_block_sha256=native.digest(source),
                current_block_sha256=native.digest(active),record_ids=ids,checked_command_pair_prefix=count_a,
                current_pair_prefix=count_b))
    assert len(triage)==sum(d["marked"] for d in totals.values())
    resolved={(r["file_path"],r["block"],r["current_reference"]["offset"]):r for r in rows}
    for q in triage:
        match=resolved.get((q["file_path"],q["block"],q["offset"]))
        if match:
            assert q["stored_body_hex"]==match["current_hex"][2:]
            q["disposition"]=match["decision"]
            q["source_id"]=match["id"]
    ROOT.mkdir()
    base.save(TRIAGE,dict(candidate_sha256=candidate,per_archive=totals,records=triage,
        raw_signature_screen_only=True,new_editorial_credit=0))
    base.save(REVIEW,dict(candidate_sha256=candidate,clean_sha256=current["clean_input_sha256"],
        translation_policy="natural-dialogue-v2",target_locale="en-US",records=rows,groups=groups,
        counts=dict(Counter(row["change_class"] for row in rows)),triage_sha256=base.digest(TRIAGE),
        new_editorial_credit=0,native_and_gameplay_verification_of_changes_pending=True))
    print(f"Reviewed {len(rows)} records in {len(groups)} groups. {dict(Counter(row['change_class'] for row in rows))}",flush=True)


def preflight():
    assert not PREFLIGHT.exists()
    draft,current=map(base.load,(REVIEW,parent.RELEASE))
    assert draft["candidate_sha256"]==current["candidate_sha256"]==base.digest(parent.ROM)
    ctx=native.RegisteredRuntime(parent.RELEASE,current["own_registered_startup"],captain=3)
    font=ctx.image.read_file("/GRP/KANJI.FNT")
    renderer=display.clipped_renderer(ctx)
    plans,pictures,open_cases={},[],[]
    default_company={0:"Castor Company",1:"Bergstrom Fleet",2:"Argot Company",3:"Li Fleet"}
    default_first={0:"Rafael",1:"Hodram",2:"Lil",3:"Maria"}
    for row in (r for r in draft["records"] if r["decision"]=="revision"):
        old,new = [bytes.fromhex(row[field]) for field in ("current_hex","source_hex")]
        key=f'{row["route"]}/{row["id"]}'
        try:
            body,plan = layout.plan_progressive(row,old[0],old[1:],new[1:])
        except (AssertionError,ValueError) as err:
            open_cases.append(dict(key=key,reason=str(err) or type(err).__name__))
            continue
        assert plan["expected_native_pages"]==1
        assert old[0]==new[0] and len(body)<300
        if row["route"]==0 and row["block"]==84 and len(body)>len(old)-1:
            open_cases.append(dict(key=key,reason="Existing continuation block needs its allocation maintained",proposed_plan=plan))
            continue
        cases=[]
        tokens=[t for t in ("FO","FI") if t.encode("ascii") in body]
        variants=[("Default widths",{"FO":default_company[row["route"]],"FI":default_first[row["route"]]})]
        if tokens:
            variants.append(("Max names",{"FO":"W"*20,"FI":"W"*16}))
        for label,names in variants:
            expanded=body
            for token in tokens:
                expanded=expanded.replace(token.encode("ascii"),names[token].encode("ascii"))
            lines=[display.display.expected(t,names) for t in plan["lines"]]
            page,=display.display.raster(ctx,font,renderer,expanded,lines,1)
            assert page["native_independent_plane_equal"]
            plane=bytes.fromhex(page["native_plane_hex"])
            pictures.append((f"{key} / {label}",plane))
            cases.append(dict(scope=label,lines=lines,pixels_sha256=native.digest(plane)))
        plans[key]=dict(plan=plan,whole_page_matches=cases)
    contact = display.display.inherited.early.contact_sheets
    sheets=FunctionType(contact.__code__,contact.__globals__|dict(ROOT=ROOT))(pictures)
    base.save(PREFLIGHT,dict(candidate_sha256=draft["candidate_sha256"],draft_sha256=base.digest(REVIEW),
        plans=plans,pending=open_cases,sheets=sheets,offline_native_only=True,
        registered_integration_and_actual_gameplay_pending=True))
    print(f"Native preflight passed for {len(plans)} proposals. {len(open_cases)} need layout follow-up.",flush=True)
    for case in open_cases:
        print(case["key"],case["reason"])


if __name__=="__main__":
    import sys
    (preflight if sys.argv[1:]==["preflight"] else main)()
