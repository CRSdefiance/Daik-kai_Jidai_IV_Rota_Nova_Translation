"""Next Inn family:exact source inventory,not prose/context approval."""

import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch import palace_label_boundaries as previous
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/inn_editorial_v800')
DOC=Path('docs/inn_inventory_v800_checkpoint.md')
IDS=tuple(range(1177,1200))


def ref(entry):
    return {k:v for k,v in vars(entry).items() if k!='text'}


def main():
    assert not DOC.exists();ROOT.mkdir(parents=True,exist_ok=True)
    clean=NdsImage.open('work/clean.nds');current=NdsImage.open('out/all_routes_combined_v799_candidate.nds')
    assert sha(Path('work/clean.nds').read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    assert sha(Path('out/all_routes_combined_v799_candidate.nds').read_bytes())=='f855781b6b2a23482874a81c4d3f8f77262fe7f7db2846399b1409da8cc67c79'
    jp_arm=clean.read_file('/__arm9__.bin');arm=current.read_file('/__arm9__.bin')
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),jp_arm)
    en=previous.current_entries(current.read_file('/COMMON/MESFILE.DK4'),arm)
    main=bytes(MainCodeFile(jp_arm,0x02000000).sections[0].data)
    rows=[]
    for n in IDS:
        words=[i for i in range(0,len(main)-3,4) if struct.unpack_from('<I',main,i)[0]==n]
        rows.append({'message_id':n,'source_hex':jp[n].text.hex(),'japanese':jp[n].text.decode('cp932'),
            'source_reference':ref(jp[n]),'current_hex':en[n].text.hex(),'current_English':en[n].text.decode('cp932'),
            'current_reference':ref(en[n]),'source_percent_s_count_inventory_only':jp[n].text.count(b'%s'),
            'unclassified_original_aligned_word_value_leads':[0x02000000+i for i in words],
            'source_context_prose_and_formatting_approval':False})
    voices=[]
    for at in range(0,len(main)-31,4):
        values=struct.unpack_from('<8i',main,at)
        if set(values)==set(range(1186,1194)):voices.append({'address':0x02000000+at,'values':list(values)})
    packet={'candidate_sha256':sha(Path('out/all_routes_combined_v799_candidate.nds').read_bytes()),
        'source_ARM9_sha256':sha(jp_arm),'current_ARM9_sha256':sha(arm),'rows':rows,
        'possible_eight_voice_tables_not_yet_bound_to_original_consumers':voices,
        'original_word_values_are_leads_not_called_dialogue_proof':True,
        'no_new_English_or_review_or_completion_credit':True,
        'producer_sha256':sha(Path('scripts/inventory_inn_editorial_v800.py').read_bytes()),'full_goal_complete':False}
    save(ROOT/'source_inventory.json',packet)
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger=read(ledger_path)
    assert ledger['records_editorially_completed']==527 and ledger['records_with_source_and_prose_pass']==530
    ledger['next_Inn_source_packet']={'inventory':str(ROOT/'source_inventory.json'),'native_IDs':list(IDS),
        'status':'inventory-only;original-speakers-argument-providers-and-branches-pending',
        'review_credit':0,'completion_credit':0}
    ledger['findings'].append({'id':'COMMON1185-buyout-rumor-wrong-faction-question','native_message_ids':[1185],
        'status':'clean-source-meaning-lead;native-context-and-prose-review-pending',
        'proof':str(ROOT/'source_inventory.json'),
        'detail':'Clean Japanese describes how upset %s was after missing a purchase. Current English asks Which faction should we oppose? The original subject/name provider and buyout-rumor path must be mapped before revision.'})
    ledger['coverage_units'][0]['next']='Map Inn1177-1199 original speakers,room charges/night count,report voices and rumor substitutions against clean Japanese.1185 has a meaning-error lead. Then continue shared1200 onward,older750-752 contexts,all routes and other prose.'
    ledger['research_checkpoints'].append({'id':'V800-Inn23-source-inventory-only','documentation':str(DOC),
        'new_source_prose_reviewed':0,'new_editorially_completed':0,'new_ROM':False,'full_goal_complete':False})
    save(ledger_path,ledger)
    summary=('After Palace completion,the next23 shared entries1177-1199 are pinned to clean Japanese and exact V799 records. '
        'They include overnight charges/stay confirmation,market-news replies,eight information-report voices,insufficient funds and battle/raid rumors. '
        '1185 has an obvious source-meaning lead:purchase disappointment versus an unrelated faction-opposition question. '
        'Word-value matches and possible voice arrays are unclassified leads;no source-context/prose approval,new translation,ROM or completion credit is added. '
        '527 COMMON complete/530 source-prose reviewed/three older contexts pending remain unchanged. Full goal active.')
    DOC.write_text('# V800: next Inn family inventory\n\n'+summary+'\n\n'
        'Packet:`work/analysis/inn_editorial_v800/source_inventory.json`. First map the actual Inn '
        'speaker/portrait provider,native night-count and price providers,report voice selector,and rumor '
        'subject/object getters. Do not infer sequential dialogue from neighboring storage or assume '
        'an NPC role from an English label. Preserve complete argument order and all current approved names. '
        'The next religious/ceremony entries begin at1200 and are outside this23-entry inventory. '
        'The separate graphics audit remains unfinished.\n',encoding='utf-8')
    for name in ('todo','translation_progress','editorial_review_goal'):
        p=Path('docs')/(name+'.md');p.write_text(p.read_text(encoding='utf-8')+'\n\n## V800: Inn inventory only\n\n'+summary+
            ' See [V800 inventory](inn_inventory_v800_checkpoint.md).\n',encoding='utf-8')
    print(f'Inn23 exact source/current entries and{len(voices)} voice-array leads inventoried;no review or completion credit.',flush=True)


if __name__=='__main__':main()
