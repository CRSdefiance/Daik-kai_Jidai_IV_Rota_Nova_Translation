"""Review and stage the complete Hamburg ceramics exchange in Lil's route."""

from hashlib import sha256
from inspect import getsource
from io import BytesIO
from pathlib import Path
from struct import pack_into, unpack_from

from PIL import Image, ImageDraw

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.retrospective_SC2_reconstruction_v2 import reconstruct
from scripts import plan_lil_B218_layout_v6881c as planner
from scripts import register_visible_gallery_captions_v1 as parent
from scripts import research_lil_B209_native_pages_v6461 as renderer
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.square_shopkeeper_font_oracles_v7020 import _expected


base = parent.base
FILE, BLOCK = '/data/SC2.DK4', 189
ARM = parent.ARM
ROOT = Path('work/lil_ceramics_wrap_20261111_v2')
ARCHIVE, PROOF = ROOT / 'SC2.DK4', ROOT / 'stored_and_native.json'
REVIEW = Path('translations/editorial_checkpoints/SharedText_20261110_v1/lil_ceramics_exchange_context_v2.json')
HISTORICAL = next(Path('work/analysis/B189_retrospective_wrap_and_roles_v7025b').glob('whole_B189*.json'))

# Decisions follow the complete clean exchange. Only the five listed rows are recompiled.
DECISIONS = (
    ('A polite collector says he finally obtained the object the other day.', 'The existing phrasing keeps the shared reference to “it” and his understated satisfaction. Keep “got hold of it” together.', 'reflow', None),
    ('The shopkeeper recognizes the subject as ceramics and asks to confirm.', 'The short question sounds like immediate recognition and preserves the pause before the answer.', 'retain', None),
    ('He confirms the piece was as fine as he expected.', 'The emphatic first sentence and the existing break after “piece” fit his pride without implying that the object exceeded his expectations.', 'retain', None),
    ('The shopkeeper is impressed and politely asks to see it.', 'The slightly formal “Splendid” fits this pair. Give the first row room for “like” so the request reads more easily.', 'reflow', None),
    ('The collector warmly invites the shopkeeper to visit his home.', 'The friendly invitation keeps his hospitality and his home as the destination.', 'retain', None),
    ('The shopkeeper says the recent ceramics-collecting craze has made fine pieces hard to find.', 'The topic and consequence carry across three complete phrases. The sentence preserves the current collecting craze and its effect on availability.', 'retain', None),
    ('The collector has heard that people who cannot judge the pieces are buying them up because the hobby is fashionable.', '“Snapping them up” conveys the buying spree and sounds natural in an irritated aside. The claim remains hearsay and concerns people who do not know the pieces’ value.', 'revise', "I hear people who don't know what they're worth are snapping them up just because they're in fashion."),
    ('The shopkeeper complains that this is a nuisance.', 'The short complaint is restrained and fits his polite conversation.', 'retain', None),
    ('The collector wholeheartedly agrees.', 'The brisk agreement closes the first conversation without adding a new point.', 'retain', None),
    ('The trader calls the port worker’s attention to the men nearby.', 'The direct wording marks the shift to the second pair and keeps the reference to the men visible in the square.', 'retain', None),
    ('The port worker identifies the two and asks what the trader means.', 'The two short questions keep his casual, initially puzzled response.', 'retain', None),
    ('The trader boasts that they bought worthless ceramics from him at an unbelievable price the other day.', 'The existing boast carries both the poor quality and the price. Keep “worthless ceramics” and “You wouldn’t believe” together.', 'reflow', None),
    ('The port worker sees good customers and suggests approaching them because cash is short.', 'The joke in “good customers” follows the trader’s boast. Three short sentences keep the financial motive and joint suggestion without a dangling question fragment.', 'revise', "Now those are good customers! We're short on cash. Why don't we go talk to them?"),
    ('The trader approves the suggestion.', 'The quick agreement preserves the pace of the exchange.', 'retain', None),
    ('The port worker says it is settled and urges him to go.', 'The compact response keeps both the decision and the invitation to act.', 'retain', None),
    ('The trader calls out to a prospective customer in a familiar, ingratiating voice.', '“Excuse me, sir!” keeps the public address and attention-getting tone without adding a rank.', 'retain', None),
    ('The system forecasts that ceramics may become fashionable in Hamburg.', '“May catch on” preserves the forecast and uncertainty. The original speakerless FE panel and its one-row text stay byte-identical.', 'retain', None),
)


def sha(data):
    return sha256(data).hexdigest()


def write_or_match(path, data):
    if path.exists():
        assert path.read_bytes() == data
    else:
        path.write_bytes(data)


