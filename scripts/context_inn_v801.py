"""Source-bound Inn argument, speaker and time-prefix research; no ROM edits."""

import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2,
    UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6,
    UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC)

from dk4tool.patch.crew_role_labels import ORIGINAL
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE, STACK, STOP
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/inn_context_v801')
ROM = Path('out/all_routes_combined_v799_candidate.nds')
LIVE = Path('E:/Rota Nova translations/Generated/work/emulation_v193/inn_v801_context')


def main():
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    raw = (LIVE/'frame_004000_arm9_ram.bin').read_bytes()
    assert sha(ROM.read_bytes()) == 'f855781b6b2a23482874a81c4d3f8f77262fe7f7db2846399b1409da8cc67c79'
    spans = [(0x5C450, 0x5D4EC), (0xB2CD8, 0xB2D58), (0x53F4C, 0x53F9C),
             (0x7E988, 0x7E9A0)]
    for lo, hi in spans:
        assert arm[lo:hi] == clean[lo:hi], hex(lo)
    u = machine(arm)
    u.mem_write(BASE, raw)

    def get(fn, args=()):
        call(u, fn, args)
        return u.reg_read(UC_ARM_REG_R0)

    def ptr(at): return struct.unpack('<I', u.mem_read(at, 4))[0]
    def text(at): return bytes(u.mem_read(at, 256)).split(b'\0')[0]
    def name(ob): return text(get(ptr(ptr(ob)+8)-BASE, (ob,))).decode('cp932')

    actors = get(0xCB184)
    hero = get(0x7F244)
    controller = get(0xCB1A8)+0x2090
    role_label_slot = get(0x86314, (2,))
    jp_ptr = struct.unpack_from('<I', clean, ORIGINAL-BASE+8)[0]
    assert clean[jp_ptr-BASE:].split(b'\0')[0].decode('cp932') == '参謀'
    assert text(ptr(role_label_slot)).decode('ascii').strip() == 'Strategist'
    role = dict(role=2, Japanese='参謀', English='Strategist',
        assigned_actor=get(0x825E4, (controller, 2)),
        fallback_speech_actor=get(0x82478, (controller, 2)))
    table = 0x021180E0
    assert tuple(struct.unpack('<8I', u.mem_read(table, 32))) == tuple(range(1186, 1194))
    voices = []
    for i in range(208):
        ob = actors+0x19E4 if i == hero else actors+4+i*32
        voice = get(0x7E988, (ob,))
        selected = get(0x53F4C, (ob, table))
        assert 0 <= voice < 8 and selected == 1186+voice
        voices.append(dict(actor_ID=i, native_actor=ob, voice=voice, message=selected))
    assert get(0x53F4C, (0, table)) == 1186

    global_at = struct.unpack_from('<I', arm, 0x5CD4C)[0]
    facility_role = ptr(global_at+0x10)
    town = get(0xB6618)
    actor_id = get(0xB2D28, (town, facility_role))
    innkeeper = get(0xB2CD8, (town, facility_role))
    assert innkeeper == (actors+0x19E4 if actor_id == hero else actors+4+actor_id*32)
    speaker = dict(current_town=town, current_facility_role=facility_role,
        original_actor_id=actor_id, original_actor_pointer=innkeeper,
        actor_display_name=name(innkeeper),
        source_provider=BASE+0xB2CD8,
        actual_capture=str(LIVE/'frame_004000_navigation.png'))

    event = 0x02450000
    times = []
    for now in range(12):
        for then in range(12):
            u.mem_write(event, bytes(8)+bytes([then])+bytes(3))
            result = text(get(0x5CA8C, (0, event, now)))
            delta = (now-then) % 12
            expected = b'This Mo' if delta == 0 else b'Last Mo' if delta == 1 else str(delta).translate(str.maketrans('0123456789','０１２３４５６７８９')).encode('cp932')+b' Mo. Ago'
            assert result == expected, (now, then, result, expected)
            times.append(dict(current_month=now, event_month=then,
                elapsed_months=delta, current_native_text_hex=result.hex(),
                current_native_text=result.decode('cp932')))

    observed = []
    def intercept(c, pc, size, unused):
        sp = c.reg_read(UC_ARM_REG_SP)
        r2, r3 = c.reg_read(UC_ARM_REG_R2), c.reg_read(UC_ARM_REG_R3)
        number = c.reg_read(UC_ARM_REG_R1)
        count = 2 if number in (1182,1184) else 3 if number in (1195,1196,1197,1198) else 1 if number in (1180,1183,1185) else 0
        args = [r2, r3, ptr(sp)][:count]
        observed.append(dict(wrapper=pc, message=number,
            speaker=c.reg_read(UC_ARM_REG_R0), arguments=[text(p).decode('cp932') for p in args],
            argument_pointers=args))
        c.reg_write(UC_ARM_REG_PC, c.reg_read(UC_ARM_REG_LR))
    def stop_at_message(c,pc,size,unused):
        intercept(c,pc,size,unused)
        c.emu_stop()
    hook = u.hook_add(UC_HOOK_CODE, intercept, begin=BASE+0x53FE4, end=BASE+0x53FE4)
    market = []
    try:
        for kind, ids in ((0,[1182,1183]),(1,[1184,1185])):
            observed.clear()
            u.mem_write(event, bytes(4)+bytes([0,kind,0,0]))
            get(0x5CC70, (0,event))
            assert [r['message'] for r in observed] == ids
            assert all(r['speaker'] == innkeeper for r in observed)
            expected = [name(get(0xCB178)+4), name(get(0xCB124)+4)]
            assert observed[0]['arguments'] == expected
            assert observed[1]['arguments'] == [name(get(0xCB160)+4)]
            assert bytes(u.mem_read(event+4,1)) == b'\x15'
            market.append(dict(source_function=BASE+0x5CC70, fixture_fields=dict(company=0,type=kind,town=0,goods=0),
                calls=list(observed), native_consumed_company_sentinel=21,
                scope='Original consumer/getters with isolated event fields; eligibility, actual display and naturally occurring market event not claimed.'))
    finally:
        u.hook_del(hook)
    stays=[]
    hooks=[u.hook_add(UC_HOOK_CODE,stop_at_message,begin=BASE+fn,end=BASE+fn)
        for fn in (0x53FE4,0x53F9C)]
    try:
        for start,number in ((0x5D3B8,1177),(0x5D3CC,1178),(0x5D1EC,1179),
                             (0x5D290,1181),(0x5D3A8,1194),(0x5D2A0,1194),(0x5D308,1199)):
            observed.clear()
            u.reg_write(UC_ARM_REG_SP,STACK);u.reg_write(UC_ARM_REG_LR,STOP)
            u.reg_write(UC_ARM_REG_R5,innkeeper);u.reg_write(UC_ARM_REG_R9,innkeeper)
            u.emu_start(BASE+start,STOP,count=10000)
            assert len(observed)==1 and observed[0]['message']==number and observed[0]['speaker']==innkeeper
            stays.append(dict(source_fragment=BASE+start,**observed[0]))
        for nights in (3,10,30):
            observed.clear()
            u.reg_write(UC_ARM_REG_SP,STACK);u.reg_write(UC_ARM_REG_LR,STOP)
            u.reg_write(UC_ARM_REG_R9,innkeeper);u.reg_write(UC_ARM_REG_R8,nights)
            u.emu_start(BASE+0x5D270,STOP,count=10000)
            assert len(observed)==1 and observed[0]['message']==1180 and observed[0]['speaker']==innkeeper
            expected=str(nights).translate(str.maketrans('0123456789','０１２３４５６７８９'))
            assert observed[0]['arguments']==[expected]
            stays.append(dict(source_fragment=BASE+0x5D270,native_selected_nights=nights,**observed[0]))
    finally:
        for h in hooks:u.hook_del(h)
    queued=[]
    def observe_report(c,pc,size,unused):
        queued.append(dict(wrapper=pc,role=c.reg_read(UC_ARM_REG_R0),
            table=c.reg_read(UC_ARM_REG_R1),company_argument=text(c.reg_read(UC_ARM_REG_R2)).decode('cp932')))
        c.emu_stop()
    hook=u.hook_add(UC_HOOK_CODE,observe_report,begin=BASE+0x53D44,end=BASE+0x53D44)
    try:
        for company in (0,1,19):
            ob=get(0xCB160)+4+company*76
            u.reg_write(UC_ARM_REG_SP,STACK);u.reg_write(UC_ARM_REG_LR,STOP)
            u.reg_write(UC_ARM_REG_R4,ob)
            u.emu_start(BASE+0x5CC28,STOP,count=10000)
            assert queued[-1]==dict(wrapper=BASE+0x53D44,role=2,table=table,company_argument=name(ob))
    finally:u.hook_del(hook)

    rumors = []
    hook = u.hook_add(UC_HOOK_CODE, stop_at_message, begin=BASE+0x53FE4, end=BASE+0x53FE4)
    try:
        for start, kind, fields in ((0x5C670,'town versus fleet',[0,0,0]),
                                     (0x5C820,'company raids town',[0,0,0]),
                                     (0x5C9D0,'company versus fleet',[0,1,0])):
            for won in (0,1):
                observed.clear()
                company_a,company_b,town_id=fields
                # Original record offsets4/5/6 hold attacker/company/town according to type.
                data=bytearray(12);data[4]=company_a;data[5]=company_b;data[6]=town_id;data[7]=won
                u.mem_write(event,bytes(data))
                time_pointer=get(0x5CA8C,(0,event,1))
                u.reg_write(UC_ARM_REG_SP,STACK);u.reg_write(UC_ARM_REG_LR,STOP)
                u.reg_write(UC_ARM_REG_R0,time_pointer);u.reg_write(UC_ARM_REG_R6,event)
                u.emu_start(BASE+start,STOP,count=10000)
                assert len(observed)==1
                row=observed[0]
                assert row['message']==((1197 if won else 1198) if start==0x5C820 else (1195 if won else 1196))
                assert row['speaker']==innkeeper and row['arguments'][0]=='Last Mo'
                town_name=name(get(0xCB178)+4+town_id*108)
                first_company=name(get(0xCB160)+4+company_a*76)
                second_company=name(get(0xCB160)+4+company_b*76)
                expected=[town_name,second_company] if start==0x5C670 else [first_company,town_name] if start==0x5C820 else [first_company,second_company]
                assert row['arguments'][1:]==expected
                rumors.append(dict(source_fragment=BASE+start, event_kind=kind, outcome_bit=won,
                    **row, scope='Original selected-event fragment only; event eligibility and actual display pending.'))
    finally:
        u.hook_del(hook)
    literals=[]
    for at in (0x5CB2C,0x5CB30,0x5CB34,0x5CB38):
        p=struct.unpack_from('<I',arm,at)[0]
        literals.append(dict(literal_offset=at,pointer=p,
            japanese=clean[p-BASE:].split(b'\0')[0].decode('cp932'),
            current_English=arm[p-BASE:].split(b'\0')[0].decode('ascii')))
    proof=dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),
        current_ARM9_sha256=sha(arm),source_ARM9_sha256=sha(clean),
        original_code_spans_equal=[dict(start=a,end=b,sha256=sha(arm[a:b])) for a,b in spans],
        live_RAM=str(LIVE/'frame_004000_arm9_ram.bin'),live_RAM_sha256=sha(raw),
        innkeeper=speaker,strategist_role=role,voice_table=table,voice_cases=voices,
        month_prefix_native_cases=times,embedded_time_literals=literals,
        market_calls=market,rumor_calls=rumors,stay_caller_fragments=stays,report_caller_fragments=queued,
        source_context_finding_1185='Innkeeper reports that the affected company was very upset after missing the buyout purchase; faction-opposition question is unrelated.',
        required_embedded_prose_review='Last Mo / This Mo / %s Mo. Ago feed battle/raid first argument. Review these owned C strings and native formatting along with Inn prose.',
        producer_sha256=sha(Path(__file__).read_bytes()),
        new_English_authored=False,ROM_changed=False,new_editorial_completion_credit=0,
        live_report_terminal_verification_pending=True,full_goal_complete=False)
    save(ROOT/'native_context.json',proof)
    print('Inn source context:208 voices,144 native month cases,4 market calls,6 rumor fragments,10 stay fragments and3 queued-report arguments; no ROM/prose completion claim.',flush=True)


if __name__=='__main__':main()
