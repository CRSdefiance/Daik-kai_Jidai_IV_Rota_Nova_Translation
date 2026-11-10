"""Bind new actors with the existing clean/current name ABI; do not approve names globally."""
import argparse
import struct
from pathlib import Path
from types import SimpleNamespace
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.registered_editorial_runtime import RegisteredRuntime
from scripts.execute_map_entity_tooltip_copy import machine_for,BASE
from scripts.audit_native_given_name_table import ordinary_getter
from scripts.probe_button_prompt_native import call
from scripts.prove_lil_B167_names_v4124b import names as original_names
from scripts.source_locked_derivation_v5118 import checked_text

PREVIOUS=Path('work/analysis/Hodram_B71_B80_identity_20261101/native_names.json')
CLEAN_PRECEDENT=Path('work/analysis/Hodram_actor34_clean_name_composition_v8732/clean_source_full_andprogressive_name_composition.json')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--actors',type=int,nargs='+',required=True)
    for arg in ('release','startup','out'):
        parser.add_argument('--'+arg,type=Path,required=True)
    args=parser.parse_args();assert not args.out.exists()
    actors=args.actors;assert actors==sorted(set(actors)) and all(0<=a<207 for a in actors)
    prior=load(PREVIOUS);precedent=load(CLEAN_PRECEDENT)
    adapter=checked_text(prior['source_owned_name_function'],{
        'all_ten_original_consumers_and_owned_or_readonly_memory_paths_exact':
        'all_requested_original_consumers_and_owned_or_readonly_memory_paths_exact'})
    clean_adapter=checked_text(adapter,{'actor = root+4+32*ident':'actor = ACTOR_OBJECTS[ident]'})
    clean=NdsImage.open('work/clean.nds');arm=clean.read_file('/__arm9__.bin');common=clean.read_file('/COMMON/MESFILE.DK4')
    assert sha(arm)==precedent['clean_ARM9_sha256']
    root=struct.unpack_from('<I',arm,0xCB18C)[0]
    assert root==precedent['source_native_getters'][0]['actor_fixture']-4-32*34
    objects={ident:root+4+32*ident for ident in actors};state={}
    def clean_machine(a,c,r,p):
        assert a==arm and c==common and r==b'' and p=={'explicit_clean_ordinary_name_fixtures':True}
        cpu=machine_for(a);before=bytes(cpu.mem_read(BASE,0x400000));executed=set()
        def exact(u,pc,size,_):
            assert BASE<=pc and pc+size<=BASE+len(a)
            assert bytes(u.mem_read(pc,size))==a[pc-BASE:pc-BASE+size]
            executed.add(pc)
        hook=cpu.hook_add(UC_HOOK_CODE,exact)
        for ident in actors:ordinary_getter(a,ident,machine=cpu)
        constructed=bytes(cpu.mem_read(BASE,0x400000));inverse=bytearray(constructed)
        for actor in objects.values():inverse[actor-BASE:actor-BASE+4]=before[actor-BASE:actor-BASE+4]
        assert bytes(inverse)==before
        def get(offset,*values):
            call(cpu,offset,tuple(values));return cpu.reg_read(UC_ARM_REG_R0)
        state.update(cpu=cpu,before=before,constructed=constructed,hook=hook)
        return cpu,get,SimpleNamespace(executed_current=executed)
    env={**original_names.__globals__,'ACTORS':actors,'ACTOR_OBJECTS':objects,'machine':clean_machine}
    exec(compile(clean_adapter,__file__+'::clean-getters','exec'),env)
    clean_names=env['names'](arm,common,b'',{'explicit_clean_ordinary_name_fixtures':True})
    cpu=state['cpu'];assert bytes(cpu.mem_read(BASE,0x400000))==state['constructed']
    for actor in objects.values():cpu.mem_write(actor,state['before'][actor-BASE:actor-BASE+4])
    assert bytes(cpu.mem_read(BASE,0x400000))==state['before'];cpu.hook_del(state['hook'])
    ctx=RegisteredRuntime(args.release,args.startup)
    env={**original_names.__globals__,'ACTORS':actors}
    exec(compile(adapter,__file__+'::current-getters','exec'),env)
    current=ctx.execute(env['names'])
    voice_env=dict(original_names.__globals__)
    exec(compile(prior['source_owned_voice_function'],__file__+'::current-voices','exec'),voice_env)
    voices=ctx.execute(voice_env['selectors'],actors)
    assert len(clean_names['rows'])==len(current['rows'])==2*len(actors)
    args.out.mkdir(parents=True)
    save(args.out/'names.json',dict(actors=actors,clean_ARM9_sha256=sha(arm),runtime=ctx.receipt(),
        clean_names=clean_names,current_names=current,voices=voices,
        clean_only_constructor_andname_ring_inverse_recovers_all4MiB=True,
        no_current_orhistorical_RAM_overlay_for_clean_names=True,
        source_owned_clean_adapter=clean_adapter,source_owned_current_adapter=adapter,
        new_credit=0,global_207_name_approval_not_granted=True,
        evidence={str(p):sha(p.read_bytes()) for p in [PREVIOUS,CLEAN_PRECEDENT,Path(__file__)]}))
    print('Bound',len(actors),'new actors;',2*len(actors),'clean andcurrent name consumers;no name revisions orcredit.')

if __name__=='__main__':main()
