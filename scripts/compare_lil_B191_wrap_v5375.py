"""Prove R64 alone changes layout,with unchanged words and source/prose negatives."""
from pathlib import Path
from dk4tool.dialogue import lil_B191_layout_v1 as old,lil_B191_layout_v3 as new
from dk4tool.dialogue.lil_B191_profile import profile_for
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B191_wrap_comparison_v5375')
if __name__=='__main__':
    assert not ROOT.exists();a=Path('translations/lil_B191_editorial_manuscript_v2.json');b=Path('translations/lil_B191_editorial_manuscript_v3.json')
    before,after=read(a),read(b);im=NdsImage.open(after['current_ROM']);arm=im.read_file('/__arm9__.bin');block=IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[191]
    cases=[];changed=[]
    for x,y in zip(before['records'],after['records'],strict=True):
        for field in ['id','source_hex','english','localization_note','editorial_decision','source_reference','current_reference','source_complete_preamble_hex']:assert x[field]==y[field]
        p=profile_for(arm,block,'FE-paper' if y['kind']=='system-FE' else 'progressive');raw=bytes.fromhex(y['source_hex'])
        left=old.encode_relocatable_dialogue(raw,y['english'],p);right=new.encode_relocatable_dialogue(raw,y['english'],p)
        assert left.encoded.hex()==x['compiled_hex'] and right.encoded.hex()==y['compiled_hex']
        lq=old.audit_relocatable_dialogue_record(raw,y['english'],p);rq=new.audit_relocatable_dialogue_record(raw,y['english'],p)
        if left.encoded!=right.encoded:changed.append(y['id'])
        cases.append(dict(id=y['id'],old_lines=lq['visible_lines'],new_lines=rq['visible_lines'],words_source_controls_and_decision_unchanged=True,
            encoded_bytes_unchanged=left.encoded==right.encoded,new_line_widths_px=rq['line_widths_px']))
    assert changed==['DK4_MES_B191_R0064'] and old.STRONG_ENDINGS==new.STRONG_ENDINGS and old.PROTECTED_BOUNDARIES==new.PROTECTED_BOUNDARIES
    r=next(r for r in after['records'] if r['source_record_index']==64);raw=bytes.fromhex(r['source_hex']);p=profile_for(arm,block)
    assert next(r for r in cases if r['id']=='DK4_MES_B191_R0064')['new_lines']==["What are you waiting for? It'll be","too late once it's sold out."]
    negatives=[]
    for label,bad in [('changed-last-source-glyph',raw[:-1]+bytes([raw[-1]^1])),('different-source-body',raw[:1]+b'Japanese')]:
        try:new.encode_relocatable_dialogue(bad,r['english'],p)
        except ValueError as error:negatives.append(dict(case=label,rejected=True,error=str(error)))
        else:raise AssertionError(label)
    for label,target in [('different-word',r['english'].replace('waiting','looking')),('different-punctuation',r['english'].replace('out.','out!')),
        ('different-case',r['english'].replace('What','WHAT')),('additional-prose',r['english']+' Yes.')]:
        labels=target.split('}',1)[1].split();assert not any(new._reviewed_ordinary_boundary_at(labels,i) for i in range(len(labels)))
        negatives.append(dict(case=label,exact_reviewed_boundary_not_inherited=True))
    initialpath=Path('work/analysis/lil_B191_fonts_v5370/all13_progressive_FE_native_planes_and104_alignment_cases.json')
    finalpath=Path('work/analysis/lil_B191_fonts_v5374b/all13_progressive_FE_native_planes_and104_alignment_cases.json')
    initial,final=read(initialpath),read(finalpath);initialcases={r['id']:r for r in initial['cases']}
    for c in final['cases']:
        if c['id']!='DK4_MES_B191_R0064':assert c['whole_native_plane_sha256']==initialcases[c['id']]['whole_native_plane_sha256']
    ROOT.mkdir(parents=True);save(ROOT/'all13_unchanged_words_and_exact_R64_boundary.json',dict(previous_manuscript=str(a),previous_manuscript_sha256=sha(a.read_bytes()),
        manuscript=str(b),manuscript_sha256=sha(b.read_bytes()),cases=cases,only_changed_record_IDs=changed,
        all13_words_controls_and_prose_unchanged=True,twelve_other_compiled_targets_exact=True,twelve_other_native_planes_exact=True,
        shared_weak_words_and_protected_phrases_unchanged=True,exact_source_and_prose_mutation_controls=negatives,
        reviewed_ordinary_boundary='Exact R64 after be:complete question stays together and following warning uses the remaining first-row space.',
        finding='work/analysis/lil_B191_wrap_finding_v5372b/exact_R64_safe_two_row_revision.json',
        no_manual_break_font_width_guard_or_pagination_exemption=True,new_credit=0,full_goal_complete=False))
    print('R64 alone uses2safe rows;all13 words/source controls and12 other targets/planes exact. Six source/prose mutation checks pass;zero credit.')
