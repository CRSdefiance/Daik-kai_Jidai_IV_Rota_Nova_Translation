"""Refine four clean-only drafts before any current-English exposure; retain originals."""
from pathlib import Path
from copy import deepcopy
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B253_B274_clean_20261110')
CHANGES={
    'B253_B264':{
        'DK4_MES_B259_R0091':('! Someone, shoot it!','Someone, shoot it!','The source exclamation is expressed by natural terminal punctuation, with no isolated leading mark.'),
        'SC3_B259_STYLE_1228_400':("Admiral! It's so cramped, we might shoot our friends!","Admiral! It's so cramped, we might shoot our own crew!",'Companions in this tactical situation are crew; friendship is not established.'),
        'SC3_B259_STYLE_2186_226':("It's not chasing us, so it must not've been hungry... What a relief.","It's not chasing us, so it must not have been hungry... What a relief.",'Avoid an ungainly double contraction while retaining the inference and relief.'),
    },
    'B265_B274':{
        'SC3_B269_STYLE_392_70':("It's so damn hot...","Man, it's hot...",'Keep the rough drawn-out complaint without adding profanity unsupported by this source.'),
    },
}

def main():
    for part,changes in CHANGES.items():
        src=ROOT/f'authored_{part}_v1.json';dst=ROOT/f'authored_{part}_v2.json';assert not dst.exists()
        doc=load(src);after=deepcopy(doc);found=set()
        for row in after['records']:
            if row[0] in changes:
                before,new,reason=changes[row[0]];assert row[2]==before
                row[2]=new;found.add(row[0])
        assert found==set(changes)
        after.update(previous_authored=str(src),previous_authored_sha256=digest(src),clean_only_amendments=[dict(id=k,before=v[0],after=v[1],reason=v[2]) for k,v in changes.items()])
        save(dst,after)
    print('Saved four clean-only refinements; original authored entries and part outputs preserved.')

if __name__=='__main__':main()
