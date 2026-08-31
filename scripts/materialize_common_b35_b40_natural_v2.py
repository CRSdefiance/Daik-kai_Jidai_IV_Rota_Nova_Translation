from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path

from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import iter_mesfile_records

ROOT = Path(__file__).resolve().parents[1]
INVENTORY_PATH = ROOT / "work/analysis/common_clean_inventory.json"
BASE_ROM = ROOT / "out/raphael_natural_v2_pre_common_accepted_rollback.nds"
SOURCE_HASH = "ecb0806b6f36f9bf4164ae46084fbbc12d4122af66b6a8920814197463f19491"


SAFE: dict[int, dict[int, str]] = {
    35: {
        1: "A boarding officer must also command troops.",
        2: "One roar from the officer rallies the troops.",
        4: "A gunner must understand gunpowder too.",
        5: "This arrow seems to sharpen an archer's focus.",
        6: "That fine edge will serve a shipwright well.",
        7: "That superb edge will serve a shipwright well.",
        8: "This edge will serve a shipwright well.",
        9: "Ancient medicine held remarkable skills.",
        10: "Knowing the body is the basis of medicine.",
        11: "Muslim medicine is said to be highly advanced.",
        12: "Wonderful... A cook's dream tool.",
        14: "Stylish boots. They should ease animal care.",
        15: "Every missionary dreams of owning this.",
        16: "A Bible anyone can understand.",
        17: "An object steeped in history.",
        18: "Winning without battle is the finest victory.",
        19: "Perhaps the great strategists of old could see the future.",
        20: "Outwitting the enemy is the heart of strategy.",
        21: "Even hard sums can be solved in an instant.",
        22: "This should prevent unfair prices in either direction.",
        23: "Mount it on any ship to speed the whole fleet.",
        24: "The crew of this ship should need less food.",
        25: "It clears dangerous clouds, so any ship will do.",
        26: "Mount it on a ship you value.",
        27: "Mount it on the ship with the strongest guns.",
        31: "A basic tool for any surveyor.",
        32: "Give it to a lookout to spot ports and discoveries.",
        33: "Fine workmanship. Northern women may value its delicacy.",
        34: "Beautiful. Great seafaring nations may prize its simple charm.",
        35: "Golden sand. Northern women are said to adore gold.",
        36: "It takes strength to use, but northern cooks would welcome it.",
        37: "Western lands will find this Eastern artwork exotic.",
        39: "Mediterranean folk raised among ruins may find this fascinating.",
        40: "This statue is famous across the Mediterranean. Many will want it.",
        41: "The Mediterranean boasts superb stained glass. They will value this.",
        42: "A girl met in China wanted this very badly.",
        44: "The Indian classics are widely read in Southeast Asia too.",
        45: "Carried from Persia to Japan, it has deep ties across Asia.",
        49: "Proof of supremacy over the Indian Ocean.",
        52: "It marks where the Mediterranean proof lies.",
        53: "It marks where the African proof lies.",
        54: "It marks where the Indian Ocean proof lies.",
        55: "It marks where the Southeast Asian proof lies.",
        56: "It marks where the East Asian proof lies.",
        57: "It marks where the New World proof lies.",
        58: "Begin the search from London.",
        59: "Begin the search from Genoa.",
    },
    36: {
        0: "This appears to be a map of the Turkish region.",
        1: "Begin the search from Sao Jorge.",
        2: "This looks like a map of Arabia.",
        3: "Head inland from Calicut.",
        5: "This is a map of the Korean Peninsula.",
        7: "Begin the search from Veracruz.",
        9: "This may relate to East Asia's proof of supremacy.",
        10: "This is surely a key to finding the New World proof.",
        11: "It may connect to the North Sea proof map.",
        12: "It seems connected to the Mediterranean proof map.",
        14: "This seems a key to the Southeast Asian proof map.",
        15: "Could this show where the East Asian proof lies?",
        16: "It may connect to the New World proof map.",
        17: "Its red outshines any ruby. Give this rare gem to the boarding officer.",
        18: "Give it to a deckhand or boarding officer.",
        19: "Give it to the boarding officer.",
        20: "Give it to a gunner.",
        21: "Give it to the purser.",
        23: "An animal horn, prized in traditional Chinese medicine.",
        24: "It holds an indescribable power. Entrust it to a proven hero.",
        25: "Such a treasure is rarely seen. Entrust it to a proven hero.",
        26: "A fragment of an ancient treasure map. Four pieces make a set.",
        27: "A fragment of an ancient treasure map. Four pieces make a set.",
        28: "A fragment of an ancient treasure map. Four pieces make a set.",
        29: "A fragment of an ancient treasure map. Four pieces make a set.",
        30: "A fragment of an ancient treasure map. Four pieces make a set.",
        31: "A fragment of an ancient treasure map. Four pieces make a set.",
        32: "A fragment of an ancient treasure map. Four pieces make a set.",
        33: "A fragment of an ancient treasure map. Four pieces make a set.",
        34: "A fragment of an ancient treasure map. Four pieces make a set.",
        35: "A fragment of an ancient treasure map. Four pieces make a set.",
        36: "A fragment of an ancient treasure map. Four pieces make a set.",
        37: "A fragment of an ancient treasure map. Four pieces make a set.",
        38: "A fragment of an ancient treasure map. Four pieces make a set.",
        39: "A fragment of an ancient treasure map. Four pieces make a set.",
        40: "A fragment of an ancient treasure map. Four pieces make a set.",
        41: "A fragment of an ancient treasure map. Four pieces make a set.",
        42: "A fragment of an ancient treasure map. Four pieces make a set.",
        43: "A fragment of an ancient treasure map. Four pieces make a set.",
        44: "A fragment of an ancient treasure map. Four pieces make a set.",
        45: "A fragment of an ancient treasure map. Four pieces make a set.",
    },
    38: {
        4: "That %s earned a fine profit. Could this be a Golden Route?",
        5: "That %s paid well. It may be a Golden Route.",
        7: "That %s paid well. Could it be a Golden Route?",
        8: "That %s made a handsome profit. It may be a Golden Route...",
        9: "That %s paid well. This must be a Golden Route!",
        10: "That %s paid well. Might this be a Golden Route?",
        11: "A Golden Route?",
        12: "A Golden Route, you say?",
        13: "What's a Golden Route?",
        14: "What's a Golden Route?",
        15: "The guild is seeking news of profitable trade routes.",
        16: "The guild is said to be seeking profitable trade routes.",
        17: "The guild is looking for news of profitable trade routes.",
        18: "The guild is looking for lucrative trade routes.",
        19: "The guild is seeking profitable trade routes.",
        20: "The guild is said to be seeking profitable trade routes.",
        21: "The guild is looking for profitable trade routes!",
        22: "The guild is reportedly seeking profitable trade routes.",
        26: "They call the most profitable routes Golden Routes and pay well for reports.",
        28: "That's amazing.",
        29: "We'll report it next time we reach a port with a guild.",
        30: "We'll tell the guild next time we reach one of its ports.",
        31: "We must tell the guild at the next port that has one.",
        32: "We must report this at the next port with a guild.",
        33: "We'll tell the guild when we next reach one of its ports.",
        34: "We must tell the guild at our next port with one.",
        35: "We'll tell the guild at the next port that has one!",
        36: "We should tell the guild at our next port with one.",
        39: "That %s paid well. Could this also be a Golden Route?",
        43: "Yes. The guild will surely recognize it!",
        44: "Yes, the guild will surely recognize it.",
        45: "Then we'll report it at the next port with a guild.",
        46: "Good. We'll tell the guild at the next port that has one.",
        47: "Then let's report it at the next port with a guild.",
        48: "Then let's tell the guild at the next port that has one.",
        49: "You found a Golden Route? Is that true?",
        50: "Selling %s bought in %s will earn a great profit.",
    },
    39: {
        0: "As a reward, for two years we'll pay %s coins whenever %s arrives.",
        1: "You found several Golden Routes? Remarkable!",
        2: "The report lists lucrative goods, including %s bought in %s.",
        3: "The report lists profitable goods, starting with %s bought in %s.",
        4: "The report lists profitable goods such as %s bought in %s.",
        5: "The report lists lucrative goods such as %s bought in %s.",
        6: "So this is it. For two years, each arrival month will pay that good's profit.",
        7: "The guild paid %s coins for discovering a Golden Route.",
    },
}

