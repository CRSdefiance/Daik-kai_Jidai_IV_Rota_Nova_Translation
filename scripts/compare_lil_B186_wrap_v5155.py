"""Prove exact R13 soft-wrap changes and preserve every other target and plane."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue import lil_B186_layout_v2 as old,lil_B186_layout_v4 as new
from dk4tool.dialogue.lil_B186_profile import profile_for
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B186_wrap_comparison_v5155')
if __name__=='__main__':
    assert not ROOT.exists()
    a=Path('translations/lil_B186_editorial_manuscript_v2.json');b=Path('translations/lil_B186_editorial_manuscript_v4.json')
    before,after=read(a),read(b);image=NdsImage.open(after['current_ROM']);arm=image.read_file('/__arm9__.bin')
    block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[186];cases=[];changed=[]
    for x,y in zip(before['records'],after['records'],strict=True):
        for key in ['id','source_hex','english','localization_note','editorial_decision','source_reference','current_reference','source_complete_preamble_hex']:
            assert x[key]==y[key]
        raw=bytes.fromhex(y['source_hex']);p=profile_for(arm,block,'FE-paper' if y['kind']=='system-FE' else 'progressive')
        left=old.encode_relocatable_dialogue(raw,y['english'],p);right=new.encode_relocatable_dialogue(raw,y['english'],p)
        assert left.encoded.hex()==x['compiled_hex'] and right.encoded.hex()==y['compiled_hex']
        lq=old.audit_relocatable_dialogue_record(raw,y['english'],p);rq=new.audit_relocatable_dialogue_record(raw,y['english'],p)
        if left.encoded!=right.encoded:changed.append(y['id'])
        cases.append(dict(id=y['id'],old_lines=lq['visible_lines'],new_lines=rq['visible_lines'],new_line_widths_px=rq['line_widths_px'],
            words_source_controls_and_decision_unchanged=True,encoded_bytes_unchanged=left.encoded==right.encoded))
    assert changed==['DK4_MES_B186_R0013']
    row=next(r for r in after['records'] if r['source_record_index']==13);raw=bytes.fromhex(row['source_hex']);p=profile_for(arm,block)
    case=next(r for r in cases if r['id']==row['id'])
    assert case['new_lines']==["Yes! The customers won't be",'satisfied with a flavor this','light. It has to be sweeet! Sweet!']
    assert old.STRONG_ENDINGS==new.STRONG_ENDINGS and old.PROTECTED_BOUNDARIES==new.PROTECTED_BOUNDARIES
    qa=new.audit_relocatable_dialogue_record(raw,row['english'],p)
    assert [(v['line'],v['after_word']) for v in qa['reviewed_ordinary_boundaries']]==[(1,'be'),(2,'this')]
    negatives=[]
    for label,bad in [('changed-last-source-glyph',raw[:-1]+bytes([raw[-1]^1])),('different-source-body',raw[:1]+b'Japanese')]:
        try:new.encode_relocatable_dialogue(bad,row['english'],p)
        except ValueError as error:negatives.append(dict(case=label,rejected=True,error=str(error)))
        else:raise AssertionError(label)
    for label,body in [('different-word',row['english'].replace('flavor','taste')),
            ('different-punctuation',row['english'].replace('Sweet!','Sweet?')),
            ('different-case',row['english'].replace('Yes!','YES!')),
            ('additional-prose',row['english']+' Yes.')]:
        labels=body.split('}',1)[1].split()
        assert not any(new._reviewed_ordinary_boundary_at(labels,i) for i in range(len(labels)))
        negatives.append(dict(case=label,exact_reviewed_boundaries_not_inherited=True))
    first=read('work/analysis/lil_B186_fonts_v5148/all12_progressive_FE_native_planes_and96_alignment_cases.json')
    final=read('work/analysis/lil_B186_fonts_v5154/all12_progressive_FE_native_planes_and96_alignment_cases.json')
    initial={r['id']:r for r in first['cases']}
    for r in final['cases']:
        if r['id']!=row['id']:assert r['whole_native_plane_sha256']==initial[r['id']]['whole_native_plane_sha256']
    ROOT.mkdir(parents=True);save(ROOT/'all12_unchanged_words_and_exact_R13_boundaries.json',dict(
        previous_manuscript=str(a),previous_manuscript_sha256=sha(a.read_bytes()),manuscript=str(b),manuscript_sha256=sha(b.read_bytes()),
        cases=cases,only_changed_record_IDs=changed,all12_words_controls_and_prose_unchanged=True,
        eleven_other_compiled_targets_exact=True,eleven_other_native_planes_exact=True,shared_weak_words_and_protected_phrases_unchanged=True,
        exact_source_and_prose_mutation_controls=negatives,reviewed_ordinary_boundaries=qa['reviewed_ordinary_boundaries'],
        final_all12_panels_viewed_on_two_sheets_after_image_return=True,
        initial_one_boundary_attempt_did_not_change_any_target_and_is_preserved=True,
        finding='work/analysis/lil_B186_wrap_reserve_finding_v5152/corrected_native_reserve_and_two_ordinary_boundaries.json',
        no_manual_break_font_width_guard_or_pagination_exemption=True,new_emulator_runs=0,new_review_credit=0,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Only R13 changes:four to three flowing rows;all12 words/controls and11 other targets/planes exact. Six mutation controls pass;no credit.')
