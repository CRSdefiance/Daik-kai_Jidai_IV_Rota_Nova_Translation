"""Review and verify five early Rafael dialogue lines with native name expansion."""

import argparse
import re
from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import generic_name_macro_owned_v5886b as macro
from scripts import register_rafael_charlotte_wraps_20261114 as parent
from scripts import stage_rafael_charlotte_wraps_20261114 as previous
from scripts import stage_rafael_early_wraps_20261111 as wraps
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.source_locked_derivation_v5118 import checked_text


base, prior, sha = previous.base, previous.prior, previous.sha
FILE, ARM, CLEAN, IlnkContainer = previous.FILE, previous.ARM, previous.CLEAN, previous.IlnkContainer
ROOT = Path('work/rafael_name_wraps_20261114_v1')
CAPTURE = ROOT / 'rafael_startup/capture_report.json'
RUNTIME = ROOT / 'rafael_native_context.json'
REVIEW = parent.TRIAGE.with_name('rafael_name_wraps_context_v1.json')
PROOF = ROOT / 'stored_and_native.json'
DEFAULTS = {'FI': 'Rafael', 'FA': 'Castor'}
TOKEN = re.compile(r'\{MACRO:(FI|FA)\}')
DECISIONS = {
    'DK4_MES_B63_R0113': ('Arcadius', "I'm sorry, {MACRO:FI}. Hiding that I'm a woman got you in trouble.",
        'Eirene apologizes for the trouble caused by concealing that she is a woman.',
        'The personal apology answers Rafael’s hurt rather than treating their argument as a dispute between her and Claudio. Rafael immediately says it was not her fault.',
        ("I'm sorry, {MACRO:FI}.", "Hiding that I'm a woman", 'got you in trouble.')),
    'DK4_MES_B64_R0134': ('Arcadius', "{MACRO:FI}, let's not dwell on what's already happened.",
        'Arcadius asks Rafael to stop worrying about what is already past.',
        'Keep the gentle, inclusive advice that leads into learning from the mistake. The brief direct address is part of the source.',
        ("let's not dwell", "what's already happened.")),
    'DK4_MES_B64_R0152': ('Claudio', "Wait! She insulted us without a word of thanks! {MACRO:FI} isn't the one to blame...",
        'Claudio protests that she insulted them without thanking them and begins to shift the blame away from Rafael.',
        'The angry interruption builds to the accusation he cuts off in his next turn. Keep the name and unfinished ending.',
        ('a word of thanks!', "{MACRO:FI} isn't the one to blame...")),
    'DK4_MES_B69_R0143': ('Charlotte', "...{MACRO:FI}, thank you so much. The villagers are smiling again, and it's all thanks to you.",
        'Charlotte thanks Rafael sincerely. She credits him for the villagers getting their smiles back.',
        'Keep the pause and open gratitude. Rafael immediately gives Charlotte credit for her hard work.',
        ('thank you so much.', 'The villagers are smiling again,', "it's all thanks to you.")),
    'DK4_MES_B70_R0050': ('Rafael', "Yes, that's right. I'm {MACRO:FI} {MACRO:FA}.",
        'Rafael politely confirms his identity with both names when Xien asks if he leads the company.',
        'Keep the direct confirmation. Xien already knows whom to ask about the Proof, and the two parts of Rafael’s name should stay together.',
        ("I'm {MACRO:FI} {MACRO:FA}.",)),
}


def expanded(text):
    return TOKEN.sub(lambda match: DEFAULTS[match[1]], text)


def bare_tokens(body):
    return re.findall(rb'FI|FA|FO|FU|%', body)


def planner():
    source = checked_text(getsource(prior.layout.plan), {
        "row['source_selector'] in [2,21]": "0 < row['source_selector'] < 207",
        'frozenset([2,21])': "frozenset([row['source_selector']])",
        "assert profile.macro_ascii_lengths['FA']==5 and profile.macro_widths['FA']==30":
            "profile=replace(profile, macro_ascii_lengths={'FI':6,'FA':6}, macro_widths={'FI':36,'FA':36})",
        'def solve(start,line):': 'def solve(start,line,budget):',
        'return (0,0,0,0),()': 'return (0,0,0,0,0),()',
        'tail=solve(stop,line+1)': 'extra=0 if final else 1+reserve\n'
            '            if extra>budget:continue\n'
            '            tail=solve(stop,line+1,budget-extra)',
        "if row['id']=='DK4_MES_B218_R0023' and pair==('it','whatever'):weak=0":
            "protected=int(pair in row['protected_pairs'])",
        '(cost[0]+tiny,cost[1]+1,cost[2]+weak,cost[3]+':
            '(cost[0]+tiny,cost[1]+protected,cost[2]+1,cost[3]+weak,cost[4]+',
        'result=solve(0,0)': "result=solve(0,0,len(bytes.fromhex(row['current_hex']))-1-len(TOKEN.sub(lambda m:m[1],body)))",
        'all_words_punctuation_and_zero_macros_unchanged=True': 'all_words_punctuation_and_macro_order_preserved=True',
    })
    env = vars(prior.layout) | dict(display=expanded, PAIRS=set(), TOKEN=TOKEN)
    exec(compile(source, __file__ + '::measured-Rafael-macro-phase-and-width', 'exec'), env)
    return FunctionType(wraps.plan_record.__code__, vars(wraps) | {'PLANNER': env['plan']})


