"""Keep complete closing thoughts together without changing prose or native width."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B176_B195_clean_20261110')
CLAUSES={
'DK4_MES_B179_R0035':'Legend says that if you dance wearing these, you can captivate any man.',
'DK4_MES_B182_R0026':'These fine swords are held to be the bane of Tokugawa, leader of Japan, and are being destroyed.',
'DK4_MES_B185_R0077':"He's probably my second favorite.",
'DK4_MES_B186_R0041':'Give my sword to that hero.',
'DK4_MES_B187_R0037':'despite persecution after persecution.',
'DK4_MES_B193_R0038':"Just like you, wouldn't you say?",
'DK4_MES_B194_R0060':'A remarkable man who would not stoop to dishonor.',
'DK4_MES_B195_R0036':'still wearing his magnificent armor...',
}


def main():
    out=ROOT/'formatting_v1/page_preferences_v2.json';assert not out.exists()
    doc=load(ROOT/'formatting_v1/formatting_input.json');rows={r['id']:r for r in doc['records']}
    prefs=load(ROOT/'formatting_v1/initial_preferences.json');assert not prefs['records']
    for key,clause in CLAUSES.items():
        row=rows[key];assert row['english'].count(clause)==1
        prefs['records'][key]=dict(page_clause=clause,reason='Keep this complete thought on one page without changing any words or narrowing the consumer.',
            exact_logical_English=row['english'],source_hex=row['source_hex'],source_reference=row['source_reference'],current_hex=row['current_hex'])
    key='DK4_MES_B191_R0031';row=rows[key]
    assert row['english']=="Admiral? What's that look for? Are you surprised to hear me taking an interest in legends?"
    prefs['records'][key]=dict(QA_line_ending_retention=dict(line_index=0,exact_line="Admiral? What's that look for?",
        reason='For belongs to the complete idiomatic question What is that look for? It is not an orphaned preposition. Retain the full-width sentence boundary; fresh native/visual/stored checks remain required.'),
        exact_logical_English=row['english'],source_hex=row['source_hex'],source_reference=row['source_reference'],current_hex=row['current_hex'])
    prefs.update(source_owned_preferences=True,no_prose_or_width_change=True,no_new_visual_or_native_approval=True,
        evidence={str(p):digest(p) for p in [ROOT/'plan_v1/automatic_plans.json',ROOT/'formatting_v1/formatting_input.json',Path(__file__)]})
    save(out,prefs);print('Prepared eight whole-thought page preferences and one exact grammatical question retention; no prose changes.')


if __name__=='__main__':main()
