"""Review the next30 SC0 name-dependent lines against clean spoken context."""

import json
import re
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.scan.sjis_scan import contains_japanese
from dk4tool.script.mesfile import export_mesfile_rows

TEXT = {
    "DK4_MES_B143_R0324": ("So, His Excellency Albuquerque has asked me to instruct you, {MACRO:FI}.", "Albuquerque has asked Silveira to give Rafael instruction.", "Preserve the respectful source address without turning Albuquerque into a hereditary Lord."),
    "DK4_MES_B143_R0424": ("Don't worry about it! Now, {MACRO:FI}, let's defeat Espinosa together!", "Silveira dismisses Rafael's apology and urges joint action against Espinosa.", "The preceding speech is an apology, so No, no is a reassurance rather than a refusal."),
    "DK4_MES_B144_R0010": ("What is it, {MACRO:FI}?", "Claudio asks why Rafael is pondering the tablets.", "A neutral question fits Rafael's puzzling, rather than suggesting a new danger or problem."),
    "DK4_MES_B144_R0160": ("Let's go look for it right away, {MACRO:FI}, Clau!", "A companion eagerly proposes going to find the Proof and addresses Rafael and Clau.", "Preserve the eagerness and source nickname in conversational English."),
    "DK4_MES_B145_R0006": ("Hey, {MACRO:FI}.", "Claudio calls for Rafael's attention.", "The existing casual address is natural and retained."),
    "DK4_MES_B145_R0196": ("Yes. {MACRO:FI}, Clau... everyone's been so kind. Clau is a little... rough around the edges, though...", "Eirene praises the crew's kindness while gently qualifying Claudio's rough manners.", "Rough around the edges conveys がさつ without inventing moral depravity or a new relationship."),
    "DK4_MES_B146_R0006": ("...{MACRO:FU}, isn't it?", "Uddin confirms Rafael's full name.", "Restore the recognition question rather than an unexplained name-only question."),
    "DK4_MES_B147_R0012": ("Forgive me for startling you, {MACRO:FI}... or perhaps I should call you the head of {MACRO:FO}.", "Uddin apologizes for surprising Rafael and upgrades his form of address to the company leader.", "Preserve his courteous correction and the company macro; no military rank is substituted for the business leadership title."),
    "DK4_MES_B150_R0069": ("We did it, {MACRO:FI}!", "A companion celebrates the successful Proof-map ritual.", "Retain the natural celebratory response."),
    "DK4_MES_B150_R0077": ("We did it, {MACRO:FI}!", "Eirene celebrates the successful Proof-map ritual.", "Preserve this independent speaker's identical response and its selector."),
    "DK4_MES_B151_R0113": ("{MACRO:FI}! Not you too! I won't accept this!", "Claudio rejects the thought that Rafael accepts Portugal's absorption by Spain.", "Restore a complete personal refusal; the next line affirms Rafael's Portuguese pride and resistance."),
    "DK4_MES_B151_R0152": ("Rushing home would take too much time and too many supplies... {MACRO:FI}, we need to think this through.", "Claudio notes the time and supply burden of rushing home and urges careful thought.", "Preserve both costs and the deliberation, without assigning a decision before Rafael's next line."),
    "DK4_MES_B151_R0208": ("{MACRO:FI}, are you really sure? You're not just giving up, are you?!", "Claudio worries that Rafael is accepting defeat and giving up.", "Keep the emotional challenge as natural questions; Rafael immediately denies giving up."),
    "DK4_MES_B151_R0246": ("Yes! Now you're talking, {MACRO:FI}! That's the spirit!", "Claudio enthusiastically praises Rafael's determination to restore Portugal.", "Localize the manly-approval exclamation by its motivational effect rather than the stiff A true man wording."),
    "DK4_MES_B151_R0293": ("Admiral {MACRO:FI}! Come to think of it, I believe the governor of Southeast Asia is Portuguese.", "A companion recalls that the regional governor is probably Portuguese, addressing Rafael as admiral.", "Restore the explicit admiral address and the uncertainty in 確か. Use the project's Southeast Asia region term."),
    "DK4_MES_B151_R0314": ("Oh, that's right! {MACRO:FI}, listen to this. I believe the governor of Southeast Asia is Portuguese.", "Julio recalls the governor's Portuguese nationality and asks Rafael to listen.", "Preserve recollection and qualified confidence, rather than asserting nationality and then asking an invented right question."),
    "DK4_MES_B151_R0334": ("Helping you matters far more to me than those details, {MACRO:FI}, my boy... I mean, Admiral.", "Julio says helping Rafael matters more than national differences, correcting his familiar boy address to admiral.", "The previous line asks whether a Spaniard should aid Portugal. Preserve Julio's personal priority and source self-correction; my boy is a familiar mentor address, not kinship."),
    "DK4_MES_B152_R0185": ("Hey, {MACRO:FI}... what does he mean by 'east of here'?", "Claudio asks what Pereira means by the eastward challenge.", "Restore the question about the meaning of the instruction, rather than asking simply what lies east."),
    "DK4_MES_B153_R0022": ("H-hey, {MACRO:FI}! Don't get carried away rubbing it! Look, it's dissolving!", "Claudio warns Rafael, who is rubbing the ancient coin with lotion, that it is dissolving.", "Keep the stammer, warning about overenthusiastic rubbing and visible dissolving effect."),
    "DK4_MES_B154_R0005": ("{MACRO:FI}, Spain seems one step ahead of us in these waters.", "Claudio observes that Spain has a head start in this region.", "The existing natural observation is retained."),
    "DK4_MES_B154_R0140": ("{MACRO:FI}…", "Claudio gently addresses Rafael while he considers the wider abuses in the New World.", "This is genuine name-only dialogue, not a VM command. Preserve its hesitation, original CP932 ellipsis glyph and selector."),
    "DK4_MES_B154_R0161": ("Well, that was helpful. Right, {MACRO:FI}?", "Claudio acknowledges useful information about the local people's suffering.", "Convey a useful report without implying that the suffering itself was a benefit."),
    "DK4_MES_B155_R0047": ("...{MACRO:FI}? You heard what they said, didn't you...?", "A companion checks that Rafael heard Escante's officers discussing their plan.", "Restore the checking question and explicit reported speech; no new plot details are inserted."),
    "DK4_MES_B156_R0022": ("{MACRO:FI}! You know we're in their way! At this rate, they'll crush us!", "Claudio warns that the rival factions see them as an obstacle and threaten them.", "The existing urgent warning is faithful and retained."),
    "DK4_MES_B156_R0025": ("Shh! Clau, {MACRO:FI}! Look over there!", "A companion hushes Claudio and Rafael and points out something to observe.", "Retain the source nickname and urgent attention shift; no object or identity is guessed."),
    "DK4_MES_B158_R0025": ("Well... you're not as innocent as I thought, {MACRO:FI}!", "Claudio teasingly suggests Rafael is more worldly than he seems when selecting a gift/trade good for Charlotte.", "Localize スミにおけない as affectionate teasing in its romantic context, not a literal corner or accusation of wrongdoing."),
    "DK4_MES_B159_R0005": ("{MACRO:FI}, can we talk for a moment?", "Eirene asks Rafael for a moment to talk.", "Use a natural gentle conversation opener."),
    "DK4_MES_B159_R0038": ("{MACRO:FI}…", "Eirene responds softly as Rafael admits that he cannot hide his feelings from her.", "Retain the short name-only response and original CP932 ellipsis; restore missing context metadata."),
    "DK4_MES_B159_R0047": ("{MACRO:FI}... 'All I think about every day is {MACRO:FI},' she told me. You're on her mind, too.", "Eirene reports that Charlotte also thinks about Rafael every day.", "Render the reported thought as quoted English to retain both dynamic name occurrences naturally, then convey the source's reciprocal too. This is a faithful localized report, not a claim of verbatim Japanese quotation or a new promise."),
    "DK4_MES_B159_R0060": ("If you had no feelings for Charlotte, {MACRO:FI}, I would have kept this to myself.", "Eirene had intended to keep the information to herself if Rafael did not care for Charlotte.", "Correct the older between us wording, which implied she had already shared it with him. Preserve the hypothetical condition and Charlotte's identity."),
}


