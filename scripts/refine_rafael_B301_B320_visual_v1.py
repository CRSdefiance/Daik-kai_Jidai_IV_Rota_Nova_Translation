"""Bind the phrase breaks found in the 19 inspected native contact sheets."""
from scripts.audit_story_glyph_consistency import load, save
from scripts.refine_rafael_B301_B320_flow_v1 import FLOW, MANUSCRIPT, ROOT, digest, sha
from scripts.verify_rafael_B301_B320_flow_delta_v1 import FINAL, FINAL_SHEETS


OUT = ROOT / 'ordinary_visual_preferences_v5.json'
PHRASES = {
    'SC0_B301_STYLE_24_216': ('out of your mind',),
    'DK4_MES_B301_R0042': ('hang around here.',),
    'DK4_MES_B301_R0054': ('go back the way we came...',),
    'SC0_B301_STYLE_870_92': ("in here, isn't there?",),
    'SC0_B301_STYLE_1300_0': ('one of our own!',),
    'SC0_B301_STYLE_1300_200': ('one of us',),
    'SC0_B301_STYLE_1300_332': ('one of our own!',),
    'SC0_B301_STYLE_1958_0': ('bring it down...',),
    'DK4_MES_B303_R0031': ("the Indian Ocean's Proof",),
    'DK4_MES_B305_R0069': ('made it to the top!',),
    'DK4_MES_B305_R0073': ('Take care out there.',),
    'DK4_MES_B305_R0097': ('cut off from everyone else?',),
    'DK4_MES_B305_R0105': ("Look how fast it's moving.",),
    'DK4_MES_B305_R0145': ('stick together,', "won't sweep us away!"),
    'DK4_MES_B305_R0198': ('Hurry up and cross!',),
    'DK4_MES_B306_R0031': ('come down with something bad.',),
    'DK4_MES_B306_R0067': ('somewhere close by!', "I'll find it, I promise!"),
    'DK4_MES_B309_R0005': ('Dead end ahead,',),
    'DK4_MES_B310_R0078': ('Everyone, stay sharp!',),
    'DK4_MES_B310_R0163': ('All of you, give me a hand!',),
    'DK4_MES_B311_R0006': ('just the right time.',),
    'DK4_MES_B311_R0017': ('places like that,',),
    'SC0_B312_STYLE_24_284': ('lose our way,',),
    'SC0_B312_STYLE_602_28': ("let's go around it.",),
    'SC0_B312_STYLE_602_164': ('Shall we go around it?',),
    'SC0_B312_STYLE_2064_140': ('out of this desert...',),
    'DK4_MES_B313_R0022': ('one of the customers,',),
    'DK4_MES_B315_R0018': ('started pouring into the mosque,',),
    'DK4_MES_B317_R0052': ('stay away.',),
    'DK4_MES_B317_R0072': ("I've been told",),
    'DK4_MES_B317_R0118': ("coming back to tell you!",),
    'DK4_MES_B318_R0137': ('the Most Gracious,', 'the Most Merciful.'),
    'DK4_MES_B318_R0141': ('Lord of heaven and earth.', 'sent to earth...'),
    'DK4_MES_B318_R0151': ('O fortunate king,',),
    'DK4_MES_B318_R0183': ('get out of here',),
    'DK4_MES_B318_R0195': ("Let's get out of here too.",),
    'DK4_MES_B320_R0031': ('Take care on the way.',),
    'DK4_MES_B320_R0099': ('The long way around',),
}


def main():
    assert not OUT.exists()
    sheet_path = FINAL_SHEETS / 'sheet_index.json'
    preferences, doc, sheets = map(load, (FLOW, MANUSCRIPT, sheet_path))
    assert sheets['native_receipt_sha256'] == digest(FINAL) and sheets['pages'] == 444
    assert len(sheets['sheets']) == 19
    assert all(digest(sheet['path']) == sheet['sha256'] for sheet in sheets['sheets'])
    rows = {row['id']: row for row in doc['records']}
    for ident, phrases in PHRASES.items():
        row = rows[ident]
        assert ident not in preferences['records'] and all(phrase in row['english'] for phrase in phrases), ident
        preferences['records'][ident] = dict(line_phrases=phrases,
            reason='The inspected native page divides a complete phrase at the line break.',
            bindings={key: sha(row[key].encode('utf-8')) for key in ('source_hex', 'current_hex', 'english')})
    preferences.update(previous_preferences_sha256=digest(FLOW), directly_viewed_sheet_index=str(sheet_path),
                       directly_viewed_sheet_index_sha256=digest(sheet_path))
    save(OUT, preferences)


if __name__ == '__main__':
    main()
