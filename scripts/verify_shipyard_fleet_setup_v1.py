"""Verify source-native dispatch, the live Yard flows and candidate startup."""

import argparse
import inspect
from hashlib import sha256
from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs
from ndspy.code import MainCodeFile
from PIL import ImageChops
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R5

from dk4tool.patch.shipyard_fleet_setup_wrap_v1 import EQUIPMENT_PARAGRAPH, HOOK, NOTICE_PARENT, PRIOR, YES_NO_PARENT
from dk4tool.rom.nds import NdsImage
from scripts import preflight_shipyard_fleet_setup_v1 as intake
from scripts import stage_shipyard_fleet_setup_v2 as stage
from scripts import verify_setup_save_equipment_v1 as precedent
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.native_machine_scoped_v764 import machine
from scripts.preflight_shared_crew_notices_v1 import with_components
from scripts.replay_shipyard_fleet_setup_v1 import EQUIPMENT, ROOT as BASELINE
from scripts.register_setup_save_equipment_v1 import RELEASE as PARENT
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_setup_save_equipment_v1 import ARM, COMMON, check_stored
from scripts.verify_captain_biographies_v1 import captured, shots
from scripts.verify_shared_crew_selector_v1 import ARGS, dispatch


ROOT, ROM, PROOF = stage.ROOT, stage.ROM, stage.PROOF
LIVE = ROOT / 'shipyard_fleet_gameplay_verification.json'
BOOT = ROOT / 'own_startup_verification.json'
CHECKPOINT = ROOT / 'approved_checkpoint.json'
CATALOGUES = ROOT / 'name_and_city_expansion_verification.json'
QA = Path('work/shipyard_fleet_setup_repo_qa_20261111.xml')
PAPER = (16, 296, 244, 344)


def selector_cases(arm, ownership):
    image = MainCodeFile(arm, 0x02000000)
    tail = image.sections[-1]
    start = ownership['selector']
    branch = start + 60
    offset = branch - tail.ramAddress
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    line, = decoder.disasm(tail.data[offset:offset + 4], branch)
    assert line.mnemonic == 'beq'
    admiral_entry = int(line.op_str.lstrip('#'), 16)
    assert start < admiral_entry < tail.ramAddress + len(tail.data)
    u = machine(arm)
    proofs = []
    targets = (PRIOR, EQUIPMENT_PARAGRAPH, admiral_entry)
    for parent, n, expected in (
        (NOTICE_PARENT, 261, EQUIPMENT_PARAGRAPH), (YES_NO_PARENT, 279, admiral_entry),
        (YES_NO_PARENT, 261, PRIOR), (NOTICE_PARENT, 279, PRIOR), (NOTICE_PARENT, 329, PRIOR),
        (NOTICE_PARENT, 260, PRIOR), (NOTICE_PARENT, 262, PRIOR),
        (YES_NO_PARENT, 278, PRIOR), (YES_NO_PARENT, 280, PRIOR), (0x02054764, 279, PRIOR),
    ):
        target, regs = dispatch(u, HOOK, {0xC4: parent, 0xD0: n}, targets)
        assert target == expected and regs[:3] == ARGS[:3]
        proofs.append(dict(parent=parent, message_ID=n, verified_first_continuation=target))
    modes = []
    for mode in (0, 1):
        u.reg_write(UC_ARM_REG_R5, mode)
        u.emu_start(0x0205A4D4, 0x020546B8, count=8)
        assert u.reg_read(UC_ARM_REG_PC) == 0x020546B8
        assert u.reg_read(UC_ARM_REG_R0) == 280 + mode
        modes.append(dict(original_fleet_picker_mode=mode, native_message_ID=280 + mode))
    return dict(dispatch_scope=proofs, original_fleet_list_modes=modes)


