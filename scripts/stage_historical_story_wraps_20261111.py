"""Review the historical wrap queue and replace only its bound story bodies."""

from collections import defaultdict
from inspect import getsource
from pathlib import Path

from PIL import Image, ImageDraw

from scripts import plan_lil_B218_layout_v6881c as layout
from scripts import register_lil_ceramics_wrap_20261111 as parent
from scripts import stage_lil_ceramics_wrap_20261111 as precedent
from scripts import verify_lil_B174_fonts_v4470 as expansion
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.scan_completed_contraction_wraps_v7831 import raw_speeches
from scripts.source_locked_derivation_v5118 import checked_text


base, sha, IlnkContainer = parent.base, precedent.sha, precedent.IlnkContainer
CLEAN, ARM = parent.parent.CLEAN, precedent.ARM
ROOT = Path('work/historical_story_wraps_20261111_v3')
QUEUE = Path('translations/editorial_checkpoints/SharedText_20261110_v1/historical_wrap_leads_current_v1.json')
REVIEW = QUEUE.with_name('historical_story_wraps_context_v3.json')
PREVIOUS = QUEUE.with_name('historical_story_wraps_context_v2.json')
PROOF = ROOT / 'stored_and_native.json'

# Each preference is an intact phrase for the automatic planner. It never supplies row positions.
DECISIONS = {
    (2,22,48): ('Lil', 'Lil takes command after Camille hesitates and orders everyone to their stations. They are leaving immediately.',
        'Retain the crisp nautical command and decisive second sentence. Lil has just asserted her role and follows it immediately with sail and anchor orders.',
        None, ("We're setting sail!",)),
    (2,22,116): ('Lil', 'Camille finally gives the orders on the Arnhem. Lil praises him and says she is counting on him.',
        'Keep the teasing praise and warm assurance together as two sentences, just before Camille worries about the voyage.',
        None, ("I'm counting on you!",)),
    (2,22,148): ('Fernando', 'Fernando explains that the permit’s tax benefit is part of the government’s effort to encourage trade.',
        'Retain the established tax-exemption term and clarify that Fernando is explaining the very permit Camille just asked about.',
        "That's the trade policy at work. It's a tax-exemption permit, too.", ("It's a tax-exemption permit, too.",)),
    (2,214,51): ('Janus', 'Janus writes that the sword attributed to Judas is reportedly a fine, sharp weapon. The sword is blameless and worth looking for.',
        'The existing letter has the right balance of hearsay and practical judgment. Preserve his understated defense before he acknowledges Manuel’s likely objection.',
        None, ("it's worth looking for", 'The blade itself', 'a keen edge')),
    (2,227,18): ('Yifa', 'During training, Yifa mentions a rumor of a cloth martial arts uniform tough enough to chip a blade that strikes it, and asks whether Lil knows it.',
        'The rumor stays speculative, and “chips sword blades” makes clear what takes the damage. The question leads directly to Lil’s disbelief that cloth could act like armor.',
        'By the way, I heard about a martial arts uniform so tough it chips sword blades. Know anything about it?',
        ('a martial arts uniform', 'so tough', 'chips sword blades', 'Know anything about it?')),
    (3,108,92): ('Sailor', 'Kuhn’s injured former employee thanks Maria for promising safety. He has no one else to turn to and brings up the Argot Company.',
        'Keep the sailor’s gratitude, dependence on Maria, and hesitant shift to the name that prompts her companion’s answer.',
        "Thanks... After what's happened, you're the only one I can turn to. So... know the Argot Company?",
        ("After what's happened", "you're the only one I can turn to", 'the Argot Company', 'know the Argot Company')),
    (3,35,25): ('Maria', 'Maria tells Hodram that whether she is his enemy depends entirely on him.',
        'Preserve her controlled pause after “enemy” and the responsibility she puts on him. Her next line turns the interrogation around.',
        None, ("That's entirely up to you.",)),
    (3,36,41): ('Lil', 'Lil says she is only helping Kuhn and accuses Maria of running China’s underworld as a pirate.',
        'Keep the defensive first sentence and the insult. Lil is repeating what she believes about Maria, and Maria answers by warning what Kuhn plans to do to her.',
        None, ("You're the one running", "China's underworld", 'you pirate!')),
}
for key in ((0,246,23),(1,237,23),(2,234,23),(3,207,22)):
    DECISIONS[key] = ('Carlo', 'Carlo tells Filipo he has finally returned to active life and is now sailing aboard these people’s ship.',
        'Retain Carlo’s matter-of-fact reply to his old acquaintance. The second sentence introduces the crew indirectly and makes Filipo notice the customers.',
        None, ("I'm aboard their ship now.",))


