"""Preserve rejected trials and qualify exact phrase/quote preferences for another trial."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.refine_hodram_B211_B230_visual_v1 import PREFERENCES
from scripts.prepare_hodram_B211_B230_formatting_v1 import OUT

TARGET=OUT/'visual_preferences_v4.json'

def main():
    assert not TARGET.exists()
    doc=load(PREFERENCES);p=doc['records']
    p['DK4_MES_B217_R0042']['page_clause']='Give my sword to that hero."'
    for ident,pairs in {
        'DK4_MES_B216_R0054':[['a','dou']],
        'DK4_MES_B216_R0058':[['zhao','yun']],
        'DK4_MES_B216_R0078':[['zhuge','liang']],
        'DK4_MES_B224_R0047':[["wasn't",'it']],
        'DK4_MES_B228_R0005':[['charles','martel']],
        'DK4_MES_B228_R0045':[['charles','martel']],
        'DK4_MES_B228_R0020':[['around','here'],['what','was']],
    }.items():p[ident]['required_pairs']=pairs
    p['DK4_MES_B228_R0020']['ordinary_boundaries']=[['here','is']]
    for ident in ['SC1_B213_STYLE_8_122','SC1_B218_STYLE_8_120','SC1_B226_STYLE_8_116']:
        p[ident]['required_pairs']=[['letter','for']]
        p[ident]['ordinary_boundaries']=[['you','from']]
    save(TARGET,doc)

if __name__=='__main__':main()
