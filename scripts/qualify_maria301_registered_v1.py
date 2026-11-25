"""Reject malformed production scopes while preserving the complete caller images."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.maria301_release_v2 import plan_release
from scripts.prepare_maria301_registered_v2 import CONFIG,QUALIFICATION,ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

OUT = ROOT/'registered_semantic_checks_v1'


def main():
    assert not OUT.exists(); conf = load(CONFIG)
    assert digest(CONFIG) == load(QUALIFICATION)['config_sha256']
    image,base = NdsImage.open(conf['parent_ROM']),NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    before,baseline = bytes(image.rom.save()),bytes(base.rom.save())
    cases = [
        ('wrong-predecessor','parent_ROM_sha256','0'*64,'complete ordered predecessor'),
        ('missing-record','record_count',300,'complete unique membership'),
        ('wrong-speech-count','speech_count',298,'exact mixed speech, voice and menu membership'),
        ('wrong-caption-count','typed_choice_count',1,'exact mixed speech, voice and menu membership'),
        ('wrong-style-count','style_count',6,'exact mixed speech, voice and menu membership'),
        ('unowned-block','blocks',conf['blocks']+[33],'changed versus control-only blocks'),
        ('missing-scoped-name','scoped_name_count',35,'all36 scoped name reviews'),
        ('wrong-captain','captain',1,'current Maria context'),
    ]
    OUT.mkdir(); rows = []
    for label,key,value,reason in cases:
        bad = deepcopy(conf);bad[key] = value;path = OUT/(label+'.json');save(path,bad)
        try:plan_release(image,base,path)
        except (ValueError,AssertionError) as exc:
            assert reason in str(exc),(label,str(exc))
            rows.append(dict(case=label,rejected=True,guard=str(exc),input_sha256=digest(path)))
        else:raise AssertionError('Accepted malformed scope: '+label)
        assert bytes(image.rom.save()) == before and bytes(base.rom.save()) == baseline
    save(OUT/'qualification.json',dict(config=str(CONFIG),config_sha256=digest(CONFIG),cases=rows,
        all8_production_scope_mutations_rejected=True,complete_parent_andbaseline_callers_unchanged=True,
        original_style_andmenu_rejections_bound_to_exact_proofs=True,new_credit=0,
        evidence={str(p):digest(p) for p in [CONFIG,QUALIFICATION,Path(__file__)]}))
    print('PASS8 production scope rejections; caller andcanonical images remain exact.')


if __name__ == '__main__':main()
