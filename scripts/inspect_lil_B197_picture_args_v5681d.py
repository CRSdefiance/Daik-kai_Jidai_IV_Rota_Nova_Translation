"""Retain the exact caller register differences before classifying a strict comparison."""
import ast,inspect
from pathlib import Path
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts import prove_lil_B145_picture_controls_v3587 as prior
from scripts.source_locked_derivation_v5118 import native_numbers
from scripts.prepare_lil_B197_research_v5676 import PARENT,ROM,PLAN
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B197_picture_args_v5681d')
if __name__=='__main__':
    assert not ROOT.exists()
    source=Path('scripts/prove_lil_B197_relocated_controls_v5681b.py')
    changes=next(ast.literal_eval(n.value) for n in ast.walk(ast.parse(source.read_text(encoding='utf-8'))) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='changes' for t in n.targets))
    original=inspect.getsource(prior.picture);adapter=original
    for a,b in changes.items():assert adapter.count(a)==1;adapter=adapter.replace(a,b)
    assert native_numbers(adapter)==native_numbers(original)
    env={**prior.__dict__};exec(compile(adapter,__file__,'exec'),env)
    images=[NdsImage.open(p) for p in [PARENT,ROM]];old,new=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[197] for im in images]
    plan=read(PLAN);ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_B197_voices_v5648/current_native_input.json',PARENT,ROOT/'current_context')
    rows=[]
    for c in plan['blocks'][0]['command_map']:
        if c['word'] not in [0x4821,0x4720,0x4735]:continue
        cases=[]
        for label,block,at in [('current',old,c['old_offset']),('relocated',new,c['new_offset'])]:
            command=dict(offset=at,word=c['word'],native_extent=c['old_extent'],whole_command_hex=block[at:at+c['old_extent']].hex())
            result=ctx.execute(env['picture'],block,command);ctx.machines.pop();cases.append(dict(version=label,**result))
        rows.append(dict(word=c['word'],old_offset=c['old_offset'],new_offset=c['new_offset'],cases=cases))
    arm=images[0].read_file('/__arm9__.bin');clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    start,end=0x28A8C,0x28B20;assert arm[start:end]==clean[start:end]
    instructions=[dict(address=i.address,mnemonic=i.mnemonic,operands=i.op_str) for i in Cs(CS_ARCH_ARM,CS_MODE_ARM).disasm(arm[start:end],0x02000000+start)]
    save(ROOT/'six_original_picture_calls_and_unmodified_callee_instructions.json',dict(cases=rows,callee_instructions=instructions,callee_exact_clean_bytes_hex=arm[start:end].hex(),
        source_owned_adapter=adapter,source_test=str(source),source_test_sha256=sha(source.read_bytes()),no_comparison_failure_waived=True,full_goal_complete=False))
    for r in rows:print(hex(r['word']),[(c['version'],c['original_picture_boundary_calls']) for c in r['cases']])
    for i in instructions[:25]:print(hex(i['address']),i['mnemonic'],i['operands'])
