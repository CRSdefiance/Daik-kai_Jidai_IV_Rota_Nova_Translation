"""Bind shared setup and equipment prose to the clean and registered native records."""

from collections import defaultdict
from hashlib import sha256
from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.register_captain_biographies_v1 import RELEASE
from scripts.register_shared_notices_v1 import CONTEXT, LEDGER
from scripts.review_literal_notice_callers_v1 import CALLS
from scripts.seal_shared_text_source_v1 import ARM, CLEAN, COMMON, reference


BASE = 0x02000000
OUTPUT = Path('translations/editorial_checkpoints/SharedText_20261110_v1/setup_save_equipment_context_v1.json')
CATALOGUE = OUTPUT.with_name('contextual_comparison_pending_consumers.json')
DATA = {
    315: ("You can't change sailor assignments during battle!",
          "The player cannot reorganize the sailor assignments while in battle.",
          "Combat blocks crew assignment changes before applying any selection.",
          "The current refusal names the blocked action and gives its cause. The short, emphatic wording suits the system notice."),
    316: ("Save the ending data?",
          "The game asks whether to save the ending data.",
          "The original ending routine asks this after displaying the ending. Yes invokes the ending-data save; No skips it.",
          "Keep the direct Yes/No question and the distinction between ending data and ordinary saved progress. The DS prompt has no memory-card destination."),
    317: ("You can't change figureheads at sea.",
          "A ship's figurehead cannot be changed while at sea.",
          "The equipment command is refused at sea before any figurehead swap.",
          "Put the condition after the action so the warning reads naturally. Figureheads stays consistent with the equipment interface."),
    318: ("This is exhibition data. If you quit, you'll lose it. Quit anyway?",
          "This is fair or exhibition data. Suspending the game will lose it, and the player must confirm.",
          "The source describes a special data type and data-loss confirmation. Its relationship to the active DS Quit prompt remains unproven.",
          "Make the consequence and choice explicit and replace the full-width I. Keep exhibition data as the provisional source term until its mode is bound."),
    319: ("Quit the game?",
          "The game asks the player to confirm interrupting the current game.",
          "The in-game quit helper asks for confirmation when the original active-game flag is set. Its result belongs to the original caller.",
          "Use the normal American English article. The ordinary quit prompt carries no claim about saving or special exhibition data."),
    320: ("Who should equip it?",
          "The game asks which crew member should equip the selected item.",
          "The original chooser obtains the prompt with the direct COMMON getter and passes it to the crew selection list when a recipient has yet to be selected.",
          "Use an open question directed at the player. The two old leading spaces are handled by the chooser layout review."),
    321: ("%s equipped %s.",
          "The first named person equipped the second named item.",
          "A result notice after an equipment operation. Three original callers pass the actor name followed by the equipment name.",
          "The current actor-then-item wording is clear and matches the other success notices. Its current padding and the registered equipment wrapper belong to display review."),
    322: ("Removed %s.",
          "The named item was removed.",
          "The removal path supplies the figurehead name. For the Demon Figurehead, this notice precedes a separate breakage notice after the player confirms.",
          "Use a concise system result in the same voice as the other equipment messages. The one source argument remains the removed item."),
    323: ("Which ship should it go on?",
          "The game asks which ship should receive the selected equipment.",
          "The player is choosing a ship for the selected figurehead. The ship selection precedes the named equipment result.",
          "Replace the inverted menu shorthand with the natural follow-up question. The selected object is already in context."),
    324: ("The Demon Figurehead broke!",
          "The figurehead called Akuma no Zō broke as a result of the removal.",
          "This result follows the removal notice only on the original item 121 branch when the player chooses to force it off.",
          "Use Demon Figurehead, the current native item 121 name, in the same short, emphatic result."),
    325: ("The Demon Figurehead won't come off. Force it off?",
          "The figurehead called Akuma no Zō is difficult to remove. The game asks whether to force it off.",
          "The player has selected item 121 for removal. No cancels before removal. Yes continues into the separate removal and breakage messages.",
          "Use the catalog name Demon Figurehead and a natural contraction. Leave the later consequence to the follow-up notices."),
    326: ("You don't have any items.",
          "The player has no items in the relevant inventory.",
          "The item-list command receives a zero count before opening the ordinary inventory list.",
          "Keep this clear statement of an empty inventory. It is distinct from having no eligible equipment."),
    327: ("%s equipped %s.",
          "The first named recipient equipped the second named item.",
          "This success notice follows the ship-target equipment path. The original caller supplies the recipient first and the equipment item second.",
          "The current wording preserves the argument order and matches the analogous crew result. Keep its separate selector and wrapping path."),
    328: ("You have nothing you can equip.",
          "The player has no items that can be equipped.",
          "The equipment list is empty after filtering for eligible items. This is a different branch from the ordinary inventory count.",
          "Use a natural phrase in place of equippable and keep the eligibility distinction."),
    329: ("%s removed %s.",
          "The first named recipient removed the second named item.",
          "The ordinary removal result follows the player choosing an equipped item. The native call supplies the owner name, then the item name.",
          "Keep the actor-then-item construction and the result tense. The current break needs to be generated after seeing the actual name lengths."),
}
LEGACY_CONTEXT = {
    98: 'The clean catalogue distinguishes no acquired items from no discovered ruins. DS notices 326 and 328 are separate inventory and equipment conditions.',
    99: 'The source concerns discovered ruins. A caller for this particular message ID is still needed.',
    100: 'The source instructs the player to select exactly three strengths. The actual DS chooser must be checked before assigning this prompt to it.',
    101: 'The source confirms three selected skills in order. Any future change must preserve all three string substitutions.',
    102: 'The source describes music and sound-effects volume. This is distinct from the DS Sailing Help and Reports prompts with independent ARM9 literals.',
    103: 'The source asks for a birthday. A birthday field on screen alone does not establish that it consumes this COMMON message.',
    104: 'The separate ARM9 chooser description for Rafael has been localized. This legacy COMMON copy currently displays unrelated square text if read.',
    105: 'The separate ARM9 chooser description for Hodram has been localized. This legacy COMMON copy currently contains unrelated square text.',
    106: 'The separate ARM9 chooser description for Lil has been localized. This legacy COMMON copy currently contains unrelated square text.',
    107: 'The separate ARM9 chooser description for Maria has been localized. This legacy COMMON copy currently contains unrelated save text.',
    108: 'This start-anyway prompt specifies four free blocks for game data. Keep its source branch distinct from system data and combined data.',
    109: 'This start-anyway prompt specifies one free block for system data.',
    110: 'This start-anyway prompt specifies five free blocks for the data to be saved.',
    111: 'The source distinguishes absent game data from corruption. The text reads naturally if this consumer is confirmed.',
    112: 'Previously reviewed active system-data absence notice. Two direct callers remain bound.',
    113: 'The stored start question replaces a four-block game-save failure in error. The source has no decision about starting.',
    114: 'The stored start question replaces a one-block system-save failure in error. The source has no decision about starting.',
    115: 'This source branch specifies five free blocks and gives no start prompt.',
    116: 'The source names a memory card and controller. Keep these terms with the legacy branch pending DS reachability evidence.',
    117: 'The catalogue entry reports game-data corruption. The qualified DS slot-specific error uses a separate ARM9 suffix and retains the slot number.',
    118: 'Previously reviewed active corruption notice. The original branch displays 122 immediately afterward.',
    119: 'The source explicitly names the memory card. The independent DS ending-save call at 0203E2F8 selects 316 with no memory-card destination.',
    120: 'Previously reviewed active setup confirmation selected at 0209DFF4.',
    121: 'Previously reviewed active start confirmation. The current bytes already restore the standalone question.',
    122: 'Previously reviewed active system-data load failure with default startup. The current bytes already restore the complete explanation.',
    123: 'Previously reviewed active system-data failure without a default-start explanation.',
    124: 'The source allows memory-card initialization to be deferred until saving and asks whether to start. DS call ownership remains pending.',
}


