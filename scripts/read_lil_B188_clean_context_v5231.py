"""Read the glass-collection exchange from clean Japanese before earlier English."""
from pathlib import Path
from copy import deepcopy
import struct
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B188_clean_context_v5231')
SOURCE=Path('work/analysis/lil_B188_clean_inventory_v5230/all_clean_B188_speeches_before_predecessor_comparison.json')
GLOSSES={
    6:('Wonderful! It is truly a work of art.','82 enthusiastically praises the item. This is the character’s judgment,not proof of provenance or narrator-confirmed artistic status. Bind actor130 before choosing a name or rank.'),
    10:('Just as you say.','96 agrees with marked deference. Preserve the courteous register without inventing lordship,nobility,kinship,employment or a personal name;bind actor150 first.'),
    14:('For such a wonderful item,surely a well-known craftsman must have made it.','82 conjectures a famous maker from the quality. Keep the inference rather than supplying a named artisan,known origin or verified attribution.'),
    18:('Indeed,that is so.','96 courteously affirms the previous inference. No maker is named;do not add evidence,price or imported origin.'),
    22:('Hmm. I had no idea things like this were in fashion.','82 discovers an existing fashion from personal ignorance. Preserve surprise and temporal perspective;do not conflate this claim with the closing tentative system forecast.'),
    26:('What is this called?','82 asks for the unfamiliar item’s name. No particular vessel shape or use has been given.'),
    30:('It is giyaman (glass).','96 supplies the source-explicit term ギヤマン and parenthetical ガラス. Preserve the cultural/lexical distinction and glass gloss;do not confuse it with diamond or invent an etymology,import source,recipe or manufacturing method.'),
    34:('Hmm. Giyaman,you say.','82 echoes the unfamiliar term reflectively. This is recognition of a newly heard name,not expertise or a second material.'),
    38:('Very well. I will add it to my collection. Gather all the giyaman in town.','82 decides to collect and issues a sweeping order. Gather/collect is explicit;purchase,price,payment,museum,donation,shortage and a specific vase/cup shape are not. Preserve the character’s enthusiasm and excess without assigning rank.'),
    41:('Yes. As you wish.','96 formally accepts the instruction. This is compliance/intention,not proof that the items have already been collected or bought.'),
    45:('Glass may become popular in Osaka.','Separate null-actor FE remains prospective. Bind approved Glass/Osaka terms before comparison. This notice does not prove the earlier scene location,natural event activation or an earned boom.'),
}
if __name__=='__main__':
    assert not ROOT.exists();source=read(SOURCE);block=bytes.fromhex(source['clean_block_hex'])
    assert source['read_no_predecessor_English'] and source['physical_speech_objects']==11 and len(source['commands'])==14
    assert set(GLOSSES)=={r['source_record_index'] for r in source['records']}
    assert [(c['offset'],c['word'],c['whole_command_hex']) for c in source['commands'] if c['word']!=0x4000]==[
        (8,0xA000,'00a0ffff01293ba1'),(476,0xC200,'00c2'),(478,0,'00000000')]
    assert len(block)==484 and 8+struct.unpack_from('<H',block,4)[0]==482 and block[482:]==bytes(2)
    rows=[]
    for original in source['records']:
        row=deepcopy(original);gloss,note=GLOSSES[row['source_record_index']]
        row.update(fresh_source_gloss=gloss,whole_exchange_note=note);rows.append(row)
    ROOT.mkdir(parents=True);save(ROOT/'all11_clean_exchange_and_fresh_glosses.json',dict(
        source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),file_path='/data/SC2.DK4',block=188,records=rows,
        physical_speech_objects=11,source_commands=14,source_stored_bytes=484,source_logical_end=482,source_alignment_tailzeros=2,
        complete_exchange_progression='82 praises the item as art;96 agrees deferentially;82 infers a famous craftsman;96 affirms;82 admits ignorance of the fashion and asks the name;96 gives giyaman (glass);82 repeats it,decides to add it to a collection and orders all in town gathered;96 accepts;a separate tentative Glass/Osaka notice follows.',
        source_fact_boundaries=[
            'Bind selectors82130 and96150 names/voices before assigning rank,profession,relationship,age or personal names. Archaic/deferential register alone does not prove nobility or kinship.',
            'Praise and conjecture about a famous craftsman remain character claims without a named maker,verified attribution,origin or item shape.',
            'Preserve source-explicit giyaman (glass) and the unfamiliar-name echo. Do not invent an etymology or replace the material with diamond.',
            'Collecting and the order to gather all in town remain intentions;do not invent completed purchases,payment,price,museum,donation or actual shortage.',
            'The separate impersonal Glass/Osaka notice is prospective and does not establish the earlier location or earned fashion.',
            'All14 linear commands,A0008,C200476,end478 and two tailzeros remain;no B187 cough/remedy assumptions or B186 exact wrap exceptions transfer.',
        ],read_no_predecessor_English=True,new_review_credit=0,new_emulator_runs=0,
        source_native_terms_predecessor_comparison_localization_formatting_actual_and_release_gates_pending=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('B188:11 fresh clean-only whole-exchange glosses;giyaman/glass,conjecture and collection intentions distinct. No old English or credit.')
