"""Check the nine revised Rafael pages and exact retained commands."""

from types import FunctionType

from scripts import review_rafael_trade_and_arms_20261119 as stage
from scripts import verify_rafael_first_voyage_debrief_20261119 as precedent

base, native = stage.base, stage.native
display, names = precedent.display, precedent.names
ROOT = stage.STAGED / 'native_display'
PROOF = ROOT / 'native_display.json'
SC0, FONT = '/data/SC0.DK4', '/GRP/KANJI.FNT'


def main():
    assert not ROOT.exists()
    stored, manuscript, release = map(base.load, (stage.PROOF, stage.OUTPUT, stage.parent.RELEASE))
    assert base.digest(stage.ROM) == stored['candidate_sha256'] and base.digest(stage.OUTPUT) == stored['manuscript_sha256']
    assert stored['predecessor_sha256'] == release['candidate_sha256'] == base.digest(stage.parent.ROM)
    assert stored['whole_parent_inverse'] and stored['changed_blocks'] == {SC0: [129, 140]}
    ctx = native.RegisteredRuntime(stage.parent.RELEASE, release['own_registered_startup'], captain=3)
    image = base.NdsImage.open(stage.ROM)
    assert all(image.read_file(p) == ctx.image.read_file(p) for p in (native.ARM, FONT, '/COMMON/MESFILE.DK4', '/data/EV0.DK4'))
    font = image.read_file(FONT)
    _, paint = display.early.prior.precedent.planners(ctx.arm)
    expand = names.expander()
    installed = names.current_names(ctx) | {'FO': 'Li Clan'}
    rows = {r['id']: r for r in manuscript['records']}
    bank = native.IlnkContainer.parse(image.read_file(SC0)).blocks
    revisions, retentions, previews, dynamic = [], [], [], []
    for group in stored['groups']:
        block = bank[group['block']]
        assert native.digest(block) == group['after']
        for command in group['commands']:
            if not command['record_ids']:
                continue
            at = command['stored_offset']
            raw = bytes.fromhex(command['stored'])
            assert raw == block[at:at + len(raw)]
            owners = [rows[i] for i in command['record_ids']]
            if all(row['decision'] == 'retention' for row in owners):
                assert command['stored'] == command['current']
                retentions.extend(row['id'] for row in owners)
                continue
            row, = owners
            ident = row['id']
            assert command['word'] == 0x4000 and raw[5] == row['source_selector']
            value = raw[5:raw.index(0, 6)]
            plan = group['plans'][ident]
            result = names.paragraph(ctx, font, paint, expand, None, installed, row, value, plan)
            macro = stage.precedent.TOKEN.findall(row['english'])
            if macro:
                token, = macro
                assert macro == stage.precedent.TOKEN.findall(bytes.fromhex(row['source_hex'])[1:].decode('cp932'))
                dynamic.append(ident)
                for label, sample in (('Rafael default', precedent.STOCK[token]), ('maximum width', precedent.MAXIMUM[token])):
                    body = value[1:].replace(token.encode(), sample.encode())
                    lines = [names.expected(s, {token: sample}) for s in plan['lines']]
                    pages = names.raster(ctx, font, paint, body, lines, 1)
                    result['layouts'].append(dict(scope=label, names={token: sample}, pages=pages))
            for layout in result['layouts']:
                page, = layout['pages']
                title = f'{ident} / {layout["scope"]}' if macro else ident
                previews.append((title, bytes.fromhex(page['native_plane_hex'])))
            revisions.append(result | dict(stored_offset=at, target_hex=value.hex(), planned_lines=plan['lines']))
    assert {r['id'] for r in revisions} | set(retentions) == rows.keys()
    assert len(revisions) == 9 and len(retentions) == 11 and len(dynamic) == 2
    ROOT.mkdir()
    contact = display.early.contact_sheets
    sheets = FunctionType(contact.__code__, contact.__globals__ | {'ROOT': ROOT})(previews)
    base.save(PROOF, dict(candidate_sha256=stored['candidate_sha256'], stage_proof_sha256=base.digest(stage.PROOF),
        revisions=revisions, retentions=retentions, dynamic_records=dynamic, previews=len(previews), sheets=sheets,
        actual_gameplay=False))
    print(f'Nine revised pages and 11 exact retentions verified. {len(previews)} previews generated.')


if __name__ == '__main__':
    main()
