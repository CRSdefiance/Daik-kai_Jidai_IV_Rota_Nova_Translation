"""Exact final parent/ID paths and equality to all inspected prospective planes."""

import inspect
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import ceremony_runtime_v808 as runtime
from scripts import probe_ceremony_layout_v807 as initial
from scripts import probe_tavern_continuation_layout_v768 as paragraphs
from scripts.context_ceremony_v806 import TABLES
from scripts.probe_button_prompt_native import BASE,STACK
from scripts.verify_arrival_native_v792 import prepared,run
from scripts.verify_village_wrap_v608 import read,save

ROOT=runtime.ROOT


def production_functions():
    source=inspect.getsource(paragraphs.format_case)
    needle='    call(u, LITERAL - BASE, (wrapped, output, 0), instruction_limit=2000000)'
    replacement='''    number=row['message_id']
    table=row.get('_selector_table',next((at for at,ids in TABLES.items() if number in ids),0))
    parent=0x02053C14 if table else 0x02053FCC if number in (1200,1201,1219) else 0x02054014
    u.mem_write(STACK+0x264,struct.pack('<I',parent))
    u.mem_write(STACK+0x274,struct.pack('<I',number))
    u.mem_write(STACK+0x270,struct.pack('<I',table))
    call(u,0x01FFCF3C-BASE,(wrapped,output,0),instruction_limit=2000000)'''
    assert source.count(needle)==1;source=source.replace(needle,replacement)
    env={**paragraphs.__dict__,'TABLES':TABLES};exec(compile(source,__file__,'exec'),env)
    ordinary=env['format_case']
    modal_source=inspect.getsource(initial.result_case)
    assert modal_source.count('348,expected')==1
    modal_source=modal_source.replace('348,expected',"row['message_id'],expected")
    modal_source=modal_source.replace('production_dispatch_ID348_proxy_only_ceremony_scope_not_yet_enabled','exact_ceremony_modal_ID_dispatch_verified')
    env={**initial.__dict__};exec(compile(modal_source,__file__,'exec'),env)
    return ordinary,env['result_case'],source,modal_source


def main():
    rom=NdsImage.open(runtime.ROM);old=rom.read_file('/__arm9__.bin')
    arm=(ROOT/'ARM9_RESEARCH_ONLY.bin').read_bytes();assert arm==runtime.apply(old)
    text=b' Complete words and original leading and trailing letters stay intact across the entire modal box.'
    changes=[];parents=[]
    for n in range(3668):
        if n%32==0:a,b=prepared(old),prepared(arm)
        x,y=run(a,0x020546E8,n,text),run(b,0x020546E8,n,text)
        if n in runtime.MODAL_IDS:
            assert not x[1] and y[1] and x!=y
            assert b' '.join(y[0].split())==b' '.join(text.split())
            changes.append(n)
        else:assert x==y,n
    for parent in (0,0xFFFFFFFF,0x120546E8,0x0205469C,0x02054720,0x02054764,0x02054014):
        for n in (*range(127,135),*range(269,273),*range(287,298),321,327,*range(344,351),0xFFFFFFFF):
            a,b=prepared(old),prepared(arm)
            assert run(a,parent,n,text)==run(b,parent,n,text),(parent,n)
            parents.append([parent,n])
    assert changes==list(runtime.MODAL_IDS)
    save(ROOT/'modal_scope.json',dict(all3668_IDs_checked=True,exact_six_new_modal_IDs=changes,
        all_other3662_modal_ID_outputs_and_wrap_selection_exact=True,wrong_parent_controls=parents,
        source_ARM9_sha256=sha(old),research_ARM9_sha256=sha(arm),
        source_unrelated292_and_previous_modal_families_preserved=True))
    print(f'3668 exact modal-ID paths and{len(parents)} wrong-parent/edge controls pass.',flush=True)
    ordinary,modal,ordinary_source,modal_source=production_functions()
    rows={r['message_id']:r for r in read('translations/ceremony_editorial_manuscript_v2.json')['records']}
    prior=read('work/analysis/ceremony_layout_v807_name_bounds/native_layout_matrix.json')
    cases=[]
    for i,p in enumerate(prior['cases']):
        n=p['id']
        if n==64:continue
        row=rows[n];values=tuple(bytes.fromhex(v) for v in p['source_values_hex'])
        case=(modal if n in runtime.MODAL_IDS else ordinary)(prepared(arm),row,values)
        assert case['formatted_hex']==p['formatted_hex'] and case['lines']==p['lines'] and not case['findings'],case
        cases.append(dict(prior_case_index=i,message_ID=n,source_values_hex=p['source_values_hex'],
            formatted_hex=case['formatted_hex'],lines=case['lines'],
            exact_native_parent_scope_and_printf_and_complete_words_and_guards_and_callee_saved_ABI=True,
            output_exact_to_previously_independently_matched_and_visually_reviewed_complete_font_plane=True))
    assert len(cases)==201
    context=read('work/analysis/ceremony_context_v806/native_context.json');heroes=[]
    for selection in context['hero_table_selections']:
        n=selection['selected_message'];row={**rows[n],'_selector_table':selection['table']}
        case=ordinary(prepared(arm),row,())
        ref=next(c for c in cases if c['message_ID']==n)
        assert case['formatted_hex']==ref['formatted_hex'] and not case['findings']
        heroes.append(dict(**selection,formatted_hex=case['formatted_hex'],
            native_53C14_pointer_contract_and_full_output_verified=True))
    assert len(heroes)==32
    save(ROOT/'effective_consumer_formats.json',dict(source_ARM9_sha256=sha(old),research_ARM9_sha256=sha(arm),
        manuscript_sha256=sha(Path('translations/ceremony_editorial_manuscript_v2.json').read_bytes()),
        actual_parent_dispatch_formats=cases,hero_pointer_scope_cases=heroes,
        previous_font_proof='work/analysis/ceremony_layout_v807_name_bounds/research_report.json',
        previous_font_proof_sha256=sha(Path('work/analysis/ceremony_layout_v807_name_bounds/research_report.json').read_bytes()),
        previous_visual_review_sha256=sha(Path('work/analysis/ceremony_layout_v807_name_bounds/visual_review.json').read_bytes()),
        ordinary_effective_program_sha256=sha(ordinary_source.encode()),modal_effective_program_sha256=sha(modal_source.encode()),
        shared64_unchanged_original_consumer_no_new_scope_or_presentation_claim=True,
        COMMON_native_copies_registered_integration_and_actual_ceremony_scenes_pending=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('201 actual-parent native formatting cases and32 hero pointer contracts equal the inspected full-font output. Actual scenes/COMMON integration pending.',flush=True)


if __name__=='__main__':main()
