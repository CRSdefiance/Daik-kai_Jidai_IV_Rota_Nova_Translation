"""Review the full early harbor, loan, and departure-preparation exchange."""
from collections import Counter
from pathlib import Path
from types import FunctionType

from scripts import observe_rafael_early_harbor_20261121 as game
from scripts import prepare_london_guild_assignments_20261118 as pairing
from scripts import stage_london_guild_assignments_20261118 as planner
from scripts.review_company_name_dialogue_20261121 import GATES, TOKEN, logical


parent, base, native = game.active, game.base, game.active.native
ROOT = Path("work/rafael_harbor_exchange_20261121")
SOURCE = ROOT / "paired_source.json"
OUTPUT = Path("translations/editorial_checkpoints/SharedText_20261110_v1/rafael_harbor_exchange_20261121_v2.json")
PREVIOUS = Path("translations/rafael_opening_contextual_final_review_v1.json")
BLOCKS = ((44,), (), (), ())
CONTEXT = ("Rafael's opening and preparation choice.",) * 4
SEGMENTS = (
    (140, "Clau brings Rafael to the harbor and talks up adventurers. Janus and Clau show him the ship they restored. Rafael wants to sail sooner and leaves to find Julio."),
    (233, "Julio challenges another advance. Rafael claims the idea and promises to repay the loan. The three leave, and Rafael explains why he wants to act without asking his father."),
    (355, "Julio returns with 30,000 gold and says he will sail with them. He makes Rafael captain, admiral and company leader, and Clau backs away from the responsibility."),
    (446, "Gratitude gives way to Clau and Julio's bickering. Rafael uses his new captain's authority to stop them. Julio points the group toward preparation."),
    (1000, "Janus offers a lesson with Julio or independent preparation. The tutorial branch names the Market, Tavern and Square, while the other branch gives Rafael a send-off."),
)
# Entries without replacement prose preserve the wording and only move line breaks.
EDITS = {
    17: ("Say, FI. What do you make of sailors?", ("What do you make of sailors?",),
         "Keep Clau's informal address and question about seafaring. The full question belongs on one line."),
    25: (None, ("Prince Henry, Duke Leon...", "Man, they're really cool!"),
         "Keep both named examples and Clau's burst of admiration together."),
    29: ("The sea is a man's great adventure!", ("a man's great adventure!",),
         "Keep Clau's swagger and the ideal he finds in going to sea."),
    67: ("Well? Surprised? We've even named her. Behold the Carteira!",
         ("We've even named her.", "Behold the Carteira!"),
         "Clau springs the surprise and announces the exact ship name with a flourish."),
    71: ("Janus and I took on an old wreck. She was little more than scrap, but we fixed her up.",
         ("an old wreck.", "little more than scrap,", "we fixed her up."),
         "Keep both men as the restorers and the wreck as salvage. Clau does not say how they acquired it."),
    74: ("We can't sail until we save up. Someday, though, we'll set out.", ("until we save up.", "Someday, though,"),
         "Keep the savings condition together before Clau's tentative promise."),
    90: ("You said we should go to sea, Clau! If we need money, we can ask Julio.",
         ("go to sea, Clau!", "If we need money,"),
         "Rafael turns Clau's own dream back on him. A direct conditional keeps the loan suggestion in a single thought."),
    103: ("Keep fixing her up, Janus and Clau! I'm counting on you!", ("Janus and Clau!", "I'm counting on you!"),
          "Keep the task Rafael calls back to both friends in one phrase."),
    114: (None, ("Once he makes up his mind,", "he can't sit still."),
          "Keep Janus's amused response together and preserve the condition before the result."),
    117: (None, ("how are the repairs coming?",),
          "Keep Clau's quick change of subject as one question."),
    124: ("Don't sweat the small stuff. You loved every minute of it!", ("the small stuff.", "every minute of it!"),
          "Keep the two colloquial phrases together as Clau defends himself."),
    163: (None, ("an honest day's work.", "to trust you?"),
          "Keep Julio's complaint about Clau and his question about trust clear."),
    174: ("Please, Julio! It was my idea. Could you lend us the money?",
          ("It was my idea.", "lend us the money?"),
          "Rafael takes responsibility and asks again for the specific loan. Keep his earnestness and the uncertainty of Julio's answer."),
    179: (None, ("What does your father say?",),
          "Keep Julio's question about the father together. The given name remains a substitution."),
    182: ("I won't turn to my father for this. Please. I swear I'll pay you back.",
          ("I won't turn to my father for this.", "I swear I'll pay you back."),
          "Keep Rafael's promise to repay the loan together before his last plea."),
    190: (None, ("Let's go, FI.", "Janus, we're leaving."),
          "Keep Clau's call to Rafael and his direction to Janus as distinct thoughts."),
    206: (None, ("Now what are we going to do?",),
          "Clau's uncertainty becomes a complete question after his show of confidence."),
    213: ("Father still treats me as a child. He'd never let me go to sea.",
          ("Father still treats me as a child.", "He'd never let me go to sea."),
          "Keep the father's treatment of Rafael and the objection to sailing intact."),
    222: ("That's the way, FI! Now that's a real man!", ("That's the way, FI!", "Now that's a real man!"),
          "Keep Clau's approving shout together after the address to Rafael."),
    225: ("We still need money to get started. Courage won't pay the bills.", ("need money to get started.", "Courage won't pay the bills."),
          "Keep Janus's practical objection together and let the dry punch line finish it."),
    268: (None, ("I'll expect it back with interest.",),
          "Preserve the loan and its interest as Julio's single condition."),
    304: (None, ("Julio's a famous navigator.",),
          "Keep Janus's defense and Julio's role legible as a complete sentence."),
    308: ("FI, you'll be captain.", ("FI, you'll be captain.",),
          "Julio addresses Rafael by his chosen name and makes the appointment in one line."),
    324: ("Want to make a name for yourself among the world's greatest sailors? Then set your sights high.",
          ("the world's greatest sailors?", "set your sights high."),
          "Keep the group Rafael wants to join and Julio's closing advice intact."),
    375: (None, ("teach you to recognize greatness.",),
          "Let Julio's whole comic threat land after the opening clause."),
    394: (None, ("break your fingers",),
          "Keep the action and its object together in Clau's retort."),
    424: ("Never mind that fool. Getting ready is most of the work. Let's gather what we need.",
          ("Getting ready is most of the work.", "Let's gather what we need."),
          "Keep Julio's proverb about preparation doing most of the work and his invitation to get supplies."),
    464: (None, ("We'll head to the Market first.",),
          "Give the first tutorial destination its own instruction and use the established menu label."),
    469: ("Before you leave any town, you should at least visit the Market, Tavern, and Square.",
          ("the Market, Tavern, and Square.",),
          "Preserve the recommendation for every departure and keep the three named menu facilities together."),
    479: (None, ("give it your best!",),
          "Keep Julio's encouragement together on the branch without the lesson."),
}
CAPTURE = {17:3611,20:3921,25:4231,29:4541,33:4851,38:5161,42:5471,45:5781,
           53:6091,57:6401,62:7021,67:7331,71:7641,74:7951,77:8261,82:8571,86:8881,90:9191}


