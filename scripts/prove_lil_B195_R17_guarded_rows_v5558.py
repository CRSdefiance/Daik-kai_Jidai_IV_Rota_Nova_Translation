"""Audit every two-row word boundary;retain three rows when native break guards require them."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.layout import lint_dialogue
from dk4tool.dialogue import lil_B195_layout_v1 as codec
from dk4tool.dialogue.lil_B195_profile import profile_for
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/lil_B195_R17_guarded_rows_v5558')
DOC=Path('translations/lil_B195_editorial_manuscript_v2.json')
FONT=Path('work/analysis/lil_B195_fonts_v5553/all20_progressive_FE_native_planes_and160_alignment_cases.json')
STOPPED=Path('work/analysis/lil_B195_layout_v5555/all20_paragraph_layout_QA.json')

if __name__=='__main__':
    assert not ROOT.exists();doc,font,stopped=map(read,[DOC,FONT,STOPPED])
    assert len(stopped['failures'])==1 and stopped['failures'][0]['id']=='DK4_MES_B195_R0017'
    assert not Path('translations/lil_B195_editorial_manuscript_v3.json').exists()
    row=next(r for r in doc['records'] if r['source_record_index']==17)
    image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin')
    block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[195]
    profile=profile_for(arm,block);raw=bytes.fromhex(row['source_hex'])
    assert profile.window_width_px==216 and profile.default_ascii_width==6 and profile.guard_linebreaks and profile.pair_phase_safe_breaks
    body=row['english'].split('}',1)[1];words=body.split();prefix='{SPEAKER:5C}'
    cases=[]
    for split in range(1,len(words)):
        first,second=' '.join(words[:split]),' '.join(words[split:])
        proposed=prefix+first+'{LB}'+second
        issues=lint_dialogue(raw,proposed,profile)
        errors=[dict(code=i.code,message=i.message,line=i.line,pixel_width=i.pixel_width) for i in issues if i.severity=='error']
        assert errors
        cases.append(dict(after_word=words[split-1],first_row=first,second_row=second,
            ASCII_characters=[len(first),len(second)],native_lint_errors=errors,not_authored_prose_or_shipped_layout=True))
    assert len(cases)==11
    tempting=next(c for c in cases if c['after_word']=='plenty')
    assert tempting['ASCII_characters']==[36,31]
    assert any(i['code']=='pair-phase-auto-wrap' for i in tempting['native_lint_errors'])
    encoded=codec.encode_relocatable_dialogue(raw,row['english'],profile)
    report=codec.audit_relocatable_dialogue_record(raw,row['english'],profile)
    assert report['visible_lines']==["Our specialty! It's made",'with plenty of cheese,','and it tastes great!']
    assert encoded.encoded.hex()==row['compiled_hex']
    assert not [i for i in report['issues'] if i['severity']=='error'] and not report.get('reviewed_ordinary_boundaries')
    case=next(c for c in font['cases'] if c['id']==row['id'])
    assert case['encoded_hex']==row['compiled_hex'] and case['all_first_final_internal_glyphs_in_order_and_unique_cells']
    assert case['one_native_page_consumes_complete_target']
    for sheet in font['review_sheets']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    reason=('Retain three rows for the complete 68-character specialty paragraph. Every two-row complete-word split fails the unchanged native lint. '
            'The apparent plenty/of split needs36 first-row ASCII cells;the validated pair-phase-auto-wrap guard rejects a full first row before an explicit break because its internal phase byte can auto-wrap before the LF. '
            'Earlier splits overfill the continuation;later splits overfill the first row. The reviewed three rows keep made with plenty of cheese and the final taste claim readable,with complete glyphs and one page. '
            'No prose shortening,manual break,viewport/metric/guard change,collocation or weak-word waiver is accepted. The stopped v2 exploration and failed planner remain preserved;v1 remains the selected formatter.')
    assert len(body)==68
    ROOT.mkdir(parents=True)
    paths=[DOC,FONT,STOPPED,Path('scripts/refine_lil_B195_wrap_v5555.py'),Path('dk4tool/dialogue/lil_B195_layout_v2.py'),
        Path('dk4tool/dialogue/lil_B195_layout_v1.py'),Path(__file__)]
    save(ROOT/'all11_two_row_splits_rejected_original_three_rows_retained.json',dict(
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),record_ID=row['id'],exact_source_hex=row['source_hex'],
        exact_logical_prose=row['english'],paragraph_ASCII_characters=len(body),all_complete_word_two_row_splits=cases,
        all11_two_row_splits_fail_unchanged_native_lint=True,only_apparent_fitting_split_is_36_cell_first_row_rejected_by_pair_phase_guard=True,
        retained_visible_rows=report['visible_lines'],retained_compiled_hex=row['compiled_hex'],retention_reason=reason,
        original_selected_formatter='dk4tool/dialogue/lil_B195_layout_v1.py',selected_formatter_unchanged=True,
        all20_paragraphs_compiled_bytes_and_current_native_planes_unchanged=True,
        all20_previews_viewed_on_three_returned_sheets=True,
        no_ordinary_boundary_exception_adopted=True,no_blank_page_glyph_bounds_control_or_pair_phase_waiver=True,
        stopped_exploration_not_an_approved_or_registered_layout=True,
        evidence={str(p):sha(p.read_bytes()) for p in paths},new_ROMs=0,new_emulator_runs=0,new_editorial_credit=0,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('R17:all11 two-row word splits reject under unchanged native guards;36/31 tempting split hits pair-phase-auto-wrap. Retain original three rows/all68 characters;no exception or prose change.')
