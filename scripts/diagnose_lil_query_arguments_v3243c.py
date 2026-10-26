"""Inspect the concrete relocated event-query call difference without relaxing it."""
from pathlib import Path
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.prove_lil_crew_items_controls_v3114 import predicate
from scripts.prepare_lil_B111_B119_research_v3240b import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save

if __name__=='__main__':
    root=Path('work/analysis/lil_B111_B119_query_diagnostic_v3243c');assert not root.exists();root.mkdir(parents=True)
    spec=next(b for b in read(PLAN)['blocks'] if b['block']==114)
    c=next(c for c in spec['command_map'] if c['word']==0x8100)
    src=read('work/analysis/lil_B111_B119_source_v3217b/complete150_reachable_Lil_clean_current_context.json')
    ctx=CurrentContext('work/analysis/lil_B111_B119_fonts_v3234c/current_native_input.json',src['historical_snapshot_ROM'],root/'current_context')
    rows=[]
    for version,path,which in [('current',PARENT,'old'),('relocated',ROM,'new')]:
        image=NdsImage.open(path);block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[114]
        at,extent=c[which+'_offset'],c[which+'_extent'];cmd=dict(offset=at,native_extent=extent,word=0x8100,whole_command_hex=block[at:at+extent].hex())
        result=ctx.execute(predicate,block,cmd);ctx.machines.pop();rows.append(dict(version=version,**result))
    arm=image.read_file('/__arm9__.bin');md=Cs(CS_ARCH_ARM,CS_MODE_ARM)
    spans={}
    for a,b in [(0x2A0F0,0x2A154),(0x23840,0x23890)]:
        spans[hex(a)]=[hex(i.address)+' '+i.mnemonic+' '+i.op_str for i in md.disasm(arm[a:b],0x02000000+a)]
    save(root/'current_relocated_query_call_diagnostic.json',dict(cases=rows,source_disassembly=spans,producer_sha256=sha(Path(__file__).read_bytes()),no_guard_or_runtime_mutation=True,full_goal_complete=False))
    print([(r['version'],r['offset'],r['original_event_completion_calls']) for r in rows])
    print(spans)
