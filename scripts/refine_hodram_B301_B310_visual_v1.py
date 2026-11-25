"""Record the direct page review and test byte-bound phrase/page refinements."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.prepare_hodram_B301_B310_formatting_v1 import ROOT,FORMATTING

INITIAL=ROOT/'formatting_v1/FE_plan_v2/automatic_plans.json'
NATIVE=ROOT/'native_resume_v3/compiled_native_pages.json'
PREFERENCES=ROOT/'formatting_v1/visual_preferences_v3.json'
VIEW=ROOT/'initial_visual_review_v3.json'

def main():
    assert not VIEW.exists() and not PREFERENCES.exists()
    doc,plan,native,sheets=map(load,(FORMATTING,INITIAL,NATIVE,ROOT/'initial_body_sheets_v2/sheet_index.json'))
    assert len(native['records'])==225 and native['pages']==229 and len(sheets['sheets'])==10
    assert sum(len(s['included']) for s in sheets['sheets'])==229
    assert all(digest(s['path'])==s['sha256'] for s in sheets['sheets'])
    rows={r['id']:r for r in doc['records']}
    preferences=deepcopy(load(ROOT/'formatting_v1/FE_guard_preferences_v2.json'))
    findings={}
    def prefer(ident,reason,**options):
        row=rows[ident]
        value={**preferences['records'].get(ident,{}),**options,'reason':reason,
            'bindings':{k:sha(row[k].encode()) for k in ['source_hex','current_hex','english']}}
        preferences['records'][ident]=value;findings[ident]=value
    def ordinary(block,index,reason,**options):
        prefer(f'DK4_MES_B{block}_R{index:04d}',reason,**options)
    def style(block,command,offset,reason,**options):
        prefer(f'SC1_B{block}_STYLE_{command}_{offset}',reason,**options)
    ordinary(302,141,'Keep the complete wait-a-little phrase together instead of a detached a-little row.',
        one_page=True,required_pairs=[['wait','a'],['a','little']])
    for block,index in [(302,137),(309,294)]:
        ordinary(block,index,'Test a complete second sentence on its own row instead of stranding Some. Preserve the scoped FE36 split-word repair where present.',
            required_pairs=[['some','appear']])
    ordinary(309,249,'Keep the complete I-am-truly-sorry apology together after the counterfactual.',
        one_page=True,required_pairs=[['i','am'],['am','truly'],['truly','sorry']])
    ordinary(310,16,'Avoid a page ending I-will-tell and a second page beginning you. Test full one-page fit without shortening the clandestine offer.',
        one_page=True,required_pairs=[["i'll",'tell'],['tell','you'],['keep','it'],['it','quiet']])
    style(302,1320,36,'Keep Let-us-proceed together instead of stranding Let at the previous row end.',
        one_page=True,required_pairs=[['let','us'],['us','proceed']])
    style(302,1320,216,'Keep go-on together in the decision to continue.',one_page=True,required_pairs=[['go','on']])
    style(302,1786,62,'Keep the complete what-shall-we-do question together after the Admiral address.',
        one_page=True,required_pairs=[['what','shall'],['shall','we'],['we','do']])
    style(302,1786,412,'Keep the complete what-should-we-do question together rather than stranding What.',
        one_page=True,required_pairs=[['what','should'],['should','we'],['we','do']])
    for offset in [0,90,300,498,716]:
        style(308,8,offset,'Keep far northeast of China continuous; remove the short of-China page where a full-width one-page fit is possible without changing prose.',
            one_page=True,required_pairs=[['far','northeast'],['northeast','of'],['of','china']])
    style(309,1590,0,'Keep prompt-treatment together in the prospective injury reassurance.',
        one_page=True,required_pairs=[['prompt','treatment']])
    for offset in [122,236]:
        style(309,1590,offset,'Keep the-wolf-has-gone reassurance continuous rather than stranding the contraction.',
            one_page=True,required_pairs=[["wolf's",'gone']])
    style(309,1590,394,'Keep right-away and the complete That-is-a-relief response together.',
        one_page=True,required_pairs=[['right','away'],["that's",'a'],['a','relief']])
    style(309,2758,32,'Keep the short question tag with the forest phrase instead of leaving only arent-we on the final row.',
        one_page=True,required_pairs=[['the','forest'],['forest',"aren't"],["aren't",'we']])
    assert len(findings)==19
    menu_paths=[ROOT/f'native_objects_v1/two/{key}/native_caption_review.png'
        for key in ['B302_C1226','B302_C2272','B304_C576']]
    menu_paths.append(ROOT/'native_objects_v1/three/native_caption_review_1.png')
    assert all(p.exists() for p in menu_paths)
    save(PREFERENCES,preferences)
    save(VIEW,dict(all229_initial_body_pages_directly_viewed=True,body_sheets=sheets['sheets'],
        all_four_menu_sheets_directly_viewed=True,menu_sheets=[dict(path=str(p),sha256=digest(p)) for p in menu_paths],
        scoped_name_visual_approval=str(ROOT/'scoped_names_visual_approval_v1.json'),
        all_body_glyphs_leading_trailing_characters_andfont_consistent=True,
        corrected_native_split_word_record='DK4_MES_B309_R0294',
        split_word_repair_not_a_blank_row=True,observed_layout_candidates=findings,
        initial_native_proof=str(NATIVE),initial_native_proof_sha256=digest(NATIVE),
        other_layouts_retained_reason='Complete short replies, natural ordinary continuations and readable balanced rows work. Keep their wording and formatter-owned breaks without invented dramatic pauses.',
        all19_candidates_require_individual_final_disposition=True,offline_only=True,
        actual_new_batch_gameplay=False,new_credit=0,
        evidence={str(p):digest(p) for p in (FORMATTING,INITIAL,NATIVE,PREFERENCES,Path(__file__))}))
    print('Viewed229 body pages, four menus and eight scoped names; saved19 layout candidates with zero credit.')

if __name__=='__main__':main()
