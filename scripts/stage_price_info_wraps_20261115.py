"""Revisit all nine Price Info descriptions that span two pages."""

from dataclasses import replace
from hashlib import sha256
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import register_refit_help_wraps_20261115 as parent
from scripts import stage_trade_good_descriptions_v4 as version_four
from scripts.preflight_shared_crew_notices_v1 import with_components
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.review_sound_bgm_titles_v1 import reference
from scripts.stage_mutiny_review_v1 import portrait_sheets
from scripts.verify_release_baseline import files


base = parent.base
ARM, COMMON, CLEAN, GATES = parent.stage.ARM, parent.stage.COMMON, parent.stage.CLEAN, parent.stage.GATES
ROOT = Path('work/price_info_wraps_20261115_v2')
ROM = ROOT / 'Price_Info_Wraps_RESEARCH_ONLY.nds'
STORED = ROOT / 'staged.json'
MANUSCRIPT = Path('translations/editorial_checkpoints/SharedText_20261110_v1/price_info_wraps_context_20261115_v2.json')

# Keep these ordinary prose paragraphs separate from the compiler's word boundaries.
REVIEWS = {
    139: ('Corn', None, ('major grains', 'New World', 'Common Era'),
          'One of the world’s three major grains with wheat and rice, cultivated in the New World before the Common Era and also used for bourbon.',
          'Retain the three complete sentences. Keep the geography and period phrases intact and end page one after the cultivation history.'),
    145: ('Cheese',
          "Lactic acid bacteria ferment milk, such as cow's or goat's, into cheese. Milk type, bacteria, and aging time affect the flavor.",
          ('Lactic acid bacteria', "cow's or goat's", 'aging time'),
          'Milk such as cows’ or goats’ milk is fermented with lactic acid bacteria. The milk, bacteria, and duration of aging affect flavor.',
          'Put the process in active voice and retain both examples, the culture and the three factors that affect taste.'),
    147: ('Bananas',
          'A large Asian perennial in the banana family. Its fruit is a tropical staple. Bananas eaten raw are sweeter than cooking varieties.',
          ('banana family', 'tropical staple', 'cooking varieties'),
          'The edible fruit of a large perennial in the banana family, native to Asia and a staple in the tropics. Raw varieties contain more sugar than cooking varieties.',
          'Restore the plant family and distinguish the sweet raw fruit from cooking varieties.'),
    157: ('Shark Fin',
          'Dried fins from large sharks. Tail fins are prized over dorsal and pectoral fins. Soak until soft, then simmer or add to soup.',
          ('Tail fins', 'pectoral fins', 'until soft'),
          'Fins from large sharks are dried. Tail fins are preferred to dorsal and pectoral fins. The fins are soaked until soft and simmered or used in soup.',
          'State the comparison plainly, then give the preparation as one instruction.'),
    159: ('Cloves',
          'Dried clove buds from the myrtle family. A fragrant spice for meat, ranked in the top three with pepper and cinnamon.',
          ('myrtle family', 'top three', 'pepper and cinnamon'),
          'The dried buds of the myrtle-family clove tree, counted among the three major spices with pepper and cinnamon. Fragrant and used in meat dishes.',
          'Retain the plant part and family, aroma, culinary use and all three spices. The heading already says Cloves.'),
    182: ('Wool',
          'Yarn and wool cloth come from sheep or goat fleece. Wool is warm, absorbent, and springy. Europeans have long worn it in winter.',
          ('wool cloth', 'goat fleece', 'in winter'),
          'Sheep and goat fleece provide yarn and woven wool. It retains heat and absorbs moisture and is elastic. It has long been used for warm clothing in Europe.',
          'Keep the two fibers, both textile uses, three properties and the historical use as clothing.'),
    190: ('Carpets',
          'Wool rugs warm and decorate rooms and keep out damp. Persian carpets are the finest handwoven rugs, prized for their art and craft.',
          ('Persian carpets', 'handwoven rugs'),
          'Wool carpets are valued for warmth, protection against damp and decoration. Persian carpets are considered the finest handwoven carpets for their art and technique.',
          'Use direct catalog prose for the three uses, then keep craftsmanship and artistic merit in the Persian comparison.'),
    199: ('Jade', None, (),
          'Jadeite can be opaque or translucent. Dark green, translucent pieces are most valuable. In China, jade ornaments also serve to ward off evil.',
          'Keep the color and translucence criteria together on page one. The intact second sentence about China belongs on the continuation page.'),
    213: ('Ginseng',
          'Dried Korean ginseng root from East Asia. It contains steroids and B vitamins. Used to nourish and strengthen the body and heart.',
          ('Korean ginseng root', 'East Asia', 'B vitamins'),
          'Dried East Asian Korean ginseng root contains steroids and B vitamins. It has been used to nourish and fortify the body and strengthen the heart.',
          'Preserve the three functions and present them as historical use. Retain the named compounds and origin.'),
}


