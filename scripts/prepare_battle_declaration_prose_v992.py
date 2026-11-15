"""Review all22 clean-source battle readiness and declaration alternatives; layout stays pending."""
from pathlib import Path
from shutil import copy2

from dk4tool.patch.activity_special_editorial_v987b import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/battle_declaration_v992')
CONTEXT = Path('work/analysis/battle_declaration_v991c/source_context_packet.json')
MANUSCRIPT = Path('translations/battle_declaration_editorial_manuscript_v1.json')
ROM = Path('out/all_routes_combined_v987_candidate.nds')
IDS = tuple(range(1889, 1911))
RETAINED = {1889, 1890, 1891, 1892, 1893, 1894, 1896, 1905, 1910}
DATA = '''1889|The speaker announces that preparations for battle are beginning,with a polite tone.|We're preparing for battle!|Retain the complete natural announcement and its immediate timing. This is preparation for battle,not a report that battle has ended or victory is certain.
1890|The speaker orders all hands to battle stations,then urges them onward.|All hands to battle stations... Let's go!|Retain the idiomatic naval order,all-hands scope and determined follow-up. The rhetorical pause is punctuation within a paragraph,not an authored display break.
1891|The speaker energetically announces that they are getting ready for battle.|We're getting ready for battle!|Retain the fluent cheerful announcement. The informal getting ready matches the energetic yo ending without inventing a new event or opponent.
1892|The speaker announces battle preparations and urges everyone to get the enemy,with a lively feminine voice.|We're preparing for battle! Let's get them!|Retain natural energetic spoken English and both source intentions. Do not impose a gendered English job title or add a specific tactic.
1893|The speaker roughly announces battle stations and urges everyone to get the enemy.|Battle stations! Let's get them!|Retain the clipped idiomatic order and rough confident encouragement. It preserves the emphatic source without adding profanity or a promised victory.
1894|The speaker announces battle stations and says they should get to it,with an older conversational voice.|Battle stations! Let's do this!|Retain the natural firm order and inclusive resolve. Do not force Japanese age-marked particles into unnatural English or invent a title or kinship.
1895|The speaker says battle is about to begin and encourages everyone to do their best.|We're going into battle! Let's do our best!|Restore the source encouragement to make an effort. The older Let's win replaces that with a different objective;the revision keeps the upbeat youthful voice and immediate battle timing.
1896|The speaker politely announces battle stations and urges everyone to scatter or sweep away the enemy.|Battle stations! Let's crush them!|Retain the natural confident martial exhortation and both source intentions. Crush them is an idiomatic forceful localization of kechirashimasho,not an actual battle-result claim.
1897|The speaker politely proposes declaring war on the named faction and asks whether that is acceptable.|We'll declare war on %s. Is that all right?|The original argument is the complete faction display name,including labels such as Castor Co. Remove the redundant possessive faction suffix and use a natural polite confirmation. Restore ordinary ASCII I;native complete-glyph proof remains pending.
1898|The speaker energetically announces a declaration of war on the named faction and asks the admiral whether that is okay.|We're declaring war on %s! Is that okay, Admiral?|Use the source complete faction label directly and retain the explicit Admiral address and lively confirmation. Do not confuse this planned declaration with a completed war or an enemy leader speaking.
1899|The speaker says they will declare war on the named faction and asks the admiral for reassuring confirmation,with a feminine polite voice.|We'll declare war on %s. That's all right, isn't it, Admiral?|Preserve the explicit Admiral address and reassurance-seeking tone as natural English. Use the complete faction display name directly;do not append an invented leader-name possessive or gendered title.
1900|The speaker roughly announces a declaration of war on the named faction and checks that the listener is sure.|We're declaring war on %s! You're sure about this?|Use the complete faction label directly and retain the rough confident announcement followed by a firm check. The question is deliberate conversational English rather than an unsupported promise or completed action.
1901|The speaker formally announces a declaration of war on the named faction and asks for agreement.|We shall declare war on %s. Do you agree?|Keep the older formal shall and the full confirmation while removing the redundant faction suffix. The name substitution remains one original percent-s argument in source order.
1902|The speaker asks whether it is okay to tell the named faction that they are going to beat them.|I'll tell %s we're going to beat them! Is that okay?|Preserve the childlike indirect threat and the act of telling the other side. Do not flatten it into a generic diplomatic formula or an immediate attack command. Use the complete faction label and ordinary ASCII I.
1903|The speaker formally announces a declaration of war on the named faction and asks for the listener's approval.|We will declare war on %s. Do I have your approval?|Use natural formal English rather than the older inverted You approve,yes. Preserve the full declaration and confirmation;the complete faction name needs no additional possessive suffix.
1904|The speaker says the faction is unidentified but proposes declaring war and asks whether that really is acceptable.|We don't know which faction this is, but we'll declare war. Is that all right?|Keep the explicit uncertainty,the declaration and the polite request for confirmation in complete natural sentences. Source dispatch can select this from a menu flag override;do not infer a specific disguise or hidden-story condition.
1905|The speaker says they have not identified the faction and asks whether to declare war despite that.|We haven't identified this faction. Shall we declare war anyway?|Retain the fluent complete uncertainty and confirmation. Anyway expresses the source concession without inventing a lack of scouting ability or a new game rule.
1906|The speaker casually says they do not know which faction this is and asks confirmation before declaring war anyway.|I don't know which faction this is. We're declaring war anyway, right?|Retain the natural conversational wording and uncertainty while replacing obsolete full-width I with ordinary ASCII. Complete native leading-letter and wrapping verification is still required.
1907|The speaker roughly says they do not know the faction but will declare war and checks that the listener is sure.|No idea which faction this is, but we're declaring war. You're sure about this?|Restore the full rough spoken meaning and explicit certainty check. Remove the old translator-authored line break and alignment padding;the formatter must place every visible line and preserve whole words.
1908|The older speaker says they do not know which faction this is but proposes declaring war and asks for confirmation.|I don't know which faction this is. Shall we declare war anyway?|Restore the omitted uncertainty and complete declaration confirmation from the old telegraphic Unknown group. Declare war. Shall preserves measured older formality without artificial archaic syntax.
1909|The speaker does not know who the others are and asks whether they should tell them they are going to attack.|I don't know who they are. Should I tell them we're going to attack?|Restore both uncertainty and the act of communicating an attack threat. The old Unknown group. Attack omits most of the meaning and can misrepresent this as a direct attack command. Do not invent the group's identity.
1910|The speaker formally says the faction is unidentified and asks whether to declare war nonetheless.|This faction is unidentified. Shall we declare war nonetheless?|Retain the complete natural formal confirmation. Nonetheless suits this formal voice and preserves the source concession;do not replace it merely to standardize every voice.'''


