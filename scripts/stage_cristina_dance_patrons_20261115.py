"""Review the shared tavern scene and stage its embedded patron labels."""

from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.raphael_system_panel_release import encode_panel
from scripts import register_square_trend_dialogue_20261115 as parent
from scripts.checkpoint_story_glyph_consistency_20261115 import catalogue
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools
from scripts.scan_completed_contraction_wraps_v7831 import raw_speeches
from scripts.stage_market_conversation_20261115 import ARM, CLEAN, GATES, digest, files
from scripts.stage_mutiny_review_v1 import portrait_sheets, render_portrait


base = parent.base
ROOT = Path('work/cristina_dance_patrons_20261115_v1')
ROM, STORED = ROOT / 'Cristina_Dance_Patrons_RESEARCH_ONLY.nds', ROOT / 'staged.json'
MANUSCRIPT = Path('translations/editorial_checkpoints/SharedText_20261110_v1/cristina_dance_patrons_20261115_v1.json')
BLOCKS = (171, 161, 158, 131)
PATRONS = ((44, 47, 61), (26, 29, 38), (84, 87, 111), (24, 27, 36))
LABELS = ('Patron 1', 'Patron 2', 'Patrons')
GLOSS = ('The first patron exclaims at how impressive the dancer is.',
         'The second patron agrees and admires both her beauty and her dancing.',
         'Both patrons call out three Bravos, drawing out the last one.')
CHEER = 'Patrons: Bravo! Bravo! Braaavo!'
EDITS = (
    ('Patron 1: Look at her go!', "Patron 2: Yeah! She's gorgeous. What a dancer!", CHEER),
    ("Patron 1: That woman's amazing!", "Patron 2: Yeah! She's gorgeous, and she can really dance!", None),
    (None, None, CHEER),
    ('Patron 1: Wow, look at her!', "Patron 2: Yeah! She's beautiful, and she can dance!", CHEER),
)
CONTEXT = (
    'After drinking, Rafael and Claudio hear the tune. Cristina dances, the patrons cheer, and Claudio’s awkward reaction ends in an apology and acceptance of her as a crewmate.',
    'Hodram and Cristina notice the music. Her dancing surprises him, and he ends by saying he can see why Mivor is taken with her.',
    'Lil and Camille tease each other and Emilio over drinks and food. Cristina dances when the tune changes. They praise her completely on her own terms.',
    'Maria notices music unfamiliar from home. Cristina dances, then tells Maria the name of the dance. Maria asks to see it again.',
)
REASONS = (
    ('Rafael’s sigh and admission begin the scene after the drinking.', 'Claudio’s boast and example set up Rafael’s correction.',
     'Rafael points out the contradiction and tells Claudio he has had too much.',
     'Cristina agrees about the drinks and trails off as she notices the music.', 'Rafael notices the energy of the tune.',
     'Claudio hears why someone might want to dance.', 'Cristina recognizes the tune and excuses herself.',
     'Rafael calls after her without guessing what she is doing.', 'The privy joke preserves Claudio’s drunken guess.',
     '', '', 'Rafael’s plainspoken praise answers the crowd’s excitement.', 'Claudio sounds at a loss after his earlier joke.',
     '', 'The repeated claps preserve the sound after the cheer.', 'Cristina says she danced on impulse because she loves the song.',
     'Rafael repeats his praise directly to Cristina.', 'Cristina is flattered and embarrassed.',
     'Claudio’s formal-sounding tease sets up the objection to his tone.', 'The pause lets Cristina take in the comment.',
     'Rafael objects to Claudio’s tone.', 'Claudio admits he judged her narrowly.',
     'Cristina’s brief surprise leaves room for the apology.', 'Keep Claudio’s plain apology.',
     'Claudio acknowledges how he used to see her and recognizes her as a crewmate.'),
    ('Hodram reflects on how much he drank.', 'Cristina agrees and notices the change.',
     'Hodram’s brief approval fits his reserved voice.', 'Cristina excuses herself as the tune begins.',
     'Hodram’s brief reaction leaves her purpose unclear.', '', '',
     'Keep his wordless reaction to the dancing.', '', 'Separate the applause from the patrons’ speech.',
     'Cristina’s short explanation keeps the spontaneous dance and her liking for the song.',
     'Hodram reconsiders the impression that she only cared about her sword.',
     'Cristina asks if he is surprised.', 'Hodram praises the dancing and connects it to Mivor’s established feelings.'),
    ('Lil’s emphatic admission fits her reaction to the drinks.', 'Camille addresses Lil through the original name substitution.',
     'Emilio’s interjection switches from drinking to eating.', 'Camille answers Emilio directly.',
     'Cristina admits how much she drank and suddenly notices something.', 'Lil likes the spirited music.',
     'Camille’s brief agreement leaves the beat to Cristina.', 'Cristina recognizes the song and excuses herself.',
     'Lil asks what Cristina is doing.', '', '', 'Lil’s direct admiration suits her voice.',
     'Camille agrees and adds his own observation.', '', 'Keep the applause on its own beat.',
     'Cristina says she couldn’t help dancing because she loves this tune.', 'Lil repeats her admiration.',
     'Camille’s comparison praises both the swordplay and the dancing.', 'Cristina’s laugh and thanks end the exchange lightly.'),
    ('Maria’s tentative reaction fits her comment on the drinks.', 'Cristina agrees and reacts to the musical change.',
     'Maria describes the unfamiliar music in terms of home.', 'Cristina recognizes the tune and excuses herself.',
     'Maria notices her leaving and asks what is wrong.', '', '', 'Maria’s short praise lands between the cheers.',
     '', 'The bracketed sound cue reads as applause from the room.',
     'Cristina explains why she felt compelled to dance.', 'Maria admires the performance and comments on its style.',
     'Cristina identifies the dance as flamenco.', 'Maria’s wish to see it again closes the exchange warmly.'),
)


