"""Read and gloss all37 clean B171 speeches before predecessor English exposure."""
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B171_clean_context_v4309')
INVENTORY = Path('work/analysis/lil_B161_B180_clean_scope_v3910/complete_clean_B161_B180_next_exchange_inventory.json')
CONTEXT = '''Read B171 as one complete37-speech nocturnal/dreamlike visitation and morning follow-up. The first speaker has selector51hex/81decimal,not a literal Q to leave in or strip from prose. Bind the current original nameplate/catalogue before choosing an approved English spelling for source サンヒョン. The clean source introduces this person as Yifa's 兄弟子,a senior fellow disciple/student in the same training tradition. This is not proof of biological brotherhood,her teacher's identity,a parental role,an official rank or a specific age. His highly deferential,old-fashioned speech contrasts with Lil's sleepy bluntness and Yifa's bright,casual voice. Preserve respectful intent through natural formal English rather than inventing a feudal title from 殿 or Japanese grammar. His faint opening honorific and repeated FI address lead into Lil's groggy response. Keep FI exactly and the opening pauses;invent no snoring,injury,attack or romance.
The visitor apologizes for the sudden intrusion,says he is not suspicious,introduces himself as Yifa's senior fellow disciple and explains he came to greet the person taking care of her. He blames his own insufficient guidance for her unrestrained upbringing. He condemns her leaving training and the mountain without their teacher's permission,and even leaving their country. This scene newly states that people of their country are forbidden to travel abroad,and that Yifa apparently does not know this. Do not name the country,law,religion,school,monarch,era or penalty. These new B171 facts must not be retrospectively inserted into B170,whose speaker gave a different limited account. Lil asks whether he means to bring Yifa back. He says he cannot:violating the national prohibition is serious and Yifa has been expelled from their dojo/training school. Preserve expulsion and the school/training relationship,not an invented death sentence,arrest,bounty or loss of supernatural ability. His statement that he has no remaining tie to her is the formal break he then qualifies emotionally.
He explains they grew up together from childhood like actual brother and sister. Preserve the explicit simile and close bond without turning it into biological kinship or a romance. He worries that an immature girl like her will behave badly before others. His request is that Lil guide her so she does not stray from the proper path,and,if possible,remind her to keep practicing even away from the mountain and obey their teacher's instructions. He closes by entrusting Yifa to Lil's care. He is not requesting money,employment,guardianship papers,reinstatement,revenge or a named job. Source references to the teacher give no gender or name. Keep the visitor's self-blame,formal severance,affection,worry and tentative appeal as his perspective;do not flatten these into a hostile demand or narrator certainty.
After a presentation transition,Lil wonders whether that was a dream and says it felt strangely real. Yifa arrives with a loud cheerful good morning and an unfinished call to leave quickly,then reacts wordlessly and senses her senior fellow disciple's presence. Lil asks whether that person's name is サンヒョン. Yifa's disbelief and familiar 兄さん address express their established siblinglike bond,not a new biological relationship. Once the name is bound,use a natural familiar address without inventing a rank. Lil explains that the man in her dream gave that name and called himself Yifa's senior fellow disciple. Yifa softly repeats the dream idea and his name,then reasons that because he cannot come down the mountain,he used 術 to visit. This is her explanation,not independent proof of a literal ghost,astral projection,telepathy,named spell or physical travel exemption. Bind the reviewed Taoist-arts terminology from B170;keep both the mountain restriction and the use of arts without supplying new mechanics.
Lil remains baffled by these arts and then remembers the training/teacher message. Preserve exactly what she relays:continue training away from the mountain and obey the teacher. She does not tell Yifa about the national travel ban or expulsion in this follow-up. Yifa responds with a fond little laugh about his perpetual worrying. After Lil's pause/question,Yifa resolves to train hard because she would hate to disappoint the named senior disciple. Lil sharply reminds her that work aboard ship comes first and training second;Yifa breezily says she understands. Preserve this affectionate-to-practical comic turn,not a ban on practice or an invented job. All37 speeches are glossed before predecessor English comparison. Source bytes retain45 commands:37 progressive speeches/eight nonrelative leaves,selectors02/19/51,FI1,FA0/FO0,no FE,typed choice,relative site,membership predicate,2000 pause or A000. Retain6000,4500,4621,61FF,6325,C200 and both ends2112/2116. Their current consumers,presentation effects,entry conditions,names,layout and representative behavior still need binding. This clean pass adds zero review/completion credit. Every wider editorial family remains open;graphics and the later older-record technical re-audit stay separate.'''