def compile_body(previous, draft, phrases, plan):
    if not phrases and draft is None:
        return previous
    english = draft or ' '.join(previous.decode('ascii').split())
    assert english.isascii() and '%' not in english and '_' not in english
    marked = english
    for phrase in phrases:
        assert marked.count(phrase) == 1
        marked = marked.replace(phrase, phrase.replace(' ', '_'))
    lines = [line.replace('_', ' ') for line in plan(marked)]
    assert ' '.join(lines) == english and all(any(phrase in line for line in lines) for phrase in phrases)
    assert 1 <= len(lines) <= 8 and all(1 <= len(line) <= 36 for line in lines)
    body = '\n'.join([*(line.ljust(len(line) + len(line) % 2) for line in lines[:-1]), lines[-1]]).encode('ascii')
    assert all(len(row) % 2 == 0 for row in body.split(b'\n')[:-1])
    return body


def native_proof(runtime, deployed, rows, env):
    staged = with_components(runtime, runtime.arm, deployed)
    raster, _, _ = env['font_tools'](runtime.image)
    kanji = runtime.image.read_file('/GRP/KANJI.FNT')
    figures = []
    for row in rows:
        n, text = row['message_id'], bytes.fromhex(row['staged_hex'])
        row['native_owner'] = env['stored_case'](staged, n, text)
        rendered = env['native_pages'](raster, runtime.arm, kanji, text)
        assert 1 <= len(rendered) <= 2
        pages = []
        for i, page in enumerate(rendered, 1):
            pixels, glyphs = page.pop('pixels'), page.pop('glyphs')
            visible = [line.rstrip() for line in page['visible_text']]
            assert ''.join(chr(g['code']) for g in glyphs) == ''.join(visible).replace(' ', '')
            assert all(g['x'] + 6 <= 216 and g['y'] + 12 <= 64 for g in glyphs)
            assert 1 <= len(visible) <= 4 and (i == len(rendered) or len(visible) == 4)
            pages.append(page | dict(visible_text=visible, pixel_sha256=sha256(pixels).hexdigest(), glyphs=len(glyphs)))
            if row['decision'] != 'retention':
                figures.append((f"{n} {row['commodity']} {i}/{len(rendered)}", pixels))
        assert ' '.join(line for page in pages for line in page['visible_text']) == row['english']
        row['pages'] = pages
    return portrait_sheets(ROOT, figures)


