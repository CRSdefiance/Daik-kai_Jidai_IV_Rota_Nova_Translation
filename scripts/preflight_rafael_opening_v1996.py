"""Unapproved formatting diagnostics; keep native speaker00 outside NUL text.

No release review gate is changed and no ROM is written. FE has a separate native
modal consumer and is explicitly left outside the progressive formatter.
"""
from collections import Counter
from pathlib import Path
import struct

from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.qa import audit_fixed_dialogue_record, audit_relocatable_dialogue_record
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_machine_scoped_v764 import machine
from scripts.native_call_abi_v764 import call
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/rafael_opening_preflight_v1996')
DOC = Path('translations/rafael_opening_contextual_editorial_manuscript_v1.json')
BASE, OWNER, INPUT, OUTPUT, LENGTH = 0x02000000,0x02650000,0x02660000,0x02661000,0x02662000


if __name__ == '__main__':
    assert not ROOT.exists()
    ROOT.mkdir(parents=True)
    cases=[]
    for version,path in [('clean','work/clean.nds'),('current','out/all_routes_combined_v1986_candidate.nds')]:
        arm=NdsImage.open(path).read_file('/__arm9__.bin');cpu=machine(arm)
        memory=bytes(cpu.mem_read(BASE,0x400000))
        for selector in (1,2,3,4):
            for previous in (0,1,2,0xFFFFFFFF):
                cpu.mem_write(INPUT-16,b'\xa5'*64)
                command=struct.pack('<HH',selector<<8,12)+b'\0'*12
                cpu.mem_write(INPUT,command)
                cpu.mem_write(OWNER-16,b'\xa5'*64)
                cpu.mem_write(OWNER,struct.pack('<2I',0,INPUT))
                owner=bytes(cpu.mem_read(OWNER-16,64))
                cpu.mem_write(OUTPUT-16,b'\xa5'*80);cpu.mem_write(OUTPUT,b'\0'*48)
                cpu.mem_write(LENGTH-16,b'\xa5'*36);cpu.mem_write(LENGTH,b'\0'*4)
                call(cpu,0x2A510,(OUTPUT,OWNER,LENGTH,previous))
                actual=struct.unpack('<I',cpu.mem_read(LENGTH,4))[0]
                expected=16 if selector==1 or previous==selector-2 else 4
                assert actual==expected,(version,selector,previous,actual,expected)
                assert bytes(cpu.mem_read(BASE,0x400000))==memory
                assert bytes(cpu.mem_read(OWNER-16,64))==owner
                assert bytes(cpu.mem_read(INPUT,len(command)))==command
                for at in (INPUT-16,INPUT+len(command),OUTPUT-16,OUTPUT+48,LENGTH-16,LENGTH+4):
                    assert bytes(cpu.mem_read(at,16))==b'\xa5'*16
                cases.append(dict(version=version,selector=selector,previous_result=previous,native_extent=actual,
                    expected_extent=expected,whole_native_ABI_owner_input_4MiB_guards_pass=True))
    save(ROOT/'conditional_span_previous_result_native_cases.json',dict(cases=cases,
        all32_original_native_cases_pass=True,explicit_FFFFFFFF_makes0200_0300_0400_fall_through=True,
        selector0100_always_skips_its_span_and_requires_recursive_body_walk=True,
        no0400_embedded_object_type_inferred=True,no_gameplay_or_reachability_credit=True))
    doc=read(DOC);profile=get_dialogue_profile('raphael-story-live');rows=[]
    for row in doc['records']:
        prefix=row['source_presentation_prefix_hex']
        assert row['review']['formatting'] is False
        if prefix=='fe':
            rows.append(dict(id=row['id'],kind='FE-separate-modal',status='unchanged-text-pending-exact-native-modal-proof',
                source_complete_preamble_hex=row['source_complete_preamble_hex']))
            continue
        source=bytes.fromhex(row['current_text_hex']);english=row['english']
        if prefix=='00':
            assert source[:1]==b'\0' and english.startswith('{SPEAKER:00}')
            source=source[1:];english=english.removeprefix('{SPEAKER:00}')
        fixed=audit_fixed_dialogue_record(source,english,profile)
        reloc=audit_relocatable_dialogue_record(source,english.removesuffix('{PAD}'),profile)
        rows.append(dict(id=row['id'],kind='progressive',speaker00_structural_byte_removed_only_for_NUL_text_formatter=prefix=='00',
            exact_native_preamble_retained_for_later_whole_command_compiler=row['source_complete_preamble_hex'],
            fixed=fixed,relocatable_diagnostic_only_not_relocation_authorization=reloc))
    issues=Counter(issue['code'] for r in rows if r['kind']=='progressive' for issue in r['fixed']['issues'])
    save(ROOT/'all115_formatter_preflight.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        records=rows,fixed_issue_counts=dict(issues),profile='raphael-story-live',
        no_gate_waived_no_prose_shortened_no_implementation_guard_changed=True,
        formatting_approved=False,ROM_changed=False,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print(dict(native_cases=len(cases),records=len(rows),fixed_issues=dict(issues)))
