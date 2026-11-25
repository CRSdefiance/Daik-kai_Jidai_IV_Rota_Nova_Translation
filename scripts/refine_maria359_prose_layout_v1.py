"""Four US-English/role refinements and exact phrase/page preferences; no display credit."""
from pathlib import Path
from copy import deepcopy
import re
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.review import validate_natural_dialogue_batch

ROOT=Path('work/Maria_B253_B274_clean_20261110')
CHANGES={
    'SC3_B259_STYLE_800_166':("...There's something here. I've an uneasy feeling...","...There's something here. I have an uneasy feeling...",'Use natural American I have rather than the British possessive contraction while retaining the elder\'s unease.'),
    'SC3_B264_STYLE_748_222':("Hmm. According to the map, we seem to be meant to make our way past here.","Hmm. According to the map, it seems we're supposed to get past here.",'Remove the awkward seem to be meant construction; preserve the elder\'s tentative reading and need to pass here.'),
    'DK4_MES_B269_R0070':("We've a long way to go. Drink your water a little at a time.","We have a long way to go. Drink your water a little at a time.",'Use natural American We have rather than the British possessive contraction; retain the distance and drinking instruction.'),
    'DK4_MES_B273_R0014':("Let me thank you on the shipyard worker's behalf.","Let me thank you on the shipwright's behalf.",'Use the approved Shipwright role consistently while preserving thanks on his behalf rather than a joint gift.'),
}
PHRASES={
    'DK4_MES_B253_R0005':['{MACRO:FA}, right?'],
    'DK4_MES_B254_R0069':['reward for you'],
    'DK4_MES_B255_R0008':['count on you'],
    'DK4_MES_B255_R0028':['reward for you'],
    'DK4_MES_B256_R0017':['Lime Drops'],
    'SC3_B259_STYLE_24_156':['get lost'],
    'SC3_B259_STYLE_800_92':["isn't there"],
    'SC3_B259_STYLE_800_198':['here, right?'],
    'SC3_B259_STYLE_1228_136':['own men'],
    'SC3_B259_STYLE_1228_332':['close quarters'],
    'SC3_B259_STYLE_1882_0':['bring it down'],
    'SC3_B259_STYLE_2186_158':['Thank goodness'],
    'DK4_MES_B260_R0004':['shark fin',"don't you"],
    'DK4_MES_B260_R0013':['palace cuisine'],
    'DK4_MES_B260_R0036':["I'm counting on you"],
    'DK4_MES_B261_R0013':['All right'],
    'DK4_MES_B261_R0063':['ancient kingdom','far inland'],
    'DK4_MES_B262_R0069':['ancient kingdom','far inland'],
    'SC3_B264_STYLE_194_112':["don't have"],
    'DK4_MES_B264_R0149':['Well spotted'],
    'DK4_MES_B264_R0157':['What a wonderful view'],
    'DK4_MES_B266_R0035':['forty days','demand stick'],
    'DK4_MES_B267_R0127':['bottomless bog'],
    'DK4_MES_B267_R0170':['all right','like this'],
    'SC3_B269_STYLE_1266_0':['out of'],
    'SC3_B269_STYLE_1266_140':['out of'],
    'SC3_B269_STYLE_1266_176':['out of'],
    'SC3_B269_STYLE_1266_254':['out of'],
    'DK4_MES_B271_R0076':['stand a chance'],
    'DK4_MES_B271_R0311':['give them'],
    'DK4_MES_B272_R0059':['like this'],
    'DK4_MES_B272_R0114':['give them'],
    'DK4_MES_B273_R0025':['gladly accept it'],
    'DK4_MES_B274_R0113':['trust our instincts'],
}