def main():
    assert not OUTPUT.exists()
    if not SOURCE.exists():
        FunctionType(pairing.main.__code__,vars(pairing)|globals())()
    packet,release,prior = map(base.load,(SOURCE,parent.RELEASE,PREVIOUS))
    sha = base.digest(parent.ROM)
    assert packet["candidate_sha256"]==release["candidate_sha256"]==sha
    assert packet["clean_sha256"]==release["clean_input_sha256"]==prior["source_ROM_sha256"]
    assert base.digest(base.REGISTRY)==release["registry_sha256"]
    previous = {row["source_reference"]["offset"]:row for row in prior["records"]}
    assert len(previous)==len(prior["records"])
    video_path = game.ROOT/"rafael/capture/capture_report.json"
    video = base.load(video_path)
    assert video["ROM_sha256"]==sha and video["cold_boot"] and not video["savestate_loaded"]
    captures = {r["frame"]:r for r in video["frames_captured"]}
    group, = packet["groups"]
    rows, plans = [], {}
    selected = set()
    for record in group["records"]:
        at, number, selector = (record[k] for k in ("source_offset","source_record_index","selector"))
        early = previous.pop(at)
        assert early["source_Japanese"]==record["Japanese"] and all(early["review"].values())
        source,current = (bytes.fromhex(record[f"{side}_body_hex"]) for side in ("source","current"))
        prefix = b"" if selector is None else bytes([selector])
        if selector is not None:
            assert (prefix+source).hex()==early["source_reference"]["hex"]
        raw = logical(record["current_English"])
        changed = number in EDITS
        new, phrases, reason = EDITS.get(number, (None,(),early["localization_note"]))
        english = raw if new is None else new
        assert TOKEN.findall(record["Japanese"])==TOKEN.findall(raw)==TOKEN.findall(english)
        context = next(note for limit,note in SEGMENTS if number<limit)
        refs = {side:dict(file_path=group["file_path"],block=44,offset=record[f"{side}_offset"],
            command_offset=record[f"{side}_command_offset"],archive_sha256=group[f"{side}_archive_sha256"],
            block_sha256=group[f"{side}_block_sha256"],exact_hex=(prefix+body).hex())
            for side,body in (("source",source),("current",current))}
        row = dict(id=early["id"],file_path=group["file_path"],route=0,block=44,
            source_record_index=number,native_command_word=record["native_command_word"],native_slots=record["slots"],
            source_selector=selector,kind="typed-choice-label" if selector is None else "progressive",
            source_reference=refs["source"],current_reference=refs["current"],source_hex=(prefix+source).hex(),
            current_hex=(prefix+current).hex(),Japanese=record["Japanese"],previous_English=raw,english=english,
            speaker=early["speaker"],context=context,source_meaning=early["source_meaning"],
            localization_note=reason,protected_phrases=list(phrases),previous_capture=captures.get(CAPTURE.get(number)),
            finding=("retention" if not changed else "wrap" if new is None else "prose and wrap"),
            decision="revision" if changed else "retention",review=dict.fromkeys(GATES,True)|{"formatting":not changed})
        if row["previous_capture"]:
            shot = row["previous_capture"]
            assert base.digest(shot["path"])==shot["PNG_sha256"]
        if changed:
            assert selector not in (None,254) and not {"FO","FU"}.intersection(TOKEN.findall(english))
            try:
                body, plan = planner.plan_progressive(row,selector,current,source)
            except AssertionError as issue:
                raise AssertionError((row["id"],english,phrases)) from issue
            assert body.rstrip(b" ")!=current.rstrip(b" "), (number,english,plan["lines"])
            assert plan["expected_native_pages"]==1
            selected.add(number)
            plans[row["id"]]=plan
        rows.append(row)
    assert not previous and selected==EDITS.keys() and len(rows)==117
    counters=Counter(row["finding"] for row in rows)
    base.save(OUTPUT,dict(translation_policy="natural-dialogue-v2",encoder="dialogue-relocatable-v1",
        target_locale="en-US",review_gates=GATES,previous_sha256=sha,previous_registry_sha256=release["registry_sha256"],
        source_packet=str(SOURCE),source_packet_sha256=base.digest(SOURCE),records=rows,plans=plans,
        decisions=dict(Counter(row["decision"] for row in rows)),findings=dict(counters),previous_gameplay_report=str(video_path),
        previous_gameplay_report_sha256=base.digest(video_path),new_editorial_credit=0,
        status="Stored compilation and revised-candidate validation pending."))
    print(len(rows),dict(counters))


if __name__=="__main__":
    main()
