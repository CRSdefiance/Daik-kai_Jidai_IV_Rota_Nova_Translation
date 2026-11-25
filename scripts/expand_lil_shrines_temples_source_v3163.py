"""Expand the source packet to include all five three-option menus."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_Shrines_Temples_source_v3163')
OLD=Path('work/analysis/lil_Shrines_Temples_source_v3159/complete220_clean_current_native_context.json')
CHOICE=Path('work/analysis/lil_three_option_source_v3162/all5_three_option_clean_current_native_pointer_proof.json')
if __name__=='__main__':
    assert not ROOT.exists();doc=deepcopy(read(OLD));choice=read(CHOICE);assert choice['candidate_sha256']==doc['current_ROM_sha256'] and choice['source_context_sha256']==sha(OLD.read_bytes())
    for b in doc['blocks']:
        b['choices']=[o for o in choice['objects']if o['block']==b['block']]
        assert all(c['word']in(0x2200,) for c in b['all_clean_native_commands']if 0x2000<=c['word']<0x4000)
        assert sum(c['word']==0x2200 for c in b['all_clean_native_commands'])==len(b['choices'])
    doc.update(previous_source_packet=str(OLD),previous_source_packet_sha256=sha(OLD.read_bytes()),previous_source_packet_did_not_include15_three_option_labels=True,typed_choice_records=choice['records'],typed_choice_labels=15,typed_choice_objects=5,total_editorial_objects=235,source_choice_pointer_proof=str(CHOICE),source_choice_pointer_proof_sha256=sha(CHOICE.read_bytes()),all_2000_group_text_commands_in_selected_blocks_classified=True,
        whole_clean_exchange_context_and_older_English_comparison_pending=True,scope='Ten complete LilSC2B101-B110 exchanges with235source/current objects:164speech(134ordinary/30FE),56stored actor-style alternatives across8source4100objects/64slots,and15choice labels in5source2200menus. All421commands retain source/current shape;114relative sites/1140clean-current cases remainbound separately. Source4100 isactor-style dispatch,not a player menu. Source2200 isthree-option playerchoice with8byteheader andindices0/1/2;count/pointer proofs arenot fullselection/cancel/nativefont/geometry proof. Preserve source aliases,dynamic selectors,preambles,substitutions andall branches. Completecleancontext,oldEnglishcomparison,glosses/prose,currentconsumer/voice/macro/font/pagination/reference/representative/release gates remainpending. Earlier220objectpacket andinitial transcripts arepreserved asnonexhaustive predecessors;no neweditorialcredit.')
    assert len(doc['records'])+len(doc['typed_actor_style_records'])+len(doc['typed_choice_records'])==235
    doc['evidence'][str(OLD)]=sha(OLD.read_bytes());doc['evidence'][str(CHOICE)]=sha(CHOICE.read_bytes());doc['evidence'][str(Path(__file__))]=sha(Path(__file__).read_bytes())
    ROOT.mkdir(parents=True);save(ROOT/'complete235_clean_current_native_context.json',doc);print('Complete235source/current packet:164speech+56alternatives+15three-option labels;zeroeditorialcredit.')
