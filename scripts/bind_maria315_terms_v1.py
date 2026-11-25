"""Bind four items,five commodities,three places and the established Proof convention."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

_prior=Path('scripts/bind_maria328_terms_v1.py').read_text(encoding='utf-8')
_start=_prior.index('    for offset, source, english in [')
_end=_prior.index('        row = field(offset,source,english)',_start)
source=checked_text(_prior,{
    'from scripts.meaning_maria328_clean_v1 import ROOT':"ROOT=Path('work/Maria_B286_B302_clean_20261110')",
    _prior[_start:_end]:"""    for offset, source, english in [
        (1172296,'錬金術の書','Alchemy Book'),(1174984,'六分儀','Sextant'),
        (1175464,'高麗青磁の香炉','Goryeo Incense Burner'),(1176112,'古代都市遺跡への地図','Ancient City Map')]:
""",
    "    location = field(1162288,'サンチャゴ大聖堂','Santiago Cathedral')":
        """    locations=[field(1192580,'サン＝ジョルジェ','Sao Jorge'),field(1196292,'ハバナ','Havana'),field(1422112,'グアム','Guam')]
    commodities=[field(p,j,e) for p,j,e in [(1437920,'金','Gold'),(1438220,'象牙','Ivory'),
        (1438496,'鉄砲','Guns'),(1438508,'大砲','Cannon'),(1438532,'甲冑','Armor')]]""",
    'locations=[location],short_Proof_UI_consumers=short,':'locations=locations,commodities=commodities,short_Proof_UI_consumers=short,',
    'body_Santiago_punctuation_variant_matches_native_location_identity=True,':
        'descriptive_celadon_qualifier_preserves_source_material_not_a_new_UI_title=True,commodity_plural_inflection_does_not_change_registered_identity=True,',
    'no_named_sword_lamp_cross_orrescuer_reward_invented=True,':'unnamed_rescuer_reward_andvillage_gift_not_named_from_unrelated_catalogue_data=True,',
    "for p in [current_path,item_path,prior_path,Path(__file__)]":"for p in [current_path,item_path,prior_path,Path('scripts/bind_maria328_terms_v1.py'),Path(__file__)]",
    'Bound six items,Santiago Cathedral,two short Proof UI consumers andexact registered Proofs of Conquest story anchor.':
        'Bound four items,five commodities,three places,two short Proof labels andexact registered narrative Proof anchor.',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-exact-installed-pointers-andunchanged-approved-story-anchor','exec'),globals())