MEANINGS = {
    10: 'The unidentified speaker faintly calls using only a trailing respectful form of address. Preserve the partial,hesitant call without inventing a personal name,rank or completed sentence.',
    14: 'Lil gives a silent pause. Keep the quiet response without supplying snoring,dialogue or an emotion not stated.',
    18: 'The visitor softly repeats a respectful address to FI. Preserve FI and the hesitant pauses;the honorific expresses respect without establishing a new title or relationship.',
    22: 'Lil responds with a drowsy or puzzled questioning sound. Preserve the slight awakening/confusion rather than a fully informed reply.',
    26: 'The visitor asks forgiveness for his sudden intrusion and says he is not a suspicious person. Preserve both courteous apology and reassurance without inventing a threat or authority.',
    29: 'The visitor politely introduces himself as サンヒョン and Yifa\'s senior fellow disciple. Bind the approved English name later;兄弟子 denotes training seniority,not biological brotherhood or the teacher himself.',
    33: 'Having learned that Lil will take care of Yifa,the visitor came to offer a brief greeting. Preserve his deferential reason for visiting without inventing payment,an agreement with their teacher or formal guardianship.',
    37: 'Lil repeats Yifa\'s name as a puzzled question. Keep the recognition and uncertainty without additional information.',
    41: 'The visitor says it is shameful,but Yifa grew up so unrestrained entirely because his own guidance was inadequate. Preserve his self-blame and judgment,not an objective narrator verdict or proof that he was her sole teacher.',
    44: 'He says it is utterly unacceptable to leave the mountain without the teacher\'s permission to escape training,and even go abroad. Keep training,mountain,lack of permission and leaving the country;do not reduce this to merely running away from home.',
    48: 'He explains that Yifa probably has no way of knowing,but people of their country are prohibited from going abroad. Preserve her apparent ignorance and the general national restriction;no country or exact law is named.',
    52: 'Lil asks whether he therefore intends to take Yifa back. Keep the tentative question rather than an accusation that he has already seized her.',
    55: 'He says he cannot bring her back even if he wished:violating the national prohibition is a serious offense,and Yifa has been expelled from their dojo/training school. Preserve cause,seriousness and expulsion without inventing an additional legal punishment.',
    58: 'He says he now has no remaining connection to her. In context this is the formal break after expulsion,qualified by his personal affection in the following speech;do not recast it as a denial of all past closeness.',
    61: 'He qualifies that statement:he and Yifa grew up together from childhood like actual brother and sister. Preserve the simile and lifelong close bond,not biological kinship or romance.',
    64: 'He worries constantly that an immature girl like Yifa will commit some impropriety or embarrass herself before others. Preserve his protective concern without inventing a specific offense or numeric age.',
    68: 'He acknowledges that his request is selfish,but asks Lil to guide Yifa so she does not stray from the right path as a person. Keep the moral-guidance request and humility without adding a religion,official duty or punishment.',
    71: 'He adds a tentative request,if possible:even away from the mountain,Yifa should not neglect training and should follow their teacher\'s instructions. Preserve the conditional appeal and both instructions;no teacher gender or name is supplied.',
    74: 'He earnestly entrusts Yifa to Lil\'s care. Preserve the warm,formal closing plea without introducing a fee,contract or job.',
    77: 'Lil wonders whether the encounter was a dream and remarks that it felt strangely real. Preserve her uncertainty rather than declaring a literal supernatural visitation as narrator fact.',
    80: 'Yifa loudly and cheerfully says good morning,then begins urging Lil to hurry and depart before breaking off. Keep the exuberance and unfinished request;do not finish the interrupted thought with a destination.',
    83: 'Yifa reacts with a wordless burst of surprise. Preserve this nonverbal beat without inventing an exclamation or explanation she has not given yet.',
    87: 'Lil asks what is wrong. Keep the plain concerned/puzzled question.',
    91: 'Yifa says she senses the presence of her senior fellow disciple. Preserve the training relationship and perception without labeling a specific supernatural power or biological brother.',
    95: 'Lil reacts to senior fellow disciple and asks whether this person might be named サンヒョン. Preserve the recognition and question;use the bound approved spelling later.',
    99: 'Yifa reacts with disbelief and asks whether the man she familiarly calls 兄さん is here. Their preceding siblinglike upbringing supports affectionate familiarity,not an assertion of biological kinship.',
    102: 'Lil explains that the person who appeared in her dream introduced himself by that name and said he was Yifa\'s senior fellow disciple. Preserve Lil\'s reported dream perspective and both pieces of identification.',
    106: 'Yifa softly repeats that he came in a dream. Preserve the reflective echo without supplying a new explanation yet.',
    110: 'Yifa softly and affectionately says サンヒョン with her familiar older-brother-style address. Preserve her warmth while avoiding a newly invented biological relationship or rank.',
    114: 'Yifa understands the visit as an act of arts:because he cannot come down the mountain,he used them to come see her. Keep the restriction and method as her explanation;do not name a spell or assert literal physical travel.',
    118: 'Lil repeats the reference to arts and says she has no idea what it means. Preserve her continuing bafflement rather than giving her knowledge she lacks.',
    122: 'Lil remembers that the visitor told Yifa not to neglect training even after leaving the mountain,and to follow the teacher\'s instructions. Preserve both relayed requests;Lil does not relay the ban or expulsion here.',
    126: 'Yifa fondly laughs at the named senior disciple\'s habitual worrying,saying he is always that way. Preserve affection and humor without making the familiar address biological kinship.',
    130: 'After a pause,Lil asks what is going on with Yifa. Keep the quiet conversational prompt without inventing tears,illness or a change of allegiance.',
    133: 'Yifa declares she will train hard because it would be wrong to disappoint サンヒョン. Preserve her renewed resolve and specific personal motivation without replacing him with the teacher.',
    137: 'Lil interrupts to insist that shipboard work comes first and training afterward. Preserve the practical priority and comic snap,not a ban on training or an invented assigned job.',
    140: 'Yifa breezily insists she understands. Preserve the casual reassurance and lively response to Lil\'s correction.',
}

