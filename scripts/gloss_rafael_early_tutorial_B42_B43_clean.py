"""Start the user-prioritized early tutorials with complete clean-source exchanges."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Rafael_early_tutorial_B42_B43_clean_20261104')
DECISIONS={
    42:dict(context='Julio teaches resupply before the first voyage. Rafael asks where to go;Claudio boasts about fighting pirates,Janus teases him,andJulio recommends learning through port visits,more companions andtrade. A loan reminder becomes a reassuring joke.',meanings=[
        'After hiring people,supplies are needed: specifically water andfood. These can be obtained at the port;Julio leads them there.',
        'The young port attendant handles resupply automatically,which makes it easy.',
        'If funds are insufficient,the attendant supplies only as much as the available money allows.',
        'Declining resupply allows changing the proportion of water andfood;Julio thinks this will not be needed very often.',
        'Without enough supplies,the sailors cannot perform at their normal strength andeven a good ship is wasted;watch the amount remaining.',
        'Julio asks whether preparations are complete.',
        'Rafael is excited to set sail at last,butasks what they should do after leaving.',
        'Claudio teases him for enthusiasm getting ahead of any actual plan.',
        'Janus laughs that he did not expect Claudio to be the one to say that.',
        'Claudio protests that Janus makes him sound as though he never thinks about anything.',
        'Janus offers a teasing apology: he is surprised Claudio has an idea,andasks to hear that excellent plan.',
        'Claudio hesitates,struggles to think,andthenhas an idea.',
        'He proposes defeating pirates,imagining himself boarding an enemy ship andknocking down one ruffian after another.',
        'Janus reacts wearily to this predictable proposal.',
        'Rafael says they should think more carefully;with their current abilities,no number of lives would be enough for such a plan.',
        'Julio agrees andrecommends first visiting ports around the Mediterranean,the North Sea andother regions.',
        'Visiting many ports will naturally build knowledge of sailing andtrade.',
        'Rafael agrees andsuggests finding more companions too.',
        'Julio agrees that their present group alone is somewhat worrying if they intend to keep voyaging.',
        'Claudio protests at the old man: why look at him while saying that?',
        'Janus calms him andagrees that more companions would be better.',
        'Julio reassures FI that he will surely be blessed with good companions.',
        'Rafael responds softly to Julio by name.',
        'Janus adds that more funds are needed to increase the number of ships andmaintain them.',
        'Julio says repeated trading in different places will naturally accumulate funds.',
        'Neglecting trade will only deplete their funds;Julio reminds them that it was originally his money andtells them to be careful.',
        'Rafael gratefully promises to earn the money properly andrepay Julio.',
        'Julio chuckles that he was joking andsays not to worry;he suggests they finally leave.',
    ],notes=['The port attendant is a young man,not a relative. Do not invent a free orautomatic-full-capacity resupply when funds are insufficient. Claudio’s boarding fantasy is not a tutorial recommendation. Julio’s loan reminder becomes a joke;do not imply he demands immediate repayment.']),
    43:dict(context='Julio moves from earlier preparation lessons to assigning navigator duties on the deck screen. He explains captain,sail handlers,helm,adjutant,surveying andlookout work,followed by the native X/menu instruction.',meanings=[
        'Julio checks that everything so far is understood,andintroduces information about navigators—that is,the companions themselves.',
        'Personnel assignment is one of an admiral’s important duties.',
        'To sail smoothly,assign each navigator a duty;do this while viewing the actual deck screen.',
        'First,FI is the captain. A ship cannot move without a captain,because it cannot decide where to go on its own.',
        'Sail handlers adjust the sails’ angle to the wind;as many sail handlers are required as there are masts.',
        'The helmsman is important when fast turns are needed.',
        'A skilled helmsman also allows the ship to move quickly into an advantageous position during naval combat.',
        'A ship can sail without an adjutant,buthaving one enables negotiation with other powers andreduces everyone’s fatigue during voyages;an unobtrusive butvaluable contributor.',
        'A surveyor enables automatic movement andshows the fleet’s latitude andlongitude;this is an important job.',
        'The lookout reports other ships’ affiliations andconditions in towns while at sea.',
        'These assignments should be enough for ordinary sailing;Julio encourages further experimentation.',
        'System instruction: press X andselect the deck screen from the menu;the deck screen allows changing navigator assignments.',
    ],notes=['Use exact approved UI duty/menu labels before localized approval. Preserve one sail handler per mast,adjutant optionality,both surveyor functions andlookout reports. The captain explanation contains the user’s reported First/font line;existing font repair must remain. No rank orrelationship is inferred from familiar honorifics.']),
}

if __name__=='__main__':
    output=ROOT/'complete_clean_meanings_before_English.json';checkpoint=ROOT/'clean_meanings_checkpoint_v1.json'
    assert not output.exists() and not checkpoint.exists()
    packet_path=ROOT/'clean_source_packet.json';packet=load(packet_path);rows=[]
    for g in packet['groups']:
        d=DECISIONS[g['block']];assert len(g['records'])==len(d['meanings'])
        assert not any(c['word'] in [0x2000,0x2100,0x2200,0x4100] for c in g['all_source_commands'])
        for r,meaning in zip(g['records'],d['meanings'],strict=True):
            assert bytes.fromhex(r['source_hex'])[1:].decode('cp932')==r['source_Japanese']
            rows.append(dict(**r,source_meaning=meaning,exchange_context=d['context'],native_identity_terms_localization_andformatting_pending=True,new_credit=0))
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger=load(ledger_path)
    keys={(r['file_path'],r['id']) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['record_keys']}
    assert len(rows)==40 and not keys & {(r['file_path'],r['id']) for r in rows}
    save(output,dict(records=rows,source_meanings=40,complete_exchanges=[42,43],source_fidelity_notes={k:v['notes'] for k,v in DECISIONS.items()},
        no_current_ROM_English_dialogue_extraction_in_this_intake=True,source_only_not_localized_English=True,no_all_historical_exposure_claim=True,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [packet_path,Path(__file__)]}))
    save(checkpoint,dict(source_meanings_saved=40,complete_blocks=[42,43],file_path='/data/SC0.DK4',ordinary_speeches=40,
        complete_clean_meanings=str(output),complete_clean_meanings_sha256=sha(output.read_bytes()),completed_overlap=[],completed_keys_checked=len(keys),
        source_selectors=sorted({r['source_selector'] for r in rows}),native_identity_terms_localized_drafts_comparison_anddisplay_pending=True,
        new_credit=0,full_goal_complete=False,guide_photos=False,user_priority='Rafael early game andall tutorials first'))
    print('Saved40 clean meanings for Rafael’s resupply,first-voyage andcrew-assignment tutorials;zero completed overlaps.')
