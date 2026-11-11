"""Replay two focused excerpts with unchanged original speaker and modal commands."""

import argparse
from pathlib import Path
from struct import pack_into, unpack_from
import sys
from types import FunctionType

from PIL import ImageChops

from scripts import replay_historical_story_wraps_20261111 as prior
from scripts import stage_story_question_wraps_20261111 as stage


base=stage.base
ROOT=Path('out/story_question_wraps_20261111_v2')
ROM=ROOT/'story_question_wraps_RESEARCH_ONLY.nds'
SETUP,LIVE,STARTUP=(ROOT/name for name in ('fixture_receipt.json','question_wrap_gameplay.json','own_startup_verification.json'))
LIL='/data/SC2.DK4'
SCENES={'london':(LIL,26,580,1098,'DK4_MES_B26_R0083'),
        'rafael':('/data/SC0.DK4',103,668,868,'DK4_MES_B103_R0053')}
MODES=tuple(f'{scene}_{side}' for scene in SCENES for side in ('before','after'))


def prepare():
    assert not ROOT.exists()
    proof,draft=map(base.load,(stage.PROOF,stage.REVIEW))
    release=base.load(stage.parent.RELEASE)
    assert base.digest(stage.parent.ROM)==proof['candidate_sha256']==release['candidate_sha256']
    assert base.digest(stage.REVIEW)==proof['review_sha256']
    original,target=[base.NdsImage.open(stage.parent.ROM) for _ in range(2)]
    before=prior.files(original)
    for path,raw in stage.prior.transform(original,draft['records']):
        assert raw==Path(proof['archives'][path]['path']).read_bytes()
        assert stage.sha(raw)==proof['archives'][path]['sha256']
        target.replace_file(path,raw)
    after=prior.files(target)
    assert before.keys()==after.keys() and {k for k in before if before[k]!=after[k]}==set(proof['archives'])
    ROOT.mkdir(); target.save(ROM)
    for path in proof['archives']:
        target.replace_file(path,before[path])
    assert bytes(target.rom.save())==stage.parent.ROM.read_bytes()
    inputs=base.load(prior.prior.INPUTS)+[dict(start=n,duration=5,buttons=['A']) for n in range(2600,5700,240)]
    base.save(ROOT/'inputs.json',inputs)
    inventory,_,_=stage.prior.scoped_inventory()
    arm=before[stage.ARM]; variants={}
    for scene,(path,block,lo,hi,ident) in SCENES.items():
        for side,fileset in (('before',before),('after',after)):
            bank=stage.IlnkContainer.parse(before[LIL]); start=bank.blocks[22]
            source=stage.IlnkContainer.parse(fileset[path]).blocks[block]
            commands,_=inventory(arm,source)
            chosen=[r for r in commands if lo<=r['offset']<hi]
            assert len(chosen)==(6 if scene=='london' else 4)
            assert all(r['word']==0x4000 and not r['ancestor_0100_offsets'] for r in chosen)
            assert chosen[0]['offset']==lo and chosen[-1]['offset']+chosen[-1]['native_extent']==hi
            end=8+unpack_from('<H',source,4)[0]
            original_end=source[end-4:end]
            assert original_end==bytes(4)
            logical=bytearray(start[:56]+source[lo:hi]+original_end)
            pack_into('<H',logical,4,len(logical)-8)
            fixture=bytes(logical)+bytes(-len(logical)%4)
            replay,_=inventory(arm,fixture)
            assert len(replay)==9+len(chosen)+1 and replay[-1]['word']==0
            assert all(a['whole_command_hex']==b['whole_command_hex'] for a,b in zip(chosen,replay[9:-1],strict=True))
            bank.blocks[22]=fixture
            image=base.NdsImage.open(stage.parent.ROM); image.replace_file(LIL,bank.to_bytes())
            filename=ROOT/f'{scene}_{side}_RESEARCH_ONLY.nds'; image.save(filename)
            variants[f'{scene}_{side}']=dict(path=filename.as_posix(),sha256=base.digest(filename),file_path=path,block=block,
                original_source_commands=[lo,hi],id=ident,fixture_sha256=stage.sha(fixture))
    base.save(SETUP,dict(candidate_sha256=base.digest(ROM),parent_sha256=release['candidate_sha256'],proof_sha256=base.digest(stage.PROOF),
        whole_parent_inverse_exact=True,fixture_ROMs=variants,fixture_scope='Two bounded original speech sequences staged at Lil’s entry, with no other source command edits.'))


