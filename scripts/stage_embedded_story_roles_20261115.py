"""Review the Boy and Foreign Girl story panels and stage label-only revisions."""

from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC

from scripts import register_cristina_dance_patrons_20261115 as parent
from scripts.checkpoint_story_glyph_consistency_20261115 import catalogue
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.native_call_abi_v764 import STOP, call
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.scan_completed_contraction_wraps_v7831 import raw_speeches
from scripts.stage_market_conversation_20261115 import ARM, CLEAN, GATES, digest, files
from scripts.stage_mutiny_review_v1 import portrait_sheets, render_portrait
from dk4tool.formats.ilnk import IlnkContainer


base = parent.base
ROOT = Path('work/embedded_story_roles_20261115_v2')
ROM, STORED = ROOT / 'Embedded_Story_Roles_RESEARCH_ONLY.nds', ROOT / 'staged.json'
MANUSCRIPT = Path('translations/editorial_checkpoints/SharedText_20261110_v1/embedded_story_roles_20261115_v2.json')
FILE, BLOCKS = '/data/SC1.DK4', (86, 142)
BOY_CONTEXT = ('Cristina tries to reassure the boy. He clings to her neck, and she realizes that '
               'both of them could drown. The three cries alternate with her attempts to steady him.')
FOREIGN = {
    15: ('Hodram offers the girl a weapon. The others fear she may attack again, '
         'but she silently indicates that she does not want it.'),
    56: ('Hodram asks whether she will leave with the other captives. She stays silent. '
         'He recalls that she comes from a different ethnic group and suggests protection in town.'),
    142: ('Hodram tries to reassure her, and the crew weighs its next move against Espinosa. '
          'The girl follows Hodram. He offers to take her with them and uses gestures and his '
          'own name to ask hers. She first says Sera, then gives her full name under her own nameplate.'),
}
BOY_GLOSS = ("The boy cries out that he's scared, twice.",
             "He repeats that he's scared as he holds on.",
             'He cries out again, drawing out the sound of how scared he is.')
BOY_NOTES = {
    0: ('The repeated short cry sounds breathless after Cristina reassures him.',
        'The clipped echo keeps his attention on his fear while he clings to her.',
        '“Help!” carries the force of his wordless cry in the drowning scene.'),
    1: ('“I’m scared” twice keeps the frightened repetition immediately after Cristina’s reassurance.',
        'The repeated wording links the cry to his clinging to Cristina.',
        'The shouted opening restores the force of his last cry as Cristina starts to sink.'),
    2: ('The opening wail and two repetitions preserve the boy’s first burst of panic.',
        'The unadorned repetition works while Cristina struggles for air.',
        'The wail leads into one final admission of fear as both are in danger.'),
    3: ('His first wail and repeated fear answer Cristina’s attempt to calm him.',
        'The words repeat through Cristina’s request to let go.',
        'The held vowel conveys the longer sound of the final frightened cry.'),
}
GIRL_NOTES = {
    15: {168: ('She reacts with surprise at the offer.', 'Keep the wordless surprise before the warning.'),
         183: ('She is tense or startled while the men speak.', 'The pause and exclamation carry her reaction without supplying words.'),
         205: ('She pauses silently before the question.', 'The pause lets Hodram ask whether she wants the weapon.'),
         212: ('She nods in reply to “Don’t want it?”', 'The gesture answers the question while the girl stays silent.')},
    56: {10: ('She says nothing after Hodram asks if she will leave with the others.',
              'Keep the silent response and the label that marks her unfamiliar origin without specifying a nationality.')},
    142: {5: ('She hesitantly makes a sound.', '“Ah...” is tentative and gives Hodram a reason to ask what is wrong.'),
          11: ('She is silent after the reassurance.', 'The silence sets up Hodram’s realization that she cannot understand him.'),
          109: ('She is quietly present after the discussion of routes and preparations.',
                'The silent beat lets a crewmate notice she is still there.'),
          179: ('She waits in silence as Hodram wonders what to do.',
                'The pause gives room for his hesitant invitation.'),
          186: ('She responds with a small nod.', 'Keep the nod and the pause. Hodram attributes the understanding to his gestures.'),
          192: ('She stays silent when he asks whether she understood.',
                'The pause supports his inference about his gestures and expression.'),
          206: ('She looks puzzled at the question about her name.',
                'A question mark conveys confusion before Hodram switches to demonstrating his own name.'),
          217: ('She tries the captain’s name back as a question.',
                'Keep the opening hesitation, the name substitution, and the questioning lilt.'),
          223: ('She repeats the captain’s name, trailing off.',
                'Keep the native name token and the quieter repetition after Hodram’s encouragement.'),
          230: ('She repeats his name emphatically.', 'The exclamation marks the change from hesitation to recognition.'),
          237: ('She hesitates when he asks for her name again.', 'Give her the silent beat before Hodram clarifies his question.'),
          243: ('She hesitates before saying her given name, Sera.',
                'Her first spoken name stays in the body. The speaker label changes only once the exchange identifies her.')},
}


