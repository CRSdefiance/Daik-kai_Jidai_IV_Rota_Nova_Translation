from scripts.audit_story_glyph_consistency import load, save
from scripts.refine_rafael_B241_B260_wraps_v1 import ROOT, PREFS
from scripts.write_rafael_B221_B240_contextual_v1 import digest

if __name__ == '__main__':
    target = ROOT/'ordinary_visual_preferences_v3.json'
    assert not target.exists()
    doc = load(PREFS)
    rules = doc['records']
    del rules['DK4_MES_B249_R0020']['page_clause']
    rules['DK4_MES_B252_R0116']['line_phrases'] = ["at the governor's office!"]
    rules['DK4_MES_B258_R0007']['line_phrases'] = ['Hey, have you been','to the pyramid yet?']
    doc['previous_preferences_sha256'] = digest(PREFS)
    save(target,doc)
