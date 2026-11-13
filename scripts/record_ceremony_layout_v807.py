"""Record inspected prospective fonts without granting production/gameplay credit."""

import shutil
from pathlib import Path

from dk4tool.patch import inn_editorial_runtime as runtime
from dk4tool.patch.arrival_notices_editorial import modal_code
from dk4tool.patch.captain_prompt_wrap import ADDRESS,SIZE
from dk4tool.patch.grand_race_menu_release import sha
from keystone import Ks,KS_ARCH_ARM,KS_MODE_THUMB
from scripts.context_ceremony_v806 import TABLES
from scripts.expand_ceremony_names_v807 import ROOT
from scripts.refine_ceremony_layout_v807 import MANUSCRIPT
from scripts.verify_village_wrap_v608 import read,save

DOC=Path('docs/ceremony_layout_v807_checkpoint.md')
LEDGER=Path('translations/editorial_review_current_v1.json')
SUMMARY=('V807 advances the52-entry ceremony draft through202 prospective native layouts and202 complete independently matched font planes. All21 site names,four protagonist given names and synthetic custom-name lengths1-23 fit with complete words and no layout findings;all17 sheets visually reviewed. Notice290 V2 preserves the spiritual-experience meaning in two natural sentences;other51 records exact. Ordinary helpers and an explicit modalID348 proxy are research only;production dispatcher,shared64 external consumers,registered integration/copies/patch and actual ceremony scenes remain. Exact proposed table needs200 bytes with phrases versus168 owned;modal uses124/128 bytes. V803 unchanged;550 complete/605 source-prose/55 pending,no completion credit. Full editorial and separate graphics audits remain unfinished.')


