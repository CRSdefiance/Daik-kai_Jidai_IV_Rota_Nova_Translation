"""Bind the additional phrase/tag findings from all 284 directly viewed pages."""
from hashlib import sha256
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.plan_rafael_B0_B34_v1 import FORMATTING, ROOT


PRIOR=ROOT/'ordinary_visual_preferences_v4.json'
OUT=ROOT/'ordinary_visual_preferences_v5.json'
SHEETS=ROOT/'body_review_sheets_v1/sheet_index.json'
RULES={
 'DK4_MES_B1_R0082':dict(line_phrases=['put it away'],reason='Keep the phrasal action together rather than put / it away.'),
 'DK4_MES_B5_R0056':dict(line_phrases=['counting on you'],reason='Keep the expression of trust and its object together.'),
 'DK4_MES_B7_R0011':dict(line_phrases=['Look at those guns!'],reason='Keep the complete short armament exclamation rather than Look / at those guns.'),
 'DK4_MES_B8_R0011':dict(line_phrases=['Here we go'],reason='Keep the battle cue together rather than Here / we go.'),
 'DK4_MES_B12_R0033':dict(line_phrases=['Listen up'],reason='Keep the phrasal command together rather than Listen / up.'),
 'DK4_MES_B20_R0028':dict(line_phrases=["another, isn't it"],ordinary_boundaries=[['after','another']],
     reason='The complete 37-cell question cannot fit one 36-cell first row. Test keeping the tag with another instead of isolating the tag on its own line.'),
 'DK4_MES_B20_R0067':dict(line_phrases=['waiting for'],reason='Keep the waiting-for expression intact in Claudio\'s eager response.'),
 'DK4_MES_B21_R0005':dict(line_phrases=['finish you off'],reason='Keep the full phrasal threat together instead of finish / you off.'),
 'DK4_MES_B24_R0056':dict(line_phrases=["Why can't you understand that?!"],reason='Keep Gerhard\'s short closing question intact rather than Why can\'t / you understand that.'),
 'DK4_MES_B25_R0048':dict(line_phrases=["You've got real talent."],reason='Keep Claudio\'s complete closing compliment together instead of stranding real talent.'),
 'DK4_MES_B26_R0006':dict(line_phrases=['next time'],reason='Keep the rematch reference together rather than next / time.'),
 'DK4_MES_B26_R0171':dict(line_phrases=['these thugs, are you?!'],reason='Keep the short question tag with its subject matter rather than on a line by itself.'),
 'DK4_MES_B26_R0287':dict(line_phrases=["life on land, doesn't it?"],reason='Keep the comparison and tag together rather than isolating doesn\'t it.'),
 'DK4_MES_B26_R0310':dict(line_phrases=['welcome aboard... Aziza!'],reason='Keep Rafael\'s complete welcome together rather than welcome / aboard.'),
 'DK4_MES_B27_R0018':dict(line_phrases=['Next time'],reason='Keep Aziza\'s rematch reference together rather than Next / time.'),
 'DK4_MES_B28_R0043':dict(line_phrases=['Next time'],reason='Keep the future encounter reference together in the alternate victory threat.'),
}


def main():
    assert not OUT.exists()
    prefs,doc,sheets=map(load,(PRIOR,FORMATTING,SHEETS))
    assert sheets['pages']==284 and len(sheets['sheets'])==12
    assert all(digest(s['path'])==s['sha256'] for s in sheets['sheets'])
    byid={r['id']:r for r in doc['records']}
    for ident,rule in RULES.items():
        row=byid[ident]
        assert ident not in prefs['records'] and all(p in row['english'] for p in rule['line_phrases']),ident
        prefs['records'][ident]={**rule,'bindings':{k:sha256(row[k].encode()).hexdigest()
            for k in ('source_hex','current_hex','english')}}
    save(OUT,{**prefs,'previous_preferences':str(PRIOR),'previous_preferences_sha256':digest(PRIOR),
        'directly_viewed_sheet_index':str(SHEETS),'directly_viewed_sheet_index_sha256':digest(SHEETS),
        'additional_visual_findings':16,'all_new_candidates_need_plan_comparison_andfresh_native_visual_review':True})
    print('Saved 16 additional observed boundary candidates. No prose changes or display approval added.')


if __name__=='__main__':main()