def callers(clean_arm, current_arm, inventory):
    result = defaultdict(list)
    disassemble = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    for row in inventory['calls']:
        number = row['message_id']
        if number not in DATA and number not in LEGACY_CONTEXT:
            continue
        start = row['file_offset'] - 16
        end = row['file_offset'] + 12
        assert row['component'] == 'arm9'
        raw = clean_arm[start:end]
        assert raw == current_arm[start:end], (number, hex(BASE + start))
        decoded = list(disassemble.disasm(raw, BASE + start))
        call = next(instruction for instruction in decoded if instruction.address == row['runtime_address'])
        assert call.mnemonic == 'bl' and int(call.op_str.lstrip('#'), 16) == row['target']
        result[number].append(dict(call=row['runtime_address'], target=row['target'],
            argument_register=row['argument_register'], source_current_equal=True, code_start=BASE + start,
            exact_hex=raw.hex(), instructions=[f'{i.address:08X} {i.mnemonic} {i.op_str}'.rstrip() for i in decoded]))
    return result


def main():
    release = load(RELEASE)
    assert digest(CLEAN) == release['clean_input_sha256']
    assert digest(release['candidate']) == release['candidate_sha256']
    clean = NdsImage.open(CLEAN)
    current = NdsImage.open(release['candidate'])
    clean_arm, arm = clean.read_file(ARM), current.read_file(ARM)
    common = current.read_file(COMMON)
    assert sha256(arm).hexdigest() == release['target_ARM9_sha256']
    assert sha256(common).hexdigest() == release['target_COMMON_sha256']
    source = common_message_entries(clean.read_file(COMMON), clean_arm)
    previous = owned_entries(common, arm, sha256(arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest())
    known = load(CALLS)
    assert known['source_rom_sha256'] == release['clean_input_sha256']
    bindings = callers(clean_arm, arm, known)
    ctx = load(LEDGER)
    assert ctx['current_integrated_candidate']['sha256'] == release['candidate_sha256']
    completed = {row['id'] for row in ctx[CONTEXT]['integrated_record_keys'] if row['file_path'] == COMMON}
    historical = {row['message_ID']: row for row in load(CATALOGUE)['records']}

    def exact_row(n):
        jp, en = source[n], previous[n]
        return dict(id=f'COMMON_MESSAGE_{n}', file_path=COMMON, message_ID=n,
            source_reference=reference(jp), source_hex=jp.text.hex(), clean_Japanese=jp.text.decode('cp932'),
            current_reference=reference(en), current_hex=en.text.hex(), current_English=en.text.decode('cp932'),
            already_credited=f'COMMON_MESSAGE_{n}' in completed, native_callers=bindings[n], new_credit=0)

    legacy = []
    for n, context in LEGACY_CONTEXT.items():
        row = exact_row(n)
        assert historical[n]['source_hex'] == row['source_hex']
        assert row['already_credited'] == (n in (112, 118, 120, 121, 122, 123))
        legacy.append(row | dict(context=context, direct_consumer_found=bool(bindings[n]),
            no_proof_of_global_unreachability=True, independent_English=historical[n]['independent_English']))

    records = []
    for n, (english, gloss, context, note) in DATA.items():
        row = exact_row(n)
        assert not row['already_credited']
        assert bool(bindings[n]) == (n != 318)
        placeholders = row['clean_Japanese'].count('%s')
        assert placeholders == english.count('%s') == row['current_English'].count('%s')
        logical_before = ' '.join(row['current_English'].split())
        records.append(row | dict(speaker='System', english=english, source_meaning=gloss, context=context,
            localization_note=note, native_substitution_count=placeholders,
            decision='retention' if english == logical_before else 'revision',
            review=dict(source=True, context=n != 318, localization=True, naturalness=True, formatting=False)))
    save(OUTPUT, dict(translation_policy='natural-dialogue-v2', target_locale='en-US', encoder='dialogue-relocatable-v1',
        review_gates=['source', 'context', 'localization', 'naturalness', 'formatting'], records=records,
        legacy_setup_and_save_records=legacy, registered_predecessor=release['candidate'],
        registered_predecessor_sha256=release['candidate_sha256'], clean_ROM_sha256=release['clean_input_sha256'],
        exact_source_current_ARM9_direct_call_windows_verified=sum(len(rows) for rows in bindings.values()),
        stored_mismatches_are_not_observed_gameplay=True, new_completion_credit=0, full_goal_complete=False,
        evidence={str(path): digest(path) for path in (RELEASE, CALLS, CATALOGUE, Path(__file__))}))
    print('15 contextual drafts, 14 with exact active caller bindings. 27 setup and save records classified by current evidence.')


if __name__ == '__main__':
    main()
