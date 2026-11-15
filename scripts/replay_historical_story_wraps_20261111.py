"""Verify the natural Lil opening and a representative initialized Carlo exchange."""

import argparse
from pathlib import Path
from struct import pack_into, unpack_from
import sys
from types import FunctionType

from PIL import ImageChops

from scripts import headless_desmume_v193 as harness
from scripts import replay_lil_ceramics_wrap_20261111 as prior
from scripts import stage_historical_story_wraps_20261111 as stage
from scripts.audit_lil_B221_English_paths_v7004 import body_masks, photos
from scripts.verify_release_baseline import files


base = stage.base
ROOT = Path('out/historical_story_wraps_20261111_v3')
ROM = ROOT / 'historical_story_wraps_RESEARCH_ONLY.nds'
SETUP, LIVE, STARTUP = (ROOT/name for name in ('fixture_receipt.json','story_wrap_gameplay.json','own_startup_verification.json'))
HISTORICAL = Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_opening_trace_v1706_RESEARCH_ONLY/capture_report.json')
LIL_REVIEW = Path('translations/lil_opening_final_review_v1.json')
PAPAL = '/data/SC2.DK4'
MODES = ('opening_before','opening_after','carlo_before','carlo_after')


def prepare():
    assert not ROOT.exists()
    proof, draft = map(base.load,(stage.PROOF,stage.REVIEW))
    assert proof['review_sha256']==base.digest(stage.REVIEW)
    old = base.load(stage.parent.RELEASE)
    assert base.digest(stage.parent.ROM)==old['candidate_sha256']==proof['candidate_sha256']
    target, original = [base.NdsImage.open(stage.parent.ROM) for _ in range(2)]
    before = files(original)
    for path, raw in stage.transform(original,draft['records']):
        evidence = proof['archives'][path]
        assert stage.sha(raw)==evidence['sha256'] and stage.sha(before[path])==evidence['source_sha256']
        assert raw==Path(evidence['path']).read_bytes()
        target.replace_file(path,raw)
    after = files(target)
    assert before.keys()==after.keys()
    assert {k for k in before if before[k]!=after[k]}==set(proof['archives'])
    assert len(proof['archives'])==4
    ROOT.mkdir()
    target.save(ROM)
    for path in proof['archives']:
        target.replace_file(path,before[path])
    assert bytes(target.rom.save())==stage.parent.ROM.read_bytes()

    opening = base.load(HISTORICAL)
    assert opening['cold_boot'] and not opening['savestate_loaded'] and not opening.get('battery_save_preloaded')
    inputs = opening['scripted_input_schedule']
    base.save(ROOT/'opening_inputs.json', inputs)
    old_sheets = base.load(LIL_REVIEW)['records']
    opening_rows = [row for row in draft['records'] if row['block']==22 and row['file_path']==PAPAL]
    opening_frames = {row['id']:next(x for x in old_sheets if x['id']==row['id'])['actual_holds'][0]['frame']
                      for row in opening_rows}
    assert len(opening_frames)==3
    carlo_inputs = base.load(prior.INPUTS) + [dict(start=n,duration=5,buttons=['A']) for n in range(2600,7600,240)]
    base.save(ROOT/'carlo_inputs.json',carlo_inputs)
    variants = {}
    inventory,_,_ = stage.scoped_inventory()
    for side, archive_raw in (('before',before[PAPAL]),('after',after[PAPAL])):
        bank = stage.IlnkContainer.parse(before[PAPAL])
        selected = stage.IlnkContainer.parse(archive_raw).blocks[234]
        end = 8+unpack_from('<H',selected,4)[0]
        prelude = bank.blocks[22][8:56]
        logical = bytearray(bank.blocks[22][:8]+prelude+selected[8:end]); pack_into('<H',logical,4,len(logical)-8)
        fixture = bytes(logical)+bytes(-len(logical)%4)
        source,_ = inventory(before[stage.ARM],selected)
        wrapped,_ = inventory(before[stage.ARM],fixture)
        assert len(source)==20 and len(wrapped)==29 and all(a['whole_command_hex']==b['whole_command_hex'] and
            a['offset']+len(prelude)==b['offset'] for a,b in zip(source,wrapped[9:],strict=True))
        bank.blocks[22]=fixture
        image=base.NdsImage.open(stage.parent.ROM)
        image.replace_file(PAPAL,bank.to_bytes())
        path=ROOT/f'carlo_{side}_RESEARCH_ONLY.nds'; image.save(path)
        variants[side] = dict(path=path.as_posix(),sha256=base.digest(path),block_sha256=stage.sha(fixture))
    base.save(SETUP,dict(parent_sha256=old['candidate_sha256'],candidate_sha256=base.digest(ROM),
        proof_sha256=base.digest(stage.PROOF), opening_frames=opening_frames, opening_end=21600,
        carlo_ROMs=variants, whole_parent_inverse_exact=True, all_Carlo_commands_preserved=True))