def load_case(case, proof):
    paths = [root / case / 'capture/capture_report.json' for root in (BASELINE, ROOT)]
    old, new = map(load, paths)
    assert old['ROM_sha256'] == proof['registered_input']['candidate_sha256']
    assert new['ROM_sha256'] == proof['research_ROM_sha256']
    assert old['core_options'] == new['core_options']
    assert old['battery_save_preloaded']['source_sha256'] == new['battery_save_preloaded']['source_sha256']
    assert all(run['cold_boot'] and not run['savestate_loaded'] and not run['callback_errors']
               and not any(value for key, value in run.items() if key.startswith('synthetic_'))
               for run in (old, new))
    terminals = [root / case / 'terminal.json' for root in (BASELINE, ROOT)]
    traces = list(map(load, terminals))
    for trace in traces:
        assert all(digest(path) == expected for path, expected in trace['evidence'].items())
    assert traces[0]['target_requests'] == traces[1]['target_requests']
    return shots(old), shots(new), traces[1]['target_requests'], paths + terminals


def modal_mask(shot, number, proof):
    row, = [r for r in proof['rendered_variants'] if r['message_ID'] == number and not r['arguments']]
    image = captured(shot)
    foreground = bytes(pixel == (0, 8, 0) for pixel in image.crop(PAPER).get_flattened_data())
    assert sha256(foreground).hexdigest() == row['native_ink_sha256'], (number, shot['frame'])
    return dict(message_ID=number, lines=row['lines'], complete_ink_and_blank_mask=True,
                ink_pixels=foreground.count(1), capture=shot)


def verify_live():
    proof = load(PROOF)
    assert digest(ROM) == proof['research_ROM_sha256']
    old_yard, yard, yard_trace, evidence = load_case('yard', proof)
    old_fleet, fleet, fleet_trace, fleet_evidence = load_case('fleet', proof)
    ids = {entry['message_ID'] for entry in yard_trace + fleet_trace}
    assert ids == {265, 280, 281, 285, 286}
    assert old_yard[7800]['framebuffer_sha256'] == yard[7800]['framebuffer_sha256']
    assert old_yard[8200]['framebuffer_sha256'] == yard[8200]['framebuffer_sha256']
    observed = [modal_mask(yard[7800], 265, proof)]
    for frame, number in ((9400, 280), (10360, 281), (10840, 285), (11680, 286)):
        observed.append(modal_mask(fleet[frame], number, proof))
        if number in (280, 281, 286):
            diff = ImageChops.difference(captured(old_fleet[frame]), captured(fleet[frame])).getbbox()
            assert diff and diff[1] >= PAPER[1] and diff[3] <= PAPER[3], (number, diff)
            observed[-1]['changed_bounds'] = list(diff)
    assert all(old_fleet[n]['framebuffer_sha256'] == fleet[n]['framebuffer_sha256']
               for n in (9640, 9880, 10600, 11080, 11440, 11560, 11800))
    assert fleet[10840]['framebuffer_sha256'] != fleet[11080]['framebuffer_sha256']
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    save(LIVE, dict(candidate_sha256=digest(ROM), observed_ids=[265, 280, 281, 285, 286], live_complete_panels=observed,
        buy_to_ship_name=yard[8200], reorganize_to_list=fleet[9640], disband_to_list=fleet[10600],
        disband_cancel=fleet[11080], disband_dock_return=fleet[11800], request_trace=yard_trace + fleet_trace,
        native_selector_controls=selector_cases(arm, proof['ownership']), hardware=False,
        original_battery_save_inputs_with_controller_and_stylus=True, inherited_formed_fleet_save_fixture=True,
        no_new_regional_fleet_formation_claim=True,
        evidence={str(path): digest(path) for path in (*evidence, *fleet_evidence, PROOF, Path(__file__))}))
    print('The live Buy, Fleet Setup, Disband selection and cancellation all passed.')


def verify_startup():
    source = checked_text(inspect.getsource(precedent.verify_startup), {
        "parent_path = BIOGRAPHIES / 'own_startup/capture/capture_report.json'":
            "parent_path = EQUIPMENT / 'own_startup/capture/capture_report.json'",
        "prior_proof = BIOGRAPHIES / 'own_startup_verification.json'":
            "prior_proof = EQUIPMENT / 'own_startup_verification.json'",
    })
    env = {**vars(precedent), **globals()}
    exec(compile(source, __file__ + '::same-cold-boot-and-name-contract', 'exec'), env)
    env['verify_startup']()


