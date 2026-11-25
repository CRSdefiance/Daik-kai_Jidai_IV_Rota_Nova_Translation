"""Bind one source payment on copied native contexts;do not claim affordability."""
import inspect,struct
from types import FunctionType
from pathlib import Path
from collections import Counter
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import prove_lil_B141_funds_v3537b as prior
from scripts.source_locked_derivation_v5118 import native_numbers
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B201_funds_v5912')
SOURCE=Path('work/analysis/lil_B201_source_v5902/all26_clean_current_complete_context_with_two_choice_labels.json')
AMOUNTS={'00a0fffffdff0191':100000}
BASE=0x02000000

def payment_at_funds_input(arm,common,raw,plan,block,command,target):
    fixtures=[]
    def same_source_with_owned_funds(a,c,r,p):
        cpu,get,provider=machine(a,c,r,p)
        # The current-snapshot machine guard remains intact. Set only the owned
        # CForce money word by executing its original setter on this CPU copy.
        fn=FunctionType(FINANCE_FN.__code__,{**FINANCE_FN.__globals__,'machine':lambda aa,cc,rr,pp:(cpu,get,provider)},argdefs=FINANCE_FN.__defaults__)
        fixture=fn(a,c,r,p,target);fixture.pop('raw_after')
        assert fixture['only_source_owned_one_funds_word_changed'] and fixture['target_funds']==target
        fixtures.append(fixture)
        return cpu,get,provider
    fn=FunctionType(PAYMENT_FN.__code__,{**PAYMENT_FN.__globals__,'machine':same_source_with_owned_funds},argdefs=PAYMENT_FN.__defaults__)
    result=fn(arm,common,raw,plan,block,command)
    assert len(fixtures)==1 and result['before_funds']==target
    return dict(fixture=fixtures[0],source_payment=result,original_snapshot_argument_unchanged=True,
        only_source_owned_money_input_set_by_original_native_setter_in_CPU_copy=True)

if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);gloss=read(packet['whole_exchange_context_notes'])
    assert list(AMOUNTS.values())==[gloss['seller_asks_and_counteroffers'][-1]]
    image=NdsImage.open(packet['current_ROM']);block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[201]
    commands=packet['blocks'][0]['all_current_native_commands'];namespace={**prior.__dict__,'AMOUNTS':AMOUNTS};adapters={}
    for name in ['finance','payment']:
        text=inspect.getsource(getattr(prior,name));original=text
        if name=='payment':
            a="command['whole_command_hex']=='00a0ffffbdff0191'";assert a in text;text=text.replace(a,"command['whole_command_hex'] in AMOUNTS")
            assert 'old-900000' in text;text=text.replace('old-900000',"old-AMOUNTS[command['whole_command_hex']]")
            assert native_numbers(original)-native_numbers(text)==Counter({900000:1}) and not native_numbers(text)-native_numbers(original)
        adapters[name]=text;exec(compile(text,__file__+'::'+name,'exec'),namespace)
    FINANCE_FN,PAYMENT_FN=namespace['finance'],namespace['payment']
    ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_B201_voices_v5903/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context')
    identity=ctx.execute(namespace['finance']);ctx.machines.pop();identity.pop('raw_after')
    assert identity['before_RAM_sha256']==identity['after_RAM_sha256'];cases=[]
    for word,amount in AMOUNTS.items():
        matching=[c for c in commands if c['whole_command_hex']==word];assert len(matching)==1;pay=matching[0]
        effect=ctx.execute(namespace['payment'],block,pay);ctx.machines.pop()
        cases.append(dict(source_offset=pay['offset'],asking_price=amount,input_kind='unchanged-current-opening-funds',
            input_funds=identity['before_funds'],source_payment=effect,not_a_selected_or_earned_purchase=True))
        for funds in [0,amount-1,amount,amount+1,amount*2]:
            applied=ctx.execute(payment_at_funds_input,block,pay,funds);ctx.machines.pop()
            cases.append(dict(source_offset=pay['offset'],asking_price=amount,input_kind='offline-only-owned-funds-boundary',
                input_funds=funds,**applied,not_a_selected_or_earned_purchase=True))
    assert len(cases)==6 and not ctx.machines
    assert all(c['source_payment']['after_funds']==max(0,c['input_funds']-c['asking_price']) for c in cases)
    save(ROOT/'one_exact100000_source_price_one_unforced_and_five_offline_payment_boundaries.json',dict(
        candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        original_selected_Lil_company_money_identity=identity,source_packed_payment_amounts=AMOUNTS,cases=cases,
        source100000_price_matches_exact_native_payment_amount=True,one_unchanged_context_case_and_five_disclosed_CPU_only_funds_inputs=True,
        native_payment_saturates_at_zero_not_a_proof_of_purchase_affordability_delegation_or_outer_eligibility=True,
        every_other_actor_roster_event_RNG_inventory_model_byte_and_ABI_guards_preserved=True,
        only_amount_data_replaces_prior900000_native_instruction_addresses_and_multiplicity_preserved=True,
        source_owned_adapters={**adapters,'payment_at_funds_input':inspect.getsource(payment_at_funds_input)},native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        source_item_acquisition_and_Charm_effect_bodies_remain_separate_unexecuted_scope=True,
        actual_B201_menu_selection_transactions_and_gameplay_unexecuted=True,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,Path(packet['whole_exchange_context_notes']),Path('scripts/prove_lil_B141_funds_v3537b.py'),Path(__file__)]},
        new_ROMs=0,new_emulator_runs=0,new_editorial_credit=0,full_goal_complete=False))
    print('Source100000 price matches one native payment:six cases(one unchanged snapshot/five disclosed CPU funds inputs). Saturating debits do not prove affordability,outer eligibility,item/stat results or an actual sale.')