def bind_planner():
    source = checked_text(getsource(layout.plan), {
        'row[\'source_selector\'] in [2,21]': "0 <= row['source_selector'] < 207",
        'frozenset([2,21])': "frozenset([row['source_selector']])",
        'def solve(start,line):': 'def solve(start,line,budget):',
        'tail=solve(stop,line+1)': 'extra=0 if final else 1+reserve\n            if extra>budget:continue\n            tail=solve(stop,line+1,budget-extra)',
        'result=solve(0,0)': "result=solve(0,0,len(bytes.fromhex(row['current_hex']))-1-len(body))",
        "if row['id']=='DK4_MES_B218_R0023' and pair==('it','whatever'):weak=0":
            "if pair in row['protected_pairs']:weak+=2",
    })
    env = vars(layout) | {'PAIRS': set()}
    exec(compile(source, __file__ + '::scoped-phrases-and-existing-phase-rules', 'exec'), env)
    return env['plan']


def block_rows(clean, current, ctx, pending):
    inventory, _, _ = scoped_inventory()
    source_arm = clean.read_file(ARM)
    groups = defaultdict(list)
    for row in pending:
        groups[row['file_path'], row['block']].append(row)
    for (path, block), rows in groups.items():
        source = IlnkContainer.parse(clean.read_file(path)).blocks[block]
        stored = IlnkContainer.parse(current.read_file(path)).blocks[block]
        assert {r['source_block_sha256'] for r in rows} == {sha(source)}
        assert {r['current_block_sha256'] for r in rows} == {sha(stored)}
        clean_commands, clean_speeches = raw_speeches(source_arm, source, inventory)
        commands, speeches = raw_speeches(ctx.arm, stored, inventory)
        assert [x['word'] for x in clean_commands] == [x['word'] for x in commands]
        assert len(speeches) == len(clean_speeches)
        assert all(a['complete_preamble_hex'] == b['complete_preamble_hex'] for a,b in zip(clean_speeches,speeches,strict=True))
        yield (path, block), (source, stored, commands, clean_speeches, speeches, rows)


