"""Next shared ceremony entries:source/current inventory,not context approval."""

import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.inn_editorial import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/ceremony_editorial_v805')
DOC=Path('docs/ceremony_inventory_v805_checkpoint.md')
IDS=tuple(range(1200,1245))


def main():
    assert not DOC.exists();ROOT.mkdir(parents=True,exist_ok=True)
    current=Path('out/all_routes_combined_v803_candidate.nds');clean=Path('work/clean.nds')
    jp_rom,en_rom=[NdsImage.open(p) for p in (clean,current)]
    jp_arm=jp_rom.read_file('/__arm9__.bin');arm=en_rom.read_file('/__arm9__.bin')
    source=common_message_entries(jp_rom.read_file('/COMMON/MESFILE.DK4'),jp_arm)
    entries=current_entries(en_rom.read_file('/COMMON/MESFILE.DK4'),arm)
    ledger=read('translations/editorial_review_current_v1.json')
    assert ledger['records_editorially_completed']==550 and ledger['records_with_source_and_prose_pass']==553
    done={n for f in ledger['completed_editorial_families'] for n in f.get('native_message_IDs',[])}
    assert not set(IDS)&done and {1199,1245,1246}<=done
    main=bytes(MainCodeFile(jp_arm,0x02000000).sections[0].data)
    leads={n:[] for n in IDS}
    for at in range(0,len(main)-3,4):
        number=struct.unpack_from('<I',main,at)[0]
        if number in leads:leads[number].append(0x02000000+at)
    def row(n):
        a,b=source[n],entries[n]
        return dict(message_id=n,japanese=a.text.decode('cp932'),source_hex=a.text.hex(),
            source_reference={k:v for k,v in vars(a).items() if k!='text'},
            current_English=b.text.decode('cp932'),current_hex=b.text.hex(),
            current_reference={k:v for k,v in vars(b).items() if k!='text'},
            unclassified_aligned_word_value_leads=leads.get(n,[]),
            inventory_only_percent_s_count=a.text.count(b'%s'),already_editorially_completed=n in done,
            context_prose_and_formatting_approval=False)
    arrays=[]
    for width in (4,8):
        for at in range(0,len(main)-width*4+1,4):
            values=struct.unpack_from('<'+'i'*width,main,at)
            found={n for n in values if n in leads}
            if len(found)>=2 and all(n==-1 or n in leads for n in values):
                arrays.append(dict(address=0x02000000+at,words=width,values=list(values),
                    kind='unclassified-word-array;actor-voice-hero-or-other-selector-not-yet-proven'))
    packet=dict(candidate=str(current),candidate_sha256=sha(current.read_bytes()),clean_source_sha256=sha(clean.read_bytes()),
        source_COMMON_sha256=sha(jp_rom.read_file('/COMMON/MESFILE.DK4')),current_COMMON_sha256=sha(en_rom.read_file('/COMMON/MESFILE.DK4')),
        source_ARM9_sha256=sha(jp_arm),current_ARM9_sha256=sha(arm),rows=[row(n) for n in IDS],
        neighbors=[row(n) for n in (1199,1245,1246)],possible_word_arrays=arrays,
        source_word_matches_are_not_called_dialogue_or_scene_sequence_proof=True,
        no_new_English_review_or_completion_credit=True,ROM_changed=False,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False)
    save(ROOT/'source_inventory.json',packet)
    ledger['next_ceremony_source_packet']=dict(inventory=str(ROOT/'source_inventory.json'),native_IDs=list(IDS),
        status='inventory-only;original-speakers-sequence-selectors-and-runtime-ceremony-name-pending',review_credit=0,completion_credit=0)
    for item in (
        dict(id='COMMON1205-1206-possible-cross-selection-fragments',native_message_ids=[1205,1206],
            detail='Clean1205 is !?/surprise punctuation;1206 asks What is it/what on earth?! Current selections are What and was that? Map original selectors and actual speakers before deciding whether these are alternatives or sequential;do not join them from storage adjacency.'),
        dict(id='COMMON1224-1225-reaction-and-chant-boundary-lead',native_message_ids=[1224,1225],
            detail='Clean1224 is a puzzled Huh?;current ! Ra appears to contain an adjacent cry fragment.1225 is the separate forceful unintelligible chant. Original consumers and complete native spans must establish ownership before revision.'),
        dict(id='COMMON1213-help-request-subject-lead',native_message_ids=[1213],
            detail='Clean repeats Help? as a reaction;current You want to help? introduces an unproven intention/subject. Resolve the original speaker and actual preceding order before authoring.'),
    ):
        ledger['findings'].append(dict(**item,status='source-inventory-lead;native-context-not-yet-reviewed',proof=str(ROOT/'source_inventory.json')))
    summary=('V805 inventories45 untouched shared ceremony entries1200-1244 against clean Japanese and exact V803 bytes/references. '
        'Potential reaction/chant fragments1205-1206 and1224-1225 and help-subject1213 are source leads only;selectors and speakers remain unmapped. '
        'Prior completed1199 and1245/1246 are pinned neighbors and receive no second credit. No prose or formatting approval,new ROM or completion credit. '
        '550 complete/553 source-prose reviewed/three older750-752 contexts remain unchanged. Full goal active.')
    ledger['latest_checkpoint']=summary
    ledger['coverage_units'][0]['next']='Map ceremony1200-1244 actual original speakers,cultural/hero/voice selectors,scene order and1219 ceremony-name argument;resolve fragment leads before writing. Preserve completed1245/1246. Then remaining shared,old750-752 contexts,all routes and other prose.'
    ledger['research_checkpoints'].append(dict(id='V805-ceremony45-inventory-only',documentation=str(DOC),new_source_prose_reviewed=0,new_editorially_completed=0,new_ROM=False,full_goal_complete=False))
    save('translations/editorial_review_current_v1.json',ledger)
    DOC.write_text('# V805: next shared ceremony inventory\n\n'+summary+'\n\n'
        'Packet: `work/analysis/ceremony_editorial_v805/source_inventory.json`. All aligned word matches and4/8-word arrays are unclassified leads;they do not prove message calls or chronological dialogue. '
        'Map the actual building/role and original scene dispatcher,who gives the orders and who reacts,whether the reaction forms are hero or voice alternatives, '
        'and the provider/meaning/bounds of1219%s. Read clean Japanese with real preceding/following calls before choosing natural American English. '
        'Do not repair fragments by joining adjacent records or copy legacy manual breaks. '
        'Inn23 is complete in unchanged registered V803;the V804 completion checkpoint and exact patch remain current. '
        'Keep graphics/18 plaques and the wider editorial goal open.\n',encoding='utf-8')
    for name in ('todo','translation_progress','editorial_review_goal'):
        p=Path('docs')/(name+'.md');text=p.read_text(encoding='utf-8');heading='## V805: ceremony inventory only'
        assert heading not in text;p.write_text(text+'\n\n'+heading+'\n\n'+summary+' See [next inventory](ceremony_inventory_v805_checkpoint.md).\n',encoding='utf-8')
    print(f'Ceremony45 exact source/current inventory;{len(arrays)} unclassified4/8-word arrays;no review/completion credit.550 complete;V803 unchanged.',flush=True)


if __name__=='__main__':main()
