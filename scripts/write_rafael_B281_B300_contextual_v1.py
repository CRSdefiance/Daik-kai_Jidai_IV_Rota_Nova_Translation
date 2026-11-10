"""Seal the complete Rafael B281–B300 contextual and speaker-name decisions."""
from copy import deepcopy
import inspect
from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import write_rafael_B261_B280_contextual_v1 as prior
from scripts.seal_rafael_B281_B300_clean_v1 import BLOCKS, ROOT, SEALED, digest
from scripts.source_locked_derivation_v5118 import checked_text


INPUTS = [SEALED/'sealed_drafts.json', *(ROOT/name for name in (
    'current_v1/current_effective.json', 'objects_v1/current_objects.json', 'names_and_terms_v1.json', 'roles.json'))]
DECISIONS = [Path(f'translations/rafael_{part}_contextual_decisions_v1.txt') for part in (
    'B281_B292', 'B293', 'B294_B300')]
OUT = Path('translations/rafael_B281_B300_contextual_review_v1.json')
LABELS = Path('translations/rafael_B281_B300_scoped_names_review_v1.json')
RELEASE = Path('work/rafael3649_release_v1/registered_release_verification.json')
PUNCTUATION = {f'DK4_MES_B293_R{index:04d}' for index in (94, 185, 404, 433, 438)}
WIDE_F = {'DK4_MES_B298_R0046', 'DK4_MES_B298_R0054'}
BROKEN_LEADS = {'SC0_B293_STYLE_328_40': '櫂', 'SC0_B293_STYLE_328_244': '蘗'}
GOLD = 'DK4_MES_B300_R0009'
FE = {
    281: {23:'System gold receipt',54:'System share notice'},
    283: {22:'System gold receipt'},
    284: {21:'System gold receipt',54:'System share notice'},
    286: {22:'System gold receipt'},
    287: {20:'System gold receipt',51:'System share notice'},
    289: {23:'System gold receipt'},
    290: {14:'System gold receipt',45:'System share notice'},
    293: {152:'System injury notice',241:'System elapsed-time notice',318:'System fatigue and injury notice'},
    299: {42:'Repeated digging sound'},
    300: {9:'System gold receipt',40:'System share notice'},
}
NAME_REVISIONS = {
    70: ('Zaganos Bei', 'Zaganos Bey',
         'Use the Bey spelling of the source ベイ already established in the Cyprus bounty briefing. Verify the exact surname field and both consumers before release.'),
}
NAME_RETENTIONS = {
    8: 'Keep Arcadius Eudoxios in dialogue and the source middle name Eirene in the full catalogue.',
    22: 'Keep Samwell Khan in dialogue and the source particle da in the full catalogue.',
    65: 'Keep the registered Plett Perrault spelling in both consumers and use Plett where the guildmaster addresses him.',
    177: 'Sect Leader fits the person who leads the chant, issues instructions and dismisses the group.',
    178: 'Follower fits the unnamed participant who echoes the chant and cheers the leader.',
}

record_source = checked_text(inspect.getsource(prior.review_record), {
    "assert draft['source_selector'] == binding['source_selector'] == 208":
        "assert draft['source_selector'] == binding['source_selector'] and binding['source_selector'] in roles",
    """    if ident == PUNCTUATION:
        assert previous == '！？' and english == '?!'
        row['current_fullwidth_punctuation_consistency_revision'] = True
    if ident in UNTRANSLATED:
        assert any('\\u3040' <= char <= '\\u9fff' for char in previous) and not retained
        row['current_effective_Japanese_requires_localization'] = True""":
        """    if ident in PUNCTUATION:
        assert previous in ('！！', '？', '…') and english in ('!!', '?', '...')
        row['current_punctuation_consistency_revision'] = True
    if ident in WIDE_F:
        assert previous.count('Ｆ') == 1 and 'Ｆrom' in previous
        assert tokens == ['FI'] and not retained
        row['current_fullwidth_initial_F_normalized'] = True
    if ident in BROKEN_LEADS:
        assert previous.startswith(BROKEN_LEADS[ident]) and not retained
        row['current_corrupt_leading_glyph'] = BROKEN_LEADS[ident]
    if ident == GOLD:
        assert previous == 'Received 100,000 coins.' and english == 'You received 10,000 gold coins.'
        assert '１００００' in draft['source_Japanese']
        row['current_reward_amount_corrected_from_clean_source'] = True""",
})
name_source = checked_text(inspect.getsource(prior.name_review), {
    """        if actor in range(151, 155):""": """        if actor in NAME_RETENTIONS:
            finding = NAME_RETENTIONS[actor]
        elif actor in range(151, 155):""",
    "f'RAFAEL261_280_NAME_{actor}'": "f'RAFAEL281_300_NAME_{actor}'",
})
env = {**vars(prior), **globals()}
exec(compile(record_source + '\n' + name_source, __file__+'::same-exact-record-and-name-binding', 'exec'), env)


def read_decisions():
    decisions = {}
    for path in DECISIONS:
        block = None
        for line in path.read_text(encoding='utf-8').splitlines():
            if not line or line.startswith('#'):
                continue
            if line.isdigit():
                block = int(line)
                assert block in BLOCKS
                continue
            key, replacement, finding = (part.strip() for part in line.split('|', 2))
            ident = f'DK4_MES_B{block}_R{int(key):04d}' if key.isdigit() else key
            assert block is not None and f'B{block}_' in ident and ident not in decisions and replacement and finding
            decisions[ident] = replacement, finding
    return decisions