def compile_records(groups, plan):
    contexts, records = [], []
    for (path, block), (source, stored, commands, clean_speeches, speeches, leads) in groups.items():
        contexts.append(dict(file_path=path, block=block, source_block_sha256=sha(source), current_block_sha256=sha(stored),
            source_progressive_exchange=clean_speeches, current_progressive_exchange=speeches))
        for lead in leads:
            ja, at = lead['source_reference'], lead['current_reference']
            i = next(i for i, row in enumerate(clean_speeches) if row['offset'] == ja['offset'])
            assert clean_speeches[i] == ja and speeches[i] == at
            actor, gloss, note, revised, phrases = DECISIONS[int(path.split('SC')[1][0]),block,ja['record_index']]
            old = bytes.fromhex(at['raw_hex'])
            src = bytes.fromhex(ja['raw_hex'])
            assert old[0] == src[0] == at['selector']
            current = ' '.join(old[1:].decode('ascii').split())
            english = revised or current
            assert all(word not in src[1:] and word not in old[1:] and word not in english.encode('ascii') for word in (b'FI',b'FA',b'FO',b'FU',b'%'))
            pairs = set()
            for phrase in phrases:
                assert phrase.casefold() in english.casefold(), (phrase,english)
                words = [layout.norm(w) for w in phrase.split()]
                pairs.update(zip(words,words[1:]))
            row = dict(id=lead['id'], file_path=path, block=block, source_selector=old[0], kind='progressive', speaker=actor,
                source_meaning=gloss, localization_note=note, context=f'Original exchange in {path}, block {block}.',
                source_reference=ja, current_reference=at, source_Japanese=src[1:].decode('cp932'),
                source_hex=src.hex(), current_hex=old.hex(), current_English=current, english=f'{{SPEAKER:{old[0]:02X}}}{english}',
                decision='revision' if revised else 'retention', protected_pairs=pairs,
                review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False))
            compiled = plan(row)
            del row['protected_pairs']
            encoded = bytes.fromhex(compiled['encoded_hex'])
            assert all(d['code']=='line-break-count' and d['severity']=='warning' for d in compiled['diagnostics']), compiled['diagnostics']
            assert ' '.join(compiled['lines']) == english
            # Leave every native offset and NUL untouched. The verified existing progressive renderer may consume trailing blank cells.
            pad = len(old)-len(encoded)
            assert 0 <= pad < 36, (row['id'], pad, compiled['lines'])
            target = encoded + b' '*pad
            assert target != old and len(target) == len(old) and target[0] == old[0] and b'\0' not in target, (row['id'], compiled['lines'])
            records.append(row | dict(automatic_layout=compiled, target_hex=target.hex(), trailing_blank_bytes=pad,
                line_count_reason='English phrase flow determines row count within the original viewport.' if compiled['diagnostics'] else None))
    return contexts, records


def native_validation(ctx, records):
    _, paint = precedent.planners(ctx.arm)
    font = ctx.image.read_file('/GRP/KANJI.FNT')
    source = checked_text(getsource(expansion.expand), {'assert identity==prefix and captain==2':'assert identity==prefix and captain==3'})
    env = vars(expansion).copy()
    exec(compile(source, __file__ + '::own-registered-processor-four-alignments', 'exec'), env)
    previous = base.load(PREVIOUS)
    assert previous['candidate_sha256'] == ctx.release['candidate_sha256']
    reused = {(row['file_path'],row['id']): row for row in previous['records']}
    pictures = []
    for row in records:
        prior = reused[row['file_path'],row['id']]
        assert prior['source_reference']==row['source_reference'] and prior['current_reference']==row['current_reference']
        for label, field in (('before','current_hex'),('after','target_hex')):
            body = bytes.fromhex(row[field])[1:]
            if prior[field] == row[field]:
                evidence = prior[label+'_native']
                bound, page = evidence['processor'], evidence['page']
                assert sha(bytes.fromhex(page['native_plane_hex']))==evidence['plane_sha256']
            else:
                bound = ctx.execute(env['expand'],body,row['source_selector'])
                display = paint(ctx.arm,font,body)
                assert display['complete_consumed_bytes']==len(body) and len(display['pages'])==1
                page, = display['pages']
            assert len(bound['cases'])==4 and all(case['output_hex']==body.hex() for case in bound['cases'])
            pixels = bytes.fromhex(page['native_plane_hex'])
            assert page['first_visible_origin']==[0,0]
            row[label+'_native'] = dict(processor=bound, page=page, plane_sha256=sha(pixels))
            pictures.append((row['file_path'].split('/')[-1][:3]+' '+row['id'].split('_B')[1]+' '+label, pixels))
    return pictures


