"""Freeze fifteen complete cooking paragraphs with three-actor native scope."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B193_native_tools_v5457')
if __name__=='__main__':
    assert not ROOT.exists();doc=read('translations/lil_B193_editorial_manuscript_v1.json');packet=read(doc['source_context'])
    keys=['source_context','control_contract','actor_voice_contract','branch_proof','source_entry_proof','source_effect_and_predicate_contract','actor_terminology_reconciliation','source_nameplate_consumer_proof']
    deps={doc[k]:doc[k+'_sha256'] for k in keys};hashes=sorted({b[k] for b in packet['blocks'] for k in ['clean_block_sha256','current_block_sha256']})
    profile=Path('dk4tool/dialogue/lil_B193_profile.py');assert not profile.exists()
    text='''"""Exact three-Lady cooking-scene progressive/FE profile."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
'''
    text+='ARM9_SHA='+repr(packet['current_ARM9_sha256'])+'\nBLOCKS=frozenset('+repr(hashes)+')\nSELECTORS=frozenset({166,167,168})\nDEPENDENCIES='+repr(deps)+'\nCONTROL='+repr(doc['control_contract'])+'\n\n'
    text+='''def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B193 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B193 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=30 or sum(r['source_selector']==254 for r in cases)!=2:raise ValueError('All15 source/current dispatch pairs required')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):raise ValueError('FE must remain null actor')
    if control['source_macro_counts']!={'FI':0,'FA':0,'FO':0}:raise ValueError('B193 has no source substitutions')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B193-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';14 original54020 speeches,three distinct source Ladies166/167/168 voice0,six original read-only names. HexA6/A7/A8 exact.18 linear commands,A0008,C200660,end662,two source tailzeros. Current V5437 font/guards;fresh approval required.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B193-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';one original24310 null actor then5473C prospective chili/Seoul notice.228x48logical/228x64physical,conservative216px planning. Chili29 and both Seoul aliases unchanged;source cooking and explicit friendship,not trade advice or earned fashion;fresh approval required.')
    raise ValueError('Unknown B193 consumer')
'''
    compile(text,str(profile),'exec');profile.write_text(text,encoding='utf-8',newline='\n')
    rows=[derive('dk4tool/dialogue/lil_B192_layout_v1.py','dk4tool/dialogue/lil_B193_layout_v1.py',{'B192':'B193','frozenset({115,153})':'frozenset({166,167,168})'})]
    rows.append(derive('scripts/plan_lil_B192_layout_v5417.py','scripts/plan_lil_B193_layout_v5458.py',{
        'B192':'B193','layout_v5417':'layout_v5458','Plan8':'Plan15','all8':'all15','len(reports)==8':'len(reports)==15','plans=8':'plans=15'}))
    rows.append(derive('scripts/verify_lil_B192_fonts_v5418.py','scripts/verify_lil_B193_fonts_v5459.py',{
        'B192':'B193','fonts_v5418':'fonts_v5459','voices_v5407':'voices_v5448','blocks[192]':'blocks[193]','blocks[191]':'blocks[192]',
        '[115,153,254]':'[166,167,168,254]','153 if selector==115 else 115':'167 if selector==166 else 166',"r['source_selector']==115":"r['source_selector']==166",
        "b'\\x73Japanese','{SPEAKER:73}Hello.'":"b'\\xa6Japanese','{SPEAKER:A6}Hello.'",'len(cases)==len(qa_reports)==8':'len(cases)==len(qa_reports)==15',
        'and64 native':'and120 native','macro_calls==64':'macro_calls==120','and64_alignment':'and120_alignment','alignment_calls=64':'alignment_calls=120',
        'progressive_alignment_calls=56':'progressive_alignment_calls=112','complete_progressive_planes=7':'complete_progressive_planes=14','all8':'all15','All8':'All15',
        'len(negatives)==18':'len(negatives)==20','and18 source-consumer':'and20 source-consumer','64 alignment cases':'120 alignment cases','one sheet needs':'two sheets need','all_three_selectors':'all_four_selectors'}))
    rows.append(derive('scripts/approve_lil_B192_native_v5419.py','scripts/approve_lil_B193_native_v5460.py',{
        'B192':'B193','native_approval_v5419':'native_approval_v5460','fonts_v5418':'fonts_v5459',"len(font['cases'])==8":"len(font['cases'])==15",
        "font['current_original_macro_alignment_calls']==64":"font['current_original_macro_alignment_calls']==120",'and64_alignment':'and120_alignment','==(7,1)':'==(14,1)',
        "len(font['negative_controls'])==18":"len(font['negative_controls'])==20", "len(font['review_sheets'])==1":"len(font['review_sheets'])==2",'blocks[192]':'blocks[193]',
        "{'revise':5,'retain-wording':3}":"{'revise':8,'retain-wording':7}","('progressive',115)":"('progressive',166)",
        'all8':'all15','All8':'All15','viewed8-panel':'viewed15-panel','on_one_sheet':'on_two_sheets','on_one_sheet=True':'on_two_sheets=True',
        'five_revisions_and_three_individually_justified_retentions':'eight_revisions_and_seven_individually_justified_retentions',
        'source_question_reversal_popularity_hyperbole_stammered_curiosity_offer_hesitant_assent_and_tentative_notice_preserved':'source_cooking_price_concern_reported_spice_classification_teaching_offer_and_explicit_friendship_preserved',
        'all64_current_native':'all120_current_native','source_consumer_negatives=18':'source_consumer_negatives=20','5 revisions/3 justified retentions,64 alignments,18 consumer':'8 revisions/7 justified retentions,120 alignments,20 consumer'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_exact_source_native_tools.json',dict(profile=str(profile),profile_sha256=sha(profile.read_bytes()),dependencies=deps,tools=rows,
        source_three_actors_18_linear_commands_and_no_macros_bound=True,no_inherited_boundary_exception=True,no_manual_break_or_font_width_metric_guard_change=True,no_credit=True,full_goal_complete=False))
