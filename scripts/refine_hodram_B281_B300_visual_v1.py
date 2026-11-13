"""Record the complete direct visual pass and test source-bound phrase/page improvements."""
from copy import deepcopy
from scripts.audit_story_glyph_consistency import load,save
from scripts.prepare_hodram_B281_B300_formatting_v1 import ROOT,FORMATTING
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from dk4tool.patch.grand_race_menu_release import sha

INITIAL=ROOT/'formatting_v1/FE_plan_v2/automatic_plans.json'
NATIVE=ROOT/'native_resume_v2/compiled_native_pages.json'
VIEW=ROOT/'initial_visual_review_v2.json'
PREFERENCES=ROOT/'formatting_v1/visual_preferences_v3.json'


def main():
    assert not VIEW.exists() and not PREFERENCES.exists()
    doc,plan,native,sheets=map(load,(FORMATTING,INITIAL,NATIVE,ROOT/'initial_body_sheets_v2/sheet_index.json'))
    assert len(native['records'])==373 and native['pages']==375 and len(sheets['sheets'])==16
    assert sum(len(s['included']) for s in sheets['sheets'])==375
    assert (native['fresh_compiled_alignments'],native['reused_compiled_alignments'])==(1132,360)
    assert all(digest(s['path'])==s['sha256'] for s in sheets['sheets'])
    rows={r['id']:r for r in doc['records']};findings={};prefs=deepcopy(load(ROOT/'formatting_v1/FE_guard_preferences_v2.json'))
    def prefer_id(ident,reason,**options):
        row=rows[ident];assert ident not in findings
        value=dict(reason=reason,bindings={k:sha(row[k].encode()) for k in ['source_hex','current_hex','english']},**options)
        findings[ident]=value;prefs['records'][ident]=value
    def prefer(block,index,reason,**options):
        prefer_id(f'DK4_MES_B{block}_R{index:04d}',reason,**options)
    def style(block,command,index,reason,**options):
        row=next(r for r in rows.values() if r['block']==block and r.get('source_command_offset')==command
            and index in r.get('source_style_indices',[]))
        prefer_id(row['id'],reason,**options)
    prefer(282,19,'Keep Iscal Yasar together and avoid a second page containing only counting on you. Test complete one-page fit.',
        one_page=True,required_pairs=[['iscal','yasar'],['i','am'],['am','counting'],['counting','on'],['on','you']])
    prefer(286,5,'Keep the I-need-you request and take-down verb continuous without adding a page.',one_page=True,
        required_pairs=[['i','need'],['need','you'],['you','to'],['take','down']])
    prefer(286,16,'Keep struck out together in the breakaway report.',one_page=True,required_pairs=[['struck','out']])
    prefer(286,75,'Test keeping one after another together; retain the original if the new opening is worse.',one_page=True,
        required_pairs=[['one','after'],['after','another']])
    prefer(287,77,'The opening Our ancestors is sparse because of the long reported verb phrase. Test an ordinary said/to boundary without a waiver.',
        one_page=True,ordinary_boundaries=[['said','to']])
    prefer(287,125,'Avoid a second page containing only you in the search; keep Once you, the named map and the join-you phrase continuous.',
        one_page=True,required_pairs=[['once','you'],['ancient','city'],['city','map'],["i'll",'join'],['join','you']])
    prefer(294,143,'Keep the complete Let us press on instruction together.',one_page=True,
        required_pairs=[['let','us'],['us','press'],['press','on']])
    prefer(295,21,'Keep only a rumor together rather than stranding Only before the final row.',one_page=True,required_pairs=[['only','a'],['a','rumor']])
    prefer(296,37,'Keep heading back together; a short complete opening question is acceptable if the second sentence stays whole.',one_page=True,
        required_pairs=[["we're",'heading'],['heading','back']])
    prefer(296,50,'Keep a great deal together so the article is not stranded at the end of the first row.',one_page=True,
        required_pairs=[['a','great'],['great','deal']])
    prefer(296,63,'Test keeping plenty of sulfur and I will make it continuous without adding a page.',one_page=True,
        required_pairs=[['plenty','of'],['of','sulfur'],["i'll",'make'],['make','it']])
    prefer(299,269,'Keep Please take shelter together as a complete evacuation instruction.',one_page=True,
        required_pairs=[['please','take'],['take','shelter']])
    prefer(300,174,'Keep give me a hand together in the urgent help request.',one_page=True,
        required_pairs=[['give','me'],['me','a'],['a','hand']])
    prefer(300,197,'Keep the complete welfare question and all right together after the breath sound.',one_page=True,
        required_pairs=[['are','you'],['you','all'],['all','right']])
    for block in [290,300]:
        style(block,24,5,'Keep the future lose-our-way warning continuous rather than stranding we will.',one_page=True,
            required_pairs=[["we'll",'lose'],['lose','our'],['our','way']])
    style(290,328,7,'Keep the complete May nothing find us wish together.',one_page=True,
        required_pairs=[['may','nothing'],['nothing','find'],['find','us']])
    style(290,1166,1,'Keep refuses to leave together instead of a short detached to-leave row.',one_page=True,
        required_pairs=[['refuses','to'],['to','leave']])
    for index in [0,6]:
        style(290,1924,index,'Keep scare/scared it together in the failed-intimidation reaction.',one_page=True,
            required_pairs=[[('scare' if index==0 else 'scared'),'it']])
    style(290,1924,1,'Keep make it flee together rather than breaking the causative phrase.',one_page=True,
        required_pairs=[['make','it'],['it','flee']])
    style(290,2398,0,'Keep we will be in danger continuous in the warning.',one_page=True,required_pairs=[["we'll",'be']])
    for index in [2,3]:
        style(290,2398,index,'Keep One of together so the quantifier is not stranded after the alarm.',one_page=True,
            required_pairs=[['one','of']])
    style(290,2398,4,'Keep we would better run together after the uncertain injury question.',one_page=True,
        required_pairs=[["we'd",'better'],['better','run']])
    style(290,3300,4,'Keep the complete forest-exit statement and affirmative ruins recognition continuous.',one_page=True,
        required_pairs=[["we're",'out'],['out','of'],['of','the'],['the','forest'],['yes','those'],['those','are']])
    style(291,24,3,'Keep get lost together in the map warning.',one_page=True,required_pairs=[['get','lost']])
    style(291,824,3,'Keep I have got a bad feeling together after the complete question.',one_page=True,
        required_pairs=[["i've",'got'],['got','a'],['a','bad'],['bad','feeling']])
    style(291,2194,0,'Keep It is not following us together instead of stranding the contraction.',one_page=True,
        required_pairs=[["it's",'not'],['not','following'],['following','us']])
    style(294,28,7,'Keep any farther together in the map prerequisite.',one_page=True,required_pairs=[['any','farther']])
    assert len(findings)==30
    menu_paths=[ROOT/f'native_objects_v1/two/{key}/native_caption_review.png' for key in ['B290_C1876','B291_C1114','B294_C820','B300_C560']]
    menu_paths.append(ROOT/'native_objects_v1/three/native_caption_review_1.png')
    save(PREFERENCES,prefs)
    save(VIEW,dict(all375_initial_body_pages_directly_viewed=True,body_sheets=sheets['sheets'],
        all_five_menu_sheets_directly_viewed=True,menu_sheets=[dict(path=str(p),sha256=digest(p)) for p in menu_paths],
        scoped_name_visual_approval=str(ROOT/'scoped_names_visual_approval_v1.json'),
        initial_FE_blank_row_corrected=1,corrected_FE_record='DK4_MES_B290_R0148',
        all_body_glyphs_leading_trailing_characters_andfont_consistent=True,observed_layout_candidates=findings,
        initial_native_proof=str(NATIVE),initial_native_proof_sha256=digest(NATIVE),
        other_layouts_retained_reason='Complete glyphs and usable width pass. Ordinary word breaks, short complete replies and necessary verb-phrase guard constraints do not require prose shortening or invented dramatic breaks.',
        sparse_injury_opening_retained_reason='The alternative full36-character first row produced an actual native blank row; the shorter opening keeps the complete verb phrase, all words and two intended rows.',
        all30_candidates_require_individual_final_disposition=True,offline_only=True,actual_new_batch_gameplay=False,new_credit=0,
        evidence={str(p):digest(p) for p in (FORMATTING,INITIAL,NATIVE,PREFERENCES,Path(__file__))}))
    print('All375 initial pages, five menus and17 name strings viewed; 30 source-bound layout candidates saved.')


if __name__=='__main__':main()
