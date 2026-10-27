"""Approve complete13 native text planes;retain reference/actual/release gates."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B24_font_approval_v1827')
OLD=Path('translations/lil_trade_routes_officers_editorial_manuscript_v2.json')
NEW=Path('translations/lil_trade_routes_officers_editorial_manuscript_v3.json')
FONT=Path('work/analysis/lil_B24_fonts_v1826/all13_native_macros_and_complete_font_planes.json')

if __name__=='__main__':
    assert not ROOT.exists()and not NEW.exists();ROOT.mkdir(parents=True)
    doc,font=read(OLD),read(FONT)
    assert font['manuscript_sha256']==sha(OLD.read_bytes())and len(font['cases'])==13 and not font['failures']and font['native_macro_calls']==104
    assert len(font['review_sheets'])==2
    for row in font['review_sheets']:assert sha(Path(row['path']).read_bytes())==row['sha256']
    by_id={r['id']:r for r in font['cases']};waivers=[]
    reasons={36:'The native balanced English uses three complete rows instead ofthe Japanese two. Both full sentences fit one four-row page with complete letters andno isolated tail;the extra automatic break is not a dramatic pause.',
        46:'The complete English contract-andtwo-birds idiom uses three automatic rows instead ofthe Japanese two. All source facts andthe idiom remain in one native page;the source LF was layout rather than an authored dramatic pause.',
        49:'Camilles praise andconfirmation fit one complete native row after FI expands toLil. The Japanese split is not a dramatic pause;preserving it would add an unnecessary English break.'}
    for row in doc['records']:
        case=by_id[row['id']];assert sha(Path(case['preview']).read_bytes())==case['preview_sha256']
        assert case['whole_native_independent_font_plane_exact']and case['all_continuation_visible_origins_equal_first_row_zero']
        assert all(d['severity']=='warning'and d['code']=='line-break-count'for d in case['diagnostics'])
        if case['diagnostics']:
            assert row['record_index']in reasons
            row['qa_waivers']=['line-break-count'];row['qa_waiver_reason']=reasons[row['record_index']]
            row['localization_note']+=' Native layout review: '+row['qa_waiver_reason']
            waivers.append({'id':row['id'],'reason':row['qa_waiver_reason']})
        row['review']['formatting']=True
    assert len(waivers)==3
    visual=ROOT/'visual_review.json'
    save(visual,{'native_font_proof':str(FONT),'native_font_proof_sha256':sha(FONT.read_bytes()),
        'two_review_sheets_all13_panels_actually_viewed':font['review_sheets'],
        'source_meanings_andboth_spoken_neighbors_reviewed':True,'complete_first_last_letters_including_Istanbul_andFI_Lil':True,
        'uniform_left_origins_no_overlap_clipping_unexpected_blank_page_or_manual_alignment':True,
        'specific_source_English_line_count_decisions':waivers,
        '104_native_macro_calls_full4MiB_ABI_and_guards_pass':True,'all13_native_independent_complete_font_planes_pass':True,
        'no_B24_actual_activation_reference_map_orregistered_release_claim':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    approved=deepcopy(doc);approved.update(formatting_review_pending=False,
        status='13-source-prose-native-andvisual-approved;reference-map-registration-andactual-pending',
        predecessor_manuscript=str(OLD),predecessor_manuscript_sha256=sha(OLD.read_bytes()),
        native_font_proof=str(FONT),native_font_proof_sha256=sha(FONT.read_bytes()),
        visual_review=str(visual),visual_review_sha256=sha(visual.read_bytes()))
    validate_natural_dialogue_batch(approved);save(NEW,approved)
    print('13 native/visual text layouts approved;three specific automatic line-count waivers. No actual orrelease completion credit.',flush=True)