def bind_runtime():
    release, report = base.load(parent.RELEASE), base.load(CAPTURE)
    assert report['ROM_sha256'] == release['candidate_sha256'] == base.digest(parent.ROM)
    assert report['frames'] == 4001 and report['cold_boot'] and not report['savestate_loaded']
    assert not report.get('battery_save_preloaded') and not report['callback_errors']
    assert not any(value for key, value in report.items() if key.startswith('synthetic_'))
    base.save(RUNTIME, dict(candidate_sha256=release['candidate_sha256'], cold_boot=True, savestate=False,
        actual_captain_getter=0, read_only_snapshot=report['read_only_RAM_snapshot'],
        capture_report=str(CAPTURE), capture_report_sha256=base.digest(CAPTURE)))
    runtime = RegisteredRuntime(parent.RELEASE, RUNTIME, captain=0)
    assert sha(runtime.arm) == release['target_ARM9_sha256']
    return runtime


def expand_source():
    source = checked_text(getsource(macro.expand), {'captain==2': 'captain==0'})
    env = vars(macro).copy()
    exec(compile(source, __file__ + '::original-Rafael-name-consumer', 'exec'), env)
    return env['expand']


def native(runtime, prefix, body, paint=None):
    expected = body.replace(b'FI', b'Rafael').replace(b'FA', b'Castor')
    result = runtime.execute(expand_source(), body, prefix)
    assert len(result['cases']) == 4
    assert all(row['output_hex'] == expected.hex() for row in result['cases'])
    if paint is None:
        return result
    display = paint(runtime.arm, runtime.image.read_file('/GRP/KANJI.FNT'), expected)
    assert display['complete_consumed_bytes'] == len(expected)
    for page in display['pages']:
        page['plane_sha256'] = sha(bytes.fromhex(page['native_plane_hex']))
    return dict(processor=result, expanded_hex=expected.hex(), pages=display['pages'])


def compile_rows(current, clean):
    checkpoint = base.load(parent.REVIEW)
    pending = base.load(parent.TRIAGE)
    assert pending['candidate_sha256'] == checkpoint['registered_candidate_sha256'] == base.digest(parent.ROM)
    bank, original = (IlnkContainer.parse(image.read_file(FILE)).blocks for image in (current, clean))
    inventory, _, _ = prior.scoped_inventory()
    source_arm, arm = clean.read_file(ARM), current.read_file(ARM)
    queue = {(x['block'], x['offset']): x for x in pending['records'] if x['file_path'] == FILE}
    plan = planner()
    contexts, records = {}, []
    for lead in checkpoint['deferred_macro_leads']:
        ident, block = lead['id'], lead['block']
        if block not in contexts:
            ja_cmd, ja_rows = prior.raw_speeches(source_arm, original[block], inventory)
            en_cmd, en_rows = prior.raw_speeches(arm, bank[block], inventory)
            assert [x['word'] for x in ja_cmd] == [x['word'] for x in en_cmd]
            assert all(a['complete_preamble_hex'] == b['complete_preamble_hex'] for a, b in zip(ja_rows, en_rows, strict=True))
            contexts[block] = dict(file_path=FILE, block=block, source_block_sha256=sha(original[block]),
                current_block_sha256=sha(bank[block]), source_progressive_exchange=ja_rows, current_progressive_exchange=en_rows)
        context = contexts[block]
        pairs = zip(context['source_progressive_exchange'], context['current_progressive_exchange'], strict=True)
        source, at = next((ja, en) for ja, en in pairs if ja['record_index'] == lead['source_reference']['record_index'])
        assert source == lead['source_reference'] and at == lead['current_reference']
        flag = queue[block, at['offset']]
        assert flag['block_sha256'] == context['current_block_sha256'] and flag['stored_body_hex'] == at['raw_hex'][2:]
        ja, old = bytes.fromhex(source['raw_hex']), bytes.fromhex(at['raw_hex'])
        assert ja[0] == old[0] == flag['source_selector']
        current_english = ' '.join(re.sub(r'FI|FA', lambda m: '{MACRO:' + m[0] + '}', old[1:].decode('ascii')).split())
        actor, english, meaning, note, phrases = DECISIONS[ident]
        token_order = [match.encode('ascii') for match in TOKEN.findall(english)]
        assert token_order == bare_tokens(ja[1:]) == bare_tokens(old[1:])
        assert all(phrase in english for phrase in phrases)
        protected = set()
        for phrase in phrases:
            words = [prior.layout.norm(word) for word in phrase.split()]
            protected.update(zip(words, words[1:]))
        row = dict(id=ident, file_path=FILE, block=block, source_selector=ja[0], kind='progressive',
            speaker=actor, source_meaning=meaning, localization_note=note, context=f'Original Rafael exchange in block {block}.',
            source_reference=source, current_reference=at, source_Japanese=ja[1:].decode('cp932'),
            source_hex=ja.hex(), current_hex=old.hex(), current_English=current_english,
            english=f'{{SPEAKER:{ja[0]:02X}}}{english}', decision='retention' if english == current_english else 'revision',
            protected_pairs=protected, review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False))
        layout = plan(row)
        assert all(d['code'] == 'line-break-count' and d['severity'] == 'warning' for d in layout['diagnostics'])
        assert ' '.join(layout['lines']) == english
        del row['protected_pairs']
        encoded = bytes.fromhex(layout['encoded_hex'])
        assert bare_tokens(encoded[1:]) == token_order and encoded[0] == ja[0] and b'\0' not in encoded[1:]
        pad = len(old) - len(encoded)
        assert 0 <= pad < 36
        row.update(automatic_layout=layout, target_hex=(encoded + b' ' * pad).hex(), trailing_blank_bytes=pad,
                   line_count_reason='Phrase flow sets line count within the original viewport.' if layout['diagnostics'] else None)
        records.append(row)
    assert {r['id'] for r in records} == DECISIONS.keys()
    return list(contexts.values()), records


