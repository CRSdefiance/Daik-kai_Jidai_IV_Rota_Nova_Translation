"""Keep strict original-snapshot guards while using source-owned CPU input setters."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B196_funds_tools_v5601b')
WRAPPER='''
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

'''
if __name__=='__main__':
    assert not ROOT.exists();p=Path('scripts/prove_lil_B196_funds_v5601.py');text=p.read_text(encoding='utf-8')
    a=text.index("            fixture=ctx.execute(namespace['finance'],funds)");b=text.index('    assert len(cases)==36',a)
    replacement="""            applied=ctx.execute(payment_at_funds_input,block,pay,funds);ctx.machines.pop()
            cases.append(dict(source_offset=pay['offset'],asking_price=amount,input_kind='offline-only-owned-funds-boundary',
                input_funds=funds,**applied,not_a_selected_or_earned_purchase=True))
"""
    row=derive(p,'scripts/prove_lil_B196_funds_v5601b.py',{
        'import inspect,struct':'import inspect,struct\nfrom types import FunctionType',
        "ROOT=Path('work/analysis/lil_B196_funds_v5601')":"ROOT=Path('work/analysis/lil_B196_funds_v5601b')",
        "if __name__=='__main__':":WRAPPER+"if __name__=='__main__':",
        '    ROOT.mkdir(parents=True);ctx=CurrentContext':
        "    FINANCE_FN,PAYMENT_FN=namespace['finance'],namespace['payment']\n    ROOT.mkdir(parents=True);ctx=CurrentContext",
        text[a:b]:replacement,
        'source_owned_adapters=adapters,':'source_owned_adapters={**adapters,\'payment_at_funds_input\':inspect.getsource(payment_at_funds_input)},'})
    ROOT.mkdir(parents=True);save(ROOT/'prepared_owned_native_input_successor.json',dict(derivation=row,
        failed_original_producer_and_partial_native_context_preserved=True,
        strict_CurrentContext_and_its_original_snapshot_and_executed_instruction_guards_unchanged=True,
        only_source_owned_funds_input_uses_original_CForce_setter_inside_an_isolated_CPU_copy=True,
        no_replacement_RAM_argument_or_initialized_overlay=True,no_ROM_or_actual_gameplay_change=True,full_goal_complete=False))
