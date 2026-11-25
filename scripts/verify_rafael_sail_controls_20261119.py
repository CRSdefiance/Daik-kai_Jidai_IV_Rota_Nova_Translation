"""Verify stored commands and native dialogue display for Rafael's sailing lesson."""

from types import FunctionType

from scripts import review_rafael_sail_controls_20261119 as stage
from scripts import verify_rafael_first_voyage_debrief_20261119 as precedent

base, native = stage.base, stage.native
display, names = precedent.display, precedent.names
ROOT = stage.STAGED / 'native_display'
PROOF = ROOT / 'native_display.json'
SC0 = '/data/SC0.DK4'


def main():
    assert not ROOT.exists()
    stored, manuscript, release = map(base.load, (stage.PROOF, stage.OUTPUT, stage.parent.RELEASE))
    assert stored['candidate_sha256'] == base.digest(stage.ROM)
    assert stored['manuscript_sha256'] == base.digest(stage.OUTPUT)
    assert stored['predecessor_sha256'] == release['candidate_sha256'] == base.digest(stage.parent.ROM)
    assert stored['whole_parent_inverse'] and stored['changed_blocks'] == {SC0: [128]}
    assert base.digest(base.REGISTRY) == release['registry_sha256']
    ctx = native.RegisteredRuntime(stage.parent.RELEASE, release['own_registered_startup'], captain=3)
    image = base.NdsImage.open(stage.ROM)
    common, font = '/COMMON/MESFILE.DK4', '/GRP/KANJI.FNT'
    for asset in (native.ARM, common, font, '/data/EV0.DK4'):
        assert image.read_file(asset) == ctx.image.read_file(asset)
    font_data = image.read_file(font)
    _, paint = display.early.prior.precedent.planners(ctx.arm)
    fe_paint = display.stage.system.native_painter(ctx)
    expand = names.expander()
    installed = names.current_names(ctx)
    group, = stored['groups']
    bank = native.IlnkContainer.parse(image.read_file(SC0)).blocks
    block = bank[128]
    assert group['block'] == 128 and group['file_path'] == SC0 and native.digest(block) == group['after']
    rows = {r['id']: r for r in manuscript['records']}
    revisions, retentions, previews, dynamic = [], [], [], []
    for command in group['commands']:
        at = command['stored_offset']
        raw = bytes.fromhex(command['stored'])
        assert raw == block[at:at + len(raw)]
        if not command['record_ids']:
            continue
        ident, = command['record_ids']
        row = rows[ident]
        if row['decision'] == 'retention':
            assert command['stored'] == command['current']
            retentions.append(ident)
            continue
        assert command['word'] == 0x4000 and raw[5] == row['source_selector']
        value = raw[5:raw.index(0, 6)]
        plan = group['plans'][ident]
        result = names.paragraph(ctx, font_data, paint, expand, fe_paint, installed, row, value, plan)
        tokens = stage.TOKEN.findall(row['english'])
        assert tokens == stage.TOKEN.findall(bytes.fromhex(row['source_hex'])[1:].decode('cp932'))
        if tokens:
            assert tokens == ['FI']
            dynamic.append(ident)
            name = precedent.STOCK['FI']
            text = value[1:].replace(b'FI', name.encode('ascii'))
            lines = [names.expected(line, {'FI': name}) for line in plan['lines']]
            pages = names.raster(ctx, font_data, paint, text, lines, 1)
            result['layouts'].append(dict(scope='Rafael default', names={'FI': name}, pages=pages))
        for layout in result['layouts']:
            page, = layout['pages']
            plane = bytes.fromhex(page['native_plane_hex'])
            if row['source_selector'] == 254:
                plane = bytes(15 if pixel else 0 for pixel in plane)
            title = f'{ident} / {layout["scope"]}' if tokens else ident
            previews.append((title, plane))
        revisions.append(result | dict(id=ident, source_selector=row['source_selector'], target_hex=value.hex(),
            stored_offset=at, planned_lines=plan['lines']))
    assert set(retentions).isdisjoint(r['id'] for r in revisions)
    assert {r['id'] for r in revisions} | set(retentions) == rows.keys()
    assert len(revisions) == 25 and len(retentions) == 20 and len(dynamic) == 4
    ROOT.mkdir()
    contact = display.early.contact_sheets
    sheets = FunctionType(contact.__code__, contact.__globals__ | {'ROOT': ROOT})(previews)
    base.save(PROOF, dict(candidate_sha256=stored['candidate_sha256'], stage_proof_sha256=base.digest(stage.PROOF),
        revisions=revisions, retentions=retentions, runtime_first_name_records=dynamic, previews=len(previews),
        sheets=sheets, actual_gameplay=False))
    print(f'Verified 25 revised pages and 20 exact retentions. Generated {len(previews)} previews.')


if __name__ == '__main__':
    main()
