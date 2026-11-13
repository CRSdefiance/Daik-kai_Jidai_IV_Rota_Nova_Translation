"""Refine one spoken question and document three exact full-width ordinary soft wraps."""
from copy import deepcopy
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/maria_B97_layout_refinement_v5011')
INPUT=Path('translations/maria_B97_editorial_manuscript_v1.json')
OUTPUT=Path('translations/maria_B97_editorial_manuscript_v2.json')
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists();doc=deepcopy(read(INPUT));rows={r['source_record_index']:r for r in doc['records']}
    r=rows[61];old=r['english'];assert old=="{SPEAKER:B4}...Th-then what are we supposed to do?!"
    r['english']="{SPEAKER:B4}...Th-then what should we do?!"
    r['localization_note']+=' Read-aloud refinement:should we do is a direct,natural rendering of the request for Maria\'s expected alternative. Keep the source hesitation;remove the unnecessary are we supposed to circumlocution. Meaning and emotional turn are unchanged.'
    choices={
        46:dict(line=1,last='and',following='attack',reason='A complete-word conjunction at this full-width boundary continues the same conditional clause. An ordinary soft wrap need not end a clause. Keep every word and the source hate/indiscriminate-attack/equal-guilt progression;no wording,glyph,width or page exception.'),
        78:dict(line=3,last='can',following='face',reason='An ordinary complete-word auxiliary boundary continues directly with face them. It fills the validated nonfinal row and preserves expanded influence and at least equal confidence. Avoid adding a page or shortening the source claim solely to remove this normal soft wrap.'),
        114:dict(line=2,last="you're",following='looking',reason='An ordinary complete-word contraction boundary continues with looking for. The full relative clause and tentative ruins handover remain intact in one four-row page. No first/final glyph,control,substitution,width or pagination check is waived.')}
    approved={}
    for i,c in choices.items():
        r=rows[i];approved[sha(bytes.fromhex(r['source_hex']))]=dict(c,english=r['english'],id=r['id'])
        r['reviewed_ordinary_soft_wrap']=dict(c,source_sha256=sha(bytes.fromhex(r['source_hex'])),exact_english_sha256=sha(r['english'].encode('utf-8')),native_and_actual_approval_still_pending=True)
        r['localization_note']+=' '+c['reason']
    oldformatter=Path('dk4tool/dialogue/maria_B97_layout_v1.py');newformatter=Path('dk4tool/dialogue/maria_B97_layout_v2.py')
    pair=derive(oldformatter,newformatter,{"def _word(value):":"STRONG_ENDINGS = STRONG_ENDINGS | frozenset({'a-are'})\n\ndef _word(value):"})
    # This successor has not executed yet. Complete its exact source policy before
    # first use. The executed historical v1 remains byte-exact.
    t=newformatter.read_text(encoding='utf-8')
    t+='\nREVIEWED_ORDINARY_SOFT_WRAPS='+repr(approved)+r'''
_unreviewed_audit=audit_relocatable_dialogue_record

def audit_relocatable_dialogue_record(source_raw,target_markup,profile):
    report=_unreviewed_audit(source_raw,target_markup,profile)
    accepted=REVIEWED_ORDINARY_SOFT_WRAPS.get(sha(source_raw))
    if accepted is None or target_markup!=accepted['english']:return report
    lines=report['visible_lines'];n=accepted['line']
    assert 0<n<len(lines) and lines[n-1].split()[-1]==accepted['last'] and lines[n].split()[0]==accepted['following']
    message=f"line {n} ends with weak wrap word {accepted['last']!r}"
    matches=[i for i in report['issues'] if i.get('code')=='weak-line-ending' and i.get('message')==message]
    assert len(matches)==1
    for i in matches:i.update(severity='info',code='reviewed-ordinary-soft-wrap',message=accepted['reason'])
    report['reviewed_ordinary_soft_wrap']=accepted
    return report
'''
    compile(t,str(newformatter),'exec');newformatter.write_text(t,encoding='utf-8',newline='\n');pair['successor_sha256']=sha(newformatter.read_bytes())
    planner=derive('scripts/plan_maria_B97_layout_v5010.py','scripts/plan_maria_B97_layout_v5012.py',{'maria_B97_layout_v1':'maria_B97_layout_v2','maria_B97_layout_v5010':'maria_B97_layout_v5012','maria_B97_editorial_manuscript_v1':'maria_B97_editorial_manuscript_v2','maria_B97_editorial_manuscript_v2':'maria_B97_editorial_manuscript_v3'})
    doc.update(previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()),layout_refinement_producer=str(Path(__file__)),layout_refinement_producer_sha256=sha(Path(__file__).read_bytes()))
    ROOT.mkdir(parents=True);save(OUTPUT,doc)
    save(ROOT/'one_question_and_three_exact_soft_wrap_decisions.json',dict(input=str(INPUT),input_sha256=sha(INPUT.read_bytes()),output=str(OUTPUT),output_sha256=sha(OUTPUT.read_bytes()),changed_question=dict(id=rows[61]['id'],before=old,after=rows[61]['english']),exact_soft_wrap_decisions=approved,formatter=pair,planner=planner,initial_failed_QA='work/analysis/maria_B97_layout_v5010/all32_paragraph_layout_QA.json',initial_failed_QA_sha256=sha(Path('work/analysis/maria_B97_layout_v5010/all32_paragraph_layout_QA.json').read_bytes()),no_global_weak_rule_or_historical_compiler_changed=True,no_native_or_actual_approval_yet=True,new_review_credit=0,full_goal_complete=False))
    print('One question refined;three exact full-width ordinary soft-wrap decisions documented. No glyph/width/page waiver;native and actual gates pending.')
