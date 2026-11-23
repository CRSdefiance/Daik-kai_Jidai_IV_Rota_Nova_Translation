"""Check all revised Ceuta pages, substitutions, and the ordinary return paths."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import FunctionType

from PIL import ImageChops

from dk4tool.dialogue.reviewed_choice_object_v2 import labels
from scripts import audit_rafael_ceuta_arrival_20261119 as baseline
from scripts import check_rafael_voyage_ceuta_20261119 as precedent
from scripts import replay_rafael_ceuta_contract_routes_20261119 as replay
from scripts import review_rafael_ceuta_contract_routes_20261119 as stage
from scripts import verify_rafael_first_voyage_debrief_20261119 as dynamic
from scripts.source_locked_derivation_v5118 import checked_text

base, native, deck = precedent.base, precedent.native, precedent.deck
ROOT = stage.STAGED / 'verified_display'
PROOF = ROOT / 'native_and_ordinary_gameplay.json'
OFFLINE_ROOT = stage.STAGED / 'native_display_v2'
OFFLINE = OFFLINE_ROOT / 'native_display.json'
STARTUP_DIR = stage.STAGED / 'own_startup'
STARTUP = stage.STAGED / 'own_startup_verification.json'


def tools():
    previous = base.load(stage.parent.RELEASE)
    ctx = native.RegisteredRuntime(stage.parent.RELEASE,previous['own_registered_startup'],captain=3)
    image = base.NdsImage.open(stage.ROM)
    assert all(ctx.image.read_file(p) == image.read_file(p) for p in (native.ARM,deck.FONT,baseline.COMMON,'/data/EV0.DK4'))
    _, paint = dynamic.display.early.prior.precedent.planners(ctx.arm)
    return ctx, image, (ctx.arm,image.read_file(deck.FONT),paint,stage.system.native_painter(ctx))


def company_page(ctx, painter, raw, plan):
    compiled = bytes.fromhex(plan['encoded_hex'])
    assert raw in (compiled,compiled+b' ') and raw[0] == 254 and raw[1:].count(b'FO') == 1
    old = dynamic.display.fe
    source = checked_text(getsource(old.expand), {
        ".replace(b'FO',b'Argot Co.')": ".replace(b'FO',b'Li Clan')",
    })
    scope = vars(old).copy()
    exec(compile(source,__file__+'::null-actor-expansion','exec'),scope)
    expanded = ctx.execute(scope['expand'],raw[1:])
    assert len(expanded['cases']) == 4
    assert {bytes.fromhex(c['output_hex']) for c in expanded['cases']} == {raw[1:].replace(b'FO',b'Li Clan')}
    cases = []
    for case in plan['company_render_cases']:
        name = case['name']
        value = name.encode('cp932')
        proposed = bytes.fromhex(case['expanded_body_hex'])
        actual = raw[1:].replace(b'FO',value)
        assert actual in (proposed,proposed+b' ')
        result = painter(actual)
        pixels = result['physical']
        assert result['complete_consumed_bytes'] == len(actual) and len(pixels) == 228*64
        assert pixels == painter(proposed)['physical']
        for i,line in enumerate(plan['lines']):
            expected = [c for c in stage.codes(line.replace('{MACRO:FO}',name).encode('cp932')) if c!=32]
            assert [e['code'] for e in result['events'] if e['y']==12*i and e['code']!=32] == expected
        assert all(not any(pixels[y*228+216:(y+1)*228]) for y in range(64))
        plane = b''.join(pixels[y*228:y*228+216] for y in range(64))
        cases.append(dict(company=name,body_hex=actual.hex(),native_plane_hex=plane.hex(),complete_safe_rows=True))
    assert len(cases) == 8
    return dict(layouts=cases,native_null_actor_substitution=expanded,plane=cases[0]['native_plane_hex'])


def native_pages():
    assert not OFFLINE_ROOT.exists()
    stored,draft = map(base.load,(stage.PROOF,stage.OUTPUT))
    assert stored['candidate_sha256'] == base.digest(stage.ROM) and stored['manuscript_sha256'] == base.digest(stage.OUTPUT)
    assert stored['whole_parent_inverse']
    ctx,image,(arm,cjk,paint,fe_paint) = tools()
    bank = native.IlnkContainer.parse(image.read_file(deck.SC0)).blocks
    rows = {r['id']:r for r in draft['records']}
    checked,retained,previews = [],[],[]
    expand = dynamic.names.expander()
    model = dynamic.names.current_names(ctx) | {'FO':'Li Clan'}
    for group in stored['groups']:
        block = bank[group['block']]
        assert native.digest(block) == group['after']
        for command in group['commands']:
            own = [rows[i] for i in command['record_ids']]
            if not own:
                continue
            at,raw = command['stored_offset'],bytes.fromhex(command['stored'])
            assert block[at:at+len(raw)] == raw
            if all(r['decision']=='retention' for r in own):
                assert command['stored'] == command['current']
                retained.extend(r['id'] for r in own)
                continue
            row, = own
            ident = row['id']
            value = raw[5:raw.index(0,6)]
            assert value[0] == row['source_selector'] and command['word'] == 0x4000
            plan = group['plans'][ident]
            if value[0] == 254:
                result = company_page(ctx,fe_paint,value,plan)
                for label in (0,2,7):
                    res = result['layouts'][label]
                    palette = bytes.fromhex(res['native_plane_hex'])
                    previews.append((f"{ident} / company sample {label}",bytes(15 if p else 0 for p in palette)))
            else:
                result = dynamic.names.paragraph(ctx,cjk,paint,expand,None,model,row,value,plan)
                named = set(stage.TOKEN.findall(row['english']))
                samples = (('Rafael default',dynamic.STOCK),('maximum planning widths',dynamic.MAXIMUM)) if named else ()
                for label, substitutions in samples:
                    wanted = {m:substitutions[m] for m in named}
                    text = stage.TOKEN.sub(lambda m:wanted[m[0]],value[1:].decode('ascii')).encode('ascii')
                    lines = [dynamic.names.expected(line,wanted) for line in plan['lines']]
                    page, = dynamic.names.raster(ctx,cjk,paint,text,lines,1)
                    result['layouts'].append(dict(scope=label,names=wanted,pages=[page],complete_body_hex=text.hex()))
                    if label == 'maximum planning widths':
                        previews.append((f'{ident} / maximum widths',bytes.fromhex(page['native_plane_hex'])))
                regular = next((v for v in result['layouts'] if v['scope']=='Rafael default'),result['layouts'][0])
                result['plane'] = regular['pages'][0]['native_plane_hex']
                previews.append((ident,bytes.fromhex(result['plane'])))
            checked.append(result | dict(id=ident,target_hex=value.hex(),planned_lines=plan['lines']))
    assert len(checked)==13 and len(retained)==19
    OFFLINE_ROOT.mkdir()
    contact = dynamic.display.early.contact_sheets
    sheets = FunctionType(contact.__code__,contact.__globals__|{'ROOT':OFFLINE_ROOT})(previews)
    base.save(OFFLINE,dict(candidate_sha256=stored['candidate_sha256'],stage_proof_sha256=base.digest(stage.PROOF),
        revisions=checked,retentions=retained,sheets=sheets))
    print('Verified all 13 native pages, exact retentions, and company and first-name width cases.')


def gameplay():
    assert not ROOT.exists()
    stored,layouts,old = map(base.load,(stage.PROOF,OFFLINE,baseline.OUTPUT))
    paths = [replay.CAPTURE/'capture_report.json',replay.ROOT/'observer/commands.json',
        replay.CAPTURE/'navigation_command_journal.json',replay.JOURNAL,replay.ROOT/'source_contract.json']
    report,trace,journal = map(base.load,paths[:3])
    prior_report,prior_trace,prior_journal = map(base.load,(baseline.run.CAPTURE/'capture_report.json',
        baseline.run.ROOT/'observer/commands.json',baseline.run.CAPTURE/'navigation_command_journal.json'))
    assert base.digest(stage.ROM) == report['ROM_sha256'] == stored['candidate_sha256'] == layouts['candidate_sha256']
    assert prior_report['ROM_sha256'] == stored['predecessor_sha256'] == old['candidate_sha256']
    assert report['frames']==prior_report['frames']==50165 and report['cold_boot'] and not report['savestate_loaded']
    assert report['scripted_input_schedule']==prior_report['scripted_input_schedule'] and journal['commands_received']==prior_journal['commands_received']
    assert not report['callback_errors'] and not any(v for k,v in report.items() if k.startswith('synthetic_'))
    assert report['core_DLL_sha256']==prior_report['core_DLL_sha256'] and report['core_options']==prior_report['core_options']
    assert not trace['errors'] and not trace['mismatches'] and not trace['unreturned_at_capture_end']
    assert trace['all_host_slots_restored_and_core_file_exact']
    donor = report['battery_save_preloaded']
    assert donor['copied_byte_exact_before_cold_boot'] and base.digest(donor['source']) == donor['source_sha256']==old['preserved_donor']
    requests = lambda data:[(r['PC'],r['caller_LR'],r['message_ID']) for r in data['COMMON_requests'] if r['frame']>=baseline.run.START]
    assert requests(trace)==requests(prior_trace) and len(requests(trace))==20
    evidence = {str(p):base.digest(p) for p in (*paths,stage.PROOF,OFFLINE,baseline.OUTPUT,Path(__file__))}
    ctx,image,painters = tools()
    bank = native.IlnkContainer.parse(image.read_file(deck.SC0)).blocks
    font = deck.GameAsciiFont.from_arm9(ctx.arm)
    shots,prior_shots = map(deck.shots,(report,prior_report))
    revisions = {r['id']:r for r in layouts['revisions']}
    older = {r['id']:r for r in old['story_panels']}
    panels,changes,menus,unvisited = [],[],[],[]
    for group,total in zip(stored['groups'],(22,27),strict=True):
        block = group['block']
        observed = precedent.tavern.observed_commands(trace,block,group['after'])
        before = precedent.tavern.observed_commands(prior_trace,block,group['before'])
        assert len(observed)==len(before)==total
        available = {c['stored_offset']:c for c in group['commands']}
        for (entry,exit),(earlier,later) in zip(observed,before,strict=True):
            at,word = entry['source']['instruction_offset'],entry['source']['first_word']
            cmd = available.pop(at)
            assert cmd['word']==word==earlier['source']['first_word'] and cmd['current_offset']==earlier['source']['instruction_offset']
            assert exit['result_words'][0] == later['result_words'][0]
            raw = bytes.fromhex(cmd['stored'])
            assert raw == bank[block][at:at+len(raw)]
            if word == 0x2100:
                assert raw == bytes.fromhex(cmd['current']) and exit['result_words']==later['result_words']==[2,0]
                assert tuple(labels(raw))==(b'Yes, please.',b'No, thanks. Got it.')
                menus.append(shots[44405])
                continue
            if word != 0x4000:
                continue
            ident, = cmd['record_ids']
            body = raw[6:raw.index(0,6)]
            body = body.replace(b'FI',b'Rafael').replace(b'FO',b'Castor Co.')
            selector,plane,mask = precedent.expected_page(painters,raw[:6]+body+b'\0','ordinary Ceuta')
            hold,screen = precedent.hold_with_mask(entry,exit,shots,font,selector,mask)
            evidence[hold['capture']] = hold['sha256']
            panels.append(dict(id=ident,current=hold,complete_mask=True))
            if ident in revisions:
                assert plane.hex()==revisions[ident]['plane']
                old_frame = prior_shots[older[ident]['hold']['frame']]
                changes.append((ident,deck.captured(old_frame),screen))
                evidence[old_frame['path']] = old_frame['PNG_sha256']
        unvisited.extend(ident for c in available.values() for ident in c['record_ids'])
    assert len(panels)==29 and len(changes)==13 and len(menus)==1
    assert unvisited==['DK4_MES_B139_R0102']
    for frame in (36475,40085,40325,42005,42965,44405,48485,50165):
        previous,current = (deck.captured(samples[frame]) for samples in (prior_shots,shots))
        assert ImageChops.difference(previous,current).getbbox() is None
        photo = shots[frame]
        evidence[photo['path']] = photo['PNG_sha256']
    ROOT.mkdir()
    render = FunctionType(precedent.render_sheets.__code__,vars(precedent)|{'ROOT':ROOT})
    sheets = render(changes,'ceuta_trade_routes',evidence)
    base.save(PROOF,dict(candidate_sha256=stored['candidate_sha256'],predecessor_sha256=stored['predecessor_sha256'],
        ordinary_gameplay_existing_save=True,panels=panels,menu=menus[0],unvisited=unvisited,hardware=False,
        shared_and_menu_return_frames_equal=True,sheets=sheets,evidence=evidence))
    print('All 29 naturally displayed panels and both choices verified, with 13 revised pages and unchanged shared paths.')


if __name__=='__main__':
    parser=ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=('offline','gameplay','patch','capture-startup','startup'))
    action=parser.parse_args().action
    scope=vars(precedent)|dict(stage=stage,STARTUP=STARTUP,STARTUP_DIR=STARTUP_DIR)
    if action in ('capture-startup','startup'):
        FunctionType(precedent.startup.__code__,scope)(action=='capture-startup')
    elif action=='patch':
        FunctionType(precedent.patch.__code__,scope)()
    else:
        {'offline':native_pages,'gameplay':gameplay}[action]()
