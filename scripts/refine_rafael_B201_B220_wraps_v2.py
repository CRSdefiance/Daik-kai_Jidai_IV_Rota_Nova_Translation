"""Improve the reviewed reading flow with exact phrase and sentence boundaries."""
from scripts.audit_story_glyph_consistency import load, save
from scripts.plan_rafael_B201_B220_v1 import FORMATTING, ROOT, digest
from scripts.refine_rafael_B201_B220_wraps_v1 import OUT as PRIOR_PREFERENCES
from dk4tool.patch.grand_race_menu_release import sha


OUT = ROOT/'ordinary_formatting_manuscript_v2.json'
PREFS = ROOT/'ordinary_visual_preferences_v3.json'
EDIT = {
    'B205_R0025': ("They're called chili peppers. I hear they're a kind of spice. They go great with the ingredients we get around here.",
        'Keep her conversational explanation, reported classification and praise for how the peppers go with local ingredients.'),
    'B208_R0229': ("(Maybe now's the time to buy.)",
        'Give Carlo a concise private suggestion, preserving both the timing and the tentativeness.'),
}
PHRASES = {
    'B201_R0026': (["just because it's fashionable."], 'Keep the reason for the buying frenzy intact.'),
    'B203_R0068': (['just because'], 'Keep the causal expression together.'),
    'B203_R0088': (['get our hands on'], 'Keep the expression for securing the dye intact.'),
    'B205_R0025': (["I hear they're", 'go great with'], 'Avoid a stranded subject and keep the cooking expression together.'),
    'B208_R0077': (['get him to lower','twice more.'], 'Keep the bargaining action and the number of further reductions intact.'),
    'B218_R0029': (["These aren't just any earrings."], 'Keep the whole boast together after the little laugh.'),
    'B218_R0048': (['just like that.','in no time.'], 'Keep each time phrase together and turn at the sentence boundary.'),
    'B218_R0100': (['Get lost.'], 'Keep the sudden dismissal as a single beat.'),
    'B218_R0119': (["don't get it"], 'Keep the expression for failing to understand together.'),
    'B220_R0073': (['I just have a feeling'], 'Keep the tentative hunch together.'),
}


def main():
    assert not OUT.exists() and not PREFS.exists()
    doc,prefs = map(load,(FORMATTING,PRIOR_PREFERENCES))
    rows = {r['id'].removeprefix('DK4_MES_'):r for r in doc['records']}
    for key,(text,note) in EDIT.items():
        row = rows[key]
        assert row['decision']=='revision' and not row['native_literal_tokens']
        row.update(visual_revision_previous_English=row['english'],english=text,
            editorial_logical_English=text,planned_English_markup=f"{{SPEAKER:{row['source_selector']:02X}}}"+text,
            finding=note,localization_note=note)
    del prefs['records']['DK4_MES_B208_R0229']
    for key,(phrases,note) in PHRASES.items():
        row = rows[key]
        assert all(p in row['english'] for p in phrases)
        prior = prefs['records'].get(row['id'],{})
        prefs['records'][row['id']] = {**prior,'line_phrases':phrases,'reason':note,
            'bindings':{k:sha(row[k].encode('utf-8')) for k in ('source_hex','current_hex','english')}}
    doc.update(previous_manuscript=str(FORMATTING),previous_manuscript_sha256=digest(FORMATTING),
        no_prose_changes_or_manual_breaks=False,author_inserted_ordinary_breaks=0,source_bound_read_aloud_refinements=sorted(EDIT))
    prefs['prior_plan_diagnostics_sha256']=digest(ROOT/'ordinary_plans_v2/diagnostics.json')
    save(OUT,doc)
    save(PREFS,prefs)


if __name__ == '__main__':
    main()

