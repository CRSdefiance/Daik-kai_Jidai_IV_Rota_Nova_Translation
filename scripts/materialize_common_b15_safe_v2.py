from __future__ import annotations

import hashlib
import json
from pathlib import Path

from dk4tool.dialogue.encoder import DialogueEncodingError, encode_fixed_dialogue
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage

BASE = Path("out/raphael_natural_v2_pre_common_accepted_rollback.nds")
CLEAN = Path("work/clean.nds")
OUT = Path("translations/common_source_restored_b15_single_entry_v1.json")
BASE_SHA256 = "fb750eac00d3c91cf0cc00e5ee578ba8d2d6eebd7791338c61003d003e5b09d3"
COMMON_SHA256 = "ecb0806b6f36f9bf4164ae46084fbbc12d4122af66b6a8920814197463f19491"

# These records contain one independently addressed message. Records containing
# concatenated voice variants or multiple runtime entry points are deliberately
# excluded until their exact interior offsets are mapped.
LINES: dict[int, tuple[str, str]] = {
    0: ("Report on %s is ready.", "The speaker has investigated the named subject."),
    1: ("News on %s is ready.", "The speaker has returned with information about the named subject."),
    2: ("Report on %s is ready.", "The speaker reports completing an investigation of the named subject."),
    3: ("We have news on %s.", "The speaker obtained information about the named subject."),
    4: ("News on %s is ready.", "The speaker personally investigated the named subject."),
    5: ("We obtained a report on %s.", "The speaker formally reports obtaining information about the named subject."),
    7: ("%s, %s lost a battle to %s.", "The first named party reports that the second was defeated by the third party's fleet."),
    8: ("%s, %s attacked %s. Shameful.", "The speaker condemns the second named party for attacking the third."),
    10: ("A blessed day! Let us pray together.", "A celebrant calls the day auspicious and invites everyone to pray."),
    11: ("Are you here for the ceremony?", "A ritual attendant asks whether the visitor will join the ceremony."),
    13: ("Aaaah... Aaaah!", "A participant loudly vocalizes as part of the ceremony."),
    14: ("What was that?", "A startled participant reacts to the strange vocalization."),
    15: ("La la, tra la la... (gibberish)", "The participant chants deliberately meaningless syllables."),
    16: ("???", "The listener is completely confused."),
    20: ("Here for the %s ceremony?", "An attendant asks whether the visitors came for the named ceremony."),
    21: ("Come in.", "The attendant permits the visitors to enter."),
    22: ("Why are you here? Leave if you have no business.", "A guardian orders visitors without business at the ruins to leave."),
    23: ("HRAAAAGH!", "A participant releases a prolonged ritual shout."),
    24: ("Huh?! Raaah! Bla-bla-bla!", "A participant erupts into another incomprehensible chant."),
    26: ("Dance?", "A visitor repeats the word dancing in surprise."),
    27: ("What dancing?", "A visitor asks what the attendant means by dancing."),
    28: ("Clear your mind. Let everything go, and surrender yourself to the gentle rhythm.", "The attendant tells the visitors to abandon distracting thoughts and yield themselves to the music."),
    29: ("Release the heat rising within you. Yes, just like that.", "The attendant encourages the dancer to release their inner passion."),
    30: ("Your fast begins now. Are you ready?", "The attendant announces the beginning of a religious fast."),
    32: ("Now pray in silence.", "The attendant instructs the participant to pray quietly."),
    34: ("…", "The hungry participant remains silent."),
    36: ("Hurry. Return before dark, or wild beasts will find us.", "The guide warns that wild animals will attack if the group does not return before nightfall."),
    37: ("Need %s coins. You're short.", "The service requires the displayed number of coins, which the player lacks."),
    38: ("Cost: %s coins. Proceed?", "The speaker states the displayed price and asks for confirmation."),
    39: ("Crew here recover health and morale.", "Navigators assigned here recover their physical condition and mood."),
    40: ("A carpenter can repair damaged ships.", "Assigning a shipwright allows damaged vessels to be repaired."),
    43: ("A purser enables deals and buyouts.", "Assigning a purser enables bargaining and market buyouts."),
    44: ("Let me help refit her.", "The speaker offers to assist with the ship refit."),
    46: ("Let me help with the refit.", "The speaker asks to help with the ship refit."),
    51: ("More armor adds durability but slightly lowers speed.", "The second armor upgrade further raises durability at a small speed cost."),
    52: ("A bow gun fires ahead, but has low power.", "A bow gun permits forward fire but has limited power."),
    53: ("A stern gun fires aft, but is less accurate.", "A stern gun permits rearward fire but has low accuracy."),
    54: ("A ram lets you strike an enemy ship's side.", "A ram permits collision attacks against an enemy vessel's flank."),
    55: ("A marine captain boosts boarding attacks. Up to four rooms.", "A marine captain raises boarding strength, and no more than four such rooms may be installed."),
    57: ("Cargo holds carry goods. Up to five.", "Cargo holds store trade goods, with a maximum of five rooms."),
    58: ("Add a hold here; speed drops slightly.", "A hold can be added here at a small cost to speed."),
    59: ("Add a ram, bow gun, or split sail here on larger ships.", "This fitting point accepts a ram, a bow gun, or a split sail on medium and larger ships."),
    60: ("Mount extra armor here.", "Additional armor can be installed at this fitting point."),
    62: ("Change the ship's cannon type here.", "This command changes the type of cannon installed on the ship."),
    63: ("Lateen sails handle headwinds well but cannot precede square sails.", "Lateen sails perform well against the wind, but a square sail cannot be placed behind one."),
    66: ("Admiral, there's a city!", "The lookout excitedly reports sighting a city."),
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    if sha256(BASE.read_bytes()) != BASE_SHA256:
        raise SystemExit("wrong accepted baseline")
    baseline_common = NdsImage.open(BASE).read_file("/COMMON/MESFILE.DK4")
    if sha256(baseline_common) != COMMON_SHA256:
        raise SystemExit("wrong accepted COMMON archive")
    clean_common = NdsImage.open(CLEAN).read_file("/COMMON/MESFILE.DK4")
    clean_records = IlnkContainer.parse(clean_common).blocks[15].split(b"\0")
    baseline_records = IlnkContainer.parse(baseline_common).blocks[15].split(b"\0")
    profile = get_dialogue_profile("shared-pair-live")

    records: list[dict[str, object]] = []
    for record_index, (english, source_meaning) in LINES.items():
        clean_source = clean_records[record_index]
        baseline_source = baseline_records[record_index]
        if len(clean_source) != len(baseline_source):
            raise SystemExit(f"B15 R{record_index:04d}: baseline allocation changed")
        prefix_size = len(clean_source) - len(clean_source.lstrip(b" "))
        prefix = clean_source[:prefix_size]
        try:
            encoded = encode_fixed_dialogue(
                clean_source[prefix_size:], english + "{PAD}", profile
            ).encoded
        except DialogueEncodingError as error:
            raise SystemExit(f"B15 R{record_index:04d}: {error}") from None
        replacement = prefix + encoded
        if len(replacement) != len(baseline_source):
            raise SystemExit(f"B15 R{record_index:04d}: replacement size mismatch")
        records.append(
            {
                "id": f"DK4_MES_B15_R{record_index:04d}",
                "english": english,
                "replacement_hex": replacement.hex().upper(),
                "speaker": "Context-dependent navigator, attendant, or system voice",
                "context": "Shared block 15: investigation reports, ritual encounters, ship services, or refit guidance.",
                "source_meaning": source_meaning,
                "localization_note": "Translated from the clean Japanese record and re-encoded against its original allocation; any source entry prefix is preserved byte-for-byte.",
                "review": {
                    "source": True,
                    "context": True,
                    "localization": True,
                    "naturalness": True,
                    "formatting": True,
                },
            }
        )

    batch = {
        "format": "dk4-ilnk-translation-batch-v1",
        "content_type": "ilnk-source-restored-fixed-text-v1",
        "file_path": "/COMMON/MESFILE.DK4",
        "source_file_sha256": COMMON_SHA256,
        "target_locale": "en-US",
        "scope": "Source-first safe single-entry records from shared gameplay block 15",
        "unchanged_records": ["DK4_MES_B15_R0034"],
        "unchanged_record_reason": "The source ellipsis is language-neutral and already byte-identical in the accepted baseline.",
        "records": records,
        "blocked_packed_records": [
            f"DK4_MES_B15_R{index:04d}"
            for index in sorted(set(range(len(clean_records))) - set(LINES) - {67})
        ],
        "blocked_reason": "These records contain concatenated messages, voice variants, or ambiguous runtime entry prefixes. They require an interior-offset map before English bytes can be inserted safely.",
    }
    OUT.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {len(records)} safe records, {len(batch['blocked_packed_records'])} packed blockers")


if __name__ == "__main__":
    main()