def references(commands, speeches):
    refs = {row['offset']: row for row in commands}
    return [{**row, 'command_offset': row['offset'] - 5,
             'complete_command_hex': refs[row['offset'] - 5]['whole_command_hex']}
            for row in speeches]


def transform(image, records):
    bank = IlnkContainer.parse(image.read_file(FILE))
    for block in BLOCKS:
        revised = bytearray(bank.blocks[block])
        for row in records:
            if row['decision'] != 'revision' or row['block'] != block:
                continue
            start = row['current_reference']['offset']
            old, new = map(bytes.fromhex, (row['current_reference']['raw_hex'], row['target_hex']))
            assert len(old) == len(new) and old[0] == new[0] == 0xFE
            end = start + len(old)
            assert revised[start:end + 1] == old + b'\0'
            revised[start:end] = new
        bank.blocks[block] = bytes(revised)
    yield FILE, bank.to_bytes()


def expansions(ctx, old, target):
    cpu, get, provider = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    field = get(0xCB184) + 0x19E4 + 0x20
    default = bytes(cpu.mem_read(field, 17)).split(b'\0', 1)[0]
    assert default == b'Maria'
    # Enter the parser at the established boundary for independent conversions.
    # The complete unmodified interpreter is exercised in the initialized replay.
    cpu.hook_add(UC_HOOK_CODE, lambda u, a, s, d: u.reg_write(UC_ARM_REG_PC, STOP),
                 begin=0x020242CC, end=0x020242CC)
    source, output = 0x02660000, 0x02662000
    guard = b'\xa5' * 16
    results = {}
    for name in (default, b'Hodram', b'Q', b'Abcdefghijklmnop'):
        cpu.mem_write(field, name.ljust(17, b'\0'))
        stored = bytes(cpu.mem_read(0x02000000, 0x400000))
        for alignment in range(4):
            for raw in (old, target):
                packet = guard + b'\xa5' * alignment + raw + b'\0' + guard
                cpu.mem_write(source - 16, packet)
                cpu.mem_write(output - 16, b'\xa5' * 288)
                call(cpu, 0x242C8, (output, source + alignment, 0), instruction_limit=300000)
                expected = raw.replace(b'FI', name)
                assert bytes(cpu.mem_read(output - 16, 288)) == (
                    guard + (expected + b'\0').ljust(272, b'\xa5'))
                assert bytes(cpu.mem_read(source - 16, len(packet))) == packet
                assert bytes(cpu.mem_read(0x02000000, 0x400000)) == stored
        results[name.decode('ascii')] = target.replace(b'FI', name)
    cpu.mem_write(field, default.ljust(17, b'\0'))
    assert bytes(cpu.mem_read(ctx.actor_root, 0x1A04)) == ctx.actor_bytes and not provider.reads
    ctx.calls.clear()
    return results


