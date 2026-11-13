"""Source/context review of the first19 SC0 confirmed-name migration records.

This authoring aid writes a research dossier, never a release batch. Speaker
metadata uses established first names when old drafts disagree about surnames.
"""

import json
import re
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.scan.sjis_scan import contains_japanese
from dk4tool.script.mesfile import export_mesfile_rows

TEXT = {
    "DK4_MES_B05_R0052": (
        "{SPEAKER:23}Now then, {MACRO:FI}, I expect you to fight hard for me too! Ha ha ha!{PAD}",
        "Silveira expects Rafael to fight energetically for his benefit as well and laughs.",
        "Retain the patron's self-interested encouragement and laughter in natural speech."),
    "DK4_MES_B128_R0012": (
        "{SPEAKER:06}Now, {MACRO:FI}, there are a few more things you can do at sea. Let me explain.{PAD}",
        "Julio offers to explain a few more actions available while sailing.",
        "Restore the personal offer to explain; the older actions need explanation fragment sounded like a manual heading."),
    "DK4_MES_B128_R0128": (
        "{SPEAKER:06}Oh, that's right! {MACRO:FI}, would you mind heading for Athens?{PAD}",
        "Remembering what he forgot, Julio apologetically asks Rafael to head for Athens.",
        "Would you mind conveys the polite request without adding a destination detail or apology formula mechanically."),
    "DK4_MES_B128_R0180": (
        "{SPEAKER:05}Oh! {MACRO:FI}, this sounds interesting!{PAD}",
        "Claudio expresses interested surprise about the plan and addresses Rafael.",
        "The existing natural reaction is faithful and retained; only the default-name formatting changes."),
    "DK4_MES_B128_R0189": (
        "{SPEAKER:06}No time like the present, {MACRO:FI}. I'm counting on you!{PAD}",
        "Julio says a good undertaking should not be delayed and entrusts it to Rafael.",
        "Localize 善は急げ by its effect and restore 頼んだよ, omitted by Go now. No new mission or promise is invented."),
    "DK4_MES_B129_R0005": (
        "{SPEAKER:06}So, {MACRO:FI}, have you figured out how to make big profits from trading?{PAD}",
        "Julio asks whether Rafael has learned the secret to large trading profits by now.",
        "Use a conversational mentor's question and preserve the trade/profit scope."),
    "DK4_MES_B133_R0060": (
        "{SPEAKER:05}(Even {MACRO:FI}...? All right, fine.){PAD}",
        "Claudio privately grumbles that even Rafael is siding with the others, then gives in.",
        "Retain the inner-thought parentheses, annoyed hesitation and resigned agreement. Context concerns recruiting Christina."),
    "DK4_MES_B134_R0023": (
        "{SPEAKER:05}{MACRO:FI}! Look out!{PAD}",
        "Claudio urgently warns Rafael of danger.",
        "Keep the concise urgent warning and name; following speech is Claudio's cry after protecting him."),
    "DK4_MES_B136_R0005": (
        "{SPEAKER:05}Hey, {MACRO:FI}!{PAD}",
        "Claudio calls for Rafael's attention.",
        "The casual call is already natural and retained."),
    "DK4_MES_B136_R0084": (
        "{SPEAKER:06}{MACRO:FI}, my boy...{PAD}",
        "Julio affectionately/teasingly addresses Rafael as a boy.",
        "My boy is the elder mentor's familiar address, not a family claim. The next spoken record asks Julio to stop calling him a boy, so deleting this term would break the exchange. Correct the awkward Rafael, boy wording."),
    "DK4_MES_B136_R0168": (
        "{SPEAKER:06}Still, I'd quite forgotten the legend of the Staff of Guidance. Is {MACRO:FI} really planning to look for it...?{PAD}",
        "Julio says he had completely forgotten the Staff of Guidance legend and wonders whether Rafael really intends to seek it.",
        "Preserve his uncertainty and third-person reflection. The next speech proposes a drink with Jenas; no quest outcome is added."),
    "DK4_MES_B139_R0005": (
        "{SPEAKER:06}Is everything going smoothly so far, {MACRO:FI}? Sea routes can be confusing. Shall I explain how they work?{PAD}",
        "Julio checks whether things are going well and offers to explain confusing sea routes.",
        "Restore 順調 as going smoothly rather than asking only whether everything is clear. Keep the optional tutorial offer."),
    "DK4_MES_B141_R0080": (
        "{SPEAKER:06}He probably sensed something in you, {MACRO:FI}.{PAD}",
        "Julio suggests that Hayreddin sensed something in Rafael.",
        "Natural direct address retains the name macro and uncertainty; no specific hidden power or achievement is invented."),
    "DK4_MES_B141_R0084": (
        "{SPEAKER:05}Heh. We can't let him down now. Right, {MACRO:FI}?{PAD}",
        "Claudio says that with such high expectations they have to act, asking Rafael to agree.",
        "Express the effect of being trusted in Claudio's casual voice; preserve the invitation to agree."),
    "DK4_MES_B143_R0068": (
        "I'm {MACRO:FU}. You sent for me, sir?{PAD}",
        "Rafael introduces himself by full name and asks whether the admiral summoned him.",
        "Restore a complete self-introduction and retain the respectful source address; no speaker prefix is added to this ordinary Rafael record."),
    "DK4_MES_B143_R0071": (
        "{SPEAKER:05}Wow, {MACRO:FI}! That was pretty impressive.{PAD}",
        "Claudio admires Rafael's formal introduction.",
        "Context supplies the just-completed introduction. Avoid making this an unsupported clothing/appearance remark or an awkward Smooth fragment."),
    "DK4_MES_B143_R0157": (
        "{SPEAKER:1E}Let's skip the greetings. This is {MACRO:FI} {MACRO:FA}. He's a very promising young man.{PAD}",
        "Albuquerque dismisses the greetings, introduces Rafael Castor and calls him a promising young man.",
        "Restore complete natural sentences and remove the added young-admiral title: the source says 青年, not an admiral rank in this introduction."),
    "DK4_MES_B143_R0161": (
        "It's... nice to meet you... I'm {MACRO:FI} {MACRO:FA}.{PAD}",
        "Rafael hesitantly greets his new acquaintance and gives his name.",
        "Preserve the nervous pauses in a complete greeting/self-introduction. The formatter owns ordinary line breaks."),
    "DK4_MES_B143_R0299": (
        "{SPEAKER:23}By the way, {MACRO:FI}, are you any good at naval battles?{PAD}",
        "Silveira changes the subject and asks whether Rafael is skilled in naval battles.",
        "Restore the topic transition and explicit naval scope, instead of the clipped good in battle question."),
}