SAFE[35].update({
    1: "Boarding officers must command troops.", 2: "One roar rallies the troops.",
    4: "Gunners must know gunpowder.", 5: "This arrow sharpens a shooter's focus.",
    6: "A fine edge aids any shipwright.", 7: "A superb edge helps shipwrights.",
    8: "This edge aids any shipwright.", 9: "Old medicine had great skill.",
    10: "Know the body: medical basics.", 11: "Muslim medicine is advanced.",
    15: "A missionary's dream item.", 16: "A clear and simple Bible.",
    17: "An item steeped in history.", 18: "Best victory needs no battle.",
    19: "Old strategists may have seen the future.", 20: "Outwitting foes is true strategy.",
    21: "Hard sums solved in an instant.", 22: "This prevents unfair buying or selling.",
    23: "Mount on any ship; the fleet speeds up.", 25: "Clears dangerous clouds; any ship will do.",
    27: "Mount on your strongest gunship.", 33: "Superb craft. Northern women may prize its delicacy.",
    35: "Golden sand. Northern women adore gold.", 36: "Takes strength, but northern cooks will love it.",
    37: "Westerners will prize this Eastern art.", 40: "Many Mediterranean buyers want this famous statue.",
    41: "Mediterranean stained glass is superb and prized.", 42: "A girl in China badly wanted this item.",
    44: "These classics are widely read in Southeast Asia.",
    45: "This Persian item reached Japan and has deep Asian ties.",
    49: "Ocean proof.", 52: "Marks Mediterranean proof.", 53: "Marks African proof.",
    54: "Marks Ocean proof.", 55: "Marks Southeast Asian proof.",
    56: "Marks East Asian proof.", 57: "Marks New World proof.",
})
SAFE[36].update({
    0: "A map of Turkey.", 2: "A map of Arabia.", 5: "Map of Korea.",
    9: "May concern East Asia's proof.", 10: "Surely a key to the New World proof.",
    11: "May link to the North Sea proof map.", 12: "Linked to the Mediterranean proof map.",
    15: "Could mark the East Asian proof.", 16: "May link to the New World proof map.",
    17: "Redder than ruby; give this gem to the boarding officer.",
    18: "Deck crew or boarders should carry this.",
    23: "An animal horn prized as Chinese medicine.",
    24: "Mysterious power. Entrust this to a proven hero.",
})
for _index in range(26, 46):
    SAFE[36][_index] = "Ancient treasure-map piece; one of a set of four."
