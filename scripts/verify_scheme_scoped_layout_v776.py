"""Verify complete original catalog layouts through the new production gate."""

import inspect
from pathlib import Path

from scripts import probe_tavern_continuation_layout_v768 as original
from scripts.native_machine_scoped_v764 import machine
from scripts.prepare_schemes_common_v776 import MANUSCRIPT,ROOT
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha


def formatter():
    source=inspect.getsource(original.format_case)
    marker='    call(u, LITERAL - BASE, (wrapped, output, 0), instruction_limit=2000000)'
    assert source.count(marker)==1
    source=source.replace(marker,'''    parent=0x02053D24 if row['message_id']>=940 else 0x02053DB8
    for off,value in ((0x264,parent),(0x274,row['message_id']),(0x27C,row['source_voice_table'])):
        u.mem_write(STACK+off,struct.pack('<I',value))
    call(u,0x01FFCF3C-BASE,(wrapped,output,0),instruction_limit=2000000)''')
    env=dict(original.__dict__)
    exec(compile(source,str(Path(__file__)),'exec'),env)
    return env['format_case'],source


def main():
    doc=read(MANUSCRIPT)
    rows={r['message_id']:r for r in doc['records']}
    arm=(ROOT/'COMBINED_ARM9_RESEARCH_ONLY.bin').read_bytes()
    plan=read(ROOT/'prospective_common_repack.json')
    assert sha(arm)==plan['target_ARM9_sha256']
    old_path=Path('work/analysis/tavern_schemes_layout_v775_v3/native_layout_matrix.json')
    cases=[r for r in read(old_path)['cases'] if not r['synthetic_23_byte_faction_boundary']]
    assert len(cases)==39730
    run,effective=formatter()
    (ROOT/'scoped_format_case.py').write_text(effective,encoding='utf-8')
    covered=set()
    for i,case in enumerate(cases):
        if i%64==0:u=machine(arm)
        n=case['id']
        result=run(u,rows[n],tuple(bytes.fromhex(s) for s in case['source_values_hex']))
        assert not result['findings'],result
        for key,value in result.items():assert value==case[key],(n,key)
        covered.add(n)
        if i%5000==0:print(f'{i}/{len(cases)} original-context layouts exact.',flush=True)
    assert covered==set(range(908,964))
    save(ROOT/'scoped_layout_verification.json',{'count':len(cases),'all56_IDs':sorted(covered),
        'target_ARM9_sha256':sha(arm),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),
        'reference_matrix_sha256':sha(old_path.read_bytes()),
        'all_native_printf_wrapped_bytes_guards_and_register_contracts_exact':True,
        'all39730_outputs_equal_reviewed_literal_layouts_without_findings':True,
        'effective_program_sha256':sha(effective.encode()),
        'no_actual_gameplay_claim':True,'producer_sha256':sha(Path(__file__).read_bytes()),
        'full_goal_complete':False})
    print('39730 layouts through both production parents/tables match reviewed outputs exactly.',flush=True)


if __name__=='__main__':main()
