"""Resolve the actual alternate escape literal and actor predicate;no prose credit."""
from pathlib import Path
import struct
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.patch.sighting_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/duel_source_v1102')


def main():
    assert not ROOT.exists()
    prior_path=Path('work/analysis/duel_source_v1101/source_context_packet.json');prior=read(prior_path)
    rom=NdsImage.open(prior['candidate']);clean=NdsImage.open('work/clean.nds')
    assert sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256']
    arm=rom.read_file('/__arm9__.bin');source=clean.read_file('/__arm9__.bin')
    table=struct.unpack_from('<I',source,0xED6C)[0];assert table==0x02117620
    ids=(1973,-1,1974,1975,1976,1977,1978,1979)
    assert struct.unpack_from('<8i',source,table-0x02000000)==ids
    assert arm[table-0x02000000:table-0x02000000+32]==source[table-0x02000000:table-0x02000000+32]
    assert arm[0x7EF28:0x7EFEC]==source[0x7EF28:0x7EFEC]
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),source)
    en=current_entries(rom.read_file('/COMMON/MESFILE.DK4'),arm)
    raw=Path(prior['source_snapshot']).read_bytes();assert sha(raw)==prior['source_snapshot_sha256']
    cpu,get=get_machine(arm,raw);actors=get(0xCB184);captain=get(0x7F244);rows=[];predicates=[]
    for actor in range(208):
        obj=actors+0x19E4 if actor==captain else actors+4+actor*32
        voice=get(0x7E988,obj);n=get(0x53F4C,obj,table)
        assert n==(ids[voice] if ids[voice]!=-1 else ids[0])
        rows.append({'actor_ID':actor,'voice':voice,'message_ID':n})
        predicates.append({'actor_ID':actor,'original_7EF28_result':get(0x7EF28,actor)})
    zero=[r['actor_ID'] for r in predicates if r['original_7EF28_result']==0]
    assert zero==[0,1,2,3]
    assert get(0x53F4C,0,table)==1973
    source_rows=[{'message_ID':n,'source_hex':jp[n].text.hex(),'source_Japanese':jp[n].text.decode('cp932'),
        'current_hex':en[n].text.hex(),'current_English':en[n].text.decode('cp932')} for n in ids if n>=0]
    ROOT.mkdir(parents=True);proof=ROOT/'escape_source_supplement.json'
    save(proof,{'prior_source_inventory':str(prior_path),'prior_source_inventory_sha256':sha(prior_path.read_bytes()),
        'exact_original_literal_address':0x0200ED6C,'original_alternate_table':table,'voice_IDs':list(ids),
        'all208_original_alternate_voice_selections':rows,'all208_original_actor_predicates':predicates,
        'zero_predicate_actor_IDs':zero,'source_and_current_seven_additional_alternatives':source_rows,
        'exact_source_consumer':'Actor IDs0..3 select original1973..1979 Admiral speech without a name argument;others select1951..1956 with the original compact-name getter.',
        'erratum':'V1101 escape_name_conditional text incorrectly guessed a2512 table. The frozen source fragments and literal prove02117620 /1973..1979 instead. No ROM bytes were changed by the mistaken note.',
        'named_and_Admiral_variants_are_independent_alternatives_not_sequential_lines':True,
        'no_new_source_prose_or_completion_credit':True,'no_actual_duel_scene_or_branch_result_claim':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger=read(ledger_path)
    assert ledger['records_editorially_completed']==1196 and ledger['records_with_source_and_prose_pass']==1234
    lead=ledger['next_duel_editorial_source_inventory_v1101']
    lead.update(escape_source_supplement=str(proof),native_message_IDs=[*range(1931,1957),*range(1973,1980)],
        original_actor_selections=1040,source_literal_erratum='V1101 guessed2512;original literal actually1973..1979. Use V1102 supplement.',
        source_prose_review_and_complete_native_consumer_mapping_still_pending=True)
    save(ledger_path,ledger)
    print('Original escape branch resolved:0..3 captain IDs use1973..1979 Admiral alternatives;other IDs use named variants.33 inventory IDs/1040 original selections;no review credit.',flush=True)


if __name__=='__main__':main()