def main():
    assert not OUT.exists() and not LABELS.exists()
    draft, current, objects, identity, role_report = map(prior.load, INPUTS)
    release = prior.load(RELEASE)
    runtime = current['runtime']
    assert all(value['runtime'] == runtime for value in (objects, identity, role_report))
    assert runtime['candidate_sha256'] == release['candidate_sha256'] == current['current_ROM_sha256']
    assert runtime['release_proof_sha256'] == digest(RELEASE) and runtime['captain'] == 0
    assert draft['complete_blocks'] == [group['block'] for group in current['groups']] == BLOCKS
    ordinary = [record for group in current['groups'] for record in group['records']]
    styles, choices = objects['style_records'], objects['choice_records']
    assert (len(ordinary), len(styles), len(choices)) == (164, 76, 5)
    assert sum(len(record['source_style_indices']) for record in styles) == objects['native_style_getter_cases'] == 88
    bound = {record['id']: record for record in ordinary + styles + choices}
    decisions = read_decisions()
    assert set(bound) == set(decisions) == {record['id'] for record in draft['records']} and len(bound) == 245, set(bound)^set(decisions)
    roles = {row['source_selector']: row for row in role_report['native_roles']['rows']}
    assert [(selector, role['resolved_actor_ID'], role['source_voice_class']) for selector, role in roles.items()] == [
        (207,0,2),(208,151,4),(211,151,4),(215,151,4),(216,151,4)]
    style_roles = {record['id']: record for record in role_report['source_records'] if '_STYLE_' in record['id']}
    assert set(style_roles) == {record['id'] for record in styles}
    names = {binding['actor_ID']: env['name_review'](binding) for binding in identity['name_bindings']}
    assert len(names) == 17
    records = [env['review_record'](row, bound[row['id']], decisions[row['id']], names, roles, style_roles)
               for row in draft['records']]
    assert [(row['id'], row['native_literal_tokens']) for row in records if row['native_literal_tokens']] == [
        ('DK4_MES_B292_R0006',['FO']), ('DK4_MES_B294_R0006',['FA']),
        ('DK4_MES_B298_R0046',['FI']), ('DK4_MES_B298_R0054',['FI'])]
    ids = {row['id']: row for row in records}
    assert ids['DK4_MES_B293_R0396']['english'] == ids['DK4_MES_B293_R0400']['english'] == ids['DK4_MES_B296_R0013']['english']
    assert ids['DK4_MES_B296_R0013']['english'].casefold().endswith(
        ids['DK4_MES_B298_R0005']['english'].removesuffix('...').casefold()+'.')
    assert ids['DK4_MES_B296_R0108']['english'].removesuffix('...') in ids['DK4_MES_B293_R0396']['english']
    evidence = {path.as_posix(): digest(path) for path in [*INPUTS, *DECISIONS, RELEASE, Path(__file__).resolve().relative_to(Path.cwd())]}
    common = dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
                  encoder='dialogue-relocatable-v1', review_gates=prior.GATES, runtime=runtime, new_credit=0)
    doc = dict(**common, format='dk4-contextual-dialogue-review-v2', file_path='/data/SC0.DK4', blocks=BLOCKS,
        records=records, source_objects=245, ordinary_speech_objects=164, physical_style_alternatives=76,
        style_objects=11, native_style_slots=88, typed_choice_objects=5, typed_choice_commands=2, control_only_blocks=[],
        **{key: current[key] for key in ('current_ROM', 'current_ROM_sha256', 'current_archive_sha256')},
        proposed_revisions=sum(row['decision'] == 'revision' for row in records),
        justified_retentions=sum(row['decision'] == 'retention' for row in records),
        punctuation_consistency_revisions=sorted(PUNCTUATION), normalized_fullwidth_F_records=sorted(WIDE_F),
        corrupted_leading_glyph_records=BROKEN_LEADS, reward_amount_correction=GOLD,
        native_macro_tokens_still_require_formatter_marking=True,
        all_individual_four_prose_gates_pass=True, all_fifth_formatting_gates_pending=True, evidence=evidence)
    for row in records:
        assert row['review'] == {gate: gate != 'formatting' for gate in prior.GATES}
    projected = deepcopy(doc)
    projected['translation_policy'] = 'natural-dialogue-v1'
    validate_natural_dialogue_batch(projected)
    try:
        validate_natural_dialogue_batch(doc)
    except ValueError as error:
        assert 'requires per-record source, context, localization, naturalness, and formatting review' in str(error)
    else:
        raise AssertionError('Unformatted manuscript unexpectedly passed the release gate')
    prior.save(LABELS, dict(**common, format='dk4-scoped-name-contextual-review-v2',
        records=list(names.values()), all_name_formatting_gates_pending=True,
        scoped_name_field_corrections_pending=sorted(NAME_REVISIONS), evidence=evidence))
    evidence[LABELS.as_posix()] = digest(LABELS)
    prior.save(OUT, doc)
    print(f"245 contextual decisions, {doc['proposed_revisions']} revisions and "
          f"{doc['justified_retentions']} retentions. 17 scoped names. Formatting remains pending.")


if __name__ == '__main__':
    main()