def main():
    oldp=Path('translations/maria_B253_B274_contextual_review_v1.json');newp=oldp.with_name('maria_B253_B274_contextual_review_v2.json')
    oldf=ROOT/'formatting_v1/formatting_input.json';newf=ROOT/'formatting_v1/formatting_input_v2.json'
    oldc=ROOT/'contextual_comparisons_v1.json';newc=ROOT/'contextual_comparisons_v2.json'
    prefpath=ROOT/'formatting_v1/page_phrase_preferences_v1.json';receipt=ROOT/'prose_layout_refinements_v1.json'
    assert not any(p.exists() for p in [newp,newf,newc,prefpath,receipt])
    original,doc,comparison=map(load,[oldp,oldf,oldc]);prose=deepcopy(original);formatted=deepcopy(doc);comp=deepcopy(comparison)
    byp={r['id']:r for r in prose['records']};byf={r['id']:r for r in formatted['records']};byc={r['id']:r for r in comp['records']}
    for ident,(before,after,reason) in CHANGES.items():
        p,f,c=byp[ident],byf[ident],byc[ident]
        assert p['english']==p['proposed_English']==c['proposed_English']==before and p['decision']=='revision'
        for r in [p,f,c]:
            assert r['review']['formatting'] is False
            r['previous_contextually_reviewed_English']=before;r['finding']+=' '+reason;r['localization_note']=r['finding'];r['proposed_English']=after
            if r is not c:r['english']=after;r['logical_English']=after
        f['editorial_logical_English']=after
    for r in formatted['records']:
        p=byp[r['id']]
        if r['kind']!='typed-choice-label':
            r['english']=re.sub(r'\b(FI|FA|FO|FU)\b',lambda m:'{MACRO:'+m[0]+'}',p['english'])
            r['planned_English_markup']='{SPEAKER:'+format(r['source_selector'],'02X')+'}'+r['english']
        assert re.sub(r'\{MACRO:(FI|FA|FO|FU)\}',lambda m:m[1],r['english'])==p['english']
        assert all(r['english'].count('{MACRO:'+t+'}')==r['source_macros'].get(t,0) for t in ['FI','FA','FO','FU'])
    prose.update(previous_manuscript=str(oldp),previous_manuscript_sha256=digest(oldp),fresh_readaloud_refinements=CHANGES,revision_retention_counts_unchanged=True)
    structural=deepcopy(prose);structural['translation_policy']='natural-dialogue-v1';validate_natural_dialogue_batch(structural)
    save(newp,prose);comp.update(previous_comparisons=str(oldc),previous_comparisons_sha256=digest(oldc));save(newc,comp)
    formatted.update(source_full_manuscript=str(newp),source_full_manuscript_sha256=digest(newp),previous_formatting_input=str(oldf),previous_formatting_input_sha256=digest(oldf),fresh_readaloud_refinements=CHANGES)
    formatted['evidence'].update({str(p):digest(p) for p in [oldp,newp,oldf,oldc,newc,Path(__file__)]});save(newf,formatted)
    prefs=load(ROOT/'formatting_v1/initial_preferences.json');assert not prefs['records']
    def entry(ident):return prefs['records'].setdefault(ident,dict(bindings={k:sha(byf[ident][k].encode()) for k in ['source_hex','current_hex','english']}))
    for ident,phrases in PHRASES.items():
        pairs=[]
        for phrase in phrases:
            assert byf[ident]['english'].count(phrase)==1,(ident,phrase)
            words=[w.lower().strip('.,!?;:"()') for w in phrase.split()]
            pairs.extend([list(p) for p in zip(words,words[1:])])
        entry(ident).update(required_pairs=pairs,reason='Preserve the reviewed phrase or short question tag: '+', '.join(phrases)+'. No prose or viewport change.')
    entry('DK4_MES_B254_R0012').update(one_page=True,page_clause='Know anything about it?',reason='Use the validated full width to avoid a second page containing only about it; retain the complete final question.')
    entry('DK4_MES_B258_R0051').update(page_clause='Some strange people have been hanging around there lately, though.',reason='The full paragraph needs pagination under complete-word/guard limits; keep the whole final statement on one page instead of stranding lately, though.')
    prefs.update(no_prose_shortened_to_fit=True,original_native_widths_bounds_guards_andpagination_contract_unchanged=True,all_preferences_source_current_English_byte_bound=True,no_native_pixel_orvisual_approval=True,new_credit=0)
    save(prefpath,prefs)
    save(receipt,dict(prose=str(newp),prose_sha256=digest(newp),comparisons=str(newc),comparisons_sha256=digest(newc),
        formatting=str(newf),formatting_sha256=digest(newf),preferences=str(prefpath),preferences_sha256=digest(prefpath),
        source_objects=359,revisions=219,retentions=140,readaloud_refinements=CHANGES,phrase_scopes=len(PHRASES),page_scopes=2,
        all_fifth_gates_pending=True,new_credit=0,full_goal_complete=False))
    print('Prepared four read-aloud refinements and36 exact phrase/page scopes; no native/visual approval.')

if __name__=='__main__':main()
