"""Bind 31 directly observed layout candidates without changing reviewed prose."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.prepare_hodram_B211_B230_formatting_v1 import FORMATTING,OUT
from scripts.review_hodram_B221_B230_contextual_v1 import ROOT
from dk4tool.patch.grand_race_menu_release import sha

PREFERENCES=OUT/'visual_preferences_v3.json'
VIEW=ROOT/'initial_visual_review_v1.json'
FINDINGS={
'DK4_MES_B213_R0027':dict(page_clause='the bane of Tokugawa, ruler of Japan,',reason='The page turn splits the bane from of Tokugawa; test keeping the complete named description together.'),
'DK4_MES_B213_R0030':dict(page_clause='I write to pass along this news.',reason='Page two contains only this news; carry the complete closing sentence.'),
'DK4_MES_B216_R0054':dict(coherent_pairs=[['a','dou']],reason='The personal name A Dou splits at the row boundary.'),
'DK4_MES_B216_R0058':dict(coherent_pairs=[['zhao','yun']],reason='Zhao Yun splits across the last two rows.'),
'DK4_MES_B216_R0078':dict(coherent_pairs=[['zhuge','liang']],page_clause="He's probably my second favorite.",reason='The name splits across rows and page two strands my second favorite after the modal opening.'),
'DK4_MES_B217_R0042':dict(page_clause='Give my sword to that hero.',reason='The command leaves only to that hero on page two.'),
'DK4_MES_B217_R0045':dict(coherent_pairs=[['descends','from']],reason='A sparse opening row separates descends from its source phrase.'),
'DK4_MES_B223_R0008':dict(coherent_pairs=[['as','smooth'],['smooth','a'],['a','talker']],reason='Keep the smooth-a-talker construction intact after the complete greeting.'),
'DK4_MES_B223_R0027':dict(page_clause='and it got me thinking.',reason='The final page strands me thinking after got on page one.'),
'DK4_MES_B223_R0046':dict(coherent_pairs=[['a','little'],['little','selfishness'],['all','the'],['the','more'],['just','about'],['about','as']],reason='The initial plan splits all the more and just about as; test complete idiomatic phrases.'),
'DK4_MES_B223_R0065':dict(coherent_pairs=[['about','to']],reason='The about-to intention is split across rows.'),
'DK4_MES_B224_R0047':dict(coherent_pairs=[["wasn't",'it']],page_clause='anything went along the way.',reason='The short question tag splits across rows and the page turn strands went along the way.'),
'DK4_MES_B224_R0061':dict(page_clause='he took a humane approach to all of it.',reason='Page two begins of it after all; carry the complete main clause.'),
'DK4_MES_B225_R0037':dict(page_clause='splendid armor and all...',reason='The final page contains only and all; carry the complete evocative armor phrase.'),
'DK4_MES_B226_R0031':dict(coherent_pairs=[['western','asia']],page_clause='stretching from Central to Western Asia some two hundred years ago.',reason='Western Asia splits at the page turn, leaving geography and date as a tail.'),
'DK4_MES_B226_R0034':dict(page_clause='while swords and spears chipped their blades against it.',reason='The final page contains only against it; keep the complete sword-and-spear clause.'),
'DK4_MES_B226_R0040':dict(page_clause='and they died with the sea almost in sight.',reason='Page two strands almost in sight; carry the complete death-and-location clause.'),
'DK4_MES_B226_R0048':dict(coherent_pairs=[['interests','you']],reason='The opening If this interests leaves its object at the next row despite a fuller alternative.'),
'DK4_MES_B226_R0067':dict(page_clause='His interest probably grew out of that.',reason='Page two strands out of that after grew.'),
'DK4_MES_B227_R0046':dict(coherent_pairs=[["i'd",'better']],reason='The short modal phrase I would better is split between rows in its contracted form.'),
'DK4_MES_B228_R0005':dict(coherent_pairs=[['charles','martel']],reason='The hero-play name Charles Martel splits across rows.'),
'DK4_MES_B228_R0020':dict(coherent_pairs=[['around','here'],['what','was']],reason='The location phrase and short recollection question split across rows, leaving a sparse opening.'),
'DK4_MES_B228_R0045':dict(coherent_pairs=[['charles','martel']],reason='Charles Martel splits in the admiral comparison.'),
'DK4_MES_B229_R0036':dict(page_clause='both the Eastern and Western Roman Empires.',reason='The page turn separates Western from Roman Empires and strands the shared name tail.'),
'DK4_MES_B229_R0044':dict(coherent_pairs=[['no','power'],['power','lasts'],['lasts','forever']],reason='Keep the short political-power maxim together instead of splitting No power from lasts forever.'),
'DK4_MES_B230_R0016':dict(page_clause="That's why you need the resolve to face your fears.",reason='The final page strands to face your fears after resolve.'),
'SC1_B213_STYLE_8_122':dict(coherent_pairs=[['letter','for']],reason='Test a fuller first row carrying letter for you rather than leaving the existential announcement very short.'),
'SC1_B218_STYLE_8_120':dict(coherent_pairs=[['letter','for']],reason='Apply the same complete letter-for-you phrasing to Janus\'s gentle announcement.'),
'SC1_B226_STYLE_8_116':dict(coherent_pairs=[['letter','for']],reason='Apply the same complete letter-for-you phrasing to Ian\'s gentle announcement.'),
'SC1_B213_STYLE_702_38':dict(coherent_pairs=[['typical','of']],reason='Keep the typical-of construction together after the complete prose appraisal.'),
'SC1_B213_STYLE_702_270':dict(coherent_pairs=[['truly','very']],reason='Keep the emphatic Truly, very Yukihisa phrase together instead of stranding its adverb.'),
}

def main():
    assert not PREFERENCES.exists() and not VIEW.exists() and len(FINDINGS)==31
    doc=load(FORMATTING);by_id={r['id']:r for r in doc['records']}
    preferences=load(OUT/'swan_FE_preferences_v2.json')
    for ident,spec in FINDINGS.items():
        row=by_id[ident]
        if 'page_clause' in spec:assert spec['page_clause'] in row['english']
        preferences['records'][ident]={**spec,'bindings':{k:sha(row[k].encode('utf-8')) for k in ['source_hex','current_hex','english']}}
    save(PREFERENCES,{**preferences,'observed_further_layout_candidates':31,'prose_unchanged':True})
    native=ROOT/'native_resume_v2/compiled_native_pages.json'
    sheet_index=ROOT/'body_sheets_v1/sheet_index.json';index=load(sheet_index)
    assert index['pages']==285 and len(index['sheets'])==12 and index['native_receipt_sha256']==digest(native)
    names=load(ROOT/'name_planes_v1/native_name_planes.json')
    two=load(ROOT/'native_objects_v1/two/complete_choice_objects.json')
    three=load(ROOT/'native_objects_v1/three/menu_provider_and_planes.json')
    sheets=[*index['sheets'],*names['review_sheets'],*[o['review_sheet'] for o in two['objects']],*three['review_sheets']]
    assert len(sheets)==17 and all(digest(s['path'])==s['sha256'] for s in sheets)
    save(VIEW,dict(native=str(native),native_sha256=digest(native),all285_initial_body_pages_directly_viewed=True,
        body_sheets=12,scoped_names=23,distinct_name_strings=22,name_sheets=2,menu_sheets=3,
        all_initial_name_andmenu_sheets_directly_viewed=True,sheets=sheets,
        observed_layout_candidates=FINDINGS,preferences=str(PREFERENCES),preferences_sha256=digest(PREFERENCES),
        initial_FE_swan_punctuation_wrap_fixed_andvisually_reviewed=True,
        justified_initial_page_retention=dict(id='DK4_MES_B224_R0068',reason='Page one ends a complete conditional clause and page two contains the complete invitation question. Keep this logical boundary unless a later concrete finding justifies change; do not force sparse opening rows merely to combine both clauses.'),
        final_formatting_gates_pending=True,actual_gameplay=False,new_credit=0,
        evidence={str(p):digest(p) for p in (FORMATTING,native,sheet_index,Path(__file__))}))
    print('Recorded direct review of all 285 body pages, 22 name strings and three menus; 31 layout candidates bound.')

if __name__=='__main__':main()
