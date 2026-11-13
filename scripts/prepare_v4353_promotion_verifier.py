"""Preserve the prior verifier and derive the next checkpoint with exact keys."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
source = ROOT/'scripts/verify_v4303_promotion.py'
target = ROOT/'scripts/verify_v4353_promotion.py'
assert not target.exists()
text = source.read_text(encoding='utf-8')
changes = {'promote_v4303_checkpoint':'promote_v4353_checkpoint',
    'all_routes_combined_v4303':'all_routes_combined_v4353',
    'B171':'B172','v4331':'v4392','V4331':'V4392','Unified V4303':'Unified V4353'}
for old in changes:
    assert old in text, old
text = re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m[0]],text)
text = text.replace("pending['B172_actual_gameplay_coverage']","pending['B172_actual_gameplay_coverage_approved']")
numbers = {'546':'547','5725':'5762','5765':'5792','3635':'3659','2090':'2103','5762':'5789','37':'27','24':'19','13':'8'}
text = re.sub(r'(?<!\d)(?:'+'|'.join(numbers)+r')(?!\d)',lambda m:numbers[m[0]],text)
compile(text,str(target),'exec')
target.write_text(text,encoding='utf-8',newline='\n')
print('prepared V4353 promotion verifier')