def transform(image, records):
    selected = [row for row in records if row['decision'] == 'revision']
    for route, block in enumerate(BLOCKS):
        file = f'/data/SC{route}.DK4'
        bank = IlnkContainer.parse(image.read_file(file))
        original = bank.blocks[block]
        revised = bytearray(original)
        for row in selected:
            if row['file_path'] != file:
                continue
            start = row['current_reference']['offset']
            old, new = map(bytes.fromhex, (row['current_reference']['raw_hex'], row['target_hex']))
            assert len(old) == len(new) and old[:1] == new[:1] == b'\xfe'
            stop = start + len(old)
            assert revised[start:stop + 1] == old + b'\0'
            revised[start:stop] = new
        bank.blocks[block] = bytes(revised)
        yield file, bank.to_bytes()


def main():
    assert not any(p.exists() for p in (MANUSCRIPT, STORED, ROM))
    release = base.load(parent.RELEASE)
    assert base.digest(parent.ROM) == release['candidate_sha256'] and base.digest(base.REGISTRY) == release['registry_sha256']
    assert base.digest(CLEAN) == release['clean_input_sha256']
    clean, image = map(base.NdsImage.open, (CLEAN, parent.ROM))
    before = files(image)
    arm, source_arm = image.read_file(ARM), clean.read_file(ARM)
    raster, _, _ = font_tools(image)
    kanji = image.read_file('/GRP/KANJI.FNT')
    inventory, _, _ = scoped_inventory()
    rules = base.load(parent.MANIFEST)['relocations'][ARM]['reviewed_name_integration']['catalog']
    original_banks = [IlnkContainer.parse(before[f'/data/SC{route}.DK4']).blocks for route in range(4)]
    original_catalogue = catalogue(arm, rules, original_banks)
    credits = {(r['file_path'], r['id']) for r in base.load(base.LEDGER)[base.CONTEXT]['integrated_record_keys']}
    rows, previews = [], []
    for route, block in enumerate(BLOCKS):
        file = f'/data/SC{route}.DK4'
        old_block = original_banks[route][block]
        source_block = IlnkContainer.parse(clean.read_file(file)).blocks[block]
        sc, source = raw_speeches(source_arm, source_block, inventory)
        ec, current = raw_speeches(arm, old_block, inventory)
        assert [r['word'] for r in sc] == [r['word'] for r in ec]
        for ordinal, (ja, en, reason) in enumerate(zip(source, current, REASONS[route], strict=True)):
            n = ja['record_index']
            stable = f'DK4_MES_B{block}_R{n:04}'
            assert (file, stable) in credits and ja['complete_preamble_hex'] == en['complete_preamble_hex']
            a, b = map(bytes.fromhex, (ja['raw_hex'], en['raw_hex']))
            japanese, current_text = [raw[1:].decode('cp932') for raw in (a, b)]
            previous = ' '.join(current_text.split())
            logical, decision = previous, 'retention'
            selected = n in PATRONS[route]
            gloss = reason
            label = {0: 'Rafael', 1: 'Hodram', 2: 'Lil', 3: 'Maria', 5: 'Claudio', 7: 'Cristina',
                     9: 'Camille', 14: 'Emilio', 254: 'Applause'}[ja['selector']]
            if selected:
                index = PATRONS[route].index(n)
                label, gloss = LABELS[index], GLOSS[index]
                assert a[0] == b[0] == 0xFE and japanese.startswith(('＜客１＞', '＜客２＞')[index == 1])
                target = EDITS[route][index]
                if target is None:
                    assert previous.startswith(label + ':')
                    reason = 'Keep the already natural cheer and the label that identifies the patron without supplying a personal name.'
                else:
                    logical, decision = target, 'revision'
                    reason = 'Match the established Patron label and keep the crowd’s excited response distinct from the captain’s reaction.'
                    if index == 2:
                        reason = 'The shared plural label identifies both patrons. Keep the three cheers and the drawn-out last one.'
            assert reason
            row = dict(id=stable, file_path=file, block=block, route=route, ordinal=ordinal, speaker=label,
                       context=CONTEXT[route], source_meaning=gloss, Japanese=japanese, english=logical,
                       source_reference=ja | {'block_sha256': digest(source_block)},
                       current_reference=en | {'block_sha256': digest(old_block)}, previous_English=previous,
                       decision=decision, localization_note=reason, review=dict.fromkeys(GATES, True))
            if selected:
                if decision == 'revision':
                    compiled = encode_panel(logical, len(b) - 1)
                    target = b'\xfe ' + compiled[1:]
                    assert len(target) == len(b) and b'%' not in target and b'\0' not in target
                    assert not any(code in target for code in (b'FI', b'FA', b'FO', b'FU', b'IC'))
                    assert ' '.join(target[1:].decode('ascii').split()) == logical
                    row['target_hex'] = target.hex()
                else:
                    target = b
                pixels, events = render_portrait(raster, arm, kanji, target[1:])
                origins = {y: min(e['x'] for e in events if e['y'] == y) for y in {e['y'] for e in events}}
                assert len(origins) <= 2 and sorted(origins) == list(range(0, 16 * len(origins), 16))
                if decision == 'revision':
                    assert set(origins.values()) == {6}
                row.update(page_sha256=digest(pixels), ink_rows=origins, ink_pixels=pixels.count(1), one_native_panel=True)
                previews.append((f'SC{route} R{n:04} {decision}', pixels))
            rows.append(row)
    assert len(rows) == 72 and len(previews) == 12 and sum(r['decision'] == 'revision' for r in rows) == 9
    hashes, new_banks = {}, []
    for file, archive in transform(image, rows):
        blocks = IlnkContainer.parse(archive).blocks
        route = int(file[-5])
        block = BLOCKS[route]
        assert [i for i, pair in enumerate(zip(blocks, original_banks[route], strict=True)) if pair[0] != pair[1]] == [block]
        old_cmd, _ = raw_speeches(arm, original_banks[route][block], inventory)
        new_cmd, installed = raw_speeches(arm, blocks[block], inventory)
        assert [(c['offset'], c['word'], c['native_extent']) for c in old_cmd] == [
            (c['offset'], c['word'], c['native_extent']) for c in new_cmd]
        assert all(a['whole_command_hex'] == b['whole_command_hex']
                   for a, b in zip(old_cmd, new_cmd, strict=True) if a['word'] != 0x4000)
        for row, bound in zip((r for r in rows if r['file_path'] == file), installed, strict=True):
            old = row['current_reference']
            assert old['complete_preamble_hex'] == bound['complete_preamble_hex']
            assert row.get('target_hex', old['raw_hex']) == bound['raw_hex']
            row['staged_reference'] = bound
        image.replace_file(file, archive)
        hashes[file] = digest(archive)
        new_banks.append(blocks)
    assert catalogue(arm, rules, new_banks) == original_catalogue
    after = files(image)
    assert {key for key in before if before[key] != after[key]} == hashes.keys()
    ROOT.mkdir(parents=True, exist_ok=True)
    image.save(ROM)
    for file in hashes:
        image.replace_file(file, before[file])
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    candidate = base.digest(ROM)
    base.save(MANUSCRIPT, dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=list(GATES), candidate_sha256=candidate,
        previous_sha256=release['candidate_sha256'], records=rows))
    base.save(STORED, dict(candidate_sha256=candidate, previous_sha256=release['candidate_sha256'],
        target_ARM9_sha256=digest(arm), target_story_archive_sha256=hashes, whole_parent_inverse=True,
        sheets=portrait_sheets(ROOT, previews), manuscript_sha256=base.digest(MANUSCRIPT)))
    print('Reviewed 72 lines and rendered all 12 patron panels. Nine revisions staged.')


if __name__ == '__main__':
    main()
