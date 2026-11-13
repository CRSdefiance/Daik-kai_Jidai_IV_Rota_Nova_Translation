"""Bind reviewed phrase/page preferences without changing prose, controls or widths."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/Maria_B216_B252_clean_20261110')
PHRASES={
'DK4_MES_B216_R0017':(["who'd been",'gold dust'],'Avoid the sparse opening and preserve the gold-dust noun phrase.'),
'DK4_MES_B219_R0009':(["King Solomon's"],'Keep the ruler reference together rather than ending a row on King.'),
'DK4_MES_B221_R0011':(['stays the same'],'Keep the final unchanged-water condition together in the puzzle instruction.'),
'DK4_MES_B221_R0052':(['get out of here','go back'],'Preserve the escape and return phrasal verbs.'),
'DK4_MES_B225_R0020':(['no! I'],'Avoid an unsupported six-character opening row before the actual request.'),
'DK4_MES_B230_R0018':(['interrupt, but','Jean Ramusio'],'Avoid a sparse opening and keep the exact personal name together.'),
'DK4_MES_B234_R0037':(["What's your type?"],'Keep the short personal question coherent rather than stranding its interrogative.'),
'DK4_MES_B235_R0008':(['eyes off'],'Keep the central eyes-off phrasal expression intact.'),
'DK4_MES_B235_R0070':(["Wouldn't it"],'Keep the short question lead together.'),
'DK4_MES_B244_R0069':(['northern continent'],'Keep the geographical noun phrase together.'),
'DK4_MES_B249_R0014':(['counting on you'],'Keep the trust expression together rather than ending the row before you.'),
}


def main():
    out=ROOT/'formatting_v1/page_phrase_preferences_v1.json';assert not out.exists()
    path=ROOT/'formatting_v1/formatting_input.json';doc=load(path);rows={r['id']:r for r in doc['records']}
    prefs=load(ROOT/'formatting_v1/initial_preferences.json');assert not prefs['records']
    def entry(key):return prefs['records'].setdefault(key,dict(bindings={k:sha(rows[key][k].encode()) for k in ['source_hex','current_hex','english']}))
    for key,(phrases,reason) in PHRASES.items():
        pairs=[]
        for phrase in phrases:
            assert rows[key]['english'].count(phrase)==1
            words=[w.lower().strip('.,!?;:"()') for w in phrase.split()]
            pairs.extend([list(p) for p in zip(words,words[1:])])
        entry(key).update(required_pairs=pairs,reason=reason)
    key='DK4_MES_B237_R0011';entry(key).update(one_page=True,page_clause='He stole a ship and fled.',
        reason='The132-character report can use the validated full width; avoid a second page containing only and fled and keep its final sentence coherent.')
    key='DK4_MES_B247_R0060';entry(key).update(page_clause="They say someone's found a pictorial map showing the way there.",
        reason='If pagination is required, keep the complete pictorial-map report on one page rather than leaving the way there alone.')
    prefs.update(source_owned_preferences=True,no_prose_or_width_change=True,no_new_visual_or_native_approval=True,
        planned_text_review_only=True,evidence={str(p):digest(p) for p in [path,ROOT/'plan_v1/automatic_plans.json',Path(__file__)]})
    save(out,prefs);print('Prepared13 byte-bound phrase/page preferences; no prose/geometry changes or display approval.')


if __name__=='__main__':main()
