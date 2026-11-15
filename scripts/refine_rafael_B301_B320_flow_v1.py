"""Bind phrase and page-flow refinements without changing the reviewed prose."""
from scripts.audit_story_glyph_consistency import load, save
from scripts.refine_rafael_B301_B320_plan_v1 import MANUSCRIPT, PREFS, ROOT, digest, sha


PRIOR = ROOT / 'refined_plan_v1/automatic_plans.json'
FLOW = ROOT / 'ordinary_visual_preferences_v4.json'
RULES = {
    'SC0_B301_STYLE_2262_0': dict(line_phrases=['seem to have been', 'not coming after us.'],
                                  reason='Keep the speculation and the observation in coherent phrases.'),
    'DK4_MES_B301_R0238': dict(line_phrases=['get out of the cave'],
                              reason='Keep the action and its destination together.'),
    'DK4_MES_B306_R0034': dict(line_phrases=['What kind of illness is it?'],
                              reason='Keep Rafael’s entire follow-up question on a line.'),
    'DK4_MES_B306_R0112': dict(line_phrases=['be all right now.', 'gone down, too.'],
                              reason='Keep the reassurance and the fever change in complete phrases.'),
    'DK4_MES_B308_R0030': dict(line_phrases=['be all right now.', 'gone down, too.'],
                              reason='Use the same phrasing and wrap as the other recovery path.'),
    'DK4_MES_B309_R0050': dict(line_phrases=["I'll take you", 'Meet me back here'],
                              reason='Keep the guide’s promise and meeting point in readable phrases.'),
    'DK4_MES_B309_R0059': dict(line_phrases=["Yeah. It's", 'Christian village.', 'in the Mediterranean.'],
                              page_clause='You can probably find a map in a town somewhere in the Mediterranean.',
                              reason='Keep the settlement name and map lead intact and avoid an isolated opener.'),
    'DK4_MES_B310_R0104': dict(line_phrases=['getting out of here!'],
                              reason='Keep Rafael’s complete retreat directive together.'),
    'DK4_MES_B312_R0117': dict(line_phrases=["Why'd we have to"],
                              reason='Keep the opening of the sailor’s question together after the breath.'),
    'SC0_B312_STYLE_1710_124': dict(line_phrases=["to the right, isn't it?"],
                                    reason='Keep the short tag with the direction.'),
    'DK4_MES_B313_R0050': dict(line_phrases=['a better dancer.', "I didn't listen too closely."],
                              page_clause="so I didn't listen too closely.",
                              reason='Keep the effect of the earrings intact and carry a full clause over the page turn.'),
    'DK4_MES_B316_R0018': dict(line_phrases=['one of the missing explorers!'],
                              reason='Keep the missing explorer reference intact.'),
    'DK4_MES_B318_R0179': dict(line_phrases=["Let's get out of here"],
                              reason='Keep the farewell’s phrasal verb and destination intact.'),
}


def main():
    assert not FLOW.exists()
    plan, preferences, manuscript = map(load, (PRIOR, PREFS, MANUSCRIPT))
    assert plan['manuscript_sha256'] == digest(MANUSCRIPT)
    assert plan['visual_preferences_sha256'] == digest(PREFS)
    rows = {row['id']: row for row in manuscript['records']}
    for ident, rule in RULES.items():
        row = rows[ident]
        phrases = rule.get('line_phrases', []) + ([rule['page_clause']] if 'page_clause' in rule else [])
        assert all(phrase in row['english'] for phrase in phrases), ident
        assert 'FE_planning_cells' not in preferences['records'].get(ident, {})
        preferences['records'][ident] = {**rule, 'bindings': {
            key: sha(row[key].encode('utf-8')) for key in ('source_hex', 'current_hex', 'english')
        }}
    preferences.update(previous_plan_sha256=digest(PRIOR), previous_preferences_sha256=digest(PREFS))
    save(FLOW, preferences)


if __name__ == '__main__':
    main()
