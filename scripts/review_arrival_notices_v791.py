"""Source-first drafts for independent arrival and relationship notices."""

from dataclasses import asdict
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.item_diplomacy_editorial import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_village_wrap_v608 import read, save

OUT=Path('translations/arrival_notices_editorial_manuscript_v1.json')
ROOT=Path('work/analysis/letter_delivery_v791')


def main():
    assert not OUT.exists()
    paths=['work/clean.nds','out/raphael_natural_v2_accepted_base.nds','out/all_routes_combined_v788_candidate.nds']
    roms=[NdsImage.open(p) for p in paths]
    components=[(r.read_file('/COMMON/MESFILE.DK4'),r.read_file('/__arm9__.bin')) for r in roms]
    clean,accepted= [common_message_entries(c,a,clean=n==0) for n,(c,a) in enumerate(components[:2])]
    current=current_entries(*components[2])
    proof=read(ROOT/'delivery_verification.json')
    assert proof['actual_formatting_defects'] and not proof['all_broader_gameplay_or_formatting_approval']
    descriptions={
        346:('The named recipient refused to accept the diplomatic letter.',
             '%s refused to accept the letter.',
             'Retain the existing complete natural sentence; do not imply refusal of a pact or truce after reading. This is refusal to receive the letter.'),
        347:('The diplomatic letter reached the named recipient.',
             'The letter has reached %s.',
             'State successful delivery without inventing acceptance of its proposal. Remove the stray R, which belongs to the independent next English notice rather than this clean Japanese message.'),
        348:('The friendship/relations score increased by the supplied amount.',
             'Relations improved by %s points.',
             'Use a complete standalone sentence and restore the missing leading R. Points makes the numeric score clear in natural English; retain the native amount unchanged. No manual wrapping or spacing.')}
    rows=[]
    for n,(meaning,english,note) in descriptions.items():
        assert clean[n].text.count(b'%s')==english.count('%s')==1
        ref=lambda e:{k:v for k,v in asdict(e).items() if k!='text'}
        source=clean[n].text.decode('cp932')
        context=('Original CScheme goodwill handler02093900: recipient refusal notice346 at02093B48; '
            'outgoing delivery notice347 at02093984; relationship increase348 at02093B04. '
            '346/347 receive the recipient faction virtual name;348 receives original numeric amount from020ABF50. '
            'Actual V788 17200/18000 display347 independently of348 at19200. Recipient dialogue and original native score changes occur between them. '
            'Native incoming/outgoing status presentation and automatic paragraph formatter must be verified before integration.')
        rows.append({'id':f'COMMON_MESSAGE_{n}','message_id':n,'interaction_group':'Diplomatic-arrival-and-relationship-notices',
            'source_hex':clean[n].text.hex(),'japanese':source,'source_reference':ref(clean[n]),
            'canonical_source_hex':accepted[n].text.hex(),'current_text_hex':current[n].text.hex(),
            'current_English':current[n].text.decode('cp932'),'current_reference':ref(current[n]),
            'source_meaning':meaning,'english':english+'{PAD}', 'speaker':'Original system courier-status narrator',
            'context':context,'localization_note':note,
            'source_native_arguments':['recipient_faction_name' if n!=348 else 'native_relationship_score_increase_without_unit'],
            'English_argument_source_indices':[0],'decision':'retain' if n==346 else 'revise',
            'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False},
            'status':'source-and-prose-reviewed-not-integrated-native-formatting-and-revised-gameplay-pending'})
    pins=[{'path':p,'ROM_sha256':sha(Path(p).read_bytes()),'COMMON_sha256':sha(c),'ARM9_sha256':sha(a)}
          for p,(c,a) in zip(paths,components,strict=True)]
    save(OUT,{'format':'dk4-common-entry-manuscript-v1','translation_policy':'natural-dialogue-v2',
        'target_locale':'en-US','encoder':'dialogue-fixed-v1','file_path':'/COMMON/MESFILE.DK4',
        'review_gates':['source','context','localization','naturalness','formatting'],'source_pins':pins,
        'records':rows,'actual_defect_proof':str(ROOT/'delivery_verification.json'),
        'status':'draft-no-ROM-change','whole_batch_completion_credit':False,
        'remaining_gates':['Original formatter/guard and substitutions','Native full font/layout/bounds',
            'Registered combined ROM and clean-input patch','Paired actual corrected arrival scenes and transitions'],
        'producer_sha256':sha(Path(__file__).read_bytes())})
    print('Three source/prose-reviewed notices drafted;formatting/integration/gameplay remain open.',flush=True)


if __name__=='__main__':main()
