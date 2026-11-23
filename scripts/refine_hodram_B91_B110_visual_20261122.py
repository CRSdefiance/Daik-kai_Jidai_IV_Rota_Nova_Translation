"""Apply the visual pass's prose and phrase-boundary refinements."""

from scripts import review_hodram_B95_B110_20261122 as previous


base = previous.base
OUTPUT = previous.COMBINED.with_name("B91_B110_contextual_v3.json")
PHRASES = {
    "91_R0042": ("doubt miracles", "get shipwrecked!", "better off than that!"),
    "91_R0050": ("got carried away", "didn't mean to insult"),
    "91_R0075": ("someone like you", "to have it.", "my lucky charm,", "in no shape"),
    "93_R0064": ("town's known for?",),
    "101_R0040": ("worry about Cristina.",),
    "101_R0043": ("trust her, Admiral.", "still my granddaughter.", "old man's side."),
    "101_R0060": ("piece of armor,", "the Mediterranean.", "the Black Sea?", "in earnest, but..."),
    "101_R0063": ("Cristina's like Minerva?", "that shield.", "I'd like her to have it..."),
    "103_R0045": ("New World.",),
    "104_R0042": ("looking for.",),
    "110_R0059": ("map to the Proof", "two Map Keys"),
}
WORDING = {"91_R0042": "Some people doubt miracles and still get shipwrecked! You're better off than that!"}


def main():
    assert not OUTPUT.exists()
    draft = base.load(previous.COMBINED)
    found = set()
    for row in draft["records"]:
        ident = row["id"].partition("_B")[2]
        if row["block"] == 97:
            row["context"] = row["context"].replace("Samwell", "Angelo")
            for key in ("source_meaning", "localization_note"):
                row[key] = row[key].replace("Samwell", "Angelo")
        if row["block"] == 101:
            row["context"] = row["context"].replace("Athena", "Minerva")
        if ident in ("110_R0015", "110_R0069"):
            beat = "wordless question" if ident == "110_R0015" else "silent pause"
            assert row["source_selector"] == 207
            row["source_meaning"] = f"The original CF selector uses runtime role zero for this {beat}."
            row["localization_note"] = f"Keep the {beat} and preserve the role selector, which resolves the name at runtime."
        if ident not in PHRASES:
            continue
        found.add(ident)
        assert row["decision"] == "revision"
        row["english"] = WORDING.get(ident, row["english"])
        phrases = PHRASES[ident]
        assert all(phrase in row["english"] for phrase in phrases)
        row["protected_phrases"] = list(phrases)
        row["visual_wrap_finding"] = (
            "The first preview broke this speech earlier than necessary. Keep the short reading units together "
            "and allow the remaining speech to use the available width."
        )
    assert found == set(PHRASES)
    base.save(OUTPUT, draft)


if __name__ == "__main__":
    main()

