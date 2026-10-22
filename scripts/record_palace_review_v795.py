"""Checkpoint source-reviewed Palace prose without granting production credit."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/palace_editorial_v795')
DOC = Path('docs/palace_editorial_v795_checkpoint.md')


def main():
    assert not DOC.exists()
    manuscript = Path('translations/palace_editorial_manuscript_v2.json')
    draft = read(manuscript)
    proof = read(ROOT/'prototype_layout/verification.json')
    assert proof['manuscript_sha256'] == sha(manuscript.read_bytes())
    assert proof['native_layouts'] == 323 and not proof['findings']
    assert len(proof['complete_font_planes']) == 40
    assert proof['all31_native_IDs'] == list(range(1146, 1177))
    for row in proof['complete_font_planes']:
        assert sha(Path(row['path']).read_bytes()) == row['sha256']
        assert row['independent_full_native_font_exact'] and not row['findings']
    for row in proof['preview_sheets']:
        assert sha(Path(row['path']).read_bytes()) == row['sha256']
    assert all(all(r['review'][k] for k in ('source','context','localization','naturalness'))
               and not r['review']['formatting'] for r in draft['records'])
    assert sum(r['decision'] == 'revise' for r in draft['records']) == 29
    save(ROOT/'prototype_layout/visual_review.json', {
        'verification_sha256': sha((ROOT/'prototype_layout/verification.json').read_bytes()),
        'all40_complete_font_planes_visually_reviewed': True,
        'four_contact_sheets_and_actual2842_plane_reviewed': True,
        'actual_fee_digits_all_four_visible': True,
        'production_dispatch_COMMON_lookup_and_revised_gameplay_pending': True,
        'no_editorial_completion_credit': True})
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = read(ledger_path)
    assert ledger['records_editorially_completed'] == 496
    assert ledger['records_with_source_and_prose_pass'] == 499
    assert ledger['active_source_prose_drafts']['native_message_IDs'] == [750,751,752]
    save(ROOT/'editorial_ledger_before_v795.json', ledger)
    ledger['records_with_source_and_prose_pass'] = 530
    ledger['records_with_source_prose_drafts'] = 530
    active = ledger['active_source_prose_drafts']
    active['native_message_IDs'] += list(range(1146,1177))
    active['manuscripts'].append(str(manuscript))
    active['status'] = '750-752-context-unmapped;Palace31-production-formatting-and-gameplay-pending'
    active['note'] = ('Palace31 have source/context/localization/naturalness review and prospective native '
        'layouts, not production-formatting approval. 750-752 still lack mapped contexts. '
        'Wider shared text, all routes and other prose remain unfinished.')
    ledger['palace_next_source_packet'].update({
        'review_credit': 31, 'completion_credit': 0,
        'reviewed_manuscript': str(manuscript), 'native_context': str(ROOT/'native_context.json'),
        'prospective_layouts': str(ROOT/'prototype_layout/verification.json'),
        'next': 'Install all31 paragraphs through an exact bounded dispatcher and COMMON repack; '
                'verify original callers, full copies, revised Palace displays, digits, pagination and return.'})
    ledger['palace_speaker_context_erratum'] = {
        'evidence': str(ROOT/'native_context.json'),
        'correction': 'Original Palace branches resolve ruler building role6/actor127, minister role11/actor121. '
                      'V794 role4/actor92 lookup was not the executed Palace speaker provider.',
        'historical_V794_record_retained': True}
    for finding in ledger['findings']:
        if finding['id'] == 'Palace1162-insufficient-funds-meaning':
            finding['status'] = 'source-context-confirmed;corrected-draft;integration-and-gameplay-pending'
            finding['proof'] = str(ROOT/'native_context.json')
    summary = ('Palace1146-1176 source/context and prose reviewed:29 proposed revisions,2 retained. '
        '323 prospective native layouts and40 full font planes pass, including all four fee digits2842. '
        'Original Market letter flags, leader/player address forms and218 monthly-price providers mapped. '
        'Monthly payments use the original multiplier/shift, not an assumed division by100. '
        'Speaker erratum:Palace ruler role6/actor127,minister role11/actor121. '
        '530 source/prose reviewed,496 complete,34 reviewed drafts pending. V792 ROM/patch unchanged; '
        'production routing, COMMON integration and revised gameplay remain required. Full goal active.')
    ledger['latest_checkpoint'] = summary
    ledger['research_checkpoints'].append({'id':'V795-Palace31-source-prose-native-layout',
        'documentation':str(DOC),'new_source_prose_reviewed':31,'new_editorially_completed':0,
        'new_ROM':False,'full_goal_complete':False})
    save(ledger_path, ledger)
    DOC.write_text('# V795: Palace source review and prospective formatting\n\n'+summary+'\n\n'
        'The reviewed manuscript is `translations/palace_editorial_manuscript_v2.json`; '
        'v1 is retained as a superseded draft. All paragraphs remain logical prose with automatic '
        'layout. Formatting gates remain false until production dispatch and integration are verified.\n\n'
        'The original Palace branches and providers were executed on captured V794 RAM, stopping '
        'before the UI wrapper. Those declared CPU inputs do not prove naturally earned eligibility. '
        'Recommendation/introduction are player-admiral flags, not ordinary inventory items. '
        'The ruler pays the player for loaned display items. 1147 receives the other faction leader\'s '
        'address form; 1151/1154 receive the player\'s address form. Native monthly-price arithmetic '
        'uses multiplier 0x51EB851F and shift36 across218 item values.\n\n'
        'V794 historical speaker attribution is superseded: actual ruler role6/actor127; minister '
        'role11/actor121. Its captured text IDs, blank page and no-payment cancellation remain valid. '
        'The prospective 2842 font plane has all digits visible, but actual repaired playback is pending.\n\n'
        'The separate graphics audit and18 plaques remain unfinished. Low-resolution Online bodies '
        'stay excluded; brown marks and approved names remain unchanged. No canonical promotion.\n',encoding='utf-8')
    for name in ('known_issues','todo','translation_progress','editorial_review_goal'):
        p = Path('docs')/(name+'.md')
        p.write_text(p.read_text(encoding='utf-8')+'\n\n## V795: Palace source/prose review\n\n'+summary+
                     ' See [V795 checkpoint](palace_editorial_v795_checkpoint.md).\n',encoding='utf-8')
    print(summary,flush=True)


if __name__ == '__main__': main()
