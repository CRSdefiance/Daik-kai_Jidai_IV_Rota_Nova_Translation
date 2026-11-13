"""Test smaller phrase groups and reject constraints that worsen complete clauses."""
from scripts.audit_story_glyph_consistency import load,save
from scripts.prepare_hodram_B211_B230_formatting_v1 import OUT

def main():
    target=OUT/'visual_preferences_v5.json';assert not target.exists()
    doc=load(OUT/'visual_preferences_v4.json');p=doc['records']
    p.pop('DK4_MES_B217_R0045')
    for ident in ['DK4_MES_B216_R0054','DK4_MES_B216_R0058']:
        p.pop(ident)
    r=p['DK4_MES_B213_R0027'];r.pop('page_clause');r['required_pairs']=[['bane','of']];r['ordinary_boundaries']=[['the','legendary']]
    p['DK4_MES_B224_R0061'].update(page_clause='to all of it.',required_pairs=[['all','of'],['of','it']])
    r=p['DK4_MES_B226_R0031'];r.pop('page_clause');r['required_pairs']=[['western','asia']]
    p['DK4_MES_B226_R0034']['page_clause']='chipped their blades against it.'
    p['DK4_MES_B226_R0040']['page_clause']='with the sea almost in sight.'
    p['DK4_MES_B226_R0067'].update(page_clause='grew out of that.',required_pairs=[['grew','out'],['out','of']])
    p['DK4_MES_B228_R0045']['required_pairs']=[['charles','martel'],['of','charles'],['no','less']]
    r=p['DK4_MES_B229_R0036'];r.pop('page_clause');r.update(one_page=True,ordinary_boundaries=[['horsemen','of']],required_pairs=[['western','roman'],['roman','empires']])
    p['DK4_MES_B230_R0016']['page_clause']='the resolve to face your fears.'
    save(target,doc)

if __name__=='__main__':main()
