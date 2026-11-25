"""Keep two phrasal verbs andavoid a sparse peace lead-in;retain the better illness wrap."""
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.meaning_maria_B51_B52_clean_v1 import ROOT
def main():
    old=ROOT/'formatting_v1/preferences_v6_page_retention.json';out=ROOT/'formatting_v1/preferences_v7_complete_clauses.json'
    assert not out.exists();p=load(old)
    p['records']['DK4_MES_B51_R0031']['required_pairs']=[['cut','off'],['hundred','years'],['years','ago']]
    p['records']['DK4_MES_B51_R0082']['required_pairs']=[['swept','up']]
    for ident in ['DK4_MES_B53_R0127','DK4_MES_B54_R0132']:
        p['records'][ident]['ordinary_boundaries']=[['come','to']]
        p['records'][ident]['reason']+=' A normal come/to location boundary avoids a sparse and peace opening on page2;the complete peace clause remains together.'
    p['records'].pop('DK4_MES_B55_R0127')
    p.update(previous_preferences=str(old),previous_preferences_sha256=digest(old),
        layout_retentions=[dict(id='DK4_MES_B55_R0127',reason='Retain the initial native-safe three-row reassurance. Forcing worried about together expands it to four rows andcreates a weaker across/the sea tail;the complete-word original is more readable.')],
        all_words_andsource_controls_unchanged=True,new_credit=0)
    save(out,p)
if __name__=='__main__':main()