SAFE[38].update({
    5: "That %s paid well. Maybe a Golden Route.",
    7: "That %s paid well. A Golden Route, perhaps?",
    8: "That %s made a fine profit. Maybe a Golden Route...",
    9: "That %s paid well. Surely a Golden Route!",
    10: "That %s paid well. A Golden Route, perhaps?",
    11: "Golden Route?", 12: "A Golden Route?", 13: "Golden Route?", 14: "Golden Route?",
    15: "The guild seeks reports on profitable trade routes.",
    16: "The guild seeks profitable routes.", 17: "The guild wants news of profitable routes.",
    20: "The guild is seeking profitable routes.", 21: "The guild wants profitable trade routes!",
    22: "The guild reportedly seeks profitable routes.",
    26: "The best trade routes are Golden Routes. The guild pays for reports.",
    29: "We'll report it at the next port with a guild.",
    30: "We'll tell the guild at its next port.",
    31: "We must tell the guild at the next port.", 32: "We must report this at the next guild port.",
    33: "We'll tell the guild at its next port.", 36: "We should tell the guild at the next port.",
    43: "Yes. The guild will accept it!", 44: "The guild will accept it.",
    46: "Good. We'll tell the guild at the next port.",
    48: "Then let's tell the guild at the next port.",
    49: "A Golden Route? Truly?", 50: "%s's %s will sell for a fortune.",
})
SAFE[39].update({
    0: "Two years: each %s arrival pays %s coins.",
    1: "Several Golden Routes? Remarkable!",
    3: "The report lists profits, starting with %s bought in %s.",
    6: "So this is it. Two years of rewards matching each profit.",
    7: "Golden Route reward from the guild: %s coins.",
})

