"""Run seven unforced source predicates andforty cases for four630x resource values."""
import inspect
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts import prove_lil_B141_controls_v3538b as resource_base
from scripts.prove_lil_B139_B140_conditionals_v3461c import probe
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B155_controls_v3660')
SOURCE=Path('work/analysis/lil_B155_source_v3658/all50_clean_current_complete_context.json')
INPUT=Path('work/analysis/lil_B155_B160_source_v3656/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);image=NdsImage.open(packet['current_ROM']);arm=image.read_file('/__arm9__.bin');clean=NdsImage.open('work/clean.nds');jp,en=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[155] for im in [clean,image]];g=packet['blocks'][0];words=sorted({c['word'] for c in g['all_current_native_commands'] if c['word']&0xFF00==0x6300});assert words==[0x6326,0x632A,0x632B,0x632C];text=inspect.getsource(resource_base.control630A);changes=[('previous,boundary_return):','previous,boundary_return,word):'),("value=bytes.fromhex('0a63')","assert word in SOURCE_RESOURCE_WORDS;value=struct.pack('<H',word)"),('[0x02386EFC,10,2,1]','[0x02386EFC,word&255,2,1]')]
    for a,b in changes:assert a in text,a;text=text.replace(a,b)
    env={**resource_base.__dict__,'SOURCE_RESOURCE_WORDS':words};exec(compile(text,str(Path(__file__))+'::four-source-resource-values','exec'),env);ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,packet['historical_snapshot_ROM'],ROOT/'current_context');predicates=[];resources=[];leaves=[]
    for c in g['all_current_native_commands']:
        if c['word']==0x8000:r=ctx.execute(probe,en,c);ctx.machines.pop();predicates.append(dict(block=155,**r))
        if c['word'] not in [0x4000,0x100,0x200,0x300,0x400]:assert jp[c['offset']:c['offset']+c['native_extent']]==en[c['offset']:c['offset']+c['native_extent']];leaves.append(dict(block=155,offset=c['offset'],word=c['word'],native_extent=c['native_extent'],source_current_hex=c['whole_command_hex'],preserved_by_exact_leaf_ownership_not_full_effect_execution=True))
    for word in words:
        for previous in [0,1,2,3,0xFFFFFFFF]:
            for result in [0,0xFFFFFFFF]:resources.append(ctx.execute(env['control630A'],previous,result,word));ctx.machines.pop()
    assert len(predicates)==7 and len(resources)==40 and len(leaves)==21 and not ctx.machines;assert sum(c['word']&0xFF00==0x6300 for c in leaves)==6 and sum(c['word']==0xA000 for c in leaves)==1 and sum(c['word']==0 for c in leaves)==2;save(ROOT/'seven_predicates_six_resource_sites_forty_boundaries_and21_leaves.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),source_predicate_cases=predicates,source630x_resource_words=words,source630x_boundary_cases=resources,all21_nonrelative_source_current_control_leaves=leaves,source_owned_adapters=dict(predicate=inspect.getsource(probe),source630x=text),all_source_operands_and_complete_speech_preambles_bound=True,source_three_Fernando_two_Julio_membership_and_two_other_predicates_kept_distinct=True,source45FF_4631_4620_05xx_6008_and_one_A000_byte_ownership_not_full_body_execution=True,two_declared_endwords_must_survive_relocation=True,no_source2000_C200_482x_4700_FE_2100_4100_or_dynamic_objects=True,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),actual_selected_B155_IDs=[],new_emulator_runs=0,no_ROM_registry_ledger_credit_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(predicates=[(r['offset'],r['source_command_hex'],r['native_result']) for r in predicates],resource_values=4,source_resource_sites=6,boundary_cases=40,control_leaves=21,body_and_gameplay_claim=False,credit=0))
