"""Keep source-approved phrases intact within the validated native width."""
from pathlib import Path

from scripts.audit_story_glyph_consistency import load, save
from scripts.write_rafael_B221_B240_contextual_v1 import digest
from scripts.draft_rafael_B249_B260_clean_v1 import OUT as ROOT

MANUSCRIPT = ROOT/'ordinary_formatting_manuscript_v1.json'
PREFS = ROOT/'ordinary_visual_preferences_v2.json'
RULES = {
    'DK4_MES_B243_R0037': dict(line_phrases=['far reaches','the Mediterranean.']),
    'DK4_MES_B245_R0030': dict(line_phrases=['sculpt with miraculous skill.']),
    'DK4_MES_B247_R0044': dict(line_phrases=['happen by.','managed to escape.']),
    'DK4_MES_B248_R0046': dict(line_phrases=['come in handy, right?']),
    'DK4_MES_B249_R0020': dict(line_phrases=["Quite a grand name, isn't it?"], page_clause='Quite a grand name,'),
    'DK4_MES_B249_R0038': dict(line_phrases=['the Isle of Skye.']),
    'DK4_MES_B251_R0119': dict(line_phrases=['jade or crystal','charges people a fortune.']),
    'DK4_MES_B252_R0116': dict(line_phrases=['turning him in',"the governor's office!"]),
    'DK4_MES_B253_R0050': dict(line_phrases=['if you get the chance.'],page_clause='You should visit'),
    'DK4_MES_B258_R0007': dict(line_phrases=['to the pyramid yet?']),
    'DK4_MES_B260_R0058': dict(line_phrases=['take it without asking?'],page_clause='But can we'),
}

if __name__ == '__main__':
    assert not PREFS.exists()
    doc = load(MANUSCRIPT)
    base = ROOT/'ordinary_visual_preferences_v1.json'
    prefs = load(base)
    prefs['previous_preferences_sha256'] = digest(base)
    for row in doc['records']:
        ident = row['id']
        if ident in RULES:
            import hashlib
            prefs['records'][ident] = {**RULES[ident], 'bindings': {
                key:hashlib.sha256(row[key].encode()).hexdigest() for key in ('source_hex','current_hex','english')},
                'reason':'Keep the marked thought or phrase intact without shortening the prose.'}
    assert prefs['records'].keys() == RULES.keys()
    save(PREFS,prefs)

