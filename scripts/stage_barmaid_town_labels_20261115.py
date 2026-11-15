"""Run the original name-line drawers, then stage the two fixed-slot translations."""

from argparse import ArgumentParser
from hashlib import sha256
from pathlib import Path
from struct import pack, unpack_from
import sys
from types import FunctionType

from PIL import Image, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_SP

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.owned_name_fields_v2 import plan_arm9_name_fields
from scripts import replay_refit_help_startup_20261115 as startup
from scripts import review_barmaid_town_labels_20261115 as prior_review
from scripts.probe_button_prompt_native import STACK, call
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_release_baseline import files


base, parent = prior_review.base, prior_review.current
ARM, COMMON, CLEAN = parent.stage.ARM, parent.stage.COMMON, parent.stage.CLEAN
BASE = prior_review.BASE
ROOT = Path('work/barmaid_town_labels_display_20261115_v1')
ROM = ROOT / 'Barmaid_Town_Labels_RESEARCH_ONLY.nds'
STORED = ROOT / 'staged.json'
SHEET = ROOT / 'original_name_renderer.png'
DEPLOYED = ROOT / 'own_label_getters.json'
WIDTHS = (240, 168)
HEADER, VIEW = 0x02450000, 0x02453000
HEIGHT = 48


def paint(cpu, font, actor, original, capacity_case, target):
    start, branch, register, cells = capacity_case
    width = cells * 6
    assert width in WIDTHS
    size = width * HEIGHT // 2
    header = pack('<5I', 4, width // 4, HEIGHT, 0x02452000 - HEADER, 20)
    cpu.mem_write(HEADER - 16, b'\xA5' * (size + 52))
    cpu.mem_write(HEADER, header + bytes(size))
    call(cpu, 0xD3D80, (VIEW,))
    cpu.mem_write(STACK, pack('<4I', width, HEIGHT, 0, 0))
    call(cpu, 0xD3AFC, (VIEW, HEADER, 0, 0))
    call(cpu, 0xD5160, (STACK, VIEW, 1))
    observed = []

    def draw(u, pc, size, data):
        assert u.reg_read(UC_ARM_REG_LR) == BASE + branch + 4
        context, string = u.reg_read(UC_ARM_REG_R0), u.reg_read(UC_ARM_REG_R1)
        assert context == STACK and bytes(u.mem_read(context + 0x24, 8)) == pack('<2I', 0, 24)
        expected = original.encode('cp932') + b'\0'
        assert bytes(u.mem_read(string, len(expected))) == expected
        observed.append((string, expected))

    hook = cpu.hook_add(UC_HOOK_CODE, draw, begin=BASE + 0xD5404, end=BASE + 0xD5404)
    cpu.reg_write(UC_ARM_REG_SP, STACK)
    cpu.reg_write(register, actor)
    try:
        cpu.emu_start(BASE + start, BASE + branch + 4, count=1_000_000)
    finally:
        cpu.hook_del(hook)
    assert cpu.reg_read(UC_ARM_REG_PC) == BASE + branch + 4 and cpu.reg_read(UC_ARM_REG_SP) == STACK
    (string, text), = observed
    assert bytes(cpu.mem_read(string, len(text))) == text
    assert bytes(cpu.mem_read(HEADER, 20)) == header
    assert bytes(cpu.mem_read(HEADER - 16, 16)) == bytes(cpu.mem_read(HEADER + 20 + size, 16)) == b'\xA5' * 16
    pixels = bytes(n for p in cpu.mem_read(HEADER + 20, size) for n in (p & 15, p >> 4))
    panel = Image.frombytes('L', (width, HEIGHT), pixels)
    box = panel.getbbox()
    assert 0 <= box[0] < box[2] <= width and 24 <= box[1] < box[3] <= 36
    if target:
        expected = Image.new('L', (width, HEIGHT))
        for i, ch in enumerate(original):
            expected.paste(font.decode(ch).convert('L').point(lambda p: int(p != 0)), (i * 6, 25))
        assert expected.tobytes() == pixels
    return panel, dict(original_caller=BASE + branch, renderer=BASE + 0xD5404, complete_name=original,
        native_origin=[0, 24], supplied_width=width, ink_bounds=box, original_draw_return_verified=True,
        exact_independent_font_match=target, bitmap_header_and_neighbor_guards_exact=True,
        pixels_sha256=sha256(pixels).hexdigest())


def stage():
    assert not ROOT.exists()
    release = base.load(parent.RELEASE)
    review = base.load(prior_review.REVIEW)
    assert base.digest(base.REGISTRY) == release['registry_sha256']
    assert review['diagnostic_reference_sheet_visually_reviewed']
    ctx = RegisteredRuntime(parent.RELEASE, release['own_registered_startup'], captain=3)
    assert ctx.release['candidate_sha256'] == review['candidate_sha256']
    clean = base.NdsImage.open(CLEAN).read_file(ARM)
    target, ownership = plan_arm9_name_fields(ctx.arm,
        dict(format='dk4-owned-name-fields-proposal-v2', runtime=ctx.receipt(), fields=review['proposal']), clean)
    assert ownership == review['planned_ARM9'] and Path(review['research_ARM9']).read_bytes() == target
    assert {field['actor'] for field in ownership['fields']} == {195, 204}
    cpu, _, provider = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    metrics = unpack_from('<I', ctx.arm, 0xD5088)[0]
    assert bytes(cpu.mem_read(metrics + 4, 8)) == pack('<2I', 6, 12)
    font = GameAsciiFont.from_arm9(target)
    active = [r for r in review['records'] if r['actor'] in prior_review.EDIT]
    proofs = []
    paper = Image.new('RGB', (980, 4 * 86), '#253039')
    labels = ImageDraw.Draw(paper)
    for column, mode in enumerate(('current', 'proposed')):
        if mode == 'proposed':
            for slot in ownership['fields']:
                p = slot['RAM_pointer']
                before, after = [bytes.fromhex(slot[key]) for key in ('old_hex', 'new_hex')]
                assert bytes(cpu.mem_read(p, len(before) + 1)) == before + b'\0'
                cpu.mem_write(p, after)
                assert bytes(cpu.mem_read(p, len(after) + 1)) == after + b'\0'
        for i, row in enumerate(active):
            parts = (row['current_primary'], row['English_city_label'])
            text = row['current_joined'] if mode == 'current' else ' '.join(parts)
            for j, case in enumerate(prior_review.CALLERS):
                panel, receipt = paint(cpu, font, row['runtime_actor'], text, case, mode == 'proposed')
                proofs.append(receipt | dict(actor=row['actor'], version=mode))
                x, y = column * 490 + 5, (i * 2 + j) * 86
                labels.text((x, y + 4), f'{parts[0]}, {mode}, {case[-1]} cells', fill='white')
                crop = panel.crop((0, 14, panel.width, 46)).point(lambda p: 25 if p else 245)
                paper.paste(crop.convert('RGB').resize((panel.width * 2, 64), Image.Resampling.NEAREST), (x, y + 20))
    assert len(proofs) == 8 and sum(row['exact_independent_font_match'] for row in proofs) == 4
    assert not provider.reads and bytes(cpu.mem_read(ctx.actor_root, 0x1A04)) == ctx.actor_bytes
    ROOT.mkdir()
    paper.save(SHEET)
    image = base.NdsImage.open(parent.ROM)
    original = files(image)
    image.replace_file(ARM, target)
    deployed = files(image)
    assert original.keys() == deployed.keys() and {p for p in original if original[p] != deployed[p]} == {ARM}
    image.save(ROM)
    image.replace_file(ARM, ctx.arm)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    base.save(STORED, dict(candidate_sha256=base.digest(ROM), previous_sha256=release['candidate_sha256'],
        target_ARM9_sha256=sha256(target).hexdigest(), target_COMMON_sha256=release['target_COMMON_sha256'],
        initial_review=str(prior_review.REVIEW), review_sha256=base.digest(prior_review.REVIEW), plan=ownership,
        native_D5404_cases=proofs, sheet=str(SHEET), sheet_sha256=base.digest(SHEET),
        ordinary_name_panel_gameplay=False, native_rendering_on_supplied_bitmap=True, hardware=False))
    print('Eight complete original name draws, four independent full masks, and whole predecessor inverse pass.')


def replay_startup():
    FunctionType(startup.main.__code__, vars(startup) | dict(stage=sys.modules[__name__]))()
    boot_path = ROOT / 'own_startup_verification.json'
    boot, staged = map(base.load, (boot_path, STORED))
    assert boot['candidate_sha256'] == staged['candidate_sha256'] == base.digest(ROM)
    snap = boot['read_only_snapshot']
    snapshot = Path(snap['path'])
    assert snap['read_only_export'] and base.digest(snapshot) == snap['sha256']
    arm = base.NdsImage.open(ROM).read_file(ARM)
    cpu, get = get_machine(arm, snapshot.read_bytes())
    actors = get(0xCB184)
    values = []
    for field in staged['plan']['fields']:
        n = field['actor']
        name, city, _ = prior_review.EDIT[n]
        obj = actors + 4 + n * 32
        joined = name + ' ' + city
        actual = [prior_review.read_text(cpu, get(method, obj)) for method in (0x7EAF4, 0x7EA48, 0x7EA8C, 0x7ED88, 0x7EDD4)]
        assert actual == [city, joined, joined, name, name]
        addr = field['RAM_pointer']
        expected = bytes.fromhex(field['new_hex']) + b'\0'
        assert bytes(cpu.mem_read(addr, len(expected))) == expected
        values.append(dict(actor=n, city=city, complete_joined_name=joined, short_name=name, address=addr))
    base.save(DEPLOYED, dict(candidate_sha256=staged['candidate_sha256'], full_name_runtime_values=values,
        actual_postboot_snapshot=True, ordinary_name_panel_gameplay=False,
        evidence={str(p): base.digest(p) for p in (boot_path, snapshot, STORED, Path(__file__))}))


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('stage', 'startup'))
    (stage if parser.parse_args().action == 'stage' else replay_startup)()