def planners(arm):
    layout = checked_text(getsource(planner.plan), {
        'in [2,21]': 'in [82,104,113,147]',
        'frozenset([2,21])': 'frozenset([82,104,113,147])',
        "if row['id']=='DK4_MES_B218_R0023' and pair==('it','whatever'):weak=0":
            "if row['id']=='DK4_MES_B189_R0006' and pair==('it','the'):weak=0",
    })
    pairs = {('hold', 'of'), ('of', 'it'), ('got', 'hold'), ('worthless', 'ceramics'),
             ('you', "wouldn't"), ("wouldn't", 'believe'), ("we're", 'short'), ('why', "don't"),
             ("don't", 'we'), ('we', 'go'), ('go', 'talk'), ('the', 'other'), ('other', 'day'), ('what', "they're")}
    env = vars(planner) | {'PAIRS': pairs}
    exec(compile(layout, __file__ + '::same-auto-pair-phase-planner', 'exec'), env)
    painter = checked_text(getsource(renderer.pages), {
        '4f4e41d26a0b24610a38a9da03dc549e4afec82121a1c72f35665104bb7ea351': sha(arm),
    })
    raster = vars(renderer) | {'expected_pixels': _expected}
    exec(compile(painter, __file__ + '::exact-current-progressive-renderer', 'exec'), raster)
    return env['plan'], raster['pages']


