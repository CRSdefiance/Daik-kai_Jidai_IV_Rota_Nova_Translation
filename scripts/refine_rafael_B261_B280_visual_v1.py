"""Bind visual wrap findings to their exact source, predecessor and reviewed prose."""
from scripts.finish_rafael_B261_B280_native_pages_v1 import MANUSCRIPT, NATIVE, ROOT, SHEETS, digest
from scripts.write_rafael_B261_B280_contextual_v1 import load, save, sha


PREVIOUS = ROOT / 'ordinary_visual_preferences_v7.json'
OUT = ROOT / 'ordinary_visual_preferences_v11.json'
RULES = {
    'B262_R0013': dict(line_phrases=['from overseas where they are,', "but I'll make an exception for you."],
                      reason='Keep the location clause and her personal exception intact.'),
    'B263_R0009': dict(one_page=True, line_phrases=['all over the world'],
                      reason='Keep the scope of the search together without pushing the answer onto another page.'),
    'B264_R0010': dict(one_page=True, line_phrases=['all over the world', "I'm afraid", 'famous ones here.'],
                      reason='Keep the scope of the search and the opening of the reply together.'),
    'B265_R0006': dict(line_phrases=["I've got a little job for you."],
                      reason='Give the job offer a full opening row and the follow-up question its own beat.'),
    'B266_R0049': dict(line_phrases=['gets all puffed up,', 'starts bossing everybody around.'],
                      reason='Keep both parts of the idiomatic complaint intact.'),
    'B267_R0069': dict(line_phrases=["King Solomon's treasury.", 'You ought to take a look.'],
                      reason='Keep the site name and the complete follow-up invitation together.'),
    'B270_R0005': dict(line_phrases=["Let's live it up today!"],
                      reason='Keep the idiom and the rest of Jacob’s invitation together.'),
    'B270_R0047': dict(line_phrases=["by now, don't you?", "You're coming with me"],
                      reason='Keep the question tag with its lead-in and the arrest directive intact.'),
    'B273_R0011': dict(line_phrases=['client list', 'the Netherlands'],
                      reason='Keep the stolen object and destination in complete phrases.'),
    'B277_R0006': dict(line_phrases=['I need you to take down.', "I'm counting on you."],
                      reason='Keep the phrasal verb intact.'),
    'B277_R0009': dict(page_clause='From what I hear,', line_phrases=["Name's Julian Vermeer.", 'in the Mediterranean.'],
                      reason='Begin the second page with the reported lead so the location stays with the cargo work.'),
    'B279_R0026': dict(line_phrases=['as soon as you can.', 'From what I hear,'],
                      reason='Keep both the urgency and the lead’s reporting cue together.'),
    'B280_R0006': dict(line_phrases=["You've got a heart, don't you?"],
                      reason='Keep the question tag with its lead-in.'),
    'B280_R0009': dict(line_phrases=["young woman's", 'Give her a hand, would you?'],
                      reason='Keep the noun phrase and the appeal with its question tag together.'),
    'B280_R0013': dict(line_phrases=['Plett Perrault.', "You'll help her, right?"],
                      reason='Keep the established name intact and keep the tag with the appeal.'),
}


def main():
    assert not OUT.exists()
    doc, prefs, sheets = map(load, (MANUSCRIPT, PREVIOUS, SHEETS / 'sheet_index.json'))
    assert sheets['native_receipt_sha256'] == digest(NATIVE) and sheets['pages'] == 131
    assert len(sheets['sheets']) == 6
    assert all(digest(row['path']) == row['sha256'] for row in sheets['sheets'])
    rows = {row['id']: row for row in doc['records']}
    for suffix, rule in RULES.items():
        row = rows['DK4_MES_' + suffix]
        prefs['records'][row['id']] = {**rule, 'bindings': {
            key: sha(row[key].encode('utf-8')) for key in ('source_hex', 'current_hex', 'english')
        }}
    prefs.update(previous_preferences_sha256=digest(PREVIOUS), native_visual_sheet_index_sha256=digest(SHEETS/'sheet_index.json'))
    save(OUT, prefs)


if __name__ == '__main__':
    main()
