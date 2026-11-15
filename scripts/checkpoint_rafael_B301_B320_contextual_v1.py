"""Verify clean drafts and checkpoint exact contextual decisions from complete exchanges."""
from pathlib import Path

from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_rafael3894_registered_v1 import LEDGER, NEXT, PACKAGE, RELEASE
from scripts.checkpoint_rafael_B168_B169_research_v1 import link
from scripts.save_editorial_progress_checkpoint_v6 import checkpoint
from scripts.seal_rafael_B301_B320_clean_v1 import BLOCKS, ROOT, SEALED, digest
from scripts.write_rafael_B281_B300_contextual_v1 import name_source, record_source
from scripts.write_rafael_B261_B280_contextual_v1 import GATES, MACROS
from scripts.source_locked_derivation_v5118 import checked_text


DRAFT = SEALED / 'sealed_drafts.json'
CURRENT = ROOT / 'current_v1/current_effective.json'
OBJECTS = ROOT / 'objects_v1/current_objects.json'
NAMES = ROOT / 'names_and_terms_v1.json'
ROLES = ROOT / 'roles.json'
DECISIONS = [Path(f'translations/rafael_B{start}_B{start+4}_contextual_decisions_v1.txt') for start in (301, 306)]
PARTIAL = ROOT / 'B301_B310_contextual_review_v1.json'
NAME_REVIEW = Path('translations/rafael_B301_B320_scoped_names_review_v1.json')

NAME_REVISIONS = {}
NAME_RETENTIONS = {
    0: 'Rafael Castor is the approved default name. The dialogue continues to use the runtime name token where the source does.',
    4: 'Janus Pasar is the established full spelling. His fearful reply at the bridge calls for no separate title.',
    5: 'Claudio Manaus fits both consumers. Use Clau only where his crew uses the source nickname.',
    7: 'Cristina Erneco is the established spelling for this exact actor and her brief forest exchange.',
    8: 'Keep Arcadius Eudoxios on the nameplate and the source middle name Eirene in the full catalogue.',
    17: 'Keep Al Shin on the nameplate and the source middle element Ferid in the catalogue. His crewmates address him as Al.',
    19: 'Carlo Sinat is the established spelling for the speaker who marvels at the remedy.',
    92: 'Barkeep fits the tavern contact who tells the Vedas legend and offers advice about the curse.',
    95: 'Patron fits the tavern customer who relays the Basra message. The internal portrait category adds no public title.',
    97: 'Patron fits the unnamed customer who tells Rafael about the missing explorers.',
    135: 'Priest fits the source ritual role and the speaker entrusted with recognizing the Veda and passing on the coin.',
    148: 'Guildmaster identifies the Istanbul contact by his established role. The dialogue establishes his family situation on its own.',
    151: 'Sailor fits the progressive nameplate during the expedition. Retainer preserves the broader source class in the full catalogue.',
    162: 'Boy is a natural label for the source role and leaves his name unstated.',
    182: 'Explorer directly identifies the freed speaker and applies to the expedition without adding a rank.',
    192: 'Matilda is the established name of the Genoa contact who recommends the Colosseum.',
    197: 'Safia is the established name of the Basra contact who asks about the earrings and shares the mosque lead.',
    199: 'Lucia is the established name of the Malacca contact who warns about the forest.',
    203: 'Sakura is the established name of the source speaker who checks the map and sees the travelers off.',
}
FE = {
    301: {86: 'Tiger growl', 129: 'Tiger roar', 201: 'System injury notice'},
    305: {164: 'System fatigue and group-loss notice'},
    310: {99: 'System injury notice', 202: 'System fatigue notice'},
    312: {129: 'System fatigue notice', 179: 'System group-loss notice'},
    316: {14: 'Unseen explorer', 26: 'Unseen voice', 35: 'Unseen voice', 38: 'Unseen voice'},
    318: {75: 'Unseen voice', 198: 'Unseen voice', 205: 'Unseen voice'},
    320: {155: 'System elapsed-time and fatigue notice'},
}
BROKEN_LEADS = {'SC0_B305_STYLE_1042_60': '裕', 'DK4_MES_B306_R0034': '百'}
WIDE_I = 'DK4_MES_B310_R0057'
JAPANESE = 'DK4_MES_B309_R0047'
PUNCTUATION = {'DK4_MES_B304_R0023', 'DK4_MES_B306_R0026', 'DK4_MES_B316_R0030'}