SAFE[35].update({
    1: "Boarders must command troops.", 5: "This arrow sharpens focus.",
    19: "Old strategists saw the future.", 22: "Stops unfair buying and selling.",
    23: "Mount it to speed the fleet.", 25: "Clears bad clouds on any ship.",
    35: "Northern women prize gold sand.", 37: "Westerners prize Eastern art.",
    42: "A Chinese girl badly wanted this.",
    44: "These classics are popular across Southeast Asia.",
})
SAFE[36].update({
    12: "Mediterranean proof-map link.",
    17: "Redder than ruby. Give this gem to boarders.",
    18: "Deck crew or boarders carry it.",
    24: "A proven hero should bear its strange power.",
})
for _index in range(26, 46):
    SAFE[36][_index] = "Old map piece; four make a set."
SAFE[38].update({
    5: "Good profit on %s. Golden Route?", 7: "Big profit on %s. Golden Route?",
    8: "Big profit on %s. Golden Route?", 9: "Big profit on %s. Golden Route!",
    10: "Big profit on %s. Golden Route?", 11: "Gold Route?",
    15: "The guild seeks profitable-route reports.",
    17: "Guild seeks profitable routes.", 20: "Guild seeks profitable routes.",
    21: "Guild seeks profitable routes!", 30: "Tell the guild at the next port.",
    31: "Tell the guild at the next port.", 33: "Tell the guild at the next port.",
    36: "Tell the guild at the next port.", 46: "Tell the guild at the next port.",
    48: "Tell the guild at the next port.",
})
SAFE[39][0] = "Two years: %s pays %s coins."
SAFE[36][17] = "Redder than ruby. Boarders should bear this gem."
SAFE[38][15] = "Guild seeks profitable routes."


PACKED = {
    35: {0, 3, 13, 28, 29, 30, 38, 43, 46, 47, 48, 50, 51},
    36: {4, 6, 8, 13, 22},
    38: {6, 23, 24, 25, 27, 37, 38, 40, 41, 42, 51},
    39: {117},
    40: set(range(31)),
}

EXCLUDED_DATA = {36: set(range(46, 65)), 37: set(range(18)), 38: {0, 1, 2, 3}, 39: set(range(8, 117))}
PADDING_ONLY = {38: {52}, 40: {31}}


def context_for(block: int) -> str:
    return {
        35: "An item expert explains an officer assignment, equipment effect, gift preference, or proof-map clue.",
        36: "An item expert identifies a map, artifact, equipment use, or ancient map fragment.",
        38: "Crew members discuss discovery and reporting of a profitable Golden Route.",
        39: "A guild official or crew member reports Golden Route rewards and profitable goods.",
    }[block]


