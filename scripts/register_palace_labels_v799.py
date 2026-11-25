"""Register reviewed Palace menu labels after the entire V797 stack."""

from copy import deepcopy
from pathlib import Path

from dk4tool.patch import palace_label_boundaries as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=owned.ROOT
MANUSCRIPT=Path('translations/palace_menu_labels_manuscript_v1.json')
CONFIG=Path('translations/palace_label_boundaries_release_v1.json')


def main():
    assert not MANUSCRIPT.exists() and not CONFIG.exists()
    native=read(ROOT/'native_verification.json')
    assert len(native['full_font_planes'])==6
    for r in native['full_font_planes']:assert sha(Path(r['path']).read_bytes())==r['sha256']
    save(ROOT/'visual_review.json',{'all_six_full_font_planes_reviewed':True,
        'preview_sha256':native['preview_sha256'],'complete_first_and_final_letters_and_single_line_bounds':True,
        'actual_menu_playback_still_required':True})
    rom=NdsImage.open('out/all_routes_combined_v797_candidate.nds');arm=rom.read_file('/__arm9__.bin')
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    canonical=NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/__arm9__.bin')
    meanings=('Obtain a contract to trade in this city.','Contribute money to the city\'s military defenses.',
        'Use a Market letter of recommendation.','Use a Market letter of introduction.',
        'Lend one of the player\'s items to the ruler for display.','Take back an item the player lent to the ruler.')
    notes=('Keep the complete word and relocate it with its NUL.','Spell out military investment without the inherited abbreviation.',
        'The distinct letter type is a clear menu choice;replace the unnatural Use Recommend.',
        'Name the introduction letter distinctly from a recommendation;the menu selection submits it.',
        'Retain the idiomatic existing action Lend Item.',
        'Reclaim precisely requests return of the player\'s own loaned property. The Palace Lend Item context supplies the noun;do not imply returning someone else\'s borrowed item.')
    records=[]
    for i,(pointer,jp,en,meaning,note) in enumerate(zip(owned.OLD,owned.JAPANESE,owned.LABELS,meanings,notes,strict=True)):
        assert clean[pointer-owned.BASE:].split(b'\0',1)[0].decode('cp932')==jp
        records.append({'id':f'PALACE_MENU_{i}','english':en,'japanese':jp,'source_hex':jp.encode('cp932').hex(),
            'source_pointer':pointer,'menu_record':owned.TABLE+16*i,
            'speaker':'Native Palace menu action,not spoken dialogue',
            'context':'Original5D4FC initializer copies the six records.5D518..5D60C applies trading-share,Market-letter,headquarters and item-ownership eligibility. Corresponding original Palace branch action and mapped31 paragraphs establish meaning.',
            'source_meaning':meaning,'localization_note':note,
            'review':{g:True for g in ('source','context','localization','naturalness','formatting')},
            'status':'source-native-reviewed-experimental-actual-menu-pending'})
    save(MANUSCRIPT,{'format':'dk4-palace-menu-manuscript-v1','translation_policy':'natural-dialogue-v2',
        'encoder':'dialogue-relocatable-v1','target_locale':'en-US',
        'review_gates':['source','context','localization','naturalness','formatting'],
        'native_format':'single-line-ui-Cstring;complete reviewed six-pointer relocation map',
        'complete_source_ownership_map':str(ROOT/'source_ownership.json'),'records':records,
        'source_ARM9_sha256':sha(clean),'canonical_ARM9_sha256':sha(canonical),'current_ARM9_sha256':sha(arm)})
    target,proof=owned.plan(arm);assert target==(ROOT/'ARM9_RESEARCH_ONLY.bin').read_bytes()
    registry=read('translations/release_stack.json');assert 'all-routes-unified-v799' not in registry['profiles']
    inherited=deepcopy(registry['profiles']['all-routes-unified-v797']);frozen={}
    for v in inherited.values():
        if isinstance(v,str) and v.endswith('.json') and Path(v).exists():
            cfg=read(v);frozen[v]=sha(Path(v).read_bytes())
            for p,h in cfg.get('dependencies',{}).items():assert sha(Path(p).read_bytes())==h,p;frozen[p]=h
    save(ROOT/'frozen_prior_dependencies.json',frozen);save(ROOT/'release_stack_before_v799.json',registry)
    paths=[Path('dk4tool/patch/palace_label_boundaries.py'),Path('scripts/prepare_palace_labels_v799.py'),
        ROOT/'source_ownership.json',ROOT/'native_verification.json',ROOT/'visual_review.json']
    save(CONFIG,{'format':'dk4-palace-label-boundaries-v1','source_arm9_sha256':owned.SOURCE,
        'source_common_sha256':sha(rom.read_file('/COMMON/MESFILE.DK4')),'target_arm9_sha256':sha(target),
        'manuscript':str(MANUSCRIPT),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),
        'dependencies':{str(p):sha(p.read_bytes()) for p in paths}})
    assert owned.apply_release(arm,CONFIG)[0]==target
    registry['profiles']['all-routes-unified-v799']={**inherited,'palace_label_boundaries':str(CONFIG),
        'status':'experimental','description':'Full V797 plus six source-reviewed Palace menu labels and strict C-string terminators inside original text spans. Actual expanded menu verification pending.'}
    save('translations/release_stack.json',registry)
    assert all(sha(Path(p).read_bytes())==h for p,h in frozen.items())
    print('V799 Palace labels registered;all earlier profiles and dependencies preserved;actual menu pending.',flush=True)


if __name__=='__main__':main()
