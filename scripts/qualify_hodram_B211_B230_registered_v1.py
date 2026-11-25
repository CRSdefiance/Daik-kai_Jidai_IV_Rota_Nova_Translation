"""Reject malformed production scope inputs and verify caller purity on every failure."""
from copy import deepcopy
from dk4tool.patch.hodram_b211_b230_release_v1 import plan_release
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.prepare_hodram_B211_B230_registered_v1 import CONFIG,QUALIFICATION,ROOT

OUT=ROOT/'registered_semantic_checks_v1'

def main():
    assert not OUT.exists()
    conf=load(CONFIG);qualification=load(QUALIFICATION)
    assert digest(CONFIG)==qualification['config_sha256']
    image=NdsImage.open(conf['parent_ROM']);base=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    before,baseline=bytes(image.rom.save()),bytes(base.rom.save())
    OUT.mkdir();rows=[]
    cases=[('wrong-predecessor','parent_ROM_sha256','0'*64,'complete ordered predecessor'),
        ('missing-record','record_count',276,'complete unique membership'),
        ('wrong-speech-count','speech_count',269,'exact mixed speech, voice and menu membership'),
        ('wrong-caption-count','typed_choice_count',6,'exact mixed speech, voice and menu membership'),
        ('wrong-style-count','style_count',28,'exact mixed speech, voice and menu membership'),
        ('changed-control-only-scope','blocks',conf['blocks']+[222],'changed versus control-only blocks'),
        ('missing-scoped-name','scoped_name_count',22,'all scoped name decisions'),
        ('wrong-FE-scope','FE_count',3,'all four distinct FE panels')]
    for name,key,value,reason in cases:
        bad=deepcopy(conf);bad[key]=value;path=OUT/(name+'.json');save(path,bad)
        try:plan_release(image,base,path)
        except (ValueError,AssertionError) as exc:
            assert reason in str(exc),(name,str(exc))
            rows.append(dict(case=name,rejected=True,guard=str(exc),input_sha256=digest(path)))
        else:raise AssertionError('Accepted malformed production input: '+name)
        assert bytes(image.rom.save())==before and bytes(base.rom.save())==baseline
    save(OUT/'qualification.json',dict(config=str(CONFIG),config_sha256=digest(CONFIG),cases=rows,
        all8_production_scope_mutations_rejected=True,complete_parent_andbaseline_callers_unchanged=True,
        native_style_andmenu_semantic_negatives_reused_from_exact_proofs=True,new_credit=0,
        evidence={str(p):digest(p) for p in (CONFIG,QUALIFICATION,__file__)}))
    print('PASS eight malformed production inputs rejected by their intended guards; both complete caller ROMs unchanged.')

if __name__=='__main__':main()
