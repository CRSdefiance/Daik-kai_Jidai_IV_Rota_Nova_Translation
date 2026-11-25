"""Resolve the initial wrap warnings and three stranded story page endings."""
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.plan_rafael_B181_B187_story_v1 import ROOT, FORMATTING, PREFERENCES


OUT = ROOT / 'story_formatting_manuscript_v2.json'
PREFS = ROOT / 'story_visual_preferences_v2.json'
REPLACEMENTS = {
    (181, 152): ("Why are you so impressed? This is ridiculous. Let's go!",
        "Keep Claudio's irritation and brisk decision to leave after Rafael praises Yifa."),
    (183, 47): ("To avoid training, she left the mountain without our teacher's leave. She even left the country. It's inexcusable.",
        "Preserve her reason for leaving, the lack of permission, the mountain, the country and Sanghyeon's disapproval."),
    (185, 43): ("Was that his name? I'm sorry, I don't remember. I think he went to the Tomb of King Muryeong.",
        "Keep Reika's apology and uncertainty about Julian's name and where he went."),
    (186, 168): ("That'd be a fine reason, but no. My grandfather sailed the world. I've wanted to follow his example since I was a boy.",
        "Keep the flirtatious joke, actual grandfather, worldwide voyages and childhood admiration."),
    (186, 171): ("What's the world like? And the town where my grandfather was born? I want to find out. That's why I want to go.",
        "Keep the wider world and his grandfather's birthplace as the two questions motivating his voyage."),
}
PHRASES = {
    (187, 26): ('get to know each other.',),
    (187, 51): ('Stay out of it!',),
    (187, 72): ("We'll settle this at sea!",),
}


def main():
    assert not OUT.exists() and not PREFS.exists()
    doc, preferences = map(load, (FORMATTING, PREFERENCES))
    seen = set()
    for row in doc['records']:
        key = row['block'], row['source_record_index']
        if key not in REPLACEMENTS and key not in PHRASES:
            continue
        note = 'Keep the complete spoken unit together in the native modal layout.'
        if key in REPLACEMENTS:
            replacement, note = REPLACEMENTS[key]
            assert row['decision'] == 'revision' and not row['native_literal_tokens']
            row.update(visual_revision_previous_English=row['english'], english=replacement,
                editorial_logical_English=replacement, planned_English_markup=f"{{SPEAKER:{row['source_selector']:02X}}}" + replacement,
                finding=note, localization_note=note)
        pref = preferences['records'].get(row['id'], {})
        phrases = PHRASES.get(key, pref.get('line_phrases', ()))
        assert all(p in row['english'] for p in phrases)
        if phrases:
            preferences['records'][row['id']] = dict(line_phrases=phrases, reason=note,
                bindings={k: sha(row[k].encode('utf-8')) for k in ('source_hex','current_hex','english')})
        seen.add(key)
    assert seen == set(REPLACEMENTS) | set(PHRASES)
    doc.update(previous_manuscript=str(FORMATTING), previous_manuscript_sha256=sha(FORMATTING.read_bytes()),
        source_bound_read_aloud_refinements=sorted(seen), authored_breaks=0)
    save(OUT,doc)
    save(PREFS,preferences)


if __name__ == '__main__':
    main()