def main(preview):
    assert not REVIEW.exists() and not PROOF.exists()
    release = base.load(parent.RELEASE)
    assert base.digest(parent.ROM) == release['candidate_sha256'] and base.digest(CLEAN) == release['clean_input_sha256']
    current, clean = (base.NdsImage.open(path) for path in (parent.ROM, CLEAN))
    contexts, records = compile_rows(current, clean)
    for row in records:
        print(row['id'], row['decision'], [expanded(line) for line in row['automatic_layout']['lines']], flush=True)
    if preview:
        return
    runtime = bind_runtime()
    default = native(runtime, 0, b'FI FA')
    _, paint = prior.precedent.planners(runtime.arm)
    pictures = []
    for row in records:
        for label, field in [('before', 'current_hex'), ('after', 'target_hex')]:
            body = bytes.fromhex(row[field])[1:]
            display = native(runtime, row['source_selector'], body, paint)
            assert len(display['pages']) == 1 and display['pages'][0]['first_visible_origin'] == [0, 0]
            page = display['pages'][0]
            if label == 'after':
                encoded = bytes.fromhex(row['automatic_layout']['encoded_hex'])[1:]
                raw = encoded.replace(b'FI', b'Rafael').replace(b'FA', b'Castor')
                unpadded, = paint(runtime.arm, runtime.image.read_file('/GRP/KANJI.FNT'), raw)['pages']
                assert page['native_plane_hex'] == unpadded['native_plane_hex']
            pictures.append((row['id'].split('_B')[1] + ' ' + label, bytes.fromhex(page['native_plane_hex'])))
            row[label + '_native'] = display
    retained = [row for row in records if row['current_hex'] == row['target_hex']]
    changed = [row for row in records if row['current_hex'] != row['target_hex']]
    archives = {}
    for name, raw in prior.transform(current, changed):
        path = ROOT / Path(name).name
        path.write_bytes(raw)
        archives[name] = dict(path=path.as_posix(), sha256=sha(raw), source_sha256=sha(current.read_file(name)))
    sheets = FunctionType(wraps.contact_sheets.__code__, vars(wraps) | {'ROOT': ROOT})(pictures)
    base.save(REVIEW, dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=['source', 'context', 'localization', 'naturalness', 'formatting'],
        candidate_sha256=release['candidate_sha256'], records=changed, unchanged_leads=retained,
        complete_exchange_references=contexts, zero_new_credit=True, full_goal_complete=False))
    base.save(PROOF, dict(candidate_sha256=release['candidate_sha256'], review_sha256=base.digest(REVIEW),
        archives=archives, sheets=sheets, blocks=[[FILE, group['block']] for group in contexts],
        unchanged_terminators_offsets_block_extents_and_unowned_bytes=True, archive_inverses_exact=True,
        checked_complete_native_pages=len(pictures), checked_original_processor_alignments=8 * len(records),
        verified_default_name_expansion=default, native_runtime=runtime.receipt()))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preview', action='store_true')
    main(parser.parse_args().preview)