def main():
    assert not any(path.exists() for path in (STORED, ROM, MANUSCRIPT))
    prior = base.load(parent.RELEASE)
    assert base.digest(base.REGISTRY) == prior['registry_sha256']
    assert base.digest(CLEAN) == prior['clean_input_sha256']
    assert base.digest(parent.MANIFEST) == prior['manifest_sha256']
    ctx = RegisteredRuntime(parent.RELEASE, prior['own_registered_startup'], captain=3)
    clean, image = base.NdsImage.open(CLEAN), ctx.image
    arm, source_arm = ctx.arm, clean.read_file(ARM)
    before = files(image)
    raster, _, _ = font_tools(image)
    kanji = image.read_file('/GRP/KANJI.FNT')
    inventory, _, _ = scoped_inventory()
    original = [IlnkContainer.parse(before[f'/data/SC{i}.DK4']).blocks for i in range(4)]
    actors = base.load(parent.MANIFEST)['relocations'][ARM]['reviewed_name_integration']['catalog']
    baseline = catalogue(arm, actors, original)
    credits = {(r['file_path'], r['id']) for r in base.load(base.LEDGER)[base.CONTEXT]['integrated_record_keys']}
    rows, previews, contexts = [], [], []
    scopes = [(0, 83), (1, 86), (2, 73), (3, 58), (1, 15), (1, 56), (1, 142)]
    for route, block in scopes:
        path, old_block = f'/data/SC{route}.DK4', original[route][block]
        source_block = IlnkContainer.parse(clean.read_file(path)).blocks[block]
        sc, ja = raw_speeches(source_arm, source_block, inventory)
        ec, en = raw_speeches(arm, old_block, inventory)
        ja, en = references(sc, ja), references(ec, en)
        assert [c['word'] for c in sc] == [c['word'] for c in ec]
        boy = (route, block) in scopes[:4]
        label, source_label = ('Boy', '＜男の子＞') if boy else ('Foreign Girl', '＜異国の少女＞')
        indices = (26, 29, 31) if boy else tuple(i for i, r in enumerate(ja) if r['record_index'] in GIRL_NOTES[block])
        assert indices == tuple(i for i, r in enumerate(ja) if r['selector'] == 254 and
                                bytes.fromhex(r['raw_hex'])[1:].decode('cp932').startswith(source_label))
        context = BOY_CONTEXT if boy else FOREIGN[block]
        first, stop = (24, 34) if boy else (0, len(ja)) if block != 15 else (28, 42)
        contexts.append(dict(file_path=path, block=block, context=context, source_block_sha256=digest(source_block),
            current_block_sha256=digest(old_block), source_speech_refs=ja[first:stop], current_speech_refs=en[first:stop]))
        for index, ordinal in enumerate(indices):
            source, current = ja[ordinal], en[ordinal]
            number = source['record_index']
            stable = f'DK4_MES_B{block}_R{number:04}'
            assert (path, stable) in credits and source['complete_preamble_hex'] == current['complete_preamble_hex']
            assert source['selector'] == current['selector'] == 254
            old = bytes.fromhex(current['raw_hex'])
            name = label.encode()
            bracket = b'<' + name + b'>'
            assert old[0] == 254 and old[1:].startswith((bracket, name + b':'))
            revise = old[1:].startswith(bracket)
            target = old
            if revise:
                tail = old[len(bracket) + 1:]
                # Return the released ASCII cell to padding. Preserve the
                # newline and FI byte positions in the two-row heading.
                suffix = tail + b' ' if boy else b' ' + tail
                target = b'\xfe' + name + b':' + suffix
            assert len(target) == len(old) and target.count(b'\n') == old.count(b'\n')
            macro_offsets = [i for i in range(len(old)) if old[i:i + 2] == b'FI']
            assert macro_offsets == [i for i in range(len(target)) if target[i:i + 2] == b'FI']
            assert not any(token in target for token in (b'%', b'\0', b'FA', b'FO', b'FU', b'IC'))
            gloss, reason = (BOY_GLOSS[index], BOY_NOTES[route][index]) if boy else GIRL_NOTES[block][number]
            if revise:
                reason += ' Use the established colon label for this role.'
            decision = 'revision' if revise else 'retention'
            expanded = expansions(ctx, old[1:], target[1:]) if macro_offsets else {'stored': target[1:]}
            pages = []
            for example, body in expanded.items():
                pixels, events = render_portrait(raster, arm, kanji, body)
                levels = sorted({event['y'] for event in events})
                assert levels == list(range(0, 16 * len(body.split(b'\n')), 16))
                if revise:
                    assert all(min(event['x'] for event in events if event['y'] == y) == 0 for y in levels)
                case = dict(example=example, rendered_text=body.decode('cp932'), page_sha256=digest(pixels),
                            ink_pixels=pixels.count(1), rows=len(levels))
                pages.append(case)
                previews.append((f'SC{route} B{block} R{number:04} {example}', pixels))
            row = dict(id=stable, file_path=path, block=block, route=route, ordinal=ordinal, speaker=label,
                Japanese=bytes.fromhex(source['raw_hex'])[1:].decode('cp932'),
                previous_English=' '.join(old[1:].decode('ascii').split()),
                english=' '.join(target[1:].decode('ascii').split()), source_meaning=gloss, context=context,
                source_reference=source, current_reference=current, decision=decision, localization_note=reason,
                source_block_sha256=digest(source_block), current_block_sha256=digest(old_block),
                review=dict.fromkeys(GATES, True), FI_offsets=macro_offsets, native_pages=pages, one_native_panel=True)
            if target.count(b'\n'):
                row['layout_note'] = ('Keep the embedded speaker heading on its own row during the pauses, gestures '
                                      'and name exchange. The second row fits a full 16-byte player name.')
            if revise:
                row['target_hex'] = target.hex()
            rows.append(row)

    assert len(rows) == 29 and len(previews) == 38 and sum(r['decision'] == 'revision' for r in rows) == 15
    target_file, packed = next(transform(image, rows))
    revised_bank = IlnkContainer.parse(packed).blocks
    assert tuple(i for i, pair in enumerate(zip(revised_bank, original[1], strict=True)) if pair[0] != pair[1]) == BLOCKS
    for block in BLOCKS:
        old, new = original[1][block], revised_bank[block]
        before_commands, _ = raw_speeches(arm, old, inventory)
        commands, speech = raw_speeches(arm, new, inventory)
        owned = {row['current_reference']['command_offset'] for row in rows if row['decision'] == 'revision'
                 and row['file_path'] == FILE and row['block'] == block}
        for c, d in zip(before_commands, commands, strict=True):
            assert all(c[key] == d[key] for key in ('offset', 'word', 'native_extent'))
            assert (c['whole_command_hex'] != d['whole_command_hex']) == (c['offset'] in owned)
        installed = {r['record_index']: r for r in references(commands, speech)}
        for row in rows:
            if row['file_path'] != FILE or row['block'] != block:
                continue
            current = row['current_reference']
            updated = installed[current['record_index']]
            assert current['complete_preamble_hex'] == updated['complete_preamble_hex']
            assert row.get('target_hex', current['raw_hex']) == updated['raw_hex']
            row['staged_reference'] = updated | {'block_sha256': digest(new)}
    for row in rows:
        row.setdefault('staged_reference', row['current_reference'] | {'block_sha256': row['current_block_sha256']})
    assert catalogue(arm, actors, [original[0], revised_bank, *original[2:]]) == baseline
    image.replace_file(target_file, packed)
    after = files(image)
    assert before.keys() == after.keys() and {path for path in before if before[path] != after[path]} == {FILE}
    ROOT.mkdir(parents=True, exist_ok=True)
    image.save(ROM)
    image.replace_file(FILE, before[FILE])
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    candidate = base.digest(ROM)
    base.save(MANUSCRIPT, dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=list(GATES), candidate_sha256=candidate,
        previous_sha256=prior['candidate_sha256'], records=rows, surrounding_exchanges=contexts,
        substitutions=ctx.receipt() | {'macro_input_alignments': [0, 1, 2, 3], 'isolated_parser': '0x020242C8',
                      'modal_context_argument': 0, 'macro_records': 3, 'maximum_test_name_bytes': 16}))
    base.save(STORED, dict(candidate_sha256=candidate, previous_sha256=prior['candidate_sha256'],
        target_ARM9_sha256=digest(arm), target_story_archive_sha256={FILE: digest(packed)},
        whole_parent_inverse=True, sheets=portrait_sheets(ROOT, previews), manuscript_sha256=base.digest(MANUSCRIPT)))
    print('Staged 15 label edits, justified 14 retentions and rendered 38 native cases.')


if __name__ == '__main__':
    main()
