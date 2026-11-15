"""Bind the distinct source funding amounts on copied native contexts."""
import inspect,struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import prove_lil_B141_funds_v3537b as prior
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.prove_lil_B139_B140_conditionals_v3461c import probe
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B142_B143_funds_v3579')
SOURCE=Path('work/analysis/lil_B142_B145_source_v3571/all38_clean_current_complete_context.json')
BASE=0x02000000
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);im=NdsImage.open(packet['current_ROM']);blocks=IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks
    namespace=dict(prior.__dict__);adapters={}
    for name in ['finance','payment']:
        text=inspect.getsource(getattr(prior,name))
        if name=='payment':
            old="command['whole_command_hex']=='00a0ffffbdff0191'";assert old in text;text=text.replace(old,"command['whole_command_hex'] in {'00a0ffffbdff0191','00a0ffffedff0191'}")
            assert 'old-900000' in text;text=text.replace('old-900000',"old-{'00a0ffffbdff0191':900000,'00a0ffffedff0191':300000}[command['whole_command_hex']]")
        adapters[name]=text;exec(compile(text,str(Path(__file__))+'::'+name,'exec'),namespace)
    ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_B142_B145_voices_v3572/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context');identity=ctx.execute(namespace['finance']);ctx.machines.pop();identity.pop('raw_after');assert identity['before_RAM_sha256']==identity['after_RAM_sha256'];cases=[]
    for block,word,inputs in [(142,'00a0ffffbdff0191',[0,899999,900000,999999,1000000,1000001,2000000]),(143,'00a0ffffedff0191',[0,299999,300000,300001,600000,1000000])]:
        g=next(g for g in packet['blocks'] if g['block']==block);pay=next(c for c in g['all_current_native_commands'] if c['whole_command_hex']==word)
        for funds in inputs:
            fixture=ctx.execute(namespace['finance'],funds);ctx.machines.pop();applied=fixture.pop('raw_after');assert struct.unpack_from('<I',applied,fixture['funds_field']-BASE)[0]==funds
            raw=bytearray(ctx.raw);struct.pack_into('<I',raw,fixture['funds_field']-BASE,funds);raw=bytes(raw);fixture['historical_plus_only_funds_input_RAM_sha256']=sha(raw);pred=None
            if block==142:
                condition=next(c for c in g['all_current_native_commands'] if c['whole_command_hex']=='0080ffff0e0001a1');pred=ctx.execute(probe,blocks[block],condition,raw=raw);ctx.machines.pop();assert pred['native_result']==[2,0 if funds<1000000 else 1 if funds==1000000 else 2,0,0,0,0]
            effect=ctx.execute(namespace['payment'],blocks[block],pay,raw=raw);ctx.machines.pop();cases.append(dict(block=block,input_funds=funds,offline_fixture=fixture,source_predicate=pred,source_payment=effect,isolated_decoder_case_not_claimed_reachable_or_earned=True))
    assert len(cases)==13 and not ctx.machines
    save(ROOT/'two_distinct_source_payments13_boundaries_and_million_threshold.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),original_selected_Lil_company_money_identity=identity,cases=cases,B142_threshold=1000000,B142_payment=900000,B143_payment=300000,B143_has_no_inline_money_predicate_and_EV2_eligibility_unexecuted=True,all_tests_copied_offline_native_contexts_not_gameplay=True,source_owned_adapters=adapters,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),no_ROM_registry_ledger_credit_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('13 payment cases pass: B142 million threshold/900000 payment; B143300000 payment. No earned event claim.')
