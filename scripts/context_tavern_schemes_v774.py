"""Execute original scheme consumer fragments and their real name providers."""

import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2,
    UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
    UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_SP)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE, STACK
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/tavern_schemes_editorial_v774')
TABLES = {
    0x02118340: (908,909,910,-1,911,912,913,914),
    0x02118320: (915,-1,916,-1,917,918,919,920),
    0x02118300: (921,-1,922,-1,923,924,925,926),
    0x02117B40: (927,-1,928,-1,929,930,931,932),
    0x021182C0: (933,-1,934,935,936,937,938,939),
    0x021182A0: (940,941,942,943,944,945,946,947),
    0x02118280: (948,949,950,951,952,953,954,955),
    0x02118260: (956,957,958,959,960,961,962,963),
}


def main():
    rom = NdsImage.open('out/all_routes_combined_v773_candidate.nds')
    arm = rom.read_file('/__arm9__.bin')
    source = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    report_path = Path('E:/Rota Nova translations/Generated/work/emulation_v193/condition_rumor_v774_second_round_live/capture_report.json')
    report = read(report_path)
    snap = next(r for r in report['read_only_capture_RAM_snapshots'] if r['frame'] == 3200)
    raw = Path(snap['path']).read_bytes()
    assert sha(raw) == snap['sha256'] and report['ROM_sha256'] == sha(Path(report['ROM']).read_bytes())
    u = machine(arm)
    u.mem_write(BASE, raw)

    def get(fn, args=()):
        call(u, fn, args)
        return u.reg_read(UC_ARM_REG_R0)

    def ptr(at): return struct.unpack('<I', u.mem_read(at,4))[0]
    def text(at): return bytes(u.mem_read(at,256)).split(b'\0')[0]
    def name(obj): return text(get(ptr(ptr(obj)+8)-BASE, (obj,)))

    officers, factions, towns = get(0xCB184), get(0xCB160), get(0xCB178)
    names = [{'index':i, 'object':factions+4+76*i,
              'name_hex':name(factions+4+76*i).hex(),
              'name':name(factions+4+76*i).decode('cp932')} for i in range(21)]
    assert ptr(factions+4+76*21) == 0  # Original null/none slot, not a named faction.
    voices = []
    for table, ids in TABLES.items():
        assert struct.unpack('<8i',u.mem_read(table,32)) == ids
        assert arm[table-BASE:table-BASE+32] == source[table-BASE:table-BASE+32]
        for i in range(40):
            actor = officers+4+32*i
            voice = get(0x7E988,(actor,))
            selected = get(0x53F4C,(actor,table))
            assert selected == (ids[voice] if ids[voice] != -1 else ids[0])
            voices.append({'table':table,'actor_index':i,'voice':voice,'selected_ID':selected})
        assert get(0x53F4C,(0,table)) == ids[0]

    faction_a, faction_b, town_id = factions+4, factions+4+76, 2
    town_name = name(towns+4+108*town_id)
    fa, fb = name(faction_a), name(faction_b)
    assert town_name == b'Amsterdam'
    events = []

    def observe(c, pc, size, unused):
        table = c.reg_read(UC_ARM_REG_R1)
        argc = 0 if table not in (0x02118320,0x021182A0,0x02118280,0x02118260) else 1 if table == 0x02118320 else 2
        args = [text(c.reg_read(r)).hex() for r in (UC_ARM_REG_R2,UC_ARM_REG_R3)[:argc]]
        events.append({'wrapper':pc,'role':c.reg_read(UC_ARM_REG_R0),'table':table,'arguments_hex':args})
        c.emu_stop()

    hooks = [u.hook_add(UC_HOOK_CODE,observe,begin=BASE+fn,end=BASE+fn) for fn in (0x53D44,0x53CB0)]
    cases = []
    spans = []
    try:
        def run(lo, hi, registers, table, args, description):
            assert arm[lo:hi] == source[lo:hi]
            spans.append([lo,hi])
            events.clear()
            u.reg_write(UC_ARM_REG_SP,STACK)
            for r,v in registers: u.reg_write(r,v)
            u.emu_start(BASE+lo,BASE+hi,count=10000)
            assert len(events) == 1 and events[0]['role'] == 2
            assert events[0]['table'] == table and events[0]['arguments_hex'] == [a.hex() for a in args], events
            cases.append({'original_fragment':[lo,hi], 'description':description, **events[0]})

        run(0x57334,0x5734C,((UC_ARM_REG_R6,officers),(UC_ARM_REG_R7,1)),
            0x02118340,(), 'Strategist introduction before scheme choice; no substituted price')
        labels = []
        for action, expected in ((6,b'Lure Fleet'),(7,b'Forge Papers'),(8,b'Bad Rumors'),(9,b'Bribe')):
            label = text(get(0x93D5C,(action,)))
            assert label == expected
            labels.append({'action':action,'label_hex':label.hex(),'label':label.decode()})
            run(0x56F30,0x56F48,((UC_ARM_REG_R9,action),),0x02118320,(label,),
                'Scheme label, then first opposing faction selection')
        for action, table in ((6,0x02118300),(8,0x02117B40)):
            run(0x57104,0x5715C,((UC_ARM_REG_R0,action),(UC_ARM_REG_R1,0),(UC_ARM_REG_R2,0)),
                table,(), 'Original Lure Fleet destination' if action == 6 else 'Original Bad Rumors location')
        run(0x51B64,0x51B90,((UC_ARM_REG_R10,4),),0x021182C0,(),
            'Mode4 second faction for forged-paper discord; selected first faction excluded by earlier source filter')
        run(0x56CB0,0x56CF8,((UC_ARM_REG_R7,faction_a),(UC_ARM_REG_R6,town_id)),
            0x021182A0,(fa,town_name),'Lure confirmation: faction name, then destination town')
        run(0x56E30,0x56E68,((UC_ARM_REG_R6,faction_a),(UC_ARM_REG_R4,faction_b)),
            0x02118280,(fa,fb),'Discord confirmation: first faction, then second faction')
        run(0x56B60,0x56BA4,((UC_ARM_REG_R6,faction_a),(UC_ARM_REG_R5,town_id)),
            0x02118260,(town_name,fa),'Bad Rumors confirmation: town FIRST, faction SECOND')
    finally:
        for h in hooks: u.hook_del(h)
    save(ROOT/'native_context.json',{
        'candidate_sha256':sha(Path('out/all_routes_combined_v773_candidate.nds').read_bytes()),
        'source_ARM9_sha256':sha(source),'current_ARM9_sha256':sha(arm),
        'capture_report':str(report_path),'read_only_snapshot':snap,
        'source_current_executable_fragments_exact':spans,
        'original_voice_tables':{hex(k):v for k,v in TABLES.items()},
        'all320_actual_actor_voice_selections':voices,'eight_original_null_fallbacks_verified':True,
        'all21_initialized_native_faction_names':names,'original_faction21_null_slot_verified':True,
        'four_original_scheme_labels':labels,
        'eleven_original_consumer_fragments':cases,
        'no_gameplay_activation_or_successful_scheme_claim':True,
        'scope':'Original native fragments up to unchanged portrait wrappers, on captured RAM; selection dialogs and event outcomes not executed.',
        'producer_sha256':sha(Path(__file__).read_bytes())})
    print('320 voice selections, eight fallbacks and eleven original scheme/argument fragments pass.',flush=True)


if __name__ == '__main__': main()