def prepare_review(text=TEXT, output=Path("translations/confirmed_name_route_editorial_v234.json"), metadata=None):
    metadata = metadata or {}
    prepared = json.loads(Path("work/analysis/confirmed_names_v198/confirmed_source_locked_drafts.json").read_text(encoding="utf-8"))
    drafted = {r["id"]: r for r in prepared["records"] if r["file_path"] == "/data/SC0.DK4"}
    clean = NdsImage.open("work/clean.nds")
    raw = clean.read_file("/data/SC0.DK4")
    source = export_mesfile_rows(raw, "/data/SC0.DK4", include_non_japanese=True)
    by_id = {r["id"]: r for r in source}
    canonical_by_id = None
    records = []
    for record_id, (prose, meaning, note) in text.items():
        if record_id in drafted:
            old = drafted[record_id]
        else:
            hint = metadata.get(record_id, {}).get("related_record_template")
            if hint not in drafted:
                raise ValueError("Related scene correction lacks a calibrated template")
            if canonical_by_id is None:
                canonical = NdsImage.open("out/raphael_natural_v2_accepted_base.nds")
                canonical_by_id = {r["id"]: r for r in export_mesfile_rows(
                    canonical.read_file("/data/SC0.DK4"), "/data/SC0.DK4", include_non_japanese=True)}
            old = dict(drafted[hint])
            old["source_hex"] = canonical_by_id[record_id]["source_hex"]
            old["japanese_source"] = by_id[record_id]["japanese"]
            old["english"] = "{SPEAKER:08}{PAD}"
        original = by_id[record_id]
        if original["japanese"] != old["japanese_source"]:
            raise ValueError("Immutable Japanese source differs")
        selectors = re.findall(r"\{SPEAKER:[^}]+\}", old["english"])
        english = "".join(selectors) + prose + "{PAD}"
        tokens = lambda text: re.findall(r"\{(?:SPEAKER|MACRO):[^}]+\}", text)
        if tokens(english) != tokens(old["english"]):
            raise ValueError("Existing selector/macro order changed")
        block = record_id.split("_R")[0]
        spoken = [r for r in source if r["id"].startswith(block + "_R")
                  and (contains_japanese(r["japanese"]) or any(m in r["japanese"] for m in ("FI", "FA", "FO", "FU")))]
        at = next(i for i, r in enumerate(spoken) if r["id"] == record_id)
        speaker = old.get("speaker") or ("Claudio" if "{SPEAKER:05}" in english else "Eirene")
        if "{SPEAKER:05}" in english:
            speaker = "Claudio"
        elif "{SPEAKER:06}" in english:
            speaker = "Julio"
        elif "{SPEAKER:08}" in english:
            speaker = "Eirene, using the Arcadius identity where the scene still does so"
        context = old.get("context") or (
            "Claudio responds to Rafael's worries about abuses throughout the New World."
            if "B154" in record_id else "Eirene mediates Charlotte's feelings after Rafael confides in her.")
        speaker = metadata.get(record_id, {}).get("speaker", speaker)
        context = metadata.get(record_id, {}).get("context", context)
        records.append({"file_path": "/data/SC0.DK4", "id": record_id,
                        "expected_source_hex": old["source_hex"], "clean_source_hex": original["source_hex"],
                        "clean_Japanese": original["japanese"], "english": english, "speaker": speaker,
                        "original_speaker_metadata": old.get("speaker"),
                        "proposed_profile_hint": old["proposed_profile"],
                        "related_scene_dependency": record_id not in drafted,
                        "context": context + " Previous/next clean spoken records reviewed, including name-only utterances.",
                        "clean_spoken_neighbors": [{"id": r["id"], "japanese": r["japanese"], "source_hex": r["source_hex"]}
                                                   for r in spoken[max(0, at - 1):at + 2]],
                        "source_meaning": meaning, "localization_note": note,
                        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
                        "review": {"source": True, "context": True, "localization": True,
                                   "naturalness": True, "formatting": False}})
    payload = {"format": "dk4-confirmed-name-editorial-overrides-v1", "not_a_release_batch": True,
               "clean_SC0_sha256": sha(raw), "records": records,
               "all_other_records_not_approved_by_this_subset": True,
               "native_transport_scene_and_release_pending": True}
    output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"source_reviewed_records": len(records), "formatting_pending": True, "ROM_modified": False}))


if __name__ == "__main__":
    prepare_review()