def stage():
    assert not PROOF.exists() and not REVIEW.exists()
    release = base.load(parent.RELEASE)
    assert base.digest(parent.ROM) == release['candidate_sha256']
    assert base.digest(parent.CLEAN) == release['clean_input_sha256']
    clean, image = map(base.NdsImage.open, (parent.CLEAN, parent.ROM))
    arm, clean_arm = image.read_file(ARM), clean.read_file(ARM)
    assert sha(arm) == release['target_ARM9_sha256']
    bank = IlnkContainer.parse(image.read_file(FILE))
    original, before = IlnkContainer.parse(clean.read_file(FILE)).blocks[BLOCK], bank.blocks[BLOCK]
    history = base.load(HISTORICAL)
    assert sha(original) == history['source_block_sha256'] and sha(before) == history['current_block_sha256']
    inventory, _, _ = scoped_inventory()
    clean_commands, clean_speeches = inventory(clean_arm, original)
    old_commands, old_speeches = inventory(arm, before)
    words = [0xA000] + [0x4000] * 17 + [0xC200, 0]
    assert [c['word'] for c in clean_commands] == [c['word'] for c in old_commands] == words
    plan, paint = planners(arm)
    font = image.read_file('/GRP/KANJI.FNT')
    names = {82: 'Shopkeeper', 104: 'Trader', 113: 'Port Worker', 147: 'Guildmaster', 254: 'Market forecast'}
    records, refs, panels, parts = [], [], [], []
    cursor = 0
    for src, old, historical, decision in zip(clean_speeches, old_speeches, history['records'], DECISIONS, strict=True):
        ja, at = src['offset'] + 5, old['offset'] + 5
        source = original[ja:original.index(0, ja+1)]
        previous = before[at:before.index(0, at+1)]
        preamble = original[ja-5:ja+1]
        assert preamble == before[at-5:at+1] and source[0] == previous[0]
        assert source.hex() == historical['source_hex'] and previous.hex() == historical['current_hex']
        speaker = source[0]
        kind = 'FE' if speaker == 254 else 'progressive'
        ident = f'DK4_MES_B{BLOCK}_R{original[:ja].count(bytes(1)):04d}'
        assert ident == historical['source_id']
        gloss, note, action, draft = decision
        logical = ' '.join(previous[1:].decode('ascii').split())
        text = draft or logical
        assert all(token not in source[1:] and token not in text.encode('ascii') for token in (b'FI', b'FA', b'FO', b'FU', b'%'))
        row = dict(id=ident, file_path=FILE, block=BLOCK, source_selector=speaker, kind=kind, speaker=names[speaker],
            source_Japanese=source[1:].decode('cp932'), source_meaning=gloss, localization_note=note,
            context='Hamburg ceramics collectors, followed by the nearby trader and port worker and the market forecast.',
            decision='revision' if draft else 'retention', layout_decision=action, current_English=logical,
            english=f'{{SPEAKER:{speaker:02X}}}{text}' if kind == 'progressive' else text,
            source_hex=source.hex(), current_hex=previous.hex(), source_complete_preamble_hex=preamble.hex(),
            source_reference=dict(file_path=FILE, block=BLOCK, offset=ja, bytes=len(source), record_index=original[:ja].count(bytes(1))),
            current_reference=dict(file_path=FILE, block=BLOCK, offset=at, bytes=len(previous), record_index=before[:at].count(bytes(1))),
            current_record_index=before[:at].count(bytes(1)),
            review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False))
        compiled = previous
        if action != 'retain':
            layout = plan(row)
            assert not any(issue['severity'] == 'error' for issue in layout['diagnostics'])
            assert all(issue['code'] == 'line-break-count' for issue in layout['diagnostics'])
            assert ' '.join(layout['lines']) == text and len(layout['lines']) <= 4
            compiled = bytes.fromhex(layout['encoded_hex'])
            row['automatic_layout'] = layout
            if layout['diagnostics']:
                row['source_break_count_review'] = 'The English boast uses its natural sentence pause and original viewport. Japanese source rows do not fix English row count.'
        pad = len(compiled) % 2 != len(previous) % 2
        value = compiled + b' ' * pad
        assert (value != previous) == (action != 'retain')
        parts.append(before[cursor:at]); new_at = sum(map(len, parts)); parts.append(value)
        cursor = at + len(previous)
        row.update(compiled_hex=compiled.hex(), target_hex=value.hex(), target_offset=new_at)
        if action != 'retain':
            for label, body in (('before', previous[1:]), ('after', value[1:])):
                display = paint(arm, font, body)
                assert display['complete_consumed_bytes'] == len(body) and len(display['pages']) == 1
                page, = display['pages']
                pixels = bytes.fromhex(page.pop('native_plane_hex'))
                panels.append((f'{ident.rsplit("_", 1)[-1]} {label}', pixels))
                row[label + '_native'] = page | {'plane_sha256': sha(pixels), 'plane_hex': pixels.hex()}
        records.append(row)
        refs.append(dict(id=ident, source_reference=row['source_reference'], current_reference=row['current_reference'],
            old_offset=at, old_length=len(previous), old_hex=previous.hex(), compiled_hex=compiled.hex(),
            target_hex=value.hex(), source_selector=speaker, source_complete_preamble_hex=preamble.hex(),
            new_offset=new_at, new_length=len(value), parity_space_added=pad))
    old_end = 8 + unpack_from('<H', before, 4)[0]
    target = bytearray(b''.join(parts) + before[cursor:old_end])
    end = len(target)
    pack_into('<H', target, 4, end-8)
    target = bytes(target) + bytes(-end % 4)
    for ref in refs:
        ref['new_record_index'] = target[:ref['new_offset']].count(bytes(1))
    new_commands, new_speeches = inventory(arm, target)
    assert len(new_speeches) == 17 and [c['word'] for c in new_commands] == words
    mapped = [dict(word=old['word'], old_offset=old['offset'], new_offset=new['offset'],
                   old_extent=old['native_extent'], new_extent=new['native_extent'],
                   source_0100_ancestors=old['ancestor_0100_offsets'], target_0100_ancestors=new['ancestor_0100_offsets'])
              for old, new in zip(old_commands, new_commands, strict=True)]
    group = dict(file_path=FILE, block=BLOCK, source_block_sha256=sha(before), clean_block_sha256=sha(original),
        source_bytes=len(before), source_logical_end=old_end, source_tail_bytes=len(before)-old_end,
        target_bytes=len(target), target_logical_end=end, target_tail_bytes=len(target)-end, target_block_sha256=sha(target),
        target_header_hex=target[:8].hex(), text_records=refs, relative_fixups=[], command_map=mapped, all_target_commands=new_commands)
    packet = dict(block=BLOCK, current_block_sha256=sha(before), clean_block_sha256=sha(original),
                  current_logical_end=old_end, all_current_commands=old_commands)
    assert reconstruct(before, original, group, packet, records, []) == target
    bank.blocks[BLOCK] = target
    target_archive = bank.to_bytes()
    bank.blocks[BLOCK] = before
    assert bank.to_bytes() == image.read_file(FILE)
    changed = [r['id'] for r in records if r['layout_decision'] != 'retain']
    assert len(changed) == 5 and len(panels) == 10
    ROOT.mkdir(exist_ok=True)
    write_or_match(ARCHIVE, target_archive)
    sheet = Image.new('RGB', (888, 5*154), '#263238')
    draw = ImageDraw.Draw(sheet)
    for index, (label, pixels) in enumerate(panels):
        x, y = (index % 2)*444, (index//2)*154
        picture = Image.new('RGB', (216, 64))
        colors = {0: (239,232,201), 1: (0,8,0), 15: (98,97,98)}
        picture.putdata([colors[v] for v in pixels])
        draw.text((x+4,y+2), label, fill='white')
        sheet.paste(picture.resize((432,128), Image.Resampling.NEAREST), (x+4,y+21))
    sheet_path = ROOT / 'before_and_after.png'
    rendered_sheet = BytesIO()
    sheet.save(rendered_sheet, format='PNG')
    write_or_match(sheet_path, rendered_sheet.getvalue())
    review = dict(translation_policy='natural-dialogue-v2', target_locale='en-US', encoder='dialogue-relocatable-v1',
        review_gates=['source', 'context', 'localization', 'naturalness', 'formatting'], records=records,
        candidate_sha256=release['candidate_sha256'], clean_ROM_sha256=release['clean_input_sha256'],
        wording_retentions=15, wording_revisions=2, stored_changes=changed, new_dialogue_credit=0, full_goal_complete=False)
    base.save(REVIEW, review)
    base.save(PROOF, dict(candidate_sha256=release['candidate_sha256'], ARM9_sha256=sha(arm),
        source_archive_sha256=sha(image.read_file(FILE)), target_archive_sha256=sha(target_archive),
        review_sha256=base.digest(REVIEW), sheet=sheet_path.as_posix(), sheet_sha256=base.digest(sheet_path),
        group=group, current_packet=packet, clean_and_current_block_inverses_exact=True,
        entire_parent_archive_inverse_exact=True, representative_gameplay_pending=True, new_dialogue_credit=0))
    print(f'17 complete decisions, five changed pages verified offline. Block {len(before)} to {len(target)} bytes.')


if __name__ == '__main__':
    stage()
