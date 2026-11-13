"""Persist fresh source meanings before comparison with predecessor English."""
from pathlib import Path
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/earlier_common_wraps_glosses_v4976')
SOURCE=Path('work/analysis/earlier_common_wraps_clean_v4975/clean_only_target_and_neighbor_records.json')
GLOSSES={
    682:('Business/the economy? We cannot worry about that now. I just want peace to come soon.',
        'A courteous distressed reply rejects ordinary business talk because of more pressing unrest. The source wishes for peace;verify the selecting branch before specifying a war.'),
    764:("You do not have enough money. This is not charity;without money,I cannot show it to you.",
        'A blunt colloquial refusal to show something because payment is insufficient. The object and service must come from the original caller;do not invent goods,prices,donations or a kinship/rank.'),
    774:('Oh,right! As thanks for selling the fashionable goods,I will write you a letter of introduction.',
        'An afterthought offers an introduction as thanks for the sale. The wording contains no large-quantity qualification;preserve the distinction from neighboring reward variants.'),
    775:('And as thanks for selling such a large quantity of fashionable goods,I will write you a letter of recommendation.',
        'A connective continuation thanks the player specifically for a large sale and offers a recommendation. Do not replace this with the introduction in774 or imply an already-issued letter before the offer.'),
}
if __name__=='__main__':
    assert not ROOT.exists();source=read(SOURCE);assert source['read_no_predecessor_English']
    rows=[{**r,'fresh_source_gloss':GLOSSES[r['message_ID']][0],'whole_context_note':GLOSSES[r['message_ID']][1]} for r in source['records'] if r['target']]
    assert [r['message_ID'] for r in rows]==[682,764,774,775]
    ROOT.mkdir(parents=True);save(ROOT/'four_clean_source_glosses_before_English.json',dict(source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),records=rows,
        read_no_predecessor_English=True,current_consumer_and_whole_exchange_reconciliation_pending=True,new_editorial_credit=0,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
