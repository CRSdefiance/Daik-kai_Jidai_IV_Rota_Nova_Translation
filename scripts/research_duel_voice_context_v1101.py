"""Inventory next original duel alternatives and consumers;no prose/completion credit."""
from dataclasses import asdict
from pathlib import Path
import struct
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.patch.sighting_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/duel_source_v1101')
ROM=Path('out/all_routes_combined_v1086_candidate.nds')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/sighting_v1094_1086_compassReady8')
BASE=0x02000000
TABLES={
    'challenge':(0x02117340,tuple(range(1931,1939))),
    'acceptance':(0x02117360,(1939,1940,1941,1942,1943,-1,1944,-1)),
    'defeated_opponent_threat':(0x021174E0,(1945,-1,-1,1946,1947,1948,1949,1950)),
    'cover_for_defeated_captain':(0x02117500,(1951,-1,1952,1953,1954,1955,1956,-1))}


def main():
    assert not ROOT.exists()
    rom=NdsImage.open(ROM);clean_path=Path('work/clean.nds');clean=NdsImage.open(clean_path)
    assert sha(ROM.read_bytes())=='df958b7289743e8eca79c9a6a216e134c9a2590321597f7bead15111ee8d748f'
    assert sha(clean_path.read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    arm=rom.read_file('/__arm9__.bin');source=clean.read_file('/__arm9__.bin')
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),source)
    en=current_entries(rom.read_file('/COMMON/MESFILE.DK4'),arm)
    report_path=CAP/'capture_report.json';report=read(report_path);snapshot=CAP/'frame_005310_arm9_ram.bin'
    receipt=next(r for r in report['read_only_pause_RAM_snapshots'] if r['frame']==5310)
    raw=snapshot.read_bytes();assert sha(raw)==receipt['sha256'] and len(raw)==0x400000
    assert report['cold_boot'] and not report['savestate_loaded'] and report['ROM_sha256']==sha(ROM.read_bytes())
    cs=Cs(CS_ARCH_ARM,CS_MODE_ARM);fragments=[]
    for lo,hi in ((0xD458,0xD4D0),(0xEA1C,0xEB94),(0xEB94,0xED74),(0x53F0C,0x53FE4),(0x7E988,0x7E9A0)):
        assert arm[lo:hi]==source[lo:hi]
        fragments.append({'start':BASE+lo,'end':BASE+hi,'clean_and_current_sha256':sha(source[lo:hi]),
            'instructions':[f'{i.address:08X} {i.mnemonic} {i.op_str}' for i in cs.disasm(source[lo:hi],BASE+lo)]})
    cpu,get=get_machine(arm,raw);actors=get(0xCB184);captain=get(0x7F244);assert captain==1
    selections=[];nulls=[];tables=[]
    for family,(table,ids) in TABLES.items():
        assert tuple(struct.unpack_from('<8i',source,table-BASE))==ids
        assert arm[table-BASE:table-BASE+32]==source[table-BASE:table-BASE+32]
        refs=[BASE+i for i in range(0,len(source)-3,4) if source[i:i+4]==struct.pack('<I',table)]
        tables.append({'family':family,'address':table,'voice_IDs':list(ids),'original_aligned_pointer_references':refs})
        for actor in range(208):
            obj=actors+0x19E4 if actor==captain else actors+4+actor*32
            voice=get(0x7E988,obj);assert 0<=voice<8
            n=get(0x53F4C,obj,table);expected=ids[voice] if ids[voice]!=-1 else ids[0]
            assert n==expected
            selections.append({'family':family,'actor_ID':actor,'voice_class':voice,'message_ID':n,'fallback':ids[voice]==-1})
        n=get(0x53F4C,0,table);assert n==ids[0]
        nulls.append({'family':family,'null_actor_selects':n})
    assert len(selections)==832 and {r['message_ID'] for r in selections}==set(range(1931,1957))
    rows=[]
    for n in range(1930,1958):
        rows.append({'message_ID':n,'selected_inventory':1931<=n<=1956,
            'source_reference':{k:v for k,v in asdict(jp[n]).items() if k!='text'},
            'source_hex':jp[n].text.hex(),'source_Japanese':jp[n].text.decode('cp932'),
            'current_reference':{k:v for k,v in asdict(en[n]).items() if k!='text'},
            'current_hex':en[n].text.hex(),'current_English':en[n].text.decode('cp932'),
            'original_runtime_string_arguments':jp[n].text.count(b'%s')})
    ROOT.mkdir(parents=True)
    save(ROOT/'source_context_packet.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'clean_ROM_sha256':sha(clean_path.read_bytes()),'source_snapshot':str(snapshot),'source_snapshot_sha256':sha(raw),
        'terminal_report':str(report_path),'terminal_report_sha256':sha(report_path.read_bytes()),
        'tables':tables,'all832_original_actor_voice_selections':selections,'all4_null_actor_controls':nulls,
        'original_code_and_equal_current_fragments':fragments,'source_and_current_neighbors':rows,
        'challenge_and_acceptance_have_distinct_original_duel_text_consumer':{'wrapper':BASE+0xD458,
            'voice_source':'controller+0x34+side*4 actor pointer','original_printf_call':BASE+0xCE898,'display_call':BASE+0xDA28,
            'challenge_side':0,'acceptance_side':1,'not_ordinary_speech_53914_or_sighting_formatter':True},
        'challenge_name_source':'EA1C uses original actor+0x24 getter for IDs28..43,otherwise actor+0x20;exact resulting names still require getter/context proof.',
        'post_duel_branch':'EB94 reads player actor4C4 HP:positive chooses opponent side1 threat;nonpositive selects First Mate or original alternate actor,then 53F0C speech. No branch result was forced.',
        'escape_name_conditional':'Original actor-ID predicate7EF28 selects either different2512 table or1951..1956 with compact-name argument. Predicate meaning/actual eligibility still needs review.',
        'unreviewed_findings':['Current1932/1935/1937 use fullwidth F and1939/1941/1942/1943 fullwidth I;review complete initial glyphs under their actual consumers rather than blindly replacing.',
            'Current1940 omits source amusement;1950 changes next time will be different into a guaranteed loss;source/prose review still required.'],
        'no_new_prose_source_review_credit_or_actual_duel_scene_claim':True,'no_ROM_or_live_RAM_changes':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger=read(ledger_path)
    assert ledger['records_editorially_completed']==1196 and ledger['records_with_source_and_prose_pass']==1234
    ledger['next_duel_editorial_source_inventory_v1101']={'proof':str(ROOT/'source_context_packet.json'),
        'native_message_IDs':list(range(1931,1957)),'original_actor_selections':832,
        'source_prose_review_and_complete_native_consumer_mapping_still_pending':True,'completed_entries_added':0}
    save(ledger_path,ledger)
    print('Next26 duel alternatives inventoried:832 source selections,4 null controls,distinct original consumers. No prose/completion credit.',flush=True)


if __name__=='__main__':main()