def verify_catalogues():
    proof, preflight = map(load, (PROOF, intake.PROOF))
    assert preflight['registered_input'] == proof['registered_input']
    parent = load(PARENT)
    ctx = intake.modal.RegisteredRuntime(PARENT, parent['own_registered_startup'], captain=3)
    assert ctx.receipt() == proof['registered_input']
    image = NdsImage.open(ROM)
    clone = with_components(ctx, image.read_file(ARM), image.read_file(COMMON))
    raster, _, _ = intake.modal.font_tools(image)
    font = intake.modal.GameAsciiFont.from_arm9(clone.arm)
    source = {r['message_ID']: r for r in load(stage.MANUSCRIPT)['records']}
    stored = {r['message_ID']: r['stored_hex'] for r in proof['records']}
    samples = {
        261: [(r['text'],) for r in preflight['current_native_town_names']],
        279: [(r['given'], r['surname']) for r in preflight['current_native_given_and_surnames'] if r['given']],
    }
    run = check_stored()
    results = []
    for n, variants in samples.items():
        english = stage.AMENDMENTS[n]['english']
        row = source[n] | dict(english=english, current_hex=stored[n],
            current_copies=[dict(wrapper=source[n]['native_callers'][0]['target'])])
        for args in dict.fromkeys(variants):
            case = run(clone, row, args)
            clone.calls.clear()
            lines = [line.strip() for line in case['native_wrapper_lines']]
            assert 1 <= len(lines) <= 3 and all(line for line in lines)
            assert all(0 < len(line.encode('cp932')) <= 36 for line in lines)
            wide_raw = any(width > 36 for width in case['native_width_units'])
            if wide_raw:
                # Raw widths include pair-phase blanks. Check the actual bitmap when
                # those bytes put a row over the nominal byte count.
                _, checked_lines, _, _ = intake.modal.render(raster, font, clone.arm,
                    bytes.fromhex(case['native_wrapper_output_hex']))
                assert checked_lines == lines
            assert n != 279 or lines[-1].endswith('as admiral?')
            results.append(dict(message_ID=n, arguments=args, lines=lines, expanded_hex=case['expanded_hex'],
                native_display_hex=case['native_wrapper_output_hex'], raw_guard_width_verified_in_font=wide_raw))
    save(CATALOGUES, dict(candidate_sha256=digest(ROM), rows=results, towns=90,
        checked_stock_name_pairs=sum(r['message_ID'] == 279 for r in results),
        source_eligibility_not_inferred_from_render_samples=True, formatting_offline=True,
        evidence={str(p): digest(p) for p in (intake.PROOF, PROOF, Path(__file__))}))
    print(f'{len(results)} native city and name expansions fit the complete original modal body.')


def approve(viewed):
    proof, live, startup = map(load, (PROOF, LIVE, BOOT))
    assert viewed == [sheet['sha256'] for sheet in proof['sheets']]
    assert all(digest(sheet['path']) == sheet['sha256'] for sheet in proof['sheets'])
    assert proof['research_ROM_sha256'] == live['candidate_sha256'] == startup['candidate_sha256'] == digest(ROM)
    assert load(CATALOGUES)['candidate_sha256'] == digest(ROM)
    save(CHECKPOINT, dict(candidate_sha256=digest(ROM), approved_for_registered_successor=True,
        observed_ids=live['observed_ids'], stored_records=len(proof['records']),
        viewed_pages=sum(sheet['pages'] for sheet in proof['sheets']),
        evidence={str(path): digest(path) for path in (PROOF, LIVE, BOOT, QA, CATALOGUES, Path(__file__))}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('live', 'startup', 'catalogues', 'approve'))
    parser.add_argument('--viewed-sheets', nargs='+')
    args = parser.parse_args()
    if args.action == 'approve':
        approve(args.viewed_sheets)
    elif args.action == 'live':
        verify_live()
    elif args.action == 'catalogues':
        verify_catalogues()
    else:
        verify_startup()