def transform(image, records):
    by_file = defaultdict(lambda: defaultdict(list))
    for row in records:
        by_file[row['file_path']][row['block']].append(row)
    for path, groups in by_file.items():
        archive = IlnkContainer.parse(image.read_file(path))
        before = list(archive.blocks)
        for index, rows in groups.items():
            old, target = archive.blocks[index], bytearray(archive.blocks[index])
            for row in rows:
                at = row['current_reference']['offset']
                previous, body = map(bytes.fromhex, (row['current_hex'],row['target_hex']))
                assert old[at:at+len(previous)+1]==previous+b'\0' and target[at:at+len(previous)]==previous
                assert len(previous)==len(body) and previous[0]==body[0]
                target[at:at+len(body)] = body
            archive.blocks[index] = bytes(target)
        raw = archive.to_bytes()
        restored = IlnkContainer.parse(raw)
        assert [i for i,(a,b) in enumerate(zip(before,restored.blocks,strict=True)) if a!=b] == sorted(groups)
        for index, rows in groups.items():
            block = bytearray(restored.blocks[index])
            for row in rows:
                at = row['current_reference']['offset']
                previous, body = map(bytes.fromhex,(row['current_hex'],row['target_hex']))
                assert block[at:at+len(body)+1]==body+b'\0'
                block[at:at+len(body)] = previous
            restored.blocks[index] = bytes(block)
        assert restored.to_bytes()==image.read_file(path)
        yield path, raw


def main():
    assert not ROOT.exists() and not REVIEW.exists()
    release = base.load(parent.RELEASE)
    assert base.digest(CLEAN)==release['clean_input_sha256']
    ctx = RegisteredRuntime(parent.RELEASE,release['own_registered_startup'],captain=3)
    pending = [r for r in base.load(QUEUE)['records'] if r['further_contextual_and_consumer_review']]
    groups = dict(block_rows(base.NdsImage.open(CLEAN),ctx.image,ctx,pending))
    contexts, records = compile_records(groups,bind_planner())
    assert len(records)==12 and len(contexts)==10
    for row in records:
        print(row['file_path'],row['id'],row['automatic_layout']['lines'],row['trailing_blank_bytes'],flush=True)
    pictures = native_validation(ctx,records)
    ROOT.mkdir()
    paths = {}
    for name, raw in transform(ctx.image,records):
        path = ROOT / Path(name).name
        path.write_bytes(raw)
        paths[name] = dict(path=path.as_posix(),sha256=sha(raw),source_sha256=sha(ctx.image.read_file(name)))
    sheets = []
    colors = {0:(239,232,201),1:(0,8,0),15:(98,97,98)}
    for start in range(0,len(pictures),8):
        sheet = Image.new('RGB',(888,616),'#263238'); draw = ImageDraw.Draw(sheet)
        for i,(title,pixels) in enumerate(pictures[start:start+8]):
            x,y = i%2*444,i//2*154
            draw.text((x+4,y+2),title,fill='white')
            plane = Image.new('RGB',(216,64)); plane.putdata([colors[v] for v in pixels])
            sheet.paste(plane.resize((432,128),Image.Resampling.NEAREST),(x+4,y+21))
        path = ROOT / f'before_after_{len(sheets)+1}.png'; sheet.save(path)
        sheets.append(dict(path=path.as_posix(),sha256=base.digest(path)))
    base.save(REVIEW,dict(translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',
        review_gates=['source','context','localization','naturalness','formatting'],candidate_sha256=release['candidate_sha256'],
        records=records,complete_exchange_references=contexts,zero_new_credit=True,full_goal_complete=False))
    base.save(PROOF,dict(candidate_sha256=release['candidate_sha256'],review_sha256=base.digest(REVIEW),archives=paths,sheets=sheets,
        blocks=[list(key) for key in groups],unchanged_terminators_offsets_block_extents_and_unowned_bytes=True,
        archive_inverses_exact=True,checked_complete_native_pages=24,checked_original_processor_alignments=96,
        exact_prior_page_reuse_source=PREVIOUS.as_posix(),exact_prior_page_reuse_sha256=base.digest(PREVIOUS)))


if __name__=='__main__':
    main()
