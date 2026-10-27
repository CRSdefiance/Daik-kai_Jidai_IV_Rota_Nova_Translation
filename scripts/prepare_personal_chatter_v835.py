"""Clean-source review and original actor-specific Deck Personnel selection."""

import struct
import unicodedata
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_dialogue_editorial import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/personal_chatter_v835')
ROM = Path('out/all_routes_combined_v834_candidate.nds')
MANUSCRIPT = Path('translations/personal_chatter_editorial_manuscript_v1.json')
RAM = Path('work/emulation_v193/refit_dialogue_v834_helper_after/frame_003200_arm9_ram.bin')
BASE = 0x02000000

# Wording is authored from the Japanese, not inherited positions or allocation.
# The formatting gate remains false until this distinct native UI is mapped.
PROSE = {
    1361: ("Mm, what a lovely sound!", 'Approves the pleasant musical tone with a gentle affirmative response.', 'Use a soft English response and preserve appreciation of the sound;no invented instrument.', 'revise'),
    1362: ("...That's quite well done...", 'Quietly judges the result to be quite good.', 'Retain the natural understated appraisal and deliberate pauses;the source does not name the object.', 'retain'),
    1363: ('Zzz... Honestly, Camille... Zzz...', 'Talks in her sleep,exasperatedly addressing Camille between snores.', 'Retain the natural half-asleep address and approved Camille spelling;do not invent a dream event or relationship.', 'retain'),
    1364: ('Good tea.', 'Briefly compliments the tea.', 'This short conversational fragment is natural and faithful;expansion would add no meaning.', 'retain'),
    1365: ("Mm-hmm. That's a good story.", 'Repeatedly acknowledges what is being said and calls it a good story or account.', 'Restore the independent affirmative comment. The old lookout sentence is unrelated to this actor-specific source.', 'revise'),
    1366: ('99, 100, 101... Hrrrgh! 102...', 'Counts99,100,101,then strains audibly to reach102.', 'Preserve all four counts and the exertion in natural English vocalization. Digits reflect the original counting style;no exercise type is invented.', 'revise'),
    1367: ("Ahhh! That's the stuff!", 'A long satisfied exhalation followed by a slurred cry that something tastes good.', 'Localize the exhalation and slurred delight idiomatically;do not transliterate the comic pronunciation as an English proper word or invent a named drink.', 'revise'),
    1368: ('La la la! Dancing makes me happy!', 'Musical vocalization followed by happiness while dancing.', 'Render the four musical notes as natural humming syllables,keeping the cheerful dancing statement.', 'revise'),
    1369: ('Hmm... Ancient lore... I see...', 'Muses over something ancient,then signals understanding.', 'Keep the ancient subject broad as lore;do not invent a civilization,artifact or historical claim. Restore the source realization.', 'revise'),
    1370: ("Looking up at the sky like this... It's so relaxing.", 'Says that gazing at the sky like this brings relief or calm.', 'Restore the act of looking at the sky and the personal sense of calm in a natural reflective voice.', 'revise'),
    1371: ('A warrior trains every day.', 'Constant training;for a warrior,every day is practice.', 'Retain the concise natural English formulation:daily training expresses the repeated source idea without adding facts.', 'retain'),
    1372: ('Nice rod! Time for a big catch.', 'Praises the fishing rod and resolves to catch something big.', 'Retain the natural enthusiastic wording;the catch remains an intention,not a reported result.', 'retain'),
    1373: ('My blade shines beautifully, as always...', 'Admires the fine shine of his own sword,as usual.', 'Restore the source habitual as-always observation while retaining blade as natural English for his sword.', 'revise'),
    1374: ("There! Turned out well, wouldn't you say?", 'Emphatically presents a good result and asks for agreement.', 'Keep the confident presentation and rhetorical invitation to admire it;do not invent what he made.', 'revise'),
    1375: ('Mmm, delicious! Sneaking a bite is the best!', 'Says it tastes good and celebrates secretly sampling the food.', 'Use sneaking a bite for tsumamigui rather than the unnatural secret taste;retain the playful delight.', 'revise'),
    1376: ("Tch. The sea air's ruining my hair.", 'Clicks his tongue in annoyance because the sea breeze is damaging his hair.', 'Preserve the irritation and ongoing hair complaint in natural speech.', 'revise'),
    1377: ('Swinging a sword calms me.', 'Says he feels calm when swinging a sword.', 'Retain the complete natural sentence;no battle or enemy is implied by the source.', 'retain'),
    1378: ("A man's fists do the talking. Gotta keep training!", 'Boasts that a man competes with his fists and must keep training.', 'Use a familiar macho English idiom for the fist boast and restore the missing constant-training resolve.', 'revise'),
    1379: ("If I mix this medicine in... Ah, so that's it!", 'Considers mixing in this medicine,then reacts with discovery.', 'Restore the medicine and conditional experiment;do not invent ingredients or a medical effect.', 'revise'),
    1380: ('Zzz... Mmph... (Nods off.) Zzz...', 'Snores,mumbles sleepily,nods off,and snores again.', 'Retain the sleepy vocalization and explicit parenthetical nod that the old English omitted.', 'revise'),
    1381: ('I wanna gamble.', 'Roughly or casually expresses a desire to gamble.', 'Use a casual wish rather than Gotta,which suggests an obligation absent from the source.', 'revise'),
    1382: ("Stronger... I'm going to keep getting stronger...", 'Resolves to grow stronger and stronger without limit.', 'Preserve the repeated determined stronger and ongoing resolve in natural speech.', 'revise'),
    1383: ('Zzz... Delicious... Zzz.', 'Murmurs that something tastes good while sleeping.', 'Retain the natural sleep-talk and snores;do not invent a dream meal.', 'retain'),
    1384: ('The color, the sheen, the balance... A masterpiece.', 'Appraises color or luster and balance,then calls it a masterpiece.', 'Restore the explicit masterpiece appraisal and sheen;the object remains unspecified,as in the source.', 'revise'),
    1385: ('Water for you... The flowers are so happy...', 'Offers water and says the flowers are very happy,in simple hesitant speech.', 'Keep the gentle simple phrases and personification of flowers;use understandable English without caricaturing her limited Japanese.', 'revise'),
}


