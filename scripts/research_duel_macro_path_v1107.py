"""Trace the complete original duel text path;correct the incomplete wrapper note."""
from pathlib import Path
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/duel_consumer_v1107')


def main():
    assert not ROOT.exists()
    old=read('work/analysis/duel_source_v1101/source_context_packet.json')
    clean=NdsImage.open('work/clean.nds');current_path=Path('out/all_routes_combined_v1105_candidate.nds')
    current=NdsImage.open(current_path);source=clean.read_file('/__arm9__.bin');arm=current.read_file('/__arm9__.bin')
    assert sha(current_path.read_bytes())==read(current_path.with_suffix('.manifest.json'))['candidate_sha256']
    cs=Cs(CS_ARCH_ARM,CS_MODE_ARM);fragments=[];calls={}
    for lo,hi in ((0xD458,0xD4D0),(0xDA28,0xDB5C)):
        assert source[lo:hi]==arm[lo:hi]
        instructions=list(cs.disasm(source[lo:hi],0x02000000+lo))
        for instruction in instructions:
            if instruction.mnemonic=='bl':calls[instruction.address]=int(instruction.op_str.lstrip('#'),16)
        fragments.append({'start':0x02000000+lo,'end':0x02000000+hi,'source_and_current_sha256':sha(source[lo:hi]),
            'instructions':[f'{i.address:08X} {i.mnemonic} {i.op_str}' for i in instructions]})
    for caller,target in ((0x0200D488,0x02053F4C),(0x0200D48C,0x0205528C),(0x0200D4A4,0x020CE898),
        (0x0200D4B8,0x0200DA28),(0x0200DA80,0x02053914),(0x0200DAC0,0x020D5404)):
        assert calls[caller]==target
    ROOT.mkdir(parents=True);proof=ROOT/'duel_text_consumer_source_path.json'
    save(proof,{'candidate':str(current_path),'candidate_sha256':sha(current_path.read_bytes()),
        'prior_source_inventory':'work/analysis/duel_source_v1101/source_context_packet.json',
        'original_equal_current_fragments':fragments,'exact_original_BL_call_targets':{hex(k):hex(v) for k,v in calls.items()},
        'original_pipeline':['D458 selects side actor/voice and loads native message','CE898 expands runtime opponent-name argument',
            'DA28 invokes53914 speech macro/literal processing','DA28 constructs its own text context and callsD5404 bitmap renderer'],
        'source_inventory_erratum':'V1101 not_ordinary_speech_53914_or_sighting_formatter was too broad. The distinct duel widget DOES call53914 atDA80. Its original parent/context/geometry still differs from ordinary speech and must be independently calibrated.',
        'one_logical_paragraph_before_macro_expansion_required':True,
        'literal_I_followed_by_authored_LF_remains_unsafe_here_as_in_existing_macro_contract':True,
        'no_claim_that_existing_sighting_wrapping_membership_automatically_covers_duel_parent':True,
        'complete_native_context_dimensions_palette_crop_glyphs_wrapping_and_UI_transitions_pending':True,
        'no_ROM_live_state_prose_or_completion_credit_change':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger=read(ledger_path)
    assert ledger['records_editorially_completed']==1196 and ledger['records_with_source_and_prose_pass']==1267
    ledger['duel_prose_v1103'].update(native_consumer_path_supplement=str(proof),
        macro_pipeline_note='DuelDA28 calls53914 beforeD5404. Keep prose one paragraph until original expansion;independent parent/bitmap calibration remains required.')
    ledger['next_duel_editorial_source_inventory_v1101']['consumer_macro_path_supplement']=str(proof)
    save(ledger_path,ledger)
    print('Original duel path verified:D458 -> CE898 -> DA28 ->53914 ->D5404. Source-note correction recorded;native geometry still pending.',flush=True)


if __name__=='__main__':main()
