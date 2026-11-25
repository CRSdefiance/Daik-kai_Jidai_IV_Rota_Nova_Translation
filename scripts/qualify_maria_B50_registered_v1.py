"""Reject malformed production scopes before staging the repeated-control transaction."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.maria_B50_release_v1 import plan_release
from scripts.prepare_maria_B50_registered_v1 import ROOT,CONFIG,QUALIFICATION
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

OUT=ROOT/'registered_semantic_checks_v1'
def main():
    assert not OUT.exists();conf=load(CONFIG);assert digest(CONFIG)==load(QUALIFICATION)['config_sha256']
    image=NdsImage.open(conf['parent_ROM']);base=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    before,baseline=bytes(image.rom.save()),bytes(base.rom.save());OUT.mkdir();rows=[]
    cases=[('wrong-predecessor','parent_ROM_sha256','0'*64,'complete ordered predecessor'),
        ('missing-source-record','record_count',15,'unique complete source membership'),
        ('wrong-speech-count','speech_count',15,'source/native panel membership'),
        ('missing-native-panel','native_commands',16,'source/native panel membership'),
        ('wrong-FE-owner','FE_owner_ID','DK4_MES_B50_R0036','exact single FE owner'),
        ('unowned-block','blocks',[50,51],'complete B50 source exchange'),
        ('missing-scoped-name','scoped_name_IDs',[3,10,28],'four relevant scoped identities'),
        ('wrong-captain','captain',1,'current Maria context')]
    for label,key,value,message in cases:
        wrong=deepcopy(conf);wrong[key]=value;path=OUT/(label+'.json');save(path,wrong)
        try:plan_release(image,base,path)
        except (ValueError,AssertionError) as exc:
            assert message in str(exc),(label,str(exc));rows.append(dict(case=label,rejected=True,guard=str(exc),input_sha256=digest(path)))
        else:raise AssertionError('Accepted '+label)
        assert bytes(image.rom.save())==before and bytes(base.rom.save())==baseline
    save(OUT/'qualification.json',dict(config=str(CONFIG),config_sha256=digest(CONFIG),cases=rows,
        all8_production_scope_mutations_rejected=True,complete_parent_andbaseline_callers_unchanged=True,
        seven_native_FE_insertion_rejections_bound_in_frozen_research=True,new_credit=0,
        evidence={str(p):digest(p) for p in [CONFIG,QUALIFICATION,Path(__file__)]}))
    print('PASS8 production scope rejections;seven insertion rejects retained;caller images unchanged.')
if __name__=='__main__':main()
