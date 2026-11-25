"""Try phrase-preserving constraints for four observed boundary problems; prose stays exact."""
from hashlib import sha256
from scripts.audit_story_glyph_consistency import load, save
from scripts.plan_rafael_B0_B34_v1 import FORMATTING, PREFERENCES, ROOT


OUT=ROOT/'ordinary_visual_preferences_v2.json'
RULES={
 'DK4_MES_B1_R0058':dict(line_phrases=['put it'],reason='Keep the short verb-object phrase together in Rafael\'s cabin tease.'),
 'DK4_MES_B24_R0038':dict(line_phrases=['You may not know it'],ordinary_boundaries=[['but','your']],
     reason='Keep the opening idiom intact and permit the ordinary conjunction boundary after the complete initial clause, avoiding a sparse three-line layout.'),
 'DK4_MES_B25_R0033':dict(page_clause="the distant memory of a mother's heartbeat.",
     line_phrases=['as though awakening',"a mother's heartbeat"],
     reason='A four-row partition cannot fit the unchanged stanza. Test carrying its full memory image onto page two rather than starting with a stranded of phrase.'),
 'DK4_MES_B25_R0043':dict(line_phrases=['set it to music'],reason='Keep Rafael\'s offer to set the poem to music together instead of breaking set from its object.'),
}


def main():
    assert not OUT.exists()
    doc,prefs=map(load,(FORMATTING,PREFERENCES)); byid={r['id']:r for r in doc['records']}
    for ident,rule in RULES.items():
        row=byid[ident]
        prefs['records'][ident]={**rule,'bindings':{k:sha256(row[k].encode()).hexdigest() for k in ('source_hex','current_hex','english')}}
    save(OUT,{**prefs,'candidate_constraints_require_plan_comparison_andfresh_native_review':True})
    print('Saved four phrase/layout candidates; unchanged logical prose.')


if __name__=='__main__':main()