if __name__ == '__main__':
    assert not ROOT.exists()
    lead = deepcopy(next(b for b in read(INVENTORY)['blocks'] if b['block'] == 171))
    clean = Path('work/clean.nds')
    image = NdsImage.open(clean)
    block = IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[171]
    assert sha(clean.read_bytes()) == 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    assert sha(block) == lead['clean_block_sha256'] == '3eef66f9ac4a87991b9a95665470b95d831b5d9e657ef44d6ebf2942369c8fed'
    assert len(block) == 2120 and lead['speeches'] == len(lead['records']) == 37
    assert lead['source_selectors'] == [2, 25, 81] and lead['source_macro_counts'] == {'FI': 1, 'FA': 0, 'FO': 0}
    assert lead['FE_panels'] == lead['typed_menu_2100_commands'] == lead['typed_actor_style_4100_commands'] == lead['relative_sites'] == 0
    commands = lead['complete_native_commands']
    assert len(commands) == 45 and [c['offset'] for c in commands if c['word'] == 0] == [2112, 2116]
    assert not any(c['word'] in [0x2000, 0xA000, 0x8000] for c in commands)
    for c in commands:
        at = c['offset']
        assert block[at:at + c['native_extent']].hex() == c['whole_command_hex']
    assert {r['source_record_index'] for r in lead['records']} == set(MEANINGS)
    for row in lead['records']:
        at, raw = row['source_reference']['offset'], bytes.fromhex(row['source_hex'])
        assert block[at:at + len(raw)] == raw and block[at + len(raw)] == 0
        assert block[at - 5:at + 1].hex() == row['source_complete_preamble_hex']
        assert raw[1:].decode('cp932') == row['source_Japanese']
        row.update(fresh_source_gloss=MEANINGS[row['source_record_index']], whole_exchange_context=CONTEXT,
                   clean_source_complete_exchange_read_before_predecessor_English=True)
    ROOT.mkdir(parents=True)
    transcript = ROOT / 'SC2_B171_complete_clean_exchange_and_glosses.txt'
    lines = [CONTEXT]
    for row in lead['records']:
        lines.extend(['\n' + row['id'] + ' selector' + format(row['source_selector'], '02X'), row['source_Japanese'], row['fresh_source_gloss']])
    transcript.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    save(ROOT / 'all37_complete_B171_exchange_and_fresh_glosses.json', dict(format='dk4-editorial-clean-source-context-v1',
        source_ROM=str(clean), source_ROM_sha256=sha(clean.read_bytes()), source_SC2_sha256=sha(image.read_file('/data/SC2.DK4')),
        block=lead, total_editorial_objects=37, whole_exchange_context=CONTEXT, source_transcript=str(transcript),
        source_transcript_sha256=sha(transcript.read_bytes()), all37_clean_source_read_and_individually_glossed_before_predecessor_English=True,
        current_names_voices_terms_entry_conditions_macros_native_layout_actual_and_release_still_pending=True,
        no_predecessor_English_exposed=True, no_new_ROM_registry_ledger_orreview_credit=True, source_prose_or_completion_credit_added=0,
        new_emulator_runs=0, full_goal_complete=False, evidence={str(p): sha(p.read_bytes()) for p in [INVENTORY, transcript, Path(__file__)]}))
    print(dict(clean_objects=37, commands=45, selectors=[2,25,81], FI=1, FE=0, menus=0, current_English_unexposed=True, ledger_credit=0, full_goal_active=True))