review_source = checked_text(record_source, {
    "assert previous in ('！！', '？', '…') and english in ('!!', '?', '...')":
        "assert (previous, english) in (('？','...?'), ('！？','?!'))",
    """    if ident in WIDE_F:
        assert previous.count('Ｆ') == 1 and 'Ｆrom' in previous
        assert tokens == ['FI'] and not retained
        row['current_fullwidth_initial_F_normalized'] = True""":
        """    if ident == WIDE_I:
        assert previous.startswith('Ｉ') and english.startswith('I') and tokens == ['FI'] and not retained
        row['current_fullwidth_initial_I_normalized'] = True""",
    """    if ident == GOLD:
        assert previous == 'Received 100,000 coins.' and english == 'You received 10,000 gold coins.'
        assert '１００００' in draft['source_Japanese']
        row['current_reward_amount_corrected_from_clean_source'] = True""":
        """    if ident == JAPANESE:
        assert not previous.isascii() and not retained
        row['current_effective_Japanese_requires_localization'] = True""",
})
label_source = checked_text(name_source, {"f'RAFAEL281_300_NAME_{actor}'": "f'RAFAEL301_320_NAME_{actor}'"})
env = dict(globals())
env['re'] = __import__('re')
exec(compile(review_source + '\n' + label_source, __file__ + '::exact-source-and-current-records', 'exec'), env)


def read_decisions(paths):
    decisions = {}
    for path in paths:
        block = None
        for line in path.read_text(encoding='utf-8').splitlines():
            if not line or line.startswith('#'):
                continue
            if line.isdigit():
                block = int(line)
                continue
            key, replacement, finding = (part.strip() for part in line.split('|', 2))
            ident = f'DK4_MES_B{block}_R{int(key):04d}' if key.isdigit() else key
            assert block in BLOCKS and f'B{block}_' in ident and ident not in decisions
            assert replacement and finding
            decisions[ident] = replacement, finding
    return decisions


