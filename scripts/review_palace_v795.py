"""Clean-source Palace glosses before natural American English paragraphs."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.context_palace_v795 import ROOT,ROM,IDS
from scripts.verify_village_wrap_v608 import read,save

MANUSCRIPT=Path('translations/palace_editorial_manuscript_v1.json')
# Each entry is source meaning,then localized English;layout remains unapproved.
LINES={
1146:('The city already contracts with many factions and cannot accommodate another.',"Unfortunately, this city already has contracts with several factions. There's no room for another."),
1147:('The city has an exclusive contract with the named faction leader and cannot contract with anyone else.',"This city has an exclusive contract with %s. We can't sign a contract with anyone else."),
1148:('There is no room in this city for another faction.',"Unfortunately, there's no room for another faction to trade in this city."),
1149:('The ruler agrees to trading in this city and states its minimum contract fee in gold coins.',"You wish to trade in this city? Very well. The minimum contract fee is %s gold coins."),
1150:('Further trade expansion here is not permitted;use the held Market letter in another city.',"I can't allow you to expand your trade here any further. Use that letter in another city."),
1151:('The ruler praises the addressed player for helping defend a city where they do not even have a trading contract.',"Ah, %s! It's generous of you to help defend this city when you don't even have a trading contract here."),
1152:('The player already monopolizes this city and should use the held Market letter in another city.',"You already have a monopoly on trade in this city. You should use that letter in another city."),
1153:('The ruler asks to see the Market letter of recommendation the player says they hold.',"What? You have a letter of recommendation from the Market? Let me see it."),
1154:('The ruler greets the addressed player and confirms their wish to help defend the city.',"Ah, %s! You wish to contribute to the city's defenses?"),
1155:('The ruler asks to see the Market letter of introduction the player says they hold.',"What? You have a letter of introduction from the Market? Let me see it."),
1156:('The ruler agrees to trading here after considering the request,and gives the minimum contract fee in gold coins.',"You'd like to trade here? Hmm... Very well. The minimum contract fee is %s gold coins."),
1157:('The permitted trade share depends on the contract fee paid;the ruler asks how much the player will pay.',"Your market share will depend on the contract fee you pay. How much will you offer?"),
1158:('The ruler is annoyed by the player backing out or failing to decide.',"Bah! Make up your mind."),
1159:('The ruler permits the player to trade in this city.',"Very well. You may trade in this city."),
1160:('The ruler praises the admirable intention and commendable contribution.',"Hmm. That's an admirable gesture. Very commendable."),
1161:('The player need not show off when they have so little money.',"Hmm... There's no need to show off when you have so little money."),
1162:('The player does not have enough money to pay the contract fee and should come back.',"You don't have enough money for the contract fee. Come back when you do."),
1163:('The ruler lets past grievances go and permits trade in this city.',"Let bygones be bygones. You may trade here."),
1164:('The player will lend a rare item for display in the ruler castle;the ruler asks which item.',"You'll lend one of your rare items for display in my castle? Which one will it be?"),
1165:('The ruler admires the fine item with delighted appreciation.',"Oh, what a magnificent piece! Truly splendid..."),
1166:('The ruler offers to pay the supplied gold-coin amount each month for that item and asks agreement.',"For that item, I can offer %s gold coins a month. Is that acceptable?"),
1167:('The ruler acknowledges taking the item into custody.',"Very well. It's in my care now."),
1168:('The ruler eagerly anticipates displaying the item and imagines everyone astonished.',"I can't wait to show it off. I can already picture everyone's astonishment!"),
1169:('The player wants to reclaim an item previously entrusted to the ruler;which should be returned?',"You'd like to reclaim something you lent me? Which item should I return?"),
1170:('The ruler reluctantly accepts the player taking back that particular item.',"You want that one back? Oh, very well..."),
1171:('The ruler agrees to return the item to the player.',"Very well. I'll return it to you."),
1172:('The ruler expresses disappointment.',"What a pity..."),
1173:('The city people seem to have become receptive because of the player contributions.',"Your contributions seem to have won over the people of this city."),
1174:('A letter of introduction is inadequate;the ruler might consider a letter of recommendation.',"Hmm... A letter of introduction won't do. With a letter of recommendation, I might consider it."),
1175:('The ruler trusts the player and permits increasing their trade share in this city.',"Yes, I can trust you. I'll allow you to increase your market share in this city."),
1176:('The ruler trusts the player and permits them to trade in this city.',"Yes, I can trust you. You may trade in this city.")}


def main():
    assert not MANUSCRIPT.exists() and tuple(LINES)==IDS
    context=read(ROOT/'native_context.json')
    assert {r['id'] for r in context['all31_original_message_call_fragments']}==set(IDS)
    packet=read('work/analysis/palace_editorial_v794/source_inventory.json')
    canonical=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    accepted=common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'),canonical.read_file('/__arm9__.bin'),clean=False)
    arguments={1147:'native_other_faction_leader_address_form',1151:'native_player_admiral_address_form',
        1154:'native_player_admiral_address_form',1149:'native_contract_fee_without_unit',
        1156:'native_contract_fee_without_unit',1166:'native_monthly_loan_payment_without_unit'}
    rows=[]
    for source in packet['rows']:
        n=source['id'];meaning,english=LINES[n]
        assert english==' '.join(english.split()) and english.isascii()
        assert bytes.fromhex(source['source_hex']).count(b'%s')==english.count('%s')==int(n in arguments)
        cases=[r for r in context['all31_original_message_call_fragments'] if r['id']==n]
        speakers=sorted({r['speaker'] for r in cases})
        ruler=context['ruler_role6_actor127'];minister=context['minister_role11_actor121']
        assert len(speakers)==1 and speakers[0] in (ruler,minister)
        speaker='Original Palace ruler NPC,building role6' if speakers[0]==ruler else 'Original Palace minister NPC,building role11'
        scene=('The original Palace contract/Market-letter,defense-contribution or treasure-loan branch selects this fixed message. '
            f'Original call fragments: {", ".join(hex(r["source_fragment"]) for r in cases[:4])}. '
            'V795 executes the original providers and stops before the dialogue wrapper. The actual Istanbul ruler is actor127 and minister121;the older role4 ruler assumption is superseded. '
            'Original prior/next branch messages,source capacity/fee conditions and item-return sequence determine context,not adjacent message storage. '
            'Market introduction flag0 and recommendation flag1 are distinct;flag2 means no letter. '
            'All names/amounts are original native arguments;no invented title,kinship or numeric conversion. Actual revised playback remains pending.')
        note='Natural American English,read in the original branch sequence. Preserve the ruler formal or minister administrative voice;one logical paragraph without padding or manual breaks.'
        if n in (1147,1151,1154):note+=' Use the supplied native form of address (such as Castor or Bergstrom),without inventing a rank,gendered honorific or faction suffix.'
        if n in (1150,1152,1153,1155,1174):note+=' Explicit letter references are supported by the native held-letter branch. Keep introduction and recommendation separate.'
        if n==1156:note+=' Replace the old positioned/padded four-row fee offer,which produced an actual extra blank page. Verify every expanded fee digit in native and actual presentation.'
        if n==1162:note+=' Correct the older reversal The fee is too high. The source condition is the wallet being below the calculated minimum fee.'
        if n==1166:note+=' The ruler pays the player monthly. Keep the original provided amount;all218 original item-price multiply/shift providers are verified independently.'
        decision='retain' if english==' '.join(source['current'].split()) else 'revise'
        rows.append({'id':f'COMMON_MESSAGE_{n}','message_id':n,'interaction_group':'Palace-contracts-Market-letters-defense-and-treasure-loans',
            'source_hex':source['source_hex'],'japanese':source['Japanese'],'source_reference':source['clean_reference'],
            'canonical_source_hex':accepted[n].text.hex(),'current_text_hex':source['current_hex'],'current_English':source['current'],
            'current_reference':source['current_reference'],'source_meaning':meaning,'english':english+'{PAD}',
            'speaker':speaker,'context':scene,'localization_note':note,'source_native_arguments':[arguments[n]] if n in arguments else [],
            'English_argument_source_indices':[0] if n in arguments else [],'decision':decision,
            'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False},
            'status':'source-context-prose-reviewed-native-layout-production-and-revised-playback-pending'})
    assert sum(r['decision']=='retain' for r in rows)==2
    pins=packet['source_pins']+[{'path':'out/raphael_natural_v2_accepted_base.nds','ROM_sha256':sha(Path('out/raphael_natural_v2_accepted_base.nds').read_bytes())}]
    save(MANUSCRIPT,{'format':'dk4-common-entry-manuscript-v1','translation_policy':'natural-dialogue-v2','encoder':'dialogue-fixed-v1',
        'target_locale':'en-US','file_path':'/COMMON/MESFILE.DK4','review_gates':['source','context','localization','naturalness','formatting'],
        'source_pins':pins,'native_context_proof':str(ROOT/'native_context.json'),'native_context_sha256':sha((ROOT/'native_context.json').read_bytes()),
        'records':rows,'status':'source-context-and-prose-only-draft','whole_batch_completion_credit':False,
        'remaining_gates':['Complete original paragraph routing for direct and yes/no Palace consumers','All real substitution layouts and independent complete fonts',
            'No-growth COMMON/runtime production integration and registered combined ROM','Exact clean-input patch','Actual revised contract,loan and normal return/startup samples'],
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('31 source/context/prose paragraphs reviewed:29 revised,2 retained. Native formatting/integration/revised gameplay still pending.',flush=True)


if __name__=='__main__':main()
