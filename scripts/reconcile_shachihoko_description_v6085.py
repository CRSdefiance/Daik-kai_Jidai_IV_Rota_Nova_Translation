"""Bind the newly found shared description and its staged literal before any release."""
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/shachihoko_description_v6085')
CENSUS=Path('work/analysis/shachihoko_current_context_v6078/four_complete_source_current_exchanges_and_raw_Orca_candidates.json')
def ref(entry):
    return dict(message_ID=entry.message_id,block=entry.block,table_offset=entry.table_offset,block_offset=entry.block_offset,copy_end=entry.copy_end,record_index=entry.record_index,start=entry.start,end=entry.end,text_hex=entry.text.hex(),text=entry.text.decode('cp932'))
if __name__=='__main__':
    assert not ROOT.exists();census=read(CENSUS);current=NdsImage.open(census['candidate']);clean=NdsImage.open('work/clean.nds');ca,ja=[r.read_file('/__arm9__.bin') for r in [current,clean]]
    source=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),ja);target=owned_entries(current.read_file('/COMMON/MESFILE.DK4'),ca,read('translations/shop657_full_width_reflow_release_v1.json')['directory_sha256'])
    jp=source[2931];now=target[2931];assert jp.text.decode('cp932')=='尾を逆立て、敵を威嚇するような姿をしたシャチの船首像。恐ろしい嵐も、これを付けた艦隊を避けるという言い伝えがある。'
    assert now.text.startswith(b'An orca figurehead')
    payload=bytes(MainCodeFile(ca,0x02000000).sections[3].data[:-48]);assert len(payload)==123040 and ca.count(payload)==1
    literal=b'An orca figurehead raises its tail to threaten\0foes. Even fierce storms';at=payload.index(literal);assert payload.count(literal)==1
    ROOT.mkdir(parents=True);save(ROOT/'clean_description_neighbor_context_current_COMMON_and_staged_copy_lead.json',dict(
        candidate=census['candidate'],candidate_sha256=census['candidate_sha256'],source_description=ref(jp),current_description=ref(now),
        source_neighbors=[ref(source[i]) for i in range(2928,2935)],
        clean_first_gloss='A shachi figurehead posed with its tail raised as if threatening an enemy. There is a legend that even fearsome storms avoid a fleet carrying it.',
        cultural_reconciliation='Unlike the castle speeches\' シャチホコ,this independent description uses シャチ. Preserve that exact source distinction as evidence. The item title 鯱の像,the four complete castle exchanges and the upturned ornament image support reviewing Shachihoko as the shared title. Do not claim that the independent description itself literally says シャチホコ,or that orca was an impossible dictionary reading. Any coordinated localization must preserve the threatening upturned pose and the reported storm legend,without asserting a guaranteed game effect or adding architectural lore to Jam\'s letter.',
        provisional_description='A shachihoko figurehead posed with its tail raised to threaten foes. Legend says even fearsome storms avoid a fleet carrying it.',
        provisional_description_not_formatted_or_approved=True,
        staged_literal=dict(ARM9_file_offset=ca.index(payload)+at,staged_payload_offset=at,deployed_address=0x02387A20+at,matched_hex=literal.hex(),bound_to_same_current_description_text=True,native_consumer_and_pointer_ownership_not_yet_bound=True),
        original_older_description_manuscript='translations/common_b32_packed_manuscript_v2.json',original_older_description_manuscript_sha256=sha(Path('translations/common_b32_packed_manuscript_v2.json').read_bytes()),
        no_shared_item_name_release_until_COMMON_description_and_active_staged_consumers_reconciled=True,
        nickname_Orca_occurrences_remain_separate_source_owned_alias_leads=True,no_global_substitution=True,
        item_name_research_still_provisional_not_registered_or_promoted=True,new_review_credit=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [CENSUS,Path(__file__)]}))
    print('COMMON2931 clean shachi/pose/storm legend bound with seven source neighbors and current staged-copy lead. Item label+description coordination required before release;no credit.')
