"""Measure source-authored FE staging and preflight ordinary FE wraps on the unchanged painter."""
from collections import defaultdict
from pathlib import Path
from types import FunctionType

from dk4tool.patch.grand_race_menu_release import sha
from scripts import Rafael_B45_FE_source_painter_v7894 as source_FE
from scripts import square_shopkeeper_font_oracles_v7020 as old_font
from scripts.audit_story_glyph_consistency import load, save
from scripts.check_editorial_compiled_pages_v6 import check_FE_rows
from scripts.plan_rafael_B166_B167_ordinary_v1 import ROOT, STAGED
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime

PLAN = ROOT / 'ordinary_plans_v2/automatic_plans.json'
OUT = ROOT / 'native_FE_source_staging_v1'


def digest(path):
    return sha(Path(path).read_bytes())


def observed_rows(events):
    rows = defaultdict(list)
    for e in events:
        code = e['code']
        if code == 32:
            continue
        text = bytes([code]).decode('cp932') if e['kind']=='ascii' else code.to_bytes(2,'big').decode('cp932',errors='replace')
        rows[e['y']].append((e['x'],text))
    return [dict(y=y,x=entries[0][0],text=''.join(t for _,t in entries)) for y,entries in sorted(rows.items())]


def build_painter(rt):
    ctx = RegisteredRuntime(rt['release_proof'],rt['startup_proof'],captain=0)
    assert ctx.receipt()==rt
    factory = FunctionType(old_font.make_painter.__code__,
        {**old_font.make_painter.__globals__,'CURRENT_ARM9':sha(ctx.arm)},argdefs=old_font.make_painter.__defaults__)
    fe = FunctionType(source_FE.make_source_painter.__code__,
        {**source_FE.make_source_painter.__globals__,'CURRENT_ARM9':sha(ctx.arm),'ASCII_painter':factory},
        argdefs=source_FE.make_source_painter.__defaults__)
    return fe(ctx.image)


def run():
    assert not OUT.exists()
    staged,plan = map(load,(STAGED,PLAN))
    painter,calibration = build_painter(staged['runtime'])
    output=[]
    def render(raw):
        data=painter(raw)
        return dict(rows=observed_rows(data['events']),complete_consumed_bytes=data['complete_consumed_bytes'],
            physical_sha256=sha(data['physical']),logical_sha256=sha(data['logical']))
    def body(row,key):
        raw=bytes.fromhex(row[key])
        if key in ('source_hex','current_hex'):
            assert raw[0]==254
            raw=raw[1:]
        return raw.replace(b'FI',b'Rafael').replace(b'FA',b'Castor').replace(b'FU',b'Rafael Castor')
    for r in staged['records']:
        raw_source,raw_current=(body(r,k) for k in ('source_hex','current_hex'))
        samples={}
        for side,raw in [('source',raw_source),('current',raw_current)]:
            try:
                samples[side]=render(raw)
            except AssertionError as err:
                samples[side]=dict(failure=repr(err))
        output.append(dict(id=r['id'],source_reference=r['source_reference'],current_reference=r['current_reference'],
            source_prefix_rows=len(raw_source)-len(raw_source.lstrip(b'\n')),source=r['source_Japanese'],
            current=r['current_stored_text'],finding=r['FE_layout_finding'],observations=samples))
    ordinary=[]
    for p in plan['records']:
        if p['source_selector']!=254:
            continue
        b=bytes.fromhex(p['encoded_hex'])
        assert b[0]==254
        b=b[1:].replace(b'FI',b'Rafael')
        try:
            r=painter(b)
            pos=observed_rows(r['events'])
            proof=check_FE_rows(b,r)
            ordinary.append(dict(id=p['id'],planned=p['lines'],observed=pos,pass_rows=proof))
        except AssertionError as err:
            ordinary.append(dict(id=p['id'],planned=p['lines'],observed=pos,failure=repr(err)))
    assert len(output)==22 and len(ordinary)==7
    OUT.mkdir()
    save(OUT/'native_FE_rows.json',dict(runtime=staged['runtime'],staged=output,ordinary=ordinary,calibration=calibration,
        same_current_original_painter_for_source_placement_and_revised_ordinary_preflight=True,
        source_macros_expanded_to_current_Rafael_defaults_for_only_control_position_diagnostic=True,
        native_ABI_stored_and_actual_gameplay_not_executed_by_this_preflight=True,new_credit=0,
        evidence={str(p):digest(p) for p in [PLAN,STAGED,Path(__file__),Path(source_FE.__file__)]}))
    print('Ordinary FE row failures:',[(r['id'],r.get('failure')) for r in ordinary if 'failure' in r])
    print('Source FE anchors:',[(r['id'],[(e['x'],e['y']) for e in r['observations']['source'].get('rows',[])])
        for r in output])


if __name__ == '__main__':
    run()
