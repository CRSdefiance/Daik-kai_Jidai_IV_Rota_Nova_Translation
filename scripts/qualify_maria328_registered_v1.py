"""Reject eight malformed production scopes without modifying either caller image."""
from copy import deepcopy
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.maria328_release_v1 import plan_release
from scripts.prepare_maria328_registered_v1 import CONFIG,QUALIFICATION,ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

def main():
    out=ROOT/'registered_semantic_checks_v1';assert not out.exists()
    conf=load(CONFIG);assert digest(CONFIG)==load(QUALIFICATION)['config_sha256']
    image,base=NdsImage.open(conf['parent_ROM']),NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    before,baseline=bytes(image.rom.save()),bytes(base.rom.save())
    cases=[('wrong-predecessor','parent_ROM_sha256','0'*64,'complete ordered predecessor'),
        ('missing-record','record_count',327,'unique complete source membership'),
        ('wrong-speech-count','speech_count',312,'exact source/native consumer scope'),
        ('wrong-caption-count','typed_choice_count',14,'exact source/native consumer scope'),
        ('wrong-style-count','style_count',23,'exact source/native consumer scope'),
        ('unowned-block','blocks',conf['blocks']+[96],'21 complete source exchanges'),
        ('missing-scoped-name','scoped_name_count',23,'all scoped name gates'),
        ('wrong-captain','captain',1,'exact current route and continuation owner')]
    out.mkdir();rows=[]
    for label,key,value,reason in cases:
        bad=deepcopy(conf);bad[key]=value;path=out/(label+'.json');save(path,bad)
        try:plan_release(image,base,path)
        except (ValueError,AssertionError) as exc:
            assert reason in str(exc),(label,str(exc));rows.append(dict(case=label,rejected=True,guard=str(exc),input_sha256=digest(path)))
        else:raise AssertionError('Accepted malformed scope: '+label)
        assert bytes(image.rom.save())==before and bytes(base.rom.save())==baseline
    save(out/'qualification.json',dict(config=str(CONFIG),config_sha256=digest(CONFIG),cases=rows,
        all8_production_scope_mutations_rejected=True,complete_parent_andbaseline_callers_unchanged=True,
        original_style_menu_andFE_rejections_bound_to_exact_proofs=True,new_credit=0,
        evidence={str(p):digest(p) for p in [CONFIG,QUALIFICATION,__file__]}))
    print('PASS8 production scope rejections; complete caller andcanonical images remain exact.')

if __name__=='__main__':main()
