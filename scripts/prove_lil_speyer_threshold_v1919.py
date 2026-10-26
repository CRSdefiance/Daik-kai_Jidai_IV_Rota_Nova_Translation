"""Source-bound Speyer cash threshold cases, strictly disposable copied state."""
import struct
from pathlib import Path
from unicorn import UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_Speyer_threshold_v1919')
CONTEXT = Path('work/analysis/lil_Speyer_context_v1918/original_Hamburg_predicate_and57_macro_contexts.json')
BASE = 0x02000000
SCRATCH = 0x02640000

if __name__ == '__main__':
    assert not ROOT.exists()
    proof = read(CONTEXT)
    image,clean = NdsImage.open(proof['candidate']),NdsImage.open('work/clean.nds')
    arm = image.read_file('/__arm9__.bin')
    spans = [(0x2472C,0x247EC),(0x257C0,0x25800),(0x3CC80,0x3CCD0),(0x2A724,0x2A744)]
    assert all(arm[a:b] == clean.read_file('/__arm9__.bin')[a:b] for a,b in spans)
    raw = Path(proof['snapshot']).read_bytes()
    assert sha(raw) == proof['snapshot_sha256']
    ev = image.read_file('/data/EV2.DK4')
    owner = BASE+raw.find(ev[:96])-0x34
    event = proof['event128']['original_event']['actual_native_event_pointer']
    source_flag_pointer = 36147160
    source_flag_word = struct.unpack_from('<I',raw,source_flag_pointer-BASE)[0]
    assert source_flag_word == 0xA101002C
    # TypeA / property1 / company1: compare native current funds to5*10^4.
    company_index = (source_flag_word >> 16) & 31
    assert company_index == 1 and (source_flag_word >> 24) & 15 == 1
    rows = []
    for amount,expected in ((34882,0),(49999,0),(50000,1),(50001,1)):
        cpu,get = get_machine(arm,raw)
        companies = get(0xCB160)
        company = companies+4+company_index*76
        original = get(0x3CCC8,company)
        assert original == 34882
        fleet = get(0xCB1A8)+4+2*132
        cpu.mem_write(fleet+0x3C,b'\x05')
        cpu.mem_write(owner+0x2454,struct.pack('<3I',7,5,3))
        context_before = bytes(cpu.mem_read(BASE,0x400000))
        get(0x3CC80,company,(amount-original)&0xFFFFFFFF)
        assert get(0x3CCC8,company) == amount
        before = bytes(cpu.mem_read(BASE,0x400000))
        cash_changes = [dict(address=BASE+i,before=a,after=b) for i,(a,b) in enumerate(zip(context_before,before,strict=True)) if a!=b]
        assert all(r['address'] in range(company+12,company+16) for r in cash_changes)
        get(0xCC9A8,SCRATCH+0x80,get(0xCB1B4))
        cpu.mem_write(SCRATCH+0x200,struct.pack('<2I',0,source_flag_pointer))
        comparison = get(0x256A0,SCRATCH+0x200)
        assert comparison == (0 if amount < 50000 else 1 if amount == 50000 else 2)
        accepted = get(0x2A690,comparison,5)
        assert accepted == expected
        writes=[]
        def write(c,access,address,size,value,data):
            if BASE<=address<BASE+0x400000:writes.append(dict(PC=c.reg_read(UC_ARM_REG_PC),address=address,bytes=size,value=value))
        cpu.hook_add(UC_HOOK_MEM_WRITE,write)
        result = get(0x220D8,owner,event,SCRATCH+0x80,0)
        assert result == expected and bytes(cpu.mem_read(BASE,0x400000)) == before and not writes
        rows.append(dict(offline_funds=amount,original_funds=original,native_company_ID=company_index,
            company_pointer=company,cash_field=company+12,original_cash_setter=BASE+0x3CC80,
            setter_changed_only_cash_field=True,offline_cash_changes=cash_changes,native_comparison=comparison,
            comparison_mode5_accepts_equal_or_greater=bool(accepted),full_original_predicate_result=result,
            predicate_all4MiB_unchanged_and_no_write_callbacks=True,no_live_state_or_earned_funds_claim=True))
    ROOT.mkdir(parents=True)
    save(ROOT/'original_event128_fifty_thousand_cash_boundary.json',dict(candidate=proof['candidate'],
        candidate_sha256=proof['candidate_sha256'],snapshot=proof['snapshot'],snapshot_sha256=sha(raw),
        prior_context=str(CONTEXT),prior_context_sha256=sha(CONTEXT.read_bytes()),
        original_source_flag_ID=131,original_source_flag_pointer=source_flag_pointer,
        original_source_flag_word_hex=f'{source_flag_word:08x}',native_company_ID=1,
        company_name='Argot Co.',company_name_provenance='Native 0203CF9C company1 name query on a separate copy of the same snapshot.',
        required_cash=50000,exact_original_runtime_spans=[dict(start=BASE+a,end_exclusive=BASE+b,sha256=sha(arm[a:b]))for a,b in spans],
        cases=rows,source_predicate_all_other_conditions_accept_in_disclosed_Hamburg_context=True,
        no_ROM_live_RAM_orcompletion_changes=True,actual_scheduler_and_scene_activation_pending=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(Argot_funds=34882,required=50000,full_predicate_boundaries=[(r['offline_funds'],r['full_original_predicate_result'])for r in rows],
        all_cases_disposable_only=True,actual_activation_pending=True))
