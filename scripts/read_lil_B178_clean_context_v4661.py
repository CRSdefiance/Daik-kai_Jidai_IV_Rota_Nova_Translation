"""Read/gloss the complete B178 home-baking exchange before predecessor English."""
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B178_clean_context_v4661')
INVENTORY=Path('work/analysis/lil_B161_B180_clean_scope_v3910/complete_clean_B161_B180_next_exchange_inventory.json')
CONTEXT=(
    'Read all thirteen B178 speeches as one light social exchange about baking bread at home. '
    'A6 declares baking one\'s own bread best. A7 agrees and says her husband was delighted too. '
    'A8 asks whether baking it oneself really makes it that good. A6 enthusiastically repeats '
    'that it is wonderful and invites agreement. A7 boasts that the bakery around the corner '
    'cannot compare. A8 considers trying it herself. A6 encourages her;A7 offers to teach her; '
    'A8 responds with pleased surprise. A6 immediately suggests going to buy ingredients. '
    'A7 asks what is needed;A8 proposes wheat first. The impersonal FE notice forecasts that '
    'wheat seems likely to catch on in アムステルダム. Preserve the progression from shared '
    'enthusiasm and praise through curiosity,encouragement,help and gratitude to a practical '
    'shopping plan and prospective commodity news.\n\n'
    'The native names/voices of A6,A7,A8 remain to bind. A7 explicitly mentions her husband; '
    'that relationship is supported for A7 alone. No spouse or kinship is specified for the '
    'others,and the text identifies no husband by name. Do not invent neighbors,sisters, '
    'royalty,rank,occupation or prior friendship. Feminine conversational register alone '
    'does not identify a named character. 自分で焼く means baking it oneself/home baking, '
    'not necessarily doing every task alone. うちも makes A7\'s household another pleased '
    'example;do not add a time,meal,children or a completed commercial sale.\n\n'
    'The comparison with the corner bakery is A7\'s enthusiastic boast,not an objective '
    'narrator ruling,an accusation of bad or unsafe food,or a statement that a bakery closes. '
    'A7 offers to teach and later asks what ingredients are needed. Retain those exact '
    'speaker assignments and their ordinary comic/conversational sequence;do not repair '
    'an imagined contradiction by moving a line to another actor or inventing a deliberate '
    'deception. A8\'s wheat suggestion does not establish baking expertise. 小麦 is wheat, '
    'not an authorization to substitute flour or add yeast,butter,eggs,a recipe,quantities '
    'or prices. Shopping is proposed;no purchase or baking lesson is shown completed.\n\n'
    'The final しそう remains prospective likelihood,not a confirmed or earned boom. The '
    'city is explicit only there;do not assign the preceding exchange a location or invent '
    'chronological continuity with B177. All thirteen speeches have static selectors A6/ '
    'A7/A8 or impersonal FE and zero FI/FA/FO substitutions. The linear structural stream '
    'contains16 commands:opaque A0008 raw00a0ffff010002a1,thirteen speeches,C200488 and '
    'single four-byte end490,logical494/stored496. No relative site,predicate,2000 pause, '
    'resource,presentation word or typed object. Native entry,names,controls,layout,actual '
    'coverage and cumulative integration remain to bind. No natural selection or earned '
    'fashion state is established. This producer reads no predecessor English and adds no credit.'
)
MEANINGS={
    7:'A6 says that,after all,baking bread oneself is best. Preserve enthusiastic praise for home baking,without inventing a recipe,earlier failure or isolation from all help.',
    10:'A7 agrees and says that her own husband was delighted too. Preserve the explicit husband relationship for this speaker and shared enthusiasm;name no husband and add no children,meal,time or relationship for A6/A8.',
    13:'A8 asks whether bread is really that delicious when one bakes it oneself. Preserve curiosity and the question rather than inventing contempt for the others or an established personal experience.',
    17:'A6 emphatically says it is absolutely wonderful and appeals for agreement with the conversational ねえ. Preserve enthusiasm and social agreement-seeking,without adding a new factual superlative comparison.',
    21:'A7 agrees and boasts that even the bakery around that corner is no match. Preserve the specific nearby corner bakery and the idiomatic comparison as this speaker\'s praise,not a narrator fact,food-safety accusation or threatened business closure.',
    24:'A8 acknowledges this and wonders whether she should try making bread too. Preserve tentative interest and self-directed consideration,not a promise that she has already baked it.',
    28:'A6 encourages A8 to do so. Preserve the friendly/direct encouragement without inventing a formal order,rank or family address.',
    32:'A7 offers to teach A8. Preserve the offered help and speaker assignment;add no fee,professional qualification or completed lesson.',
    36:'A8 reacts with pleased surprise,really,and says she is happy about the offer. Preserve warmth and gratitude/pleasure,not romantic affection or a new kinship label.',
    40:'A6 proposes that they go buy the ingredients right away. Preserve the inclusive invitation,shopping purpose and immediacy;no purchase,quantity,price or sale has occurred yet.',
    43:'A7 wonders what ingredients they will need. Preserve this exact speaker and question after her teaching offer;do not reassign it or invent an explanatory joke or deception.',
    47:'A8 suggests that wheat would naturally come first. Preserve the basic ingredient suggestion and agreement-seeking tone;小麦 is wheat,not flour or a full recipe.',
    51:'An impersonal FE notice forecasts that wheat seems likely to become fashionable in アムステルダム. Preserve the explicit city and prospective likelihood;do not assert an active or earned boom,completed transaction or earlier scene location.',
}

