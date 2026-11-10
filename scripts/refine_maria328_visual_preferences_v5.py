"""Keep final clauses whole and repair one newly observed FE extra-row defect."""
from copy import deepcopy
from hashlib import sha256
from scripts.meaning_maria328_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

def main():
    before=ROOT/'formatting_FE_v1/preferences_visual_v4.json'
    target=ROOT/'formatting_FE_v1/preferences_visual_v5.json';assert not target.exists()
    pref=deepcopy(load(before));doc=ROOT/'formatting_FE_v1/physical_manuscript.json'
    rows={r['id']:r for r in load(doc)['records']}
    rules={
        'DK4_MES_B88_R0204':dict(page_clause="but apparently you don't know about uses like these.",reason='The viewed page leaves uses like these alone after A. Keep the whole contrasting clause at the second-panel start without shortening the reveal.'),
        'DK4_MES_B94_R0073':dict(page_clause='and it will cost you your lives.',reason='The host plan separates cost from you your lives across A. Keep the complete consequence clause on the second panel; no shortened fatal warning or sparse opening is required.'),
        'DK4_MES_B92_R0017':dict(FE_planning_cells=36,reason='Fresh native row-membership checking finds an unintended extra row from this exact36-visible-cell opening. Apply the existing scoped guard reserve; all other remaining FE rows are35 or fewer and keep their existing plans.'),
    }
    for ident,fields in rules.items():
        rule=pref['records'].setdefault(ident,{})
        if 'reason' in rule:fields['reason']=rule['reason']+' '+fields['reason']
        row=rows[ident];rule.update(fields,bindings={k:sha256(row[k].encode()).hexdigest() for k in ['source_hex','current_hex','english']})
    pref.update(previous_preferences=str(before),previous_preferences_sha256=digest(before),
        native_row_failure_log=str(ROOT/'native_final_v1.log'),native_row_failure_log_sha256=digest(ROOT/'native_final_v1.log'),new_credit=0)
    save(target,pref)
    print('Selected two coherent continuation clauses andone source-bound FE row repair; unchanged prose andnative assertions.')

if __name__=='__main__':main()
