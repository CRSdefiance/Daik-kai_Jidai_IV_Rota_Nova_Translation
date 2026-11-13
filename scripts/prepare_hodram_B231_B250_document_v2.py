"""Add the route-level schema field without changing any prepared record or macro proof."""
from scripts.audit_story_glyph_consistency import load,save
from scripts.prepare_hodram_B231_B250_formatting_v1 import FORMATTING,OUT
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

DOCUMENT=OUT/'formatting_input_v2.json'
def main():
    assert not DOCUMENT.exists();doc=load(FORMATTING)
    assert 'file_path' not in doc and {r['file_path'] for r in doc['records']}=={'/data/SC1.DK4'}
    doc.update(file_path='/data/SC1.DK4',metadata_schema_source=str(FORMATTING),metadata_schema_source_sha256=digest(FORMATTING),
        all225_record_values_andmacro_proofs_unchanged=True)
    save(DOCUMENT,doc);print('Added route schema field; all 225 prepared records unchanged.')
if __name__=='__main__':main()