def capture(case):
    kind,side=case.split('_')
    setup=base.load(SETUP)
    if kind=='opening':
        rom=stage.parent.ROM if side=='before' else ROM
        expected=setup['parent_sha256' if side=='before' else 'candidate_sha256']
        exact=[2000,6000,*setup['opening_frames'].values(),20500,21200,21550]
        frames=sorted(set(exact)|{frame+delta for frame in setup['opening_frames'].values() for delta in (-48,-24,24,48)})
        end=setup['opening_end']
    else:
        fixture=setup['carlo_ROMs'][side]
        rom,expected=Path(fixture['path']),fixture['sha256']
        frames=[2100,*range(3970,4521,24),7350,7520]
        end=7600
    assert base.digest(rom)==expected
    assert not (ROOT/case).exists()
    previous=sys.argv
    try:
        sys.argv=[sys.argv[0],'--rom',str(rom),'--out',str(ROOT/case),'--frames',str(end),
            '--inputs-json',str(ROOT/f'{kind}_inputs.json'),'--capture-every','999999','--capture-at',*map(str,frames)]
        harness.main()
    finally:
        sys.argv=previous


def startup():
    setup=base.load(SETUP)
    assert setup['candidate_sha256']==base.digest(ROM)
    proof=ROOT/'startup_input.json'
    base.save(proof,dict(research_ROM_sha256=setup['candidate_sha256'],registered_input=dict(candidate_sha256=setup['parent_sha256'])))
    boot=prior.boot
    predecessor=prior.ROOT
    FunctionType(boot.startup_replay.main.__code__,vars(boot.startup_replay)|dict(EVIDENCE=proof,ROM=ROM,
        STARTUP=ROOT/'own_startup',PRIOR=predecessor/'own_startup'))()
    FunctionType(boot.startup_check.verify_startup.__code__,vars(boot.startup_check)|dict(ROOT=ROOT,ROM=ROM,
        PROOF=proof,BIOGRAPHIES=predecessor,BOOT=STARTUP))()


def verify():
    setup,draft=map(base.load,(SETUP,stage.REVIEW))
    observed={}; evidence={}
    reports={}
    for case in MODES:
        path=ROOT/case/'capture_report.json'
        kind,side=case.split('_')
        report=base.load(path)
        expected=(setup['parent_sha256' if side=='before' else 'candidate_sha256'] if kind=='opening'
                  else setup['carlo_ROMs'][side]['sha256'])
        assert report['ROM_sha256']==expected and report['cold_boot'] and not report['savestate_loaded']
        assert not report.get('battery_save_preloaded') and not report['callback_errors']
        assert not any(v for k,v in report.items() if k.startswith('synthetic_'))
        assert report['scripted_input_schedule']==base.load(ROOT/f'{kind}_inputs.json')
        reports[case]=photos(report); evidence[str(path)]=base.digest(path)
    for kind, ids in (('opening',setup['opening_frames']),('carlo',{'DK4_MES_B234_R0023':4282})):
        left,right=[reports[f'{kind}_{side}'] for side in ('before','after')]
        for ident, expected in ids.items():
            row=next(r for r in draft['records'] if r['file_path']==PAPAL and r['id']==ident)
            masks=[prior.masks(bytes.fromhex(row[f'{side}_native']['page']['native_plane_hex'])) for side in ('before','after')]
            matches=[]
            for frame in sorted(left.keys() & right.keys(),key=lambda n:abs(n-expected)):
                old,a=left[frame]; new,b=right[frame]
                if body_masks(a)!=masks[0] or body_masks(b)!=masks[1]: continue
                diff=ImageChops.difference(a,b).getbbox()
                assert diff and 16<=diff[0]<diff[2]<=232 and 296<=diff[1]<diff[3]<=360
                matches.append(dict(frame=frame,before=old,after=new,changed_bounds=diff))
            assert matches,(kind,ident,expected)
            observed[ident]=matches[0]
    unchanged = {}
    for kind, frames in (('opening',(2000,6000,20500,21200,21550)),('carlo',(2100,7350,7520))):
        left,right=[reports[f'{kind}_{side}'] for side in ('before','after')]
        unchanged[kind]=[frame for frame in frames if left[frame][0]['framebuffer_sha256']==right[frame][0]['framebuffer_sha256']]
        assert len(unchanged[kind])==len(frames)
    base.save(LIVE,dict(candidate_sha256=setup['candidate_sha256'],parent_sha256=setup['parent_sha256'],
        observed=observed,unchanged_sampled_frames=unchanged,original_body_plane_only=True,
        natural_Lil_New_Game=True,Carlo_initialized_in_Lil_entry=True,hardware=False,
        other_eight_changed_records_offline_only=True,evidence=evidence|{str(SETUP):base.digest(SETUP)}))
    print('Three ordinary opening pages and the representative Carlo page matched all native glyphs; eight surrounding frames were exact.')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=(*MODES,'prepare','verify','startup'))
    action=parser.parse_args().action
    capture(action) if action in MODES else globals()[action]()
