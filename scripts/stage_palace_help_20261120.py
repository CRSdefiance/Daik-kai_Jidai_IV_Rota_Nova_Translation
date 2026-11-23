"""Review the connected Palace Help articles and their existing continuation pages."""

from pathlib import Path
from struct import unpack_from
from types import FunctionType

from PIL import Image, ImageDraw, ImageFont

from dk4tool.dialogue import reviewed_help_pages_v16 as compiler
from dk4tool.dialogue.help_source_links import readable_source, source_links
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from scripts import check_early_HELP23_native_pages as renderer
from scripts import register_load_confirmation_20261120 as parent
from scripts.seal_shared_text_source_v1 import ARM, CLEAN
from scripts.source_locked_derivation_v5118 import checked_text


base = parent.base
HELP = '/COMMON/HELP.DK4'
CANONICAL = Path('out/raphael_natural_v2_accepted_base.nds')
ROOT = Path('work/palace_help_20261120_v2')
ROM, PROOF, PLAN = ROOT / 'Palace_Help_RESEARCH_ONLY.nds', ROOT / 'native_help_pages.json', ROOT / 'plan.json'
GATES = ('source', 'context', 'localization', 'naturalness', 'formatting')
CHILDREN = {37: 204, 38: 214, 39: 215}
CONTRACT_LIMITS = ('You can sign even if other factions hold a combined 100 percent share. In that case, you take '
                   '1 percentage point from those factions. You cannot use the letter if the town already has contracts '
                   'with three factions or your faction holds a 100 percent share.')
ARTICLES = {
    35: ("Palace / Governor's Office", (
        "Sign a contract with the town or invest in its defenses. See [[36|Contract,]] [[37|Military Investment,]] "
        "[[38|Introduction,]] [[39|Recommendation,]] [[40|Lend Item,]] and [[41|Reclaim.]]",),
        "The index uses the six original action names as displayed by the Palace menu and preserves their order."),
    37: ('Military Investment', (
        "Invest in the town's defenses in groups of 1 to 20 units. Each unit costs gold equal to 50 percent of the "
        "town's Arms rating, or 40 percent for Rafael.",
        "Investment raises the town's Arms rating. Your [[150|market share]] also rises if the total is below 100 percent "
        "or a faction you are [[187|at war]] with holds a share. A higher Arms rating makes a town less likely to surrender "
        "when attacked and lets you buy better ships and cannons."),
        "The parent page establishes the Palace and Governor's Office context. Keep the cost, share conditions and effects, "
        "and start the continuation with what the investment does."),
    38: ('Introduction (Palace)', (
        "Give the ruler or governor a [[25|Letter of Introduction]] from the Market. You can use it only in Ports. If you "
        "already have a [[36|contract,]] your [[150|market share]] rises by 5 percentage points. Otherwise, the letter "
        "lets you sign a contract.", CONTRACT_LIMITS),
        "Match the Introduction action and the Market name. Keep the Port restriction and give the exact increase in points."),
    39: ('Recommendation (Palace)', (
        "Give the ruler or governor a [[25|Letter of Recommendation]] from the Market. You can use it in a town of any "
        "size. If you already have a [[36|contract,]] your [[150|market share]] rises by 10 percentage points. Otherwise, "
        "the letter lets you sign a contract.", CONTRACT_LIMITS),
        "Match the Recommendation action and the Market name. Keep the any-size rule and the distinct increase of 10 points."),
    40: ('Lend Item (Palace)', (
        "Lend an item to the ruler or governor at your home port. You'll collect rent each month based on the item's "
        "value. You cannot lend [[4|Proofs of Conquest,]] Proof Maps, or [[142|Ancient Maps.]]",),
        "Restore both officials and keep the home-port restriction, monthly payment and three excluded item types."),
    41: ('Reclaim (Palace)', (
        "Get back an item you've lent out. You can do this only at your home port's palace or governor's office.",),
        "Match Reclaim in the paired menu and retain the home-port restriction."),
}
RETAIN = {
    36: 'The article uses the command name and clearly gives the purchase range, trade access and two restrictions.',
    25: 'The article explains who can start a trend and when a sale may earn a letter. Keep the active link back to the Palace uses.',
    149: 'Arms matches the rating named in the investment article. The original link and the two effects stay accurate.',
}