def main() -> None:
    inventory = json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))
    clean = {(int(r["block_index"]), int(r["segment_index"])): r for r in inventory["records"] if 35 <= int(r["block_index"]) <= 40}
    mesfile = NdsImage.open(BASE_ROM).read_file("/COMMON/MESFILE.DK4")
    if sha256(mesfile).hexdigest() != SOURCE_HASH:
        raise ValueError("accepted baseline MESFILE hash does not match source lock")
    accepted = {(r.block_index, r.segment_index): r for r in iter_mesfile_records(mesfile, include_non_japanese=True) if 35 <= r.block_index <= 40}
    blocked: list[dict[str, object]] = []
    audit: list[dict[str, object]] = []
    for block in range(35, 41):
        keys = sorted(index for b, index in clean if b == block)
        safe = SAFE.get(block, {})
        packed = PACKED.get(block, set())
        excluded = EXCLUDED_DATA.get(block, set())
        padding = PADDING_ONLY.get(block, set())
        if set(keys) != set(safe) | packed | excluded | padding:
            raise ValueError(f"block {block} classification is incomplete")
        records = []
        for index in keys:
            row_id = f"DK4_MES_B{block:02d}_R{index:04d}"
            source, baseline = clean[(block, index)], accepted[(block, index)]
            if len(baseline.raw_bytes) != int(source["source_length"]):
                raise ValueError(f"{row_id}: accepted and clean allocations differ")
            if index in safe:
                classification = "single-message"
                reason = "One independently addressable message with matching clean and accepted allocation."
                english = safe[index]
                records.append({
                    "id": row_id, "english": english + "{PAD}", "speaker": "Shared item adviser or crew voice",
                    "context": context_for(block), "source_meaning": english,
                    "localization_note": "Natural, concise English preserves the clean Japanese meaning within the fixed allocation.",
                    "review": {g: True for g in ("source", "context", "localization", "naturalness", "formatting")},
                })
            elif index in packed:
                classification = "packed-multiple-entry"
                reason = "Multiple messages or table fragments share this allocation; interior entry offsets are unproven."
            elif index in excluded:
                classification = "identifier-or-promotional-data"
                reason = "Music, promotional, online-service, scene, or map identifiers are not proven dialogue records."
            else:
                classification = "padding-only"
                reason = "Blank padding-only segment is preserved byte-for-byte."
            audit.append({
                "id": row_id, "block_index": block, "segment_index": index,
                "source_offset": source["source_offset"], "source_length": source["source_length"],
                "clean_source_hex": source["source_hex"], "accepted_source_hex": baseline.raw_bytes.hex().upper(),
                "japanese_markup": source["markup"], "accepted_markup_for_structure_only": baseline.text,
                "classification": classification, "safe_to_replace": index in safe, "safety_reason": reason,
            })
            if classification not in {"single-message", "padding-only"}:
                blocked.append({
                    "id": row_id, "block_index": block, "segment_index": index,
                    "speaker": "Multiple voices or internal data", "context": reason,
                    "source_meaning": "The clean Japanese content is retained verbatim for later boundary-aware editorial translation.",
                    "source_length": source["source_length"], "japanese_markup": source["markup"],
                    "classification": classification, "blocker": reason,
                    "review": {"source": True, "context": True, "localization": False, "naturalness": False, "formatting": False},
                })
        if records:
            batch = {
                "format": "dk4-ilnk-translation-batch-v1", "file_path": "/COMMON/MESFILE.DK4",
                "source_file_sha256": SOURCE_HASH, "encoder": "dialogue-fixed-v1",
                "dialogue_profile": "shared-pair-live", "translation_policy": "natural-dialogue-v2",
                "target_locale": "en-US", "review_gates": ["source", "context", "localization", "naturalness", "formatting"],
                "inventory": {"block": block, "safe_records": len(records), "total_records": len(keys)}, "records": records,
            }
            (ROOT / f"translations/common_natural_v2_b{block}_safe.json").write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ROOT / "work/analysis/common_b35_b40_entry_audit.json").write_text(json.dumps({"records": audit}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    blocked_doc = {
        "format": "dk4-blocked-editorial-inventory-v1", "file_path": "/COMMON/MESFILE.DK4",
        "source_file_sha256": SOURCE_HASH, "blocks": [35, 36, 37, 38, 39, 40], "buildable": False,
        "records": blocked,
    }
    (ROOT / "translations/common_natural_v2_b35_b40_blocked.json").write_text(json.dumps(blocked_doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
