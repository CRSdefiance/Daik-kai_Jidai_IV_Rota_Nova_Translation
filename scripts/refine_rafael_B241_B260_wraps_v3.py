"""Apply phrase and page refinements from the full visual review."""
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.refine_rafael_B241_B260_wraps_v1 import MANUSCRIPT, ROOT, digest


RULES = {
    'B241_R0025': dict(line_phrases=["Didn't you say something like that", 'about the armadillo thing?'],
        reason='Use three rows and keep the armadillo reference together.'),
    'B242_R0018': dict(line_phrases=['What brought that on?'],
        reason='Give the complete follow-up question its own row.'),
    'B242_R0068': dict(line_phrases=['the work you put in,', 'the Phoenix Bascinet.'],
        reason='Keep put in and the item title intact.'),
    'B243_R0037': dict(one_page=True, line_phrases=['far reaches', 'the Mediterranean.'],
        reason='Use four full rows and keep the geographical phrase on one page.'),
    'B245_R0030': dict(one_page=True, line_phrases=['after he died.', 'can sculpt with miraculous skill.'],
        reason='Keep the complete chisel effect on one page.'),
    'B247_R0044': dict(one_page=True, line_phrases=['happen by.', 'merchant fleet managed to escape.'],
        reason='Keep the rescue and escape on one page without stranding the fleet’s verb.'),
    'B248_R0046': dict(one_page=True, line_phrases=["even if you don't use it to gamble,", 'come in handy, right?'],
        reason='Keep Jam’s qualification and final tag on the same page.'),
    'B249_R0031': dict(page_clause='All this nonsense,', line_phrases=['a genius with a bow.', 'the ship still needs tending!'],
        reason='Start the continuation with the complaint instead of its conjunction.'),
    'B249_R0038': dict(page_clause='Others swear', line_phrases=['the Isle of Skye.', 'saw it on Lewis.'],
        reason='Keep the rival Lewis rumor as a complete sentence after the page turn.'),
    'B250_R0064': dict(line_phrases=['no question.', 'got to believe me!'],
        reason='Keep the insistence together at each boundary.'),
    'B251_R0084': dict(line_phrases=['Why do you ask about the New World?'],
        reason='Place Rafael’s entire question on its own row.'),
    'B251_R0119': dict(one_page=True, line_phrases=['jade or crystal', 'and charges people a fortune.'],
        reason='Use four available rows and keep the rumor and sales trick on one page.'),
    'B252_R0106': dict(line_phrases=["what you came for, isn't it?"],
        reason='Keep the preposition and question tag with the preceding phrase.'),
    'B252_R0116': dict(page_clause="I'm turning him in", line_phrases=['turning him in', "at the governor's office!"],
        reason='Start the next page with the barkeep’s decision instead of the particle in.'),
    'B253_R0050': dict(one_page=True, line_phrases=['wooden church', 'if you get the chance.'],
        reason='Keep the building description and invitation on one page.'),
    'B255_R0019': dict(line_phrases=["A sailor who'd been", 'the New World', 'gold dust'],
        reason='Avoid the sparse opening and keep the place name and gold dust together.'),
    'B256_R0006': dict(line_phrases=['Hey, have you heard', 'the Lamenting Jar?'],
        reason='Keep the question cue and item title intact around the name substitution.'),
}


def main():
    previous = ROOT / 'ordinary_visual_preferences_v3.json'
    target = ROOT / 'ordinary_visual_preferences_v4.json'
    assert not target.exists()
    prefs, manuscript = map(load, (previous, MANUSCRIPT))
    rows = {row['id']: row for row in manuscript['records']}
    for suffix, rule in RULES.items():
        ident = 'DK4_MES_' + suffix
        row = rows[ident]
        prefs['records'][ident] = {**rule, 'bindings': {
            key: sha(row[key].encode('utf-8')) for key in ('source_hex', 'current_hex', 'english')}}
    prefs['previous_preferences_sha256'] = digest(previous)
    save(target, prefs)


if __name__ == '__main__':
    main()