def reference(archive, block, index):
    pos = int.from_bytes(archive[8 + index * 4:12 + index * 4], 'little')
    assert archive[pos:pos + len(block)] == block
    return dict(file_path=HELP, block=index, archive_offset=pos, bytes=len(block), block_sha256=sha(block),
                archive_sha256=sha(archive))


def plan_pages(manuscript, raw):
    sections = ('{133:16,139:2,150:2,151:2,168:2}', '{133:16,139:2,150:2,151:2,168:2,37:2,38:2,39:2}')
    # Keep each original article's active continuation, including the backlinks.
    # The second military block has no live forward link and is preserved unchanged.
    source = checked_text(compiler.SOURCE, {
        'topics!=(set(range(133,202))-{181,184})': f'topics!={set(ARTICLES)!r}',
        'Exact remaining67 Help articles': 'Exact Palace Help articles',
        f'topic not in {sections[0]} or len(sections)!={sections[0]}[topic]':
            f'topic not in {sections[1]} or len(sections)!={sections[1]}[topic]',
        "168:['ＨＰ','生命力','徐々に回復']}":
            "168:['ＨＰ','生命力','徐々に回復'],37:['ラファエル','武装度'],"
            "38:['紹介状','街の規模'],39:['推薦状','街の規模']}",
        'existing={133:209,139:210,150:206,151:207,168:208}': f'existing={CHILDREN!r}',
    })
    scope = compiler.plan_articles.__globals__.copy()
    wrap = scope['wrap']
    phrases = [['5', 'percentage', 'points'], ['10', 'percentage', 'points'], ['Arms', 'rating'], ['Proof', 'Maps']]
    scope['wrap'] = FunctionType(wrap.__code__, wrap.__globals__ | {'PHRASES': [*wrap.__globals__['PHRASES'], *phrases]})
    exec(compile(source, __file__ + '::original-palace-help-compiler', 'exec'), scope)
    return scope['plan_articles'](manuscript, *raw.values(), require_formatting=False)