if __name__=='__main__':
    assert not ROOT.exists()
    lead=deepcopy(next(b for b in read(INVENTORY)['blocks'] if b['block']==178))
    clean=Path('work/clean.nds');im=NdsImage.open(clean)
    block=IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[178]
    assert sha(clean.read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    assert sha(block)==lead['clean_block_sha256']=='37c78894ad7fd955b0012326cb78086dfb0f9c4bed8e139809cf46f5cee75b8c'
    assert len(block)==496 and lead['speeches']==len(lead['records'])==13
    assert lead['source_selectors']==[166,167,168,254] and lead['source_macro_counts']=={'FI':0,'FA':0,'FO':0}
    assert lead['FE_panels']==1 and lead['relative_sites']==lead['typed_menu_2100_commands']==lead['typed_actor_style_4100_commands']==0
    commands=lead['complete_native_commands'];assert len(commands)==16
    assert [(c['offset'],c['whole_command_hex']) for c in commands if c['word']!=0x4000]==[(8,'00a0ffff010002a1'),(488,'00c2'),(490,'00000000')]
    assert not any(c['word'] in [0x100,0x200,0x300,0x400,0x8000,0x8100,0x2000] or c['word']&0xFF00==0x6300 for c in commands)
    for c in commands:
        at=c['offset'];assert block[at:at+c['native_extent']].hex()==c['whole_command_hex']
    assert {r['source_record_index'] for r in lead['records']}==set(MEANINGS)
    for r in lead['records']:
        at=r['source_reference']['offset'];raw=bytes.fromhex(r['source_hex'])
        assert block[at:at+len(raw)]==raw and block[at+len(raw)]==0
        assert block[at-5:at+1].hex()==r['source_complete_preamble_hex'] and raw[1:].decode('cp932')==r['source_Japanese']
        r.update(fresh_source_gloss=MEANINGS[r['source_record_index']],whole_exchange_context=CONTEXT,
            clean_source_complete_exchange_read_before_predecessor_English=True)
    ROOT.mkdir(parents=True)
    transcript=ROOT/'SC2_B178_complete_clean_exchange_and_glosses.txt';lines=[CONTEXT]
    for r in lead['records']:
        lines.extend(['\n'+r['id']+' selector'+format(r['source_selector'],'02X'),r['source_Japanese'],r['fresh_source_gloss']])
    transcript.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    save(ROOT/'all13_complete_B178_exchange_and_fresh_glosses.json',dict(format='dk4-editorial-clean-source-context-v1',
        source_ROM=str(clean),source_ROM_sha256=sha(clean.read_bytes()),source_SC2_sha256=sha(im.read_file('/data/SC2.DK4')),
        block=lead,total_editorial_objects=13,whole_exchange_context=CONTEXT,source_transcript=str(transcript),
        source_transcript_sha256=sha(transcript.read_bytes()),all13_clean_source_read_and_individually_glossed_before_predecessor_English=True,
        source_progressive_speeches=12,source_FE_speeches=1,source_relative_site_count=0,source_predicate_count=0,
        source_A000_count=1,source_C200_count=1,source_declared_end_offsets=[490],source_static_actor_selectors=[166,167,168],
        source_FE_notice_is_impersonal_prospective_city_commodity_fashion=True,explicit_husband_reference_for_A7_only=True,
        native_names_voices_city_wheat_and_complete_controls_to_bind=True,
        current_names_voices_terms_entry_conditions_native_layout_actual_and_release_still_pending=True,
        no_predecessor_English_exposed=True,no_new_ROM_registry_ledger_orreview_credit=True,
        source_prose_or_completion_credit_added=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [INVENTORY,transcript,Path(__file__)]}))
    print(dict(clean_objects=13,progressive=12,FE=1,commands=16,selectors=[166,167,168,254],FI=0,FA=0,FO=0,
        A000=1,C200=1,end=490,current_English_unexposed=True,credit=0))
