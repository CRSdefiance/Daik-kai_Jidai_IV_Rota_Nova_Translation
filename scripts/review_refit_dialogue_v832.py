"""Natural English draft from clean Japanese and proven Refit context."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.context_refit_dialogue_v832 import IDS, ROM, ROOT
from scripts.verify_village_wrap_v608 import read, save

MANUSCRIPT = Path('translations/refit_dialogue_editorial_manuscript_v1.json')
PROSE = {
    1256: "Admiral, I'll help with the refit too.",
    1257: "Admiral, I can help with the refit too!",
    1258: 'Admiral, let me help with the refit.',
    1259: "I'll lend a hand too, Admiral.",
    1260: "Admiral, I'll lend a hand with the refit too.",
    1261: "Admiral, I'll help refit her too!",
    1262: 'Admiral, I could help with the refit too...',
    1263: "With their help, I'll knock %s%% off the refit cost. Let's see...",
    1264: 'Which ship would you like to rename?',
    1265: 'Give it any name you like.',
    1266: 'Which ship would you like to refit?',
    1267: 'The refit will take %s.',
}
GLOSSES = {
    1256: 'A polite companion addresses the Admiral and offers to help with the refit as well.',
    1257: 'A familiar companion addresses the Admiral and says they will help with the refit too. IC is the original character-dependent first-person pronoun.',
    1258: 'The companion addresses the Admiral and asks to be allowed to help with the refit.',
    1259: 'A rough, confident companion addresses the Admiral and offers to lend a hand too.',
    1260: 'An older-sounding companion addresses the Admiral and offers to lend a hand with the refit.',
    1261: 'A youthful, familiar companion addresses the Admiral and offers to help with the refit too.',
    1262: 'A hesitant companion addresses the Admiral and trails off while offering to help with the refit.',
    1263: 'The local shipwright says that with that person helping, the refit price will be reduced by the supplied percentage, then begins to calculate the resulting amount.',
    1264: 'The local shipwright asks which ship the player wants to rename.',
    1265: 'After a ship is selected for renaming, the shipwright invites the player to choose any name they like.',
    1266: 'The local shipwright asks which ship the player wants to refit.',
    1267: 'The local shipwright asks the player to wait the supplied number of days for completion of the refit.',
}
NOTES = {
    1256: 'Restore the source Admiral address and the explicit refit offer in a polite, matter-of-fact voice. Native class1 also reaches this line through the original first-valid-entry fallback.',
    1257: 'IC supplies a first-person pronoun, not an actor name; use grammatical English I. Keep the address, enthusiasm and offer to help too. Current literal-I guard and the new queued consumer still require complete native rendering checks.',
    1258: 'Retain the request to be allowed to help, rather than flattening every voice to a statement. Restore Admiral without inventing a relationship.',
    1259: 'Lend a hand preserves the informal confident offer and too. Keep Admiral;do not add profanity or an invented technical specialty.',
    1260: 'Use a measured conversational offer for the older voice;no caricatured dialect, age label or kinship term is added.',
    1261: 'Use an eager, familiar offer. Her refers to the ship, the established nautical usage;it does not assign a gender to the companion.',
    1262: 'Restore Admiral and the refit context while preserving the hesitant unfinished offer. The ellipsis belongs to the source intent;no explicit layout break is authored.',
    1263: 'Keep the percentage discount and the calculation bridge missing from the current English. Lets see naturally expresses the source trailing calculation. One native number argument remains;%% is a literal percent for this COMMON printf consumer,not a story conversion.',
    1264: 'Use a complete natural question identifying the ship to rename. It is distinct from the following invitation to enter a name.',
    1265: 'Retain the clear natural invitation to choose any desired name. The formatter must normalize old leading alignment spaces;wording retention does not approve their layout.',
    1266: 'Use a complete conversational question instead of the current Which ship to refit fragment. Existing V831 frame20000 proves the original Shipwright context.',
    1267: 'Preserve refit completion time and all days. The proposed single %s must receive the native number plus singular/plural day unit through a narrowly scoped original-return adapter. Do not ship it with the current bare-number argument;all256 source duration bytes are mapped and the unit/runtime gate remains pending.',
}


def main():
    assert not MANUSCRIPT.exists()
    context, packet = read(ROOT / 'native_context.json'), read(ROOT / 'source_context_packet.json')
    assert context['candidate_sha256'] == packet['current_ROM_sha256'] == sha(ROM.read_bytes())
    neighbors = {r['message_id']: r for r in packet['neighbors']}
    canonical = NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    accepted = common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'), canonical.read_file('/__arm9__.bin'), clean=False)
    records = []
    voice = {1256: [0, 1], 1257: [2], 1258: [3], 1259: [4], 1260: [5], 1261: [6], 1262: [7]}
    for i in IDS:
        p = neighbors[i]
        records.append({
            'id': f'COMMON_MESSAGE_{i}', 'message_id': i, 'source_hex': p['source_hex'],
            'source_Japanese': p['Japanese'], 'canonical_source_hex': accepted[i].text.hex(),
            'current_text_hex': p['current_hex'], 'current_English': p['current_English'],
            'source_reference': p['source_reference'], 'current_reference': p['current_reference'],
            'english': PROSE[i], 'source_meaning': GLOSSES[i], 'localization_note': NOTES[i],
            'speaker': 'Assigned Shipwright companion,original voice class' + str(voice[i]) if i in voice else 'Local town Shipwright',
            'context': ('Original role13 refit assistance:assigned Shipwright,ability at least25,positive refit cost. '
                        'Native helper voice offer precedes the local shipwright percentage discount and a separate final-price confirmation.'
                        if i <= 1263 else 'Original Shipwright rename/refit interaction;renaming selection and name entry are distinct,while1267 reports the refit completion delay.'),
            'source_voice_classes': voice.get(i, []), 'native_argument_count': 1 if i in (1263, 1267) else 0,
            'argument_contract': ('Original full-width percentage number followed by the literal percent emitted by %%.' if i == 1263
                                  else 'REQUIRED PENDING:original duration number plus grammatically singular/plural day unit.' if i == 1267 else 'No runtime substitutions.'),
            'editorial_decision': 'retain' if i == 1265 else 'revise',
            'review': {'source': True, 'context': True, 'localization': True, 'naturalness': True, 'formatting': False}})
    save(MANUSCRIPT, {'format': 'dk4-refit-dialogue-editorial-manuscript-v1',
                      'translation_policy': 'natural-dialogue-v2', 'target_locale': 'en-US',
                      'encoder': 'dialogue-relocatable-v1',
                      'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
                      'status': 'source-context-and-prose-reviewed-format-runtime-integration-actual-scene-pending',
                      'file_path': '/COMMON/MESFILE.DK4',
                      'source_clean_ROM_sha256': packet['source_ROM_sha256'],
                      'current_ROM': str(ROM), 'current_ROM_sha256': sha(ROM.read_bytes()),
                      'native_context_proof': str(ROOT / 'native_context.json'),
                      'native_context_proof_sha256': sha((ROOT / 'native_context.json').read_bytes()),
                      'layout_authoring': 'One natural paragraph. No manual breaks or indentation. Exact shared paragraph and queued-role consumers require native verification;duration1267 requires a scoped number-plus-unit adapter before production.',
                      'records': records, 'full_goal_complete': False})
    save(ROOT / 'source_review.json', {
        'all12_individual_source_meanings_contexts_and_prose_reviewed': True,
        'proposed_revisions': 11, 'justified_retained_wordings': 1,
        'source_control_and_substitution_decisions': ['1257 IC is first-person pronoun',
            '1263 one native percentage argument plus literal percent', '1267 one native duration argument;day/days adapter required'],
        'no_completed_entry_credit': True, 'not_a_production_batch': True,
        'consumer_gate_pending': 'Generate complete common portrait paragraphs after numeric expansion;preserve all existing literal ship-name handling and original role/table selection.',
        'current_ROM_unchanged': str(ROM), 'manuscript_sha256': sha(MANUSCRIPT.read_bytes()),
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V832 all12 source/context/prose reviewed:11 revisions,1 retention. Duration units/native formatting and release remain pending.', flush=True)


if __name__ == '__main__':
    main()