def main():
    report=read(ROOT/'research_report.json');matrix=read(ROOT/'native_layout_matrix.json')
    assert report['layouts']==len(matrix['cases'])==202 and report['findings']==matrix['findings_count']==0
    assert report['manuscript_sha256']==sha(MANUSCRIPT.read_bytes())
    assert len(report['sheets'])==17 and len(report['complete_font_planes'])==202
    assert all(sha(Path(r['path']).read_bytes())==r['sha256'] for r in report['sheets']+report['complete_font_planes'])
    save(ROOT/'visual_review.json',dict(research_report_sha256=sha((ROOT/'research_report.json').read_bytes()),
        inspected_sheets=report['sheets'],all17_sheets_visually_inspected=True,
        consistent_visible_left_margins_complete_letters_and_bounds=True,
        generated_lines_reviewed_no_large_internal_alignment_gaps_or_stray_adjacent_text=True,
        exact_full_font_and_blank_planes=202,production_dispatch_and_actual_gameplay_approval=False))
    context=read('work/analysis/ceremony_context_v806/native_context.json');kinds={}
    for branch in context['source_branch_cases']:
        for e in branch['events']:
            if 'message' in e:kinds.setdefault(e['kind'],set()).add(e['message'])
    rows=[];total=0
    for parent,offset,high,old_values in runtime.contract_rows():
        selected=set(old_values)
        if parent==0x02054014:selected|=kinds['NPC_dialogue']-{64}
        elif parent==0x02053FCC:selected|=kinds['NPC_yes_no']
        elif parent==0x02053C14:selected|={at&65535 for at in TABLES}
        shift=(4 if parent==0x02053C14 else 5) if high else 0
        assert all(not n&((1<<shift)-1) for n in selected)
        keys=sorted((n>>shift)-512 if high else n for n in selected);ranges=[]
        for n in keys:
            if ranges and n==ranges[-1][1]+1:ranges[-1]=(ranges[-1][0],n)
            else:ranges.append((n,n))
        amount=4+2*sum((hi-lo)//32+1 for lo,hi in ranges);total+=amount
        rows.append(dict(parent=parent,stack_field=offset,high=high,original_values=list(old_values),
            proposed_values=sorted(selected),added_values=sorted(selected-set(old_values)),encoded_bytes=amount))
    assert total==174 and ((total+3)//4)*4+24==200
    modal_used=12+len(Ks(KS_ARCH_ARM,KS_MODE_THUMB).asm(modal_code()[1],ADDRESS+12)[0])
    assert modal_used==124 and SIZE==128
    save(ROOT/'runtime_size_measurement.json',dict(candidate_sha256=report['candidate_sha256'],
        seven_exact_contract_rows=rows,proposed_table_bytes=total,existing_phrase_indices_bytes=24,
        existing_private_allocation_bytes=168,proposed_aligned_total_bytes=200,deficit_bytes=32,
        existing_modal_used_bytes=modal_used,existing_modal_allocation_bytes=SIZE,
        shared64_excluded_from_new_dispatch_membership=True,ROM_or_runtime_modified=False))
    ledger=read(LEDGER)
    for key,value in (('records_editorially_completed',550),('records_with_source_and_prose_pass',605)):
        assert ledger[key]==value
    candidate=dict(ledger['current_integrated_candidate'])
    assert sha(Path(candidate['path']).read_bytes())==report['candidate_sha256']==candidate['sha256']
    doc=read(MANUSCRIPT);assert all(not r['review']['formatting'] for r in doc['records'])
    before=ROOT/'editorial_ledger_before_V807.json'
    if not before.exists():shutil.copyfile(LEDGER,before)
    drafts=ledger['active_source_prose_drafts']
    drafts['manuscripts']=[str(MANUSCRIPT) if 'ceremony_editorial_manuscript_' in p else p for p in drafts['manuscripts']]
    drafts['status']='750-752-context-unmapped;ceremony52-prospective-layouts-reviewed-production-pending'
    drafts['note']='Ceremony52 V2 has202 prospective layouts/fonts and17 inspected sheets;production dispatch,COMMON integration and actual scenes are pending. All formatting gates remain false.'
    packet=ledger['next_ceremony_source_packet'];packet.update(manuscript=str(MANUSCRIPT),
        status='source-context-prose-and-prospective-layouts-reviewed;production-and-actual-scenes-pending',
        prospective_layout_proof=str(ROOT/'research_report.json'),prospective_visual_review=str(ROOT/'visual_review.json'),
        runtime_size_measurement=str(ROOT/'runtime_size_measurement.json'))
    ledger['latest_ceremony_layout_research']=dict(documentation=str(DOC),manuscript=str(MANUSCRIPT),
        proof=str(ROOT/'research_report.json'),layouts=202,full_font_planes=202,sheets_inspected=17,
        native_formatting_production_gate_approval=False,new_editorial_completion_credit=0)
    checkpoint=dict(id='V807-ceremony52-prospective-layouts',documentation=str(DOC),
        new_source_prose_reviewed=0,new_editorially_completed=0,new_ROM=False,full_goal_complete=False)
    if not any(c['id']==checkpoint['id'] for c in ledger['research_checkpoints']):ledger['research_checkpoints'].append(checkpoint)
    ledger['latest_checkpoint']=SUMMARY
    assert ledger['current_integrated_candidate']==candidate and len(drafts['native_message_IDs'])==55
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    save(LEDGER,ledger)
    for name in ('translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md'):
        path=Path('docs')/name;text=path.read_text(encoding='utf-8')
        heading='## V807: ceremony52 prospective native layouts'
        if heading not in text:path.write_text(text+'\n\n'+heading+'\n\n'+SUMMARY+' See [V807 checkpoint](ceremony_layout_v807_checkpoint.md).\n',encoding='utf-8')
    archive=Path('E:/Rota Nova translations/Editorial review/V807 Ceremony layout research');archive.mkdir(parents=True,exist_ok=True)
    files=[MANUSCRIPT,DOC,LEDGER,*ROOT.glob('*.json'),*ROOT.glob('*.png'),
        *(Path('scripts')/n for n in ('probe_ceremony_layout_v807.py','refine_ceremony_layout_v807.py','expand_ceremony_names_v807.py','record_ceremony_layout_v807.py'))]
    copied=[]
    for p in files:
        target=archive/p.name;shutil.copyfile(p,target);assert sha(p.read_bytes())==sha(target.read_bytes())
        copied.append(dict(source=str(p),archived=str(target),sha256=sha(target.read_bytes())))
    save(archive/'archive_manifest.json',dict(artifacts=copied,ROM_changed=False,gameplay_screenshots_or_guide_promotion=False))
    print(f'V807 recorded:202 prospective layouts/fonts,17 inspected sheets,{len(copied)} archived artifacts.550 complete;605 source/prose;55 pending. V803 unchanged.',flush=True)


if __name__=='__main__':main()