def main():
    assert not ROOT.exists() and not MANUSCRIPT.exists()
    release = base.load(parent.RELEASE)
    runtime = RegisteredRuntime(parent.RELEASE, release['own_registered_startup'], captain=3)
    assert base.digest(CLEAN) == release['clean_input_sha256']
    clean = base.NdsImage.open(CLEAN)
    clean_rows = common_message_entries(clean.read_file(COMMON), clean.read_file(ARM))
    before = files(runtime.image)
    arm, common = before[ARM], before[COMMON]
    assert sha256(arm).hexdigest() == release['target_ARM9_sha256'] and sha256(common).hexdigest() == release['target_COMMON_sha256']
    directory = sha256(arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    old = owned_entries(common, arm, directory)
    credited = {row['id'] for row in base.load(base.LEDGER)[base.CONTEXT]['integrated_record_keys'] if row['file_path'] == COMMON}
    assert set(REVIEWS) == {i for i in range(137, 261) if old[i].text.count(b'\n') >= 4}
    original_blocks = IlnkContainer.parse(common).blocks
    blocks, rows, slots = list(original_blocks), [], {}
    env = version_four.stage_environment()
    for n, (name, draft, phrases, meaning, reason) in REVIEWS.items():
        prior, source = old[n], clean_rows[n]
        key = f'COMMON_MESSAGE_{n}'
        assert key in credited and b'%' not in prior.text + source.text
        body = compile_body(prior.text, draft, phrases, env['plan'])
        decision = 'retention' if body == prior.text else 'wrap revision' if draft is None else 'revision'
        if body != prior.text:
            block, lo, hi = prior.block, prior.block_offset, prior.copy_end
            raw = blocks[block][lo:hi]
            assert raw.rstrip(b'\0') == prior.text and raw.endswith(b'\0')
            assert len(body) < len(raw), (n, len(body), len(raw))
            replacement = (body + b'\0').ljust(len(raw), b'\0')
            blocks[block] = blocks[block][:lo] + replacement + blocks[block][hi:]
            slots[n] = dict(block=block, start=lo, end=hi, before=raw.hex(), after=replacement.hex(),
                            deployed=body.hex(), new_null_fields=len(prior.text) - len(body))
        rows.append(dict(id=key, message_id=n, file_path=COMMON, commodity=name, speaker='Price Info',
            context='The player opens the selected commodity’s description in Market Price Info.',
            english=' '.join(body.decode('ascii').split()), previous_English=prior.text.decode('ascii'),
            Japanese=source.text.decode('cp932'), source_meaning=meaning, localization_note=reason,
            source_reference=reference(source), current_reference=reference(prior), exact_clean_hex=source.text.hex(),
            exact_current_hex=prior.text.hex(), staged_hex=body.hex(), decision=decision,
            review=dict.fromkeys(GATES, True) | {'formatting': False}, existing_credit=True))
    deployed = IlnkContainer(blocks).to_bytes()
    rebound = owned_entries(deployed, arm, directory)
    for a, b in zip(old, rebound, strict=True):
        shifts = sum(slot['new_null_fields'] for slot in slots.values()
                     if slot['block'] == a.block and slot['end'] <= a.block_offset)
        text = bytes.fromhex(slots[a.message_id]['deployed']) if a.message_id in slots else a.text
        assert replace(a, record_index=a.record_index + shifts, text=text, end=a.start + len(text)) == b
    for row in rows:
        row['staged_reference'] = reference(rebound[row['message_id']])
    inverse = list(blocks)
    for slot in slots.values():
        i, lo, hi = slot['block'], slot['start'], slot['end']
        inverse[i] = inverse[i][:lo] + bytes.fromhex(slot['before']) + inverse[i][hi:]
    assert IlnkContainer(inverse).to_bytes() == common

    ROOT.mkdir()
    sheets = native_proof(runtime, deployed, rows, env)
    image = base.NdsImage.open(parent.ROM)
    image.replace_file(COMMON, deployed)
    changed = files(image)
    assert before.keys() == changed.keys() and {p for p in before if before[p] != changed[p]} == {COMMON}
    image.save(ROM)
    image.replace_file(COMMON, common)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    base.save(MANUSCRIPT, dict(translation_policy='natural-dialogue-v2', encoder='dialogue-relocatable-v1',
        target_locale='en-US', review_gates=list(GATES), previous_sha256=release['candidate_sha256'],
        clean_sha256=release['clean_input_sha256'], records=rows))
    base.save(STORED, dict(candidate_sha256=base.digest(ROM), previous_sha256=release['candidate_sha256'],
        target_COMMON_sha256=sha256(deployed).hexdigest(), target_ARM9_sha256=sha256(arm).hexdigest(),
        whole_parent_inverse=True, allocations=slots, preserved_entries=len(rebound) - len(slots),
        manuscript_sha256=base.digest(MANUSCRIPT), sheets=sheets))
    print([(row['message_id'], row['decision'], len(row['pages'])) for row in rows])


if __name__ == '__main__':
    main()
