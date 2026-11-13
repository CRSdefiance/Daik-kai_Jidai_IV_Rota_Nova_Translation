"""Prove the reviewed ordinary boundary changes R14 layout alone."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue import lil_B185_layout_v1 as old,lil_B185_layout_v2 as new
from dk4tool.dialogue.lil_B185_profile import profile_for
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B185_wrap_comparison_v5103b')
if __name__=='__main__':
    assert not ROOT.exists()
    a=Path('translations/lil_B185_editorial_manuscript_v2.json');b=Path('translations/lil_B185_editorial_manuscript_v3.json')
    before,after=read(a),read(b);im=NdsImage.open(after['current_ROM'])
    arm=im.read_file('/__arm9__.bin');block=IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[185]
    cases=[];changed=[]
    for x,y in zip(before['records'],after['records'],strict=True):
        for field in ['id','source_hex','english','localization_note','editorial_decision','source_reference','current_reference','source_complete_preamble_hex']:
            assert x[field]==y[field]
        p=profile_for(arm,block,'FE-paper' if y['kind']=='system-FE' else 'progressive');raw=bytes.fromhex(y['source_hex'])
        left=old.encode_relocatable_dialogue(raw,y['english'],p);right=new.encode_relocatable_dialogue(raw,y['english'],p)
        assert left.encoded.hex()==x['compiled_hex'] and right.encoded.hex()==y['compiled_hex']
        lq=old.audit_relocatable_dialogue_record(raw,y['english'],p);rq=new.audit_relocatable_dialogue_record(raw,y['english'],p)
        if left.encoded!=right.encoded:changed.append(y['id'])
        cases.append(dict(id=y['id'],old_lines=lq['visible_lines'],new_lines=rq['visible_lines'],
            words_source_controls_and_decision_unchanged=True,encoded_bytes_unchanged=left.encoded==right.encoded,
            new_line_widths_px=rq['line_widths_px']))
    assert changed==['DK4_MES_B185_R0016']
    r=next(r for r in after['records'] if r['source_record_index']==16);raw=bytes.fromhex(r['source_hex']);p=profile_for(arm,block)
    case=next(r for r in cases if r['id']=='DK4_MES_B185_R0016')
    assert case['new_lines']==['I hear furs are selling well in','this cold, and prices are going up.']
    assert old.STRONG_ENDINGS==new.STRONG_ENDINGS and old.PROTECTED_BOUNDARIES==new.PROTECTED_BOUNDARIES
    negatives=[]
    for label,bad in [('changed-last-source-glyph',raw[:-1]+bytes([raw[-1]^1])),('different-source-body',raw[:1]+b'Japanese')]:
        try:new.encode_relocatable_dialogue(bad,r['english'],p)
        except ValueError as error:negatives.append(dict(case=label,rejected=True,error=str(error)))
        else:raise AssertionError(label)
    for label,body in [('different-word',r['english'].replace('prices','costs')),
            ('different-punctuation',r['english'].replace('up.','up!')),
            ('different-case',r['english'].replace('I hear','I HEAR')),
            ('additional-prose',r['english']+' Yes.')]:
        labels=body.split('}',1)[1].split()
        assert not any(new._reviewed_ordinary_boundary_at(labels,i) for i in range(len(labels)))
        negatives.append(dict(case=label,exact_reviewed_boundary_not_inherited=True))
    initial=read('work/analysis/lil_B185_fonts_v5099/all8_progressive_FE_native_planes_and64_alignment_cases.json')
    final=read('work/analysis/lil_B185_fonts_v5102/all8_progressive_FE_native_planes_and64_alignment_cases.json')
    initial_cases={r['id']:r for r in initial['cases']}
    for r in final['cases']:
        if r['id']!='DK4_MES_B185_R0016':assert r['whole_native_plane_sha256']==initial_cases[r['id']]['whole_native_plane_sha256']
    ROOT.mkdir(parents=True)
    save(ROOT/'all8_unchanged_words_and_exact_R16_boundary.json',dict(
        previous_manuscript=str(a),previous_manuscript_sha256=sha(a.read_bytes()),manuscript=str(b),manuscript_sha256=sha(b.read_bytes()),
        cases=cases,only_changed_record_IDs=changed,all8_words_controls_and_prose_unchanged=True,
        seven_other_compiled_targets_exact=True,seven_other_native_planes_exact=True,shared_weak_words_and_protected_phrases_unchanged=True,
        exact_source_and_prose_mutation_controls=negatives,reviewed_ordinary_boundary='R16 only:complete-word soft break after in',
        finding='work/analysis/lil_B185_wrap_finding_v5100/exact_R16_visual_finding_and_boundary_review.json',
        no_manual_break_font_width_guard_or_pagination_exemption=True,new_emulator_runs=0,new_review_credit=0,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Only R16 changes to two complete rows;all8 words/source controls and7 other targets exact. Six source/prose mutation controls pass;zero credit.')
