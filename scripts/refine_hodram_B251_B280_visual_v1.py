"""Record the complete direct visual pass and byte-bound phrase/page refinements."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.prepare_hodram_B251_B280_formatting_v1 import ROOT,FORMATTING
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from dk4tool.patch.grand_race_menu_release import sha

INITIAL=ROOT/'formatting_v1/FE_plan_v2/automatic_plans.json'
NATIVE=ROOT/'native_resume_v2/compiled_native_pages.json'
VIEW=ROOT/'initial_visual_review_v2.json'
PREFERENCES=ROOT/'formatting_v1/visual_preferences_v3.json'

def main():
    assert not VIEW.exists() and not PREFERENCES.exists()
    doc,plan,native,sheets=map(load,(FORMATTING,INITIAL,NATIVE,ROOT/'initial_body_sheets_v2/sheet_index.json'))
    assert len(native['records'])==209 and native['pages']==214 and len(sheets['sheets'])==9
    assert sum(len(v['included']) for v in sheets['sheets'])==214
    assert native['fresh_compiled_alignments']==736 and native['reused_compiled_alignments']==100
    for sheet in sheets['sheets']:assert digest(sheet['path'])==sheet['sha256']
    rows={r['id']:r for r in doc['records']};findings={}
    def prefer(block,index,reason,**options):
        key=f'DK4_MES_B{block}_R{index:04d}';row=rows[key]
        findings[key]=dict(reason=reason,bindings={k:sha(row[k].encode('utf-8')) for k in ['source_hex','current_hex','english']},**options)
    prefer(251,53,'Avoid the permission question breaking after take at a page turn; test full-width one-page fit.',one_page=True)
    prefer(252,12,'Keep every named stone continuous in the riddle directions.',required_pairs=[['front','stone'],['left','stone'],['right','stone']])
    prefer(257,6,'Keep Mr. with the native FA surname instead of breaking the address.',required_pairs=[['mr','{macro:fa}']])
    prefer(259,9,'Keep the complete promise to return continuous rather than splitting go/back.',required_pairs=[["i'll",'go'],['go','back'],['back','at'],['at','once']])
    prefer(259,86,'Avoid a second page containing only with the people nearby; test one-page fit.',one_page=True)
    prefer(264,15,'Keep Gabriel Cardocci together in the identification question.',required_pairs=[['gabriel','cardocci']])
    prefer(266,6,'Keep the phrasal verb take down continuous.',required_pairs=[['take','down']])
    prefer(266,9,'Keep Julian Vermeer together and put the complete courier/location sentence on one page.',required_pairs=[['julian','vermeer']],page_clause="I hear he's working as some sort of courier in the Mediterranean.")
    prefer(267,5,'Keep the exclamatory what a phrase continuous.',required_pairs=[['what','a']])
    prefer(270,9,'Keep the whole request and short would-you tag continuous.',required_pairs=[['lend','her'],['her','a'],['a','hand'],['hand','would'],['would','you']])
    prefer(270,13,'Keep the complete approved Plett Perrault name continuous.',required_pairs=[['plett','perrault']])
    prefer(271,12,'Keep the make up for idiom continuous.',required_pairs=[['make','up'],['up','for']])
    prefer(271,66,'Keep the named Forbidden City site continuous.',required_pairs=[['forbidden','city']])
    prefer(274,76,'Avoid a page containing only like you; test one-page fit with the closing phrase intact.',one_page=True,required_pairs=[['someone','like'],['like','you']])
    prefer(277,66,'Avoid a page containing only hidden inside; test one-page fit with that phrase intact.',one_page=True,required_pairs=[['hidden','inside']])
    prefer(280,11,'Keep hiring you and Excellent work continuous in the grateful response.',required_pairs=[['hiring','you'],['excellent','work']])
    prefs=deepcopy(load(ROOT/'formatting_v1/FE_warning_preferences_v2.json'));prefs['records'].update(findings)
    save(PREFERENCES,prefs)
    menu_paths=[ROOT/'native_objects_v1/two/B251_C432/native_caption_review.png',ROOT/'native_objects_v1/two/B252_C1606/native_caption_review.png',ROOT/'native_objects_v1/three/native_caption_review_1.png']
    save(VIEW,dict(all214_initial_body_pages_directly_viewed=True,body_sheets=sheets['sheets'],
        all_three_menu_sheets_directly_viewed=True,menu_sheets=[dict(path=str(p),sha256=digest(p)) for p in menu_paths],
        scoped_name_visual_approval=str(ROOT/'scoped_names_visual_approval_v1.json'),
        initial_FE_warning_wrap_corrected=1,corrected_FE_record='DK4_MES_B252_R0184',
        all_body_glyphs_leading_trailing_characters_andfont_consistent=True,
        observed_layout_candidates=findings,initial_native_proof=str(NATIVE),initial_native_proof_sha256=digest(NATIVE),
        other_layouts_retained_reason='Readable ordinary phrase flow, full native width and complete glyphs; naturally short replies and balanced small paragraphs need no expansion or invented dramatic break.',
        all16_candidates_require_individual_final_disposition=True,offline_only=True,actual_new_batch_gameplay=False,new_credit=0,
        evidence={str(p):digest(p) for p in (FORMATTING,INITIAL,NATIVE,PREFERENCES,Path(__file__))}))
    print('All 214 initial pages and three menu sheets directly reviewed; 16 scoped visual candidates saved.')

if __name__=='__main__':main()