def main():
    assert not PARTIAL.exists() and not NAME_REVIEW.exists()
    draft, current, objects, identity, role_report, release = map(load, (DRAFT, CURRENT, OBJECTS, NAMES, ROLES, RELEASE))
    runtime = current['runtime']
    assert all(value['runtime'] == runtime for value in (objects, identity, role_report))
    assert runtime['candidate_sha256'] == release['candidate_sha256'] == current['current_ROM_sha256']
    assert runtime['release_proof_sha256'] == digest(RELEASE) and runtime['captain'] == 0
    assert draft['complete_blocks'] == [group['block'] for group in current['groups']] == BLOCKS
    assert all(digest(path) == checksum for path, checksum in draft['evidence'].items())
    ordinary = [row for group in current['groups'] for row in group['records']]
    styles, choices = objects['style_records'], objects['choice_records']
    assert (len(ordinary), len(styles), len(choices), objects['native_style_getter_cases']) == (297, 145, 11, 152)
    bound = {row['id']: row for row in ordinary + styles + choices}
    assert bound.keys() == {row['id'] for row in draft['records']} and len(bound) == 453
    roles = {row['source_selector']: row for row in role_report['native_roles']['rows']}
    assert sorted(roles) == [207, 208, 211, 214, 215, 216, 222]
    style_roles = {row['id']: row for row in role_report['source_records'] if '_STYLE_' in row['id']}
    assert style_roles.keys() == {row['id'] for row in styles}
    names = {row['actor_ID']: env['name_review'](row) for row in identity['name_bindings']}
    assert names.keys() == NAME_RETENTIONS.keys() and all(row['decision'] == 'retention' for row in names.values())
    decisions = read_decisions(DECISIONS)
    selected = [row for row in draft['records'] if row['block'] <= 310]
    assert decisions.keys() == {row['id'] for row in selected} and len(selected) == 229
    rows = [env['review_record'](row, bound[row['id']], decisions[row['id']], names, roles, style_roles) for row in selected]
    by_id = {row['id']: row for row in rows}
    pairs = ((90, 8), (96, 14), (100, 18), (105, 23), (109, 27), (112, 30), (116, 34),
             (127, 45), (134, 52), (137, 55), (142, 60))
    for immediate, later in pairs:
        assert by_id[f'DK4_MES_B306_R{immediate:04d}']['english'] == by_id[f'DK4_MES_B308_R{later:04d}']['english']
    glyph_findings = {ident: row['current_comparison_paragraph'] for ident, row in bound.items()
                      if not row['current_comparison_paragraph'].isascii()}
    assert glyph_findings.keys() == set(BROKEN_LEADS) | PUNCTUATION | {WIDE_I, JAPANESE}
    evidence = {str(path): digest(path) for path in (DRAFT, CURRENT, OBJECTS, NAMES, ROLES, RELEASE, *DECISIONS, Path(__file__))}
    common = dict(translation_policy='natural-dialogue-v2', target_locale='en-US', review_gates=GATES,
                  runtime=runtime, new_credit=0, evidence=evidence)
    revisions = sum(row['decision'] == 'revision' for row in rows)
    retentions = len(rows) - revisions
    save(NAME_REVIEW, dict(**common, format='dk4-scoped-name-contextual-review-v2',
         records=list(names.values()), all_name_formatting_gates_pending=True,
         scoped_name_field_corrections_pending=[]))
    save(PARTIAL, dict(**common, format='dk4-contextual-dialogue-review-v2', file_path='/data/SC0.DK4',
         blocks=list(range(301, 311)), records=rows, reviewed_objects=229, full_intake_objects=453,
         remaining_current_comparisons=224, proposed_revisions=revisions, justified_retentions=retentions,
         all_individual_four_prose_gates_pass=True, all_fifth_formatting_gates_pending=True,
         entire_intake_non_ASCII_findings=glyph_findings, scoped_name_review=str(NAME_REVIEW),
         scoped_name_review_sha256=digest(NAME_REVIEW)))

    ledger, package = map(load, (LEDGER, PACKAGE))
    assert ledger['current_integrated_candidate']['sha256'] == release['candidate_sha256']
    summary = (
        f'All 453 Rafael B301–B320 clean-source drafts are sealed. B301–B310 has 229 contextual decisions '
        f'with {revisions} revisions and {retentions} justified retentions. '
        'The remaining 224 comparisons and final display checks are pending. Integrated coverage is 15,739.'
    )
    doc = f"""# Rafael B301–B320 clean drafts and first contextual decisions

{summary}

The sealed drafts cover 297 speeches, 145 physical alternate voices and 11 captions. The source glossary, complete exchange context and exact byte offsets remain bound before comparison. Rafael3894 supplies all 453 current objects. The native role getter mapped seven selectors across 148 source records, the original style getter checked all 152 current slots, and both name getters supplied 19 speaker or role decisions with individual retention reasons. Final display approval is pending. {link('Sealed source drafts', DRAFT)}. {link('Exact current body bindings', CURRENT)}. {link('Current alternate voices and choices', OBJECTS)}. {link('Scoped name decisions', NAME_REVIEW)}.

The first half restores the Indian Ocean in the Vedas clue, the established Proof of Conquest term, Istanbul as the medicine destination and the untranslated guide line. It repairs three abnormal leading letters in the river warning, illness question and snake sighting. The two bedside paths now use matching wording where the Japanese repeats the scene. The remaining full-width reaction in B316 was located by the scan and awaits its contextual comparison. {link('First 229 contextual decisions', PARTIAL)}.

Continue B311–B320 against the sealed clean drafts and Rafael3894. Review the desert menu and directions, Safia's festival and mosque lead, the book title and ritual vocabulary, and the map detour. Then seal the full 453 decisions, verify layouts and representative native behavior, and integrate through the registered workflow. Graphics and the later older-record technical audit remain separate.
"""
    checkpoint(
        mutation=ROOT/'B301_B310_contextual_checkpoint_v1', batch_key=NEXT,
        batch_updates=dict(new_credit=0, independently_drafted_records=453, independent_draft_blocks=BLOCKS,
            remaining_clean_meanings_anddrafts=0, remaining_current_comparisons=224, source_only=False,
            current_bound_records=453, contextual_compared_records=229, proposed_revisions=revisions,
            justified_retentions=retentions, reviewed_names_and_roles=19, formatting_pending=True,
            partial_contextual_review=str(PARTIAL), partial_contextual_review_sha256=digest(PARTIAL),
            evidence={**ledger[NEXT]['evidence'], **evidence, str(PARTIAL): digest(PARTIAL),
                      str(NAME_REVIEW): digest(NAME_REVIEW)}),
        additional_updates={'editorial_execution_priority_20261104': dict(new_credit=0,
            current_batch='Rafael B311–B320 contextual comparison.',
            next_action='Finish the 224 remaining contextual decisions and apply the native display checks.',
            native_job_live=False, registered_build_live=False, guide_photos=False)},
        summary=summary, document='docs/editorial_Rafael_B301_B310_contextual_20261106.md',
        document_text=doc, completed=15739, protected={
            'translations/release_stack.json': release['registry_sha256'],
            release['canonical_base']: release['canonical_sha256'],
            release['candidate']: release['candidate_sha256'], release['patch']: release['patch_sha256'],
            package['zip']: package['zip_sha256'],
        },
    )
    print(summary)


if __name__ == '__main__':
    main()
