"""Meaningful negative controls for exact-current code and initialized-state gates."""
from pathlib import Path
from copy import deepcopy
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/current_native_context_controls_v4787')
INPUT=Path('work/analysis/lil_B180_voices_v4775/current_native_input.json')


def read_voice(arm,common,raw,plan):
    cpu,get,provider=machine(arm,common,raw,plan)
    actor=get(0xCB184)+4+166*32
    assert get(0x7E988,actor)==0
    return len(provider.executed_current)


def stale_instruction(arm,common,raw,plan):
    cpu,get,provider=machine(arm,common,raw,plan)
    cpu.mem_write(0x0207E988,bytes.fromhex('0000a0e1'))
    return get(0x7E988,get(0xCB184)+4+166*32)


def foreign_code(arm,common,raw,plan):
    cpu,get,provider=machine(arm,common,raw,plan)
    cpu.mem_write(0x02600100,bytes.fromhex('1eff2fe1'))
    return get(0x600100)


def actor_write(arm,common,raw,plan):
    cpu,get,provider=machine(arm,common,raw,plan)
    at=get(0xCB184)+4+166*32+24;value=cpu.mem_read(at,1)[0]
    cpu.mem_write(at,bytes([value^1]))
    return True


if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    doc=read(INPUT);ctx=CurrentContext(INPUT,'legacy-argument-not-used',ROOT/'positive_context')
    count=ctx.execute(read_voice);ctx.machines.pop();assert count>0
    cases=[]
    for label,fn,needle in [('stale_current_instruction',stale_instruction,'executed noncurrent instruction'),
                            ('unowned_executable_code',foreign_code,'executed outside current source sections'),
                            ('unowned_actor_model_write',actor_write,None)]:
        try:ctx.execute(fn)
        except AssertionError as error:
            if needle:assert needle in str(error)
            cases.append(dict(case=label,error=str(error),native_input_snapshot_unchanged=True))
            ctx.machines.clear()
        else:raise AssertionError('Accepted invalid native context: '+label)
    bad=bytearray(ctx.raw);bad[0]^=1
    try:ctx.execute(read_voice,raw=bytes(bad))
    except AssertionError:cases.append(dict(case='alternate_initialized_RAM_rejected_before_execution'))
    else:raise AssertionError('Accepted alternate initialized RAM')
    for field in ['current_ROM_sha256','current_ARM9_sha256','current_COMMON_sha256']:
        changed=deepcopy(doc);changed[field]='0'*64;p=ROOT/(field+'.json');save(p,changed)
        try:CurrentContext(p,'unused',ROOT/(field+'_forbidden_context'))
        except AssertionError:
            assert not (ROOT/(field+'_forbidden_context')).exists();cases.append(dict(case='wrong_'+field))
        else:raise AssertionError('Accepted wrong source hash')
    assert len(cases)==7 and sha(Path(INPUT).read_bytes())==sha(INPUT.read_bytes())
    save(ROOT/'positive_and7_meaningful_rejections.json',dict(positive_current_getter_executes=count,
        rejections=cases,all_rejected_before_any_ROM_or_actual_snapshot_change=True,
        source='Exact-current instruction,section,actor,initialized-RAM and hash invariants',
        no_new_emulator_run_or_review_credit=True,full_goal_complete=False))
    print('Current source getter passes;seven stale-code,foreign-code,actor-write,alternate-RAM and wrong-hash controls reject.')