def main():
    path = Path("work/analysis/confirmed_names_v198/confirmed_source_locked_drafts.json")
    prepared = json.loads(path.read_text(encoding="utf-8"))
    drafted = {r["id"]: r for r in prepared["records"] if r["file_path"] == "/data/SC0.DK4"}
    clean = NdsImage.open("work/clean.nds")
    raw = clean.read_file("/data/SC0.DK4")
    source = export_mesfile_rows(raw, "/data/SC0.DK4", include_non_japanese=True)
    by_id = {r["id"]: r for r in source}
    records = []
    for record_id, (english, meaning, note) in TEXT.items():
        old, original = drafted[record_id], by_id[record_id]
        if original["japanese"] != old["japanese_source"]:
            raise ValueError("Clean Japanese source differs from the prepared source lock")
        block = record_id.split("_R")[0]
        spoken = [r for r in source if r["id"].startswith(block + "_R") and contains_japanese(r["japanese"])]
        at = next(i for i, r in enumerate(spoken) if r["id"] == record_id)
        neighbors = [{"id": r["id"], "japanese": r["japanese"], "source_hex": r["source_hex"]}
                     for r in spoken[max(0, at - 1):at + 2]]
        tokens = lambda text: re.findall(r"\{(?:SPEAKER|MACRO):[^}]+\}", text)
        if tokens(english) != tokens(old["english"]):
            raise ValueError("Speaker/macro order changed during editorial review")
        speaker = old["speaker"]
        if "{SPEAKER:05}" in english:
            speaker = "Claudio"
        elif "{SPEAKER:06}" in english:
            speaker = "Julio"
        records.append({"file_path": "/data/SC0.DK4", "id": record_id,
                        "expected_source_hex": old["source_hex"],
                        "clean_source_hex": original["source_hex"], "clean_Japanese": original["japanese"],
                        "english": english, "speaker": speaker,
                        "original_speaker_metadata": old["speaker"],
                        "context": old["context"] + " Previous/next clean spoken records, rather than neighboring VM commands, reviewed.",
                        "clean_spoken_neighbors": neighbors, "source_meaning": meaning,
                        "localization_note": note + " Preserve the existing calibrated control preamble and all runtime macros. Formatting/native execution remain separate gates.",
                        "translation_policy": "natural-dialogue-v2", "target_locale": "en-US",
                        "review": {"source": True, "context": True, "localization": True,
                                   "naturalness": True, "formatting": False}})
    result = {"format": "dk4-confirmed-name-editorial-overrides-v1", "not_a_release_batch": True,
              "clean_SC0_sha256": sha(raw), "records": records,
              "excluded_baked_record": {"id": "DK4_MES_B141_R0107",
                                        "reason": "High presentation byte produces a misleading clean export and lacks sufficient speaker/context provenance here. Keep separate native preamble review; no approval inferred."},
              "speaker_metadata_scope": "Use existing mapped Claudio/Julio first names; inconsistent unverified surnames in old metadata are not new ROM name decisions.",
              "all_remaining_records_not_approved_by_this_subset": True}
    Path("translations/confirmed_name_route_editorial_v232.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"source_reviewed_records": len(records), "formatting_pending": True,
                      "high_control_record_not_approved": "DK4_MES_B141_R0107", "ROM_modified": False}))


if __name__ == "__main__":
    main()
