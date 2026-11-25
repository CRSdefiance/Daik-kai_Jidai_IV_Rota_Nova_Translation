"""Read both ceramic-collector and opportunistic-seller exchanges before old prose."""
from copy import deepcopy
from pathlib import Path
import struct
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B189_clean_context_v5272b')
SOURCE=Path('work/analysis/lil_B189_clean_inventory_v5271/all_clean_B189_speeches_before_predecessor_comparison.json')
GLOSSES={
    6:('The other day,I finally managed to get that item.','0x93/147 opens with satisfaction at finally obtaining the previously understood object. The next reply identifies ceramics. Keep the recent completed acquisition without inventing a price,seller,place or named item.'),
    9:('Oh,the ceramics?','0x52/82 identifies the object conversationally. It is not a question about a new purchase or a specific vase/cup shape. Bind actors93/0x52/82 before choosing roles or personal names.'),
    13:('Yes. It was the finest piece,just as I expected.','0x93/147 praises the acquisition as excellent,matching expectations. This subjective judgment sets up later dramatic irony;do not certify authenticity or objective value.'),
    16:('Wonderful. I would very much like to see it sometime.','0x52/82 politely expresses interest in viewing it. 拝見 is courteous,not evidence of a religious role,kinship,rank or a purchase offer.'),
    19:('Please do. By all means,come to my humble home.','0x93/147 warmly repeats the invitation and asks the companion to visit the speaker’s home. Preserve hospitality without inventing a mansion,estate,specific address or actual visit.'),
    22:('Still,with the recent craze for collecting ceramics,good pieces have become hard to obtain.','0x52/82 explicitly complains about availability of good pieces because of a recent collecting fashion. Preserve this source-explicit reported scarcity without extending it to every commodity,a numerical shortage,price rise or guaranteed profit.'),
    26:('Apparently people who do not understand their value have been buying them up just because they are fashionable.','0x93/147 disparages buyers who follow the fashion without appreciating value. Keep the reportedness in らしい and the character’s snobbery. Do not erase source-explicit buying-up behavior or make this narrator-confirmed market economics.'),
    30:('It is quite a nuisance.','0x52/82 agrees with annoyance. This complaint belongs to the collectors’ viewpoint,not an objective instruction to the player.'),
    34:('Exactly so.','0x93/147 firmly agrees. Keep the courteous register and shared self-satisfaction before the shift to the second pair.'),
    38:('Hey,look at those men over there.','0x68/104 directs0x71/113 to the first pair. Source explicitly says men. Keep the conversation shift and referent;bind both new speakers before assigning occupation,rank,relationship or a collective criminal title.'),
    42:('Those two together? What about them?','0x71/113 confirms which pair and asks why. They are a pair in the present scene;no kinship or romantic relationship is established.'),
    46:('The other day,they bought utterly worthless ceramics from me for an unbelievable price.','0x68/104 privately boasts about a completed sale benefiting the speaker. Worthless and unbelievable price are the seller’s claims,creating irony against the collector’s praise. No numeric price,proven valuation,specific vessel,forgery method or new completed transaction is supplied.'),
    49:('Well,those are good customers. Since we are short of money,shall we go talk to them?','0x71/113 identifies an opportunity and suggests approaching the buyers. 懐もさみしい concerns the speaking pair’s finances,not a claim that the collectors are now broke. お得意さん need not establish repeated previous transactions. Keep the proposed approach,not a completed second sale,threat or robbery.'),
    53:('Sounds good.','0x68/104 agrees to the proposed approach in a casual rough register. Do not invent a plan beyond speaking to the customers.'),
    57:('Settled,then. Let us go.','0x71/113 confirms the decision and urges movement. The next call begins the approach;no second purchase has occurred.'),
    61:('Siiir! / Excuse me,sir!','0x68/104 calls ingratiatingly to the prospective customer. だんなぁ is a sales approach/form of address here,not proof of employer,husband,master,kinship or additional rank. Localize the drawn-out familiarity naturally after binding the actual role.'),
    65:('Ceramics may become popular in Hamburg.','Separate impersonal FE forecasts possible popularity. Bind approved Ceramics/Hamburg terminology before comparison. Keep it distinct from characters’ claims of a collecting craze,scarcity and opportunistic sales;it does not establish the earlier location or earned boom.'),
}
if __name__=='__main__':
    assert not ROOT.exists();source=read(SOURCE);block=bytes.fromhex(source['clean_block_hex'])
    assert source['read_no_predecessor_English'] and source['physical_speech_objects']==17 and len(source['commands'])==20
    assert set(GLOSSES)=={r['source_record_index'] for r in source['records']}
    assert sorted({r['source_selector'] for r in source['records']})==[82,104,113,147,254]
    assert [(c['offset'],c['word'],c['whole_command_hex']) for c in source['commands'] if c['word']!=0x4000]==[
        (8,0xA000,'00a0ffff012a05a1'),(764,0xC200,'00c2'),(766,0,'00000000')]
    assert len(block)==772 and 8+struct.unpack_from('<H',block,4)[0]==770 and block[770:]==bytes(2)
    rows=[]
    for original in source['records']:
        row=deepcopy(original);gloss,note=GLOSSES[row['source_record_index']]
        row.update(fresh_source_gloss=gloss,whole_exchange_note=note);rows.append(row)
    ROOT.mkdir(parents=True);save(ROOT/'all17_clean_exchange_and_fresh_glosses.json',dict(
        source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),file_path='/data/SC2.DK4',block=189,records=rows,
        physical_speech_objects=17,source_commands=20,source_stored_bytes=772,source_logical_end=770,source_alignment_tailzeros=2,
        complete_exchange_progression='0x93/147 finally obtained ceramics and praises the piece;0x52/82 wants to see it;0x93/147 invites a home visit;both complain about the collecting craze,scarcity of good pieces and supposedly ignorant fashion buyers;0x68/104 points the pair out to0x71/113 and boasts they paid an unbelievable price for worthless ceramics;71 sees an opportunity while the speaking pair are short of money;both agree to approach;68 calls to a customer;a separate tentative Ceramics/Hamburg notice follows.',
        source_fact_boundaries=[
            'Bind hexadecimal selectors93,52,68,71 (decimal147,82,104,113) names/voices before assigning roles,rank,personal names or relationships. Both conversations and the shift between them must be reviewed together.',
            'Preserve the source-explicit recent acquisition,excellent-piece judgment,hospitality,reported collecting craze,availability complaint and hearsay about buying-up. Do not erase them to avoid source-supported economics.',
            'Preserve dramatic irony between collector praise and seller’s private worthless-ceramics/unbelievable-price boast. Neither viewpoint establishes narrator-certified value,authenticity,forgery,price or origin.',
            'The second pair’s short funds belong to the speakers,not the collector customers. The proposed approach and final hail do not establish a second completed sale,robbery,threat or recurring-customer history.',
            'The humble-home invitation does not establish a mansion or actual visit;だんなぁ does not establish kinship,employment or a new rank.',
            'The prospective impersonal Ceramics/Hamburg notice is separate from all character market claims and does not establish the earlier location or earned state.',
            'Preserve20 linear commands,17 speeches,A0008,C200764,end766 and two tailzeros. No B188 giyaman/Daimyo assumptions or old exact wrap exceptions transfer.',
        ],read_no_predecessor_English=True,new_review_credit=0,new_emulator_runs=0,
        source_native_terms_predecessor_comparison_localization_formatting_actual_and_release_gates_pending=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('B189:17 fresh clean-only glosses preserve both conversations,market claims,dramatic irony and the short-funds antecedent. No old English or credit.')
