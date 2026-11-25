"""Bind source6301/630A/6327 boundaries and both C200 consumers."""
import inspect
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import prove_lil_B141_controls_v3538b as prior
from scripts.prove_lil_B139_C200_v3461e import C200
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B142_B145_controls_v3580')
SOURCE=Path('work/analysis/lil_B142_B145_source_v3571/all38_clean_current_complete_context.json')
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);images=[NdsImage.open('work/clean.nds'),NdsImage.open(packet['current_ROM'])];blocks=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks for im in images]
    text=inspect.getsource(prior.control630A);changes=[('previous,boundary_return):','previous,boundary_return,word):'),("value=bytes.fromhex('0a63')","assert word in [0x6301,0x630A,0x6327];value=struct.pack('<H',word)"),('[0x02386EFC,10,2,1]','[0x02386EFC,word&255,2,1]')]
    for a,b in changes:assert a in text;text=text.replace(a,b)
    namespace=dict(prior.__dict__);exec(compile(text,str(Path(__file__))+'::source630x','exec'),namespace);ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_B142_B145_voices_v3572/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context');effects=[];ui=[];sites=[]
    for g in packet['blocks']:
        for c in g['all_current_native_commands']:
            if c['word'] in [0x6301,0x630A,0x6327]:sites.append(dict(block=g['block'],command=c))
            if c['word']==0xC200:
                for label,bs in zip(['clean','current'],blocks,strict=True):ui.append(dict(block=g['block'],version=label,**ctx.execute(C200,bs[g['block']],c)));ctx.machines.pop()
    assert len(sites)==4 and {s['command']['word'] for s in sites}=={0x6301,0x630A,0x6327}
    for word in [0x6301,0x630A,0x6327]:
        for previous in [0,1,2,3,0xFFFFFFFF]:
            for result in [0,0xFFFFFFFF]:effects.append(ctx.execute(namespace['control630A'],previous,result,word));ctx.machines.pop()
    assert len(effects)==30 and len(ui)==4 and all(c['source_owned_UI_request_words']==[1,0,13,0,0,0,1] for c in ui) and not ctx.machines
    save(ROOT/'source630x30_boundaries_and_four_C200_cases.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),source630x_sites=sites,source630x_cases=effects,source_C200_cases=ui,source_owned_adapters=dict(source630x=text,C200=inspect.getsource(C200)),resource_bodies_unexecuted=True,source630A_is_not_actual_payment=True,copied_London_UI_queue_is_not_selected_scene_location_or_transition=True,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),no_ROM_registry_ledger_credit_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('30 native630x boundaries and four C200 cases pass; resource bodies unexecuted.')