def capture(case):
    fixture=base.load(SETUP)['fixture_ROMs'][case]
    assert base.digest(fixture['path'])==fixture['sha256'] and not (ROOT/case).exists()
    old=sys.argv
    try:
        sys.argv=[sys.argv[0],'--rom',fixture['path'],'--out',str(ROOT/case),'--frames','5700',
            '--inputs-json',str(ROOT/'inputs.json'),'--capture-every','999999','--capture-at',
            *map(str,(2100,*range(3060,3461,20),5000,5500))]
        prior.harness.main()
    finally:
        sys.argv=old


def startup():
    setup=base.load(SETUP)
    assert setup['candidate_sha256']==base.digest(ROM)
    proof=ROOT/'startup_input.json'
    base.save(proof,dict(research_ROM_sha256=setup['candidate_sha256'],registered_input=dict(candidate_sha256=setup['parent_sha256'])))
    boot=prior.prior.boot
    FunctionType(boot.startup_replay.main.__code__,vars(boot.startup_replay)|dict(EVIDENCE=proof,ROM=ROM,
        STARTUP=ROOT/'own_startup',PRIOR=prior.ROOT/'own_startup'))()
    FunctionType(boot.startup_check.verify_startup.__code__,vars(boot.startup_check)|dict(ROOT=ROOT,ROM=ROM,
        PROOF=proof,BIOGRAPHIES=prior.ROOT,BOOT=STARTUP))()


def verify():
    assert not LIVE.exists()
    setup,draft=map(base.load,(SETUP,stage.REVIEW))
    all_frames={}; evidence={str(SETUP):base.digest(SETUP)}
    for case in MODES:
        path=ROOT/case/'capture_report.json'; report=base.load(path)
        assert report['ROM_sha256']==setup['fixture_ROMs'][case]['sha256'] and report['frames']==5700
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert not report.get('battery_save_preloaded') and not any(v for k,v in report.items() if k.startswith('synthetic_'))
        assert report['scripted_input_schedule']==base.load(ROOT/'inputs.json')
        all_frames[case]=prior.photos(report); evidence[str(path)]=base.digest(path)
    observed,unchanged={},{}
    for scene,(_,_,_,_,ident) in SCENES.items():
        old,new=[all_frames[f'{scene}_{side}'] for side in ('before','after')]
        row=next(r for r in draft['records'] if r['id']==ident)
        masks=[prior.prior.masks(bytes.fromhex(row[f'{side}_native']['page']['native_plane_hex'])) for side in ('before','after')]
        holds=[]
        for frame in sorted(old.keys() & new.keys()):
            before,a=old[frame]; after,b=new[frame]
            if prior.body_masks(a)!=masks[0] or prior.body_masks(b)!=masks[1]: continue
            diff=ImageChops.difference(a,b).getbbox()
            assert diff and 16<=diff[0]<diff[2]<=232 and 296<=diff[1]<diff[3]<=360
            holds.append(dict(frame=frame,before=before,after=after,body_difference_bounds=diff))
        assert holds,scene
        observed[ident]=holds[0]
        unchanged[scene]=[f for f in (2100,5000,5500) if old[f][0]['framebuffer_sha256']==new[f][0]['framebuffer_sha256']]
        assert len(unchanged[scene])==3
    base.save(LIVE,dict(candidate_sha256=setup['candidate_sha256'],parent_sha256=setup['parent_sha256'],observed=observed,
        unchanged_sampled_frames=unchanged,original_body_plane_only=True,initialized_excerpts_at_Lil_entry=True,
        natural_London_or_Rafael_event_activation=False,hardware=False,other_eight_records_offline_only=True,evidence=evidence))
    print('Matched complete before-and-after masks for Lil’s tag and Rafael’s selector 00 question, plus six unchanged surrounding frames.')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('action',choices=(*MODES,'prepare','startup','verify'))
    action=parser.parse_args().action
    capture(action) if action in MODES else globals()[action]()