def reference(e):
    return {k: getattr(e, k) for k in ('message_id', 'block', 'table_offset', 'block_offset', 'copy_end', 'record_index', 'start', 'end')}


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert not MANUSCRIPT.exists()
    current, clean, canonical = map(NdsImage.open, (ROM, 'work/clean.nds', 'out/raphael_natural_v2_accepted_base.nds'))
    arm, source_arm = current.read_file('/__arm9__.bin'), clean.read_file('/__arm9__.bin')
    assert sha(ROM.read_bytes()) == '16a66ac0e5e95623f5e5b4a3a5d61fe4416481539ecbd7e390dd5794a170080a'
    assert sha(Path('work/clean.nds').read_bytes()) == 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    jp = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'), source_arm)
    before = current_entries(current.read_file('/COMMON/MESFILE.DK4'), arm)
    accepted = common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'), canonical.read_file('/__arm9__.bin'), clean=False)
    source_spans = [(0x12104, 0x12920), (0x15334, 0x154E8), (0x5528C, 0x552A4)]
    for lo, hi in source_spans:
        assert source_arm[lo:hi] == arm[lo:hi]
    assert struct.unpack_from('<I', source_arm, 0x122A0)[0] == 1361
    report = read(RAM.parent / 'capture_report.json')
    snapshot = next(r for r in report['read_only_capture_RAM_snapshots'] if r['frame'] == 3200)
    raw = RAM.read_bytes()
    assert snapshot['read_only_export'] and sha(raw) == snapshot['sha256'] and len(raw) == 0x400000
    # This frame predates the earlier refit assignment fixture at the same pause.
    u = machine(arm)
    u.mem_write(BASE, raw)
    def get(fn, args=()):
        call(u, fn, args)
        return u.reg_read(UC_ARM_REG_R0)
    actors, hero = get(0xCB184), get(0x7F244)
    names = []
    for actor in range(25):
        obj = actors + 0x19E4 if actor == hero else actors + 4 + actor * 32
        table = struct.unpack('<I', u.mem_read(obj, 4))[0]
        fn = struct.unpack('<I', u.mem_read(table + 0x20, 4))[0] - BASE
        pointer = get(fn, (obj,))
        native = bytes(u.mem_read(pointer, 80)).split(b'\0')[0]
        name = unicodedata.normalize('NFKC', native.decode('cp932'))
        names.append({'actor_ID': actor, 'name': name, 'native_name_hex': native.hex(), 'native_name_pointer': pointer})
    assert names[4]['name'] == 'Janus' and names[5]['name'] == 'Claudio'
    assert names[9]['name'] == 'Camille' and names[20]['name'] == 'Fernando'
    selected = []
    def intercept(cpu, pc, size, unused):
        selected.append(cpu.reg_read(UC_ARM_REG_R0))
        cpu.reg_write(UC_ARM_REG_R0, 0x02450000)
        cpu.reg_write(UC_ARM_REG_PC, cpu.reg_read(UC_ARM_REG_LR))
    hook = u.hook_add(UC_HOOK_CODE, intercept, begin=BASE + 0x5528C, end=BASE + 0x5528C)
    selectors = []
    try:
        for actor in range(25):
            selected.clear()
            result = get(0x12104, (actor, 3))
            assert selected == [1361 + actor] and result == 0x02450000
            selectors.append({'actor_ID': actor, 'name': names[actor]['name'], 'parameter': 3,
                              'selected_native_message_ID': selected[0],
                              'original_selector_complete_ABI_call': True,
                              'COMMON_loader_intercepted_only_after_ID_selection': True})
    finally:
        u.hook_del(hook)
    dis = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    listings = {f'{lo:06X}-{hi:06X}': [f'{i.address:08X} {i.mnemonic} {i.op_str}' for i in dis.disasm(source_arm[lo:hi], BASE + lo)]
                for lo, hi in source_spans}
    context_path = ROOT / 'native_context.json'
    save(context_path, {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'source_code_spans_byte_exact': [[lo, hi, sha(arm[lo:hi])] for lo, hi in source_spans],
        'current_ARM9_sha256': sha(arm), 'source_ARM9_sha256': sha(source_arm),
        'actual_read_only_RAM': snapshot, 'actor_names': names, 'all25_native_actor_specific_selections': selectors,
        'original_selector': BASE + 0x12104, 'original_numeric_base_literal': 1361,
        'original_Deck_Personnel_consumer_return': BASE + 0x1547C,
        'original_actor_macro_expansion': BASE + 0x53914,
        'original_embedded_draw': BASE + 0x154CC, 'source_embedded_draw_Y': 60,
        'source_embedded_draw_takes_same_speaker_actor_object': True,
        'source_disassembly': listings,
        'scope': 'Native actor-specific parameter3 branch and original Deck Personnel draw binding. COMMON copy intercepted after ID selection;not actual UI activation,eligibility proof for every actor,or revised font/layout approval.',
        'parameter3_exact_UI_label_and_available_actor_activation_pending': True,
        'Fernando_name_is_fullwidth_F_plus_ernando_not_a_dropped_letter': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    packet = []
    for n in range(1357, 1391):
        packet.append({'message_id': n, 'source_Japanese': jp[n].text.decode('cp932'), 'source_hex': jp[n].text.hex(),
                       'source_reference': reference(jp[n]), 'current_hex': before[n].text.hex(),
                       'current_English': before[n].text.decode('cp932'), 'current_reference': reference(before[n])})
    save(ROOT / 'source_context_packet.json', {'neighbors1357_1390': packet,
        'independent_message_IDs_not_a_sequential_conversation': True,
        'canonical1365_1366_already_contain_unrelated_split_lookout_sentence': [accepted[n].text.hex() for n in (1365, 1366)],
        'no_new_V834_regression_inferred_from_inherited_content': True})
    rows = []
    for n, (english, gloss, note, decision) in PROSE.items():
        assert english == ' '.join(english.split()) and english.isascii()
        assert all(c not in english for c in ('%', '{', '}', '\n'))
        actor = n - 1361
        if decision == 'retain':
            assert english == before[n].text.decode('ascii').strip()
        rows.append({'id': f'COMMON_MESSAGE_{n}', 'message_id': n, 'actor_ID': actor,
            'speaker': names[actor]['name'], 'context': 'Independent actor-specific Deck Personnel comment,original selector12104 parameter3. The following storage record belongs to a different actor;not a spoken continuation.',
            'source_Japanese': jp[n].text.decode('cp932'), 'source_hex': jp[n].text.hex(), 'source_reference': reference(jp[n]),
            'canonical_source_hex': accepted[n].text.hex(), 'current_reference': reference(before[n]),
            'current_text_hex': before[n].text.hex(), 'current_English': before[n].text.decode('cp932'),
            'english': english, 'source_meaning': gloss, 'localization_note': note, 'editorial_decision': decision,
            'native_argument_count': 0, 'review': {'source': True, 'context': True, 'localization': True, 'naturalness': True, 'formatting': False}})
    save(MANUSCRIPT, {'format': 'dk4-natural-dialogue-source-manuscript-v2', 'translation_policy': 'natural-dialogue-v2',
        'target_locale': 'en-US', 'encoder': 'COMMON-native-consumer-pending',
        'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
        'status': 'source-prose-reviewed-native-UI-formatting-and-integration-pending',
        'file_path': '/COMMON/MESFILE.DK4', 'source_clean_ROM_sha256': sha(Path('work/clean.nds').read_bytes()),
        'current_ROM': str(ROM), 'current_ROM_sha256': sha(ROM.read_bytes()),
        'current_COMMON_sha256': sha(current.read_file('/COMMON/MESFILE.DK4')), 'current_ARM9_sha256': sha(arm),
        'native_context_proof': str(context_path), 'native_context_proof_sha256': sha(context_path.read_bytes()),
        'layout_authoring': 'Single logical paragraphs only;embedded Deck consumer must be mapped. Do not apply portrait-modal bounds or author manual line positions.',
        'records': rows, 'whole_batch_completion_credit': False,
        'remaining_gates': ['Exact native UI parameter3 label/activation', 'embedded text rectangle and automatic wrap/font coverage',
                            'registered combined ROM and exact patch', 'actual corrected1365/1366 sample and ordinary transitions', 'progress completion and archive'],
        'full_goal_complete': False})
    print('V835:25 independent actor comments reviewed;18 proposed revisions,7 retentions.1365/1366 wrong inherited lookout fragments identified. Native UI formatting/integration remain pending.', flush=True)


if __name__ == '__main__':
    main()