def main():
    assert not ROOT.exists() and not MANUSCRIPT.exists()
    packet = read(CONTEXT)
    assert len(packet['all832_original_object_voice_selections']) == 832
    assert len(packet['all4_null_actor_controls']) == 4
    assert len(packet['all45_original_role_wrapper_argument_and_UI_result_cases']) == 45
    assert len(packet['all24_original_branch_fragment_cases']) == 24
    assert len(packet['all20_native_complete_faction_labels']) == 20
    assert packet['ready1889_1896_uses_player_First_Mate_only_in_already_war_or_pirate_flag0_paths']
    assert packet['new_war_enemy_announcement_is_separate2201_2208_not_ready1889_1896']
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = read(ledger_path)
    assert (ledger['records_editorially_completed'], ledger['records_with_source_and_prose_pass']) == (1174, 1177)
    assert sha(ROM.read_bytes()) == packet['candidate_sha256'] == ledger['current_integrated_candidate']['sha256']
    rom, clean = map(NdsImage.open, (ROM, 'work/clean.nds'))
    jp = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'), clean.read_file('/__arm9__.bin'))
    en = current_entries(rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin'))
    source = {r['message_id']: r for r in packet['records_and_immediate_neighbors']}
    tables = {r['family']: r for r in packet['source_tables']}
    rows = []
    for line in DATA.splitlines():
        token, meaning, english, note = line.split('|')
        n = int(token)
        family = 'ready' if n <= 1896 else 'named' if n <= 1903 else 'unknown'
        s = source[n]
        expected_args = int(family == 'named')
        assert jp[n].text.hex() == s['source_hex'] and en[n].text.hex() == s['current_text_hex']
        assert english.isascii() and english == ' '.join(english.split()) and not any(c in english for c in '{}\n')
        assert english.count('%s') == jp[n].text.count(b'%s') == expected_args and '%' not in english.replace('%s', '')
        assert not any(m in english for m in ('FI', 'FA', 'FO', 'FU', 'IC'))
        decision = 'retain' if n in RETAINED else 'revise'
        if decision == 'retain': assert english == s['current_English'].strip()
        voices = [v for v, selected in enumerate(tables[family]['IDs']) if selected == n or selected == -1 and tables[family]['IDs'][0] == n]
        representatives = [r for r in packet['all45_original_role_wrapper_argument_and_UI_result_cases']
                           if r['family'] == family and r['events'][0]['message_ID'] == n and r['events'][0]['UI_result'] == 0]
        assert representatives
        context = (
            'Independent player-side First Mate battle-readiness announcement. Original6EE90 selects ready table117440 through role1 wrapper53D44 only for already-hostile or pirate targets with zero input flag. This is not the opposing leader response to a new declaration. '
            if family == 'ready' else
            'Independent player-side First Mate declaration confirmation. Original6EE90 uses named table117420 through role1 wrapper53CB0 when the target is not already at war,leader byte26 is nonzero,and the menu-derived input flag is zero. The single percent-s argument is original company virtual getter+8 supplying the COMPLETE faction display label. '
            if family == 'named' else
            'Independent player-side First Mate unidentified-faction declaration confirmation. Original6EE90 selects unknown table117400 through role1 wrapper53CB0 for its original input-flag/leader-state branches,including already-hostile and pirate confirmation paths. Do not interpret the wording as proof of a particular faction-discovery story state. ')
        context += ('Original82478 selects an actual role officer or its native fallback;the voice table chooses among independent alternatives. Named voice1 falls back to1897;unknown voice3 falls back to1904. UI0 means acceptance and UI1 cancellation through original53CB0 inversion. Accepted new hostilities separately invoke target leader table1184E0 IDs2201-2208,then original relation setters;those messages are controls outside this review. Storage neighbors are not consecutive speech. No identity,kinship,rank,earned event,battle outcome or unknown flag meaning is invented.')
        rows.append({'id': f'COMMON_MESSAGE_{n}', 'message_id': n, 'source_family': family,
                     'consumer': 'native-speech-announcement' if family == 'ready' else 'native-speech-confirmation',
                     'speaker': 'Player First Mate or original native fallback; voice classes '+','.join(map(str, voices)),
                     'source_voice_classes_including_native_fallback': voices,
                     'representative_actor_IDs': sorted({r['speaker_actor_ID'] for r in representatives}),
                     'representative_speakers': sorted({r['speaker'] for r in representatives}),
                     'context': context, 'source_Japanese': s['source_Japanese'], 'source_hex': s['source_hex'],
                     'source_reference': s['source_reference'], 'canonical_source_hex': s['canonical_text_hex'],
                     'current_reference': s['current_reference'], 'current_text_hex': s['current_text_hex'],
                     'current_English': s['current_English'], 'source_meaning': meaning, 'english': english,
                     'localization_note': note, 'editorial_decision': decision,
                     'native_argument_count': expected_args, 'source_native_macros': [],
                     'review': {'source': True, 'context': True, 'localization': True, 'naturalness': True, 'formatting': False}})
    assert tuple(r['message_id'] for r in rows) == IDS
    assert sum(r['editorial_decision'] == 'revise' for r in rows) == 13
    assert sum(r['editorial_decision'] == 'retain' for r in rows) == 9
    ROOT.mkdir(parents=True)
    policy = Path('translations/character_name_localization_policy_v1.json')
    supplement = ROOT/'source_context_and_faithfulness_review.json'
    save(supplement, {'candidate_sha256': packet['candidate_sha256'], 'source_context_sha256': sha(CONTEXT.read_bytes()),
                     'established_name_policy': {str(policy): sha(policy.read_bytes())},
                     'all22_independent_alternatives_source_gloss_and_read_aloud_pass': True,
                     'all7_named_templates_preserve_one_complete_faction_label_argument': True,
                     '1895_restores_do_our_best_instead_of_unsupported_win_substitution': True,
                     '1902_and1909_preserve_telling_target_about_threat_not_direct_attack_command': True,
                     '1907_1908_1909_restore_omitted_uncertainty_and_confirmation': True,
                     'ASCII_I_replaces_legacy_full_width_I_in1897_1902_1906_pending_native_glyph_proof': True,
                     '1907_old_authored_LF_and_alignment_removed_from_prose': True,
                     'opposing_leader2201_2208_and_neighbor1888_1911_no_new_review_credit': True,
                     'native_speaker_fallback_follows_current_fleet_not_assumed_story_captain': True,
                     'all_layout_native_font_dynamic_substitution_and_actual_gameplay_gates_pending': True})
    save(MANUSCRIPT, {'format': 'dk4-natural-dialogue-source-manuscript-v2', 'translation_policy': 'natural-dialogue-v2',
                      'target_locale': 'en-US', 'encoder': 'dialogue-relocatable-v1',
                      'consumer_layout_profile': 'battle-declaration-original-speech-modal-pending',
                      'review_gates': ['source', 'context', 'localization', 'naturalness'], 'formatting_review_pending': True,
                      'status': '22-source-prose-reviewed-native-font-dynamic-wrap-release-actual-pending',
                      'file_path': '/COMMON/MESFILE.DK4', 'source_clean_ROM_sha256': packet['source_clean_ROM_sha256'],
                      'current_ROM': str(ROM), 'current_ROM_sha256': packet['candidate_sha256'],
                      'current_COMMON_sha256': packet['COMMON_sha256'], 'current_ARM9_sha256': packet['ARM9_sha256'],
                      'native_context_proof': str(CONTEXT), 'native_context_proof_sha256': sha(CONTEXT.read_bytes()),
                      'source_context_supplement': str(supplement), 'source_context_supplement_sha256': sha(supplement.read_bytes()),
                      'records': rows, 'full_goal_complete': False})
    save(ROOT/'editorial_ledger_before_source_review.json', ledger)
    ledger['records_with_source_and_prose_pass'] = ledger['records_with_source_prose_drafts'] = 1199
    ledger['source_prose_reviewed_counts_by_file']['/COMMON/MESFILE.DK4'] = 1198
    ledger['reviewed_but_incomplete_COMMON_IDs'] = [750, 751, 752, *IDS]
    ledger['active_source_prose_drafts'] = {'native_message_IDs': [750, 751, 752, *IDS],
        'manuscripts': ['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json', str(MANUSCRIPT)],
        'status': 'three-older-context-unmapped-and22-source-prose-reviewed-native-release-actual-pending',
        'note': 'These25 pending reviewed entries are not the full remaining shared/routes/player prose or raw-source scope.'}
    checkpoint = ('V992 source/prose-reviews22 battle/declaration alternatives1889-1910:13 proposed revisions and9 justified retentions.832 original object/table selections,4 null controls,45 actual-role-wrapper argument/UI cases,24 accept/cancel branch fragments and20 native complete faction-label getters pass. Named prompts use the full faction label directly;1895 restores effort encouragement;1902/1909 retain communicated threats;1907-1909 restore omitted meaning;obsolete full-width I and old authored alignment are removed from prose. Original player First Mate readiness differs from the separately observed opposing-leader2201-2208 control. Native fonts,dynamic post-substitution wrapping,registered integration and actual representative scenes remain pending. V987 stays current;1174 complete,1199 source/prose reviewed. Older750-752,remaining shared/routes/player prose/raw inventory,separate graphics/all18 plaques,Samwell header and later older-record re-audit remain open;full goal active.')
    ledger['latest_checkpoint'] = checkpoint
    ledger['battle_declaration_v992'] = {'status': '22-source-prose-reviewed-native-release-actual-pending',
        'native_message_IDs': list(IDS), 'manuscript': str(MANUSCRIPT), 'source_context_proof': str(CONTEXT),
        'proposed_revisions': 13, 'justified_retentions': 9, 'completed_entries_added': 0}
    ledger['research_checkpoints'].append({'id': 'V992-battle-declaration22-source-prose', 'proof': str(CONTEXT),
        'manuscript': str(MANUSCRIPT), 'new_source_prose_reviews': 22, 'completed_entries_added': 0,
        'previous_goal_turn_classification': 'progress:current V987 repaired user shop676/677 preservation freshly verified against earlier corrected actual capture',
        'this_goal_turn_classification': 'progress:22 source/prose reviews with original speaker,complete faction argument,cancel/accept and opponent-control evidence',
        'full_goal_complete': False})
    previous = read(ROOT/'editorial_ledger_before_source_review.json')
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values()) == 1199 and ledger['records_editorially_completed'] == 1174
    for key in ('current_integrated_candidate', 'unresolved_graphics_work', 'older_record_reaudit_after_full_editorial_goal', 'raw_source_coverage_revisit', 'approved_name_roles', 'formatting_watchlist'):
        assert ledger[key] == previous[key]
    save(ledger_path, ledger)
    doc = Path('docs/battle_declaration_v992_source_review.md')
    assert not doc.exists()
    with doc.open('x', encoding='utf-8') as f:
        f.write('# V992: battle readiness and declaration-of-war English review\n\n'+checkpoint+'\n\n')
        for row in rows:
            f.write(f"## COMMON {row['message_id']}: {row['speaker']}\n\n"+row['source_Japanese'].replace('\n', ' ')+'\n\n'+row['source_meaning']+'\n\n'+row['english']+'\n\n'+row['localization_note']+'\n\n')
    for p in map(Path, ('docs/translation_progress.md', 'docs/editorial_review_goal.md', 'docs/todo.md', 'docs/known_issues.md')):
        with p.open('a', encoding='utf-8') as f:
            f.write('\n\n## V992: battle/declaration source review\n\n'+checkpoint+' See [V992 source review](battle_declaration_v992_source_review.md).\n')
    archive = Path('E:/Rota Nova translations/Editorial review/V992 Battle declaration source review')
    assert not archive.exists()
    files = [MANUSCRIPT, CONTEXT, supplement, Path(__file__), doc, ledger_path,
             Path('scripts/research_battle_declaration_context_v991.py'), Path('scripts/research_battle_declaration_context_v991b.py'),
             Path('scripts/research_battle_declaration_context_v991c.py'),
             Path('work/analysis/battle_declaration_v991/successor_provenance.json'), Path('work/analysis/battle_declaration_v991b/successor_provenance.json')]
    copied = []
    for source_path in files:
        target = archive/source_path.absolute().relative_to(Path.cwd())
        target.parent.mkdir(parents=True, exist_ok=True)
        assert not target.exists()
        copy2(source_path, target)
        assert source_path.read_bytes() == target.read_bytes()
        copied.append({'source': str(source_path), 'archive': str(target), 'sha256': sha(target.read_bytes())})
    save(ROOT/'archive_manifest.json', {'files': copied, 'all_hashes_verified': True, 'completed_entries_added': 0})
    print('22 source/prose reviews:13 revisions,9 retentions.1174 complete,1199 source/prose. Native post-substitution layout,release and actual scenes remain pending;goal active.')


if __name__ == '__main__':
    main()
