"""Keep the best existing description and document one page-saving ordinary wrap."""
from scripts.audit_story_glyph_consistency import load,save
from scripts.prepare_hodram_B211_B230_formatting_v1 import OUT

def main():
    target=OUT/'visual_preferences_v6.json';assert not target.exists()
    doc=load(OUT/'visual_preferences_v5.json');p=doc['records']
    p.pop('DK4_MES_B213_R0027')
    p['DK4_MES_B226_R0034']['required_pairs']=[['off','it']]
    p['DK4_MES_B229_R0036']['QA_line_ending_retention']=dict(line_index=0,
        exact_line='The Huns were nomadic horsemen of',
        reason='Retain the ordinary complete-word soft wrap after of. This keeps the complete source prose on one native page and preserves Western Roman Empires as a name. The following Asian origin completes its prepositional phrase immediately; no word or glyph is split. Rejecting this heuristic boundary needlessly adds a second page containing only Roman Empires. Native pixels, guards, width, complete consumption and page checks remain mandatory.')
    save(target,doc)

if __name__=='__main__':main()
