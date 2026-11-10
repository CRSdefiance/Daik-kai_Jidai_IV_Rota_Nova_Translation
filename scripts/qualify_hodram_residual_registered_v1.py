"""Reject eight malformed SC1 scopes and six malformed surname policies without caller mutation."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.hodram_residual_release_v2 import plan_release
from dk4tool.patch.registered_owned_name_fields_v2 import plan_release as plan_names
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.prepare_hodram_residual_registered_v2 import CONFIG,QUALIFICATION,ROOT
from scripts.prepare_hodram_residual_surnames_v1 import CONFIG as NAME_CONFIG

OUT=ROOT/'registered_semantic_checks_v1'

def main():
    assert not OUT.exists();conf=load(CONFIG);assert digest(CONFIG)==load(QUALIFICATION)['config_sha256']
    image=NdsImage.open(conf['parent_ROM']);base=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    before,baseline=bytes(image.rom.save()),bytes(base.rom.save());OUT.mkdir();rows=[]
    cases=[('wrong-predecessor','parent_ROM_sha256','0'*64,'complete ordered predecessor'),
        ('missing-record','record_count',393,'complete unique membership'),
        ('wrong-speech-count','speech_count',387,'exact mixed speech, voice and menu membership'),
        ('wrong-caption-count','typed_choice_count',5,'exact mixed speech, voice and menu membership'),
        ('wrong-style-count','style_count',46,'exact mixed speech, voice and menu membership'),
        ('changed-unowned-scope','blocks',conf['blocks']+[42],'changed versus control-only blocks'),
        ('missing-scoped-name','scoped_name_count',41,'all42 names reviewed'),
        ('wrong-FE-scope','FE_count',15,'all16 FE consumers')]
    for label,key,value,reason in cases:
        bad=deepcopy(conf);bad[key]=value;path=OUT/(label+'.json');save(path,bad)
        try:plan_release(image,base,path)
        except (ValueError,AssertionError) as exc:
            assert reason in str(exc),(label,str(exc));rows.append(dict(case=label,rejected=True,guard=str(exc),input_sha256=digest(path)))
        else:raise AssertionError('Accepted malformed scope: '+label)
        assert bytes(image.rom.save())==before and bytes(base.rom.save())==baseline
    names=load(NAME_CONFIG);ref=load(ROOT/'mixed_research_v2/research_reference.json')
    story=NdsImage.open(ref['story_only_research_ROM']);story_before=bytes(story.rom.save());name_rows=[]
    for label in ['wrong-name-parent','missing-name-policy','wrong-full-name','missing-actual-header','zero-header-minimum','wrong-policy-actor']:
        bad=deepcopy(names)
        if label=='wrong-name-parent':bad['parent_ROM_sha256']='0'*64;reason='exact complete predecessor'
        elif label=='missing-name-policy':bad['actual_policy'].pop();reason='whole reviewed field membership'
        elif label=='wrong-full-name':bad['actual_policy'][0]['full_name']='Incorrect Name';reason='reviewed complete full-name spelling'
        elif label=='missing-actual-header':bad['actual_policy'][0]['minimum_headers']=999;reason='complete actual changed progressive name'
        elif label=='zero-header-minimum':bad['actual_policy'][0]['minimum_headers']=0;reason='complete actual changed progressive name'
        else:bad['actual_policy'][0]['actor']=56;reason='individual source andfield binding'
        path=OUT/(label+'.json');save(path,bad)
        try:plan_names(story,path)
        except (ValueError,AssertionError) as exc:
            assert reason in str(exc),(label,str(exc));name_rows.append(dict(case=label,rejected=True,guard=str(exc),input_sha256=digest(path)))
        else:raise AssertionError('Accepted malformed name policy: '+label)
        assert bytes(story.rom.save())==story_before
    save(OUT/'qualification.json',dict(config=str(CONFIG),config_sha256=digest(CONFIG),cases=rows,
        all8_production_scope_mutations_rejected=True,name_config=str(NAME_CONFIG),name_config_sha256=digest(NAME_CONFIG),name_cases=name_rows,
        all6_registered_surname_policy_mutations_rejected=True,complete_parent_andbaseline_callers_unchanged=True,
        original8_owned_field_rejections_and63_style_rejections_reused_from_exact_proofs=True,new_credit=0,
        evidence={str(p):digest(p) for p in [CONFIG,QUALIFICATION,NAME_CONFIG,Path(__file__)]}))
    print('PASS8 production scope and6 surname-policy rejections; complete caller ROMs unchanged.')

if __name__=='__main__':main()
