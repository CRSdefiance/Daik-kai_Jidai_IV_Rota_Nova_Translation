"""Apply the exact storage proof join to the two corrected company-substitution pages."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

TEMPLATE=Path('scripts/prepare_rafael557_storage_inputs_v1.py')
source=checked_text(TEMPLATE.read_text(encoding='utf-8'),{
    'Rafael557_storage_inputs_v1_20261105':'Rafael557_storage_inputs_v2_20261105',
    'rafael_B141_B160_formatting_manuscript_v3.json':'rafael_B141_B160_formatting_manuscript_v4.json',
    'Rafael557_automatic_plans_v10_20261105':'Rafael557_automatic_plans_v11_20261105',
    'Rafael557_native_final_v1_20261105':'Rafael557_native_final_v2_20261105',
    'Rafael557_body_visual_review_v1_20261105':'Rafael557_body_visual_review_v2_20261105',
    "len(body['directly_opened_readable_sheets'])==42":"len(body['directly_opened_readable_sheets'])==43",
})
if __name__=='__main__':exec(compile(source,__file__+'::same-storage-input-qualification-two-punctuation-pages','exec'),globals())
