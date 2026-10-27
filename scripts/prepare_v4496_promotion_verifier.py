"""Derive the independent V4496 metadata/preservation auditor from V4445."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
source = ROOT/'scripts/verify_v4445_promotion.py'
target = ROOT/'scripts/verify_v4496_promotion.py'
assert not target.exists()
text = source.read_text(encoding='utf-8')
replacements = {
    'promote_v4445_checkpoint':'promote_v4496_checkpoint',
    'all-routes-unified-v4353':'all-routes-unified-v4445',
    'all_routes_unified_v4353':'all_routes_unified_v4445',
    'all_routes_unified_v4445':'all_routes_unified_v4496',
    'V4452':'V4512','v4452':'v4512','Unified V4445':'Unified V4496',
    'B174':'B175','lil_B174':'lil_B175',
    '== 549':'== 550',"'manifest_batches':549":"'manifest_batches':550",
    '(5800,5803,3686,2114)':'(5833,5836,3709,2124)',
    "'fresh_contextual_rereads':5800":"'fresh_contextual_rereads':5833",
    "'completed_contextual_reviews':5800":"'completed_contextual_reviews':5833",
    "'source_prose_reviews':5803":"'source_prose_reviews':5836",
    "'clean_source_speeches'] == 33":"'clean_source_speeches'] == 32",
    "'B174_uncredited_glosses':33":"'B175_uncredited_glosses':32",
}
# Longest-first simultaneous substitution avoids remapping the previous release twice.
for key in replacements:
    assert key in text, key
text = re.sub('|'.join(re.escape(k) for k in sorted(replacements,key=len,reverse=True)),
              lambda match:replacements[match.group()],text)
# The generic B174 label replacement ran simultaneously with the exact value key.
assert "'B175_uncredited_glosses':33" not in text
compile(text,str(target),'exec')
target.write_text(text,encoding='utf-8',newline='\n')
print(target.relative_to(ROOT))
