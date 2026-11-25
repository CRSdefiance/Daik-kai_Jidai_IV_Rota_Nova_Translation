"""Exercise the frozen formatter with actual changed inputs and profiles; no no-op failures count."""
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.lil_B218_retrospective_profile_v1 import contract,profile_for
from dk4tool.dialogue.lil_B218_retrospective_layout_v1 import encode_relocatable_dialogue,audit_relocatable_dialogue_record
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/retrospective_B218_policy_validation_v7849')
DOC=Path('translations/lil_B218_retrospective_layout_manuscript_v1.json')
if __name__=='__main__':
    assert not ROOT.exists();doc=read(DOC);d=contract();image=NdsImage.open(doc['current_ROM'])
    arm=image.read_file('/__arm9__.bin');block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[218]
    clean=IlnkContainer.parse(NdsImage.open('work/clean.nds').read_file('/data/SC2.DK4')).blocks[218]
    protected=[DOC,Path('translations/editorial_review_current_v1.json'),Path('translations/release_stack.json'),
        Path(doc['current_ROM']),Path('translations/lil_B218_retrospective_native_contract_v1.json'),
        Path('dk4tool/dialogue/lil_B218_retrospective_profile_v1.py'),Path('dk4tool/dialogue/lil_B218_retrospective_layout_v1.py')]
    before={str(p):sha(p.read_bytes()) for p in protected};positives=[];negatives=[]
    def reject(ident,label,original,changed,fn):
        assert original!=changed,(ident,label,'no-op')
        try:fn()
        except ValueError as e:
            negatives.append(dict(id=ident,label=label,before_sha256=sha(repr(original).encode()),
                after_sha256=sha(repr(changed).encode()),error=str(e),actual_changed_input=True))
        else:raise AssertionError((ident,label,'unexpected acceptance'))
    for row in doc['records']:
        ident=row['id'];binding=d['record_bindings'][ident];raw=bytes.fromhex(binding['compiler_source_hex']);text=row['english']
        p=profile_for(arm,block,ident);assert profile_for(arm,clean,ident)==p
        encoded=encode_relocatable_dialogue(raw,text,p);report=audit_relocatable_dialogue_record(raw,text,p)
        assert encoded.encoded.hex()==binding['compiled_hex']==row['proposed_compiled_hex']
        assert not any(i['severity'] in ['warning','error'] for i in report['issues'])
        positives.append(dict(id=ident,compiled_hex=encoded.encoded.hex(),QA=report,
            exact_original_clean_andcurrent_block_profiles_match=True))
        marker,body=text.split('}',1);marker+='}'
        bad_texts={
            'invented-family-claim':text+" She's my sister.",
            'invented-Camille-presence':text+" Camille was here.",
            'added-runtime-substitution':text+' {MACRO:FI}',
            'authored-line-break':text+'{LB}',
            'literal-line-feed':text+'\n',
            'authored-alignment':text+'{ALIGN:RIGHT}',
            'missing-first-visible-character':marker+body[1:],
            'missing-last-visible-character':text[:-1],
        }
        for label,value in bad_texts.items():reject(ident,label,text,value,lambda v=value:encode_relocatable_dialogue(raw,v,p))
        for label,value in {
            'wrong-source-selector':bytes([raw[0]^1])+raw[1:],
            'changed-final-source-byte':raw[:-1]+bytes([raw[-1]^1]),
        }.items():reject(ident,label,raw,value,lambda v=value:encode_relocatable_dialogue(v,text,p))
        lengths=dict(p.macro_ascii_lengths);lengths['FA']+=1
        bad_profiles={
            'unapproved-pagination':replace(p,max_lines=8),
            'broadened-speaker-set':replace(p,leading_speaker_bytes=p.leading_speaker_bytes|frozenset([3])),
            'changed-measured-macro-length':replace(p,macro_ascii_lengths=lengths),
            'unapproved-profile-name':replace(p,name=p.name+'-changed'),
            'changed-metrics-binding':replace(p,metrics_source=p.metrics_source+' changed'),
        }
        for label,value in bad_profiles.items():reject(ident,label,p,value,lambda v=value:encode_relocatable_dialogue(raw,text,v))
        bad_arm=bytes([arm[0]^1])+arm[1:]
        reject(ident,'wrong-runtime-image',arm,bad_arm,lambda:profile_for(bad_arm,block,ident))
        bad_block=bytes([block[0]^1])+block[1:]
        reject(ident,'wrong-source-block-header',block,bad_block,lambda:profile_for(arm,bad_block,ident))
    assert len(positives)==13 and len(negatives)==13*17
    assert before=={str(p):sha(p.read_bytes()) for p in protected}
    ROOT.mkdir(parents=True);save(ROOT/'13_positives221_actual_changing_policy_rejections.json',dict(
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),positive_records=positives,negative_cases=negatives,
        positive_count=13,negative_count=221,all_negative_inputs_actually_changed_andrejected=True,
        no_noop_schema_error_orwarning_waiver_counted=True,all_protected_ROM_policy_ledger_andregistry_bytes_unchanged=True,
        frozen_profile_geometry_source_macros_andcomplete_character_guards_enforced=True,
        sourcemeaning_family_character_macro_andmanual_layout_corruptions_rejected=True,
        negative_tests_are_offline_policy_checks_not_gameplay=True,new_credit=0,new_emulator_runs=0,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Retrospective B218 policy:13 positives/221 actual-changing guard rejections;no ROM/ledger/registry changes.')