def main():
    assert not ROOT.exists()
    release = base.load(parent.RELEASE)
    assert base.digest(parent.ROM) == release['candidate_sha256']
    assert base.digest(CLEAN) == release['clean_input_sha256'] and base.digest(base.REGISTRY) == release['registry_sha256']
    original, accepted, image = map(base.NdsImage.open, (CLEAN, CANONICAL, parent.ROM))
    raw = {k: rom.read_file(HELP) for k, rom in (('clean', original), ('canonical', accepted), ('current', image))}
    blocks = {k: IlnkContainer.parse(d).blocks for k, d in raw.items()}
    assert sha(raw['current']) == release['target_HELP_sha256']
    clean, current = blocks['clean'], blocks['current']
    assert len(clean) == 202 and len(current) == 217
    assert [i for i, b in enumerate(current) if any(l['topic_id'] == 205 for l in source_links(b))] == []
    stock_arm, arm = (rom.read_file(ARM) for rom in (original, image))
    assert sha(arm) == release['target_ARM9_sha256']
    menu_path = Path('translations/palace_menu_labels_manuscript_v1.json')
    menu_labels = []
    for r in base.load(menu_path)['records']:
        field = r['menu_record'] - 0x02000000
        sp, cp = (unpack_from('<I', binary, field)[0] for binary in (stock_arm, arm))
        japanese, english = (binary[p - 0x02000000:p - 0x02000000 + 80].split(b'\0', 1)[0]
                             for binary, p in ((stock_arm, sp), (arm, cp)))
        assert japanese.hex() == r['source_hex'] and english.decode('ascii') == r['english']
        assert r['english'] in ARTICLES[35][1][0]
        menu_labels.append(dict(id=r['id'], pointer_field=r['menu_record'], source_pointer=sp, current_pointer=cp,
                                source_hex=japanese.hex(), current_hex=english.hex(), english=r['english']))
    assert len(menu_labels) == 6
    records = []
    for topic in sorted(ARTICLES.keys() | RETAIN.keys()):
        children = [CHILDREN[topic]] if topic in CHILDREN else ([213] if topic == 25 else [])
        links = [l['topic_id'] for l in source_links(clean[topic])]
        current_links = [l['topic_id'] for n in (topic, *children) for l in source_links(current[n])
                         if l['topic_id'] not in children and l['topic_id'] != topic]
        assert links == current_links
        row = dict(id=f'HELP_TOPIC_{topic}', topic_id=topic, file_path=HELP, speaker='Help system',
            context='Palace commands and the original linked Help articles on contracts, letters and Arms.',
            source_reference=reference(raw['clean'], clean[topic], topic),
            current_reference=reference(raw['current'], current[topic], topic),
            source_Japanese=readable_source(clean[topic]), previous_English=readable_source(current[topic]),
            original_link_IDs=links, review=dict.fromkeys(GATES, True) | {'formatting': False},
            current_continuations=[dict(topic_id=n, current_hex=current[n].hex(),
                reference=reference(raw['current'], current[n], n), previous_English=readable_source(current[n])) for n in children],
            **{f'{k}_source_hex': data[topic].hex() for k, data in blocks.items()})
        if topic in ARTICLES:
            title, parts, reason = ARTICLES[topic]
            row.update(heading=title, english=' '.join(parts), localization_note=reason, decision='revision',
                       semantic_sections=list(parts), semantic_section_reason='Keep the original rule group and its follow-up intact.')
        else:
            row.update(english=' '.join(' '.join(readable_source(current[n]).split()) for n in (topic, *children)),
                       localization_note=RETAIN[topic], decision='retention', review=dict.fromkeys(GATES, True))
        records.append(row)
    manuscript = dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        file_path=HELP, records=[r for r in records if r['decision'] == 'revision'],
        **{f'source_{k}_HELP_sha256': sha(raw_data) for k, raw_data in raw.items()})
    target, plan = plan_pages(manuscript, raw)
    final = IlnkContainer.parse(target).blocks
    expected = ARTICLES.keys() | CHILDREN.values()
    assert len(final) == 217 and set(plan['owned_topic_ids']) == expected
    assert {n for n, (old, new) in enumerate(zip(current, final, strict=True)) if old != new} == expected
    image.replace_file(HELP, target)
    candidate = bytes(image.rom.save())
    image.replace_file(HELP, raw['current'])
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(candidate)
    patch, rebuilt = ROOT / 'translation.xdelta', ROOT / 'clean_rebuilt.nds'
    make_xdelta(CLEAN, ROM, patch)
    apply_xdelta(CLEAN, patch, rebuilt)
    assert rebuilt.read_bytes() == candidate
    base.save(PLAN, plan)

    helpers = renderer.original.verify.__globals__.copy()
    exec(compile(renderer.ADAPTER, __file__ + '::registered-help-parser', 'exec'), helpers)
    pages = []
    for page in plan['pages']:
        receipt, picture = helpers['verify'](arm, page)
        n = page['topic_id']
        path = ROOT / f'topic_{n}.png'
        picture.save(path)
        pages.append((n, picture))
        record = next(r for r in records if r['topic_id'] == page['source_article_id'])
        record.setdefault('native_pages', []).append(page | dict(native_display=receipt,
            registered_reference=reference(target, final[n], n), preview=str(path), preview_sha256=base.digest(path)))
    sheets = []
    font = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 18)
    for start in range(0, len(pages), 4):
        group = pages[start:start + 4]
        sheet = Image.new('RGB', (1512, 400 * ((len(group) + 1) // 2)), '#263238')
        draw = ImageDraw.Draw(sheet)
        for i, (n, pic) in enumerate(group):
            x, y = (i % 2) * 756, (i // 2) * 400
            draw.text((x + 6, y + 5), f'Help {n}', font=font, fill='white')
            sheet.paste(pic.resize((756, 360), Image.Resampling.NEAREST), (x, y + 30))
        path = ROOT / f'sheet_{len(sheets) + 1}.png'
        sheet.save(path)
        sheets.append(dict(path=str(path), sha256=base.digest(path)))

    base.save(PROOF, dict(translation_policy='natural-dialogue-v2', target_locale='en-US', review_gates=GATES,
        candidate_sha256=sha(candidate), parent_sha256=release['candidate_sha256'], target_HELP_sha256=sha(target),
        clean_input_sha256=release['clean_input_sha256'], target_ARM9_sha256=release['target_ARM9_sha256'],
        complete_parent_inverse=True, clean_input_patch_byte_exact=True, clean_input_patch_sha256=base.digest(patch),
        records=records, sheets=sheets, exact_menu_terms=menu_labels, unresolved_legacy_205_preserved=True, counted_new_records=0,
        evidence={str(p): base.digest(p) for p in (PLAN, parent.RELEASE, menu_path, Path(__file__))}))
    print(f'{len(records)} Palace Help decisions, {len(pages)} completely rendered native pages.')


if __name__ == '__main__':
    main()
