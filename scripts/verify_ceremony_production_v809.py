"""Verify stored ceremony paragraphs through their final native consumers/fonts."""

from pathlib import Path

from PIL import Image

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_ceremony_common_v809 import ROOT,MANUSCRIPT,compiled
from scripts.prepare_recruitment_common_v772 import local_entries
from scripts.verify_arrival_native_v792 import prepared
from scripts.verify_ceremony_consumers_v808 import production_functions
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read,save


def main():
    plan=read(ROOT/'prospective_common_repack.json')
    arm=(ROOT/'COMBINED_ARM9_RESEARCH_ONLY.bin').read_bytes();common=(ROOT/'COMMON_RESEARCH_ONLY.bin').read_bytes()
    assert sha(arm)==plan['target_ARM9_sha256'] and sha(common)==plan['target_COMMON_sha256']
    entries=local_entries(plan['directory_sha256'])(common,arm,clean=False)
    rows={r['message_id']:r for r in read(MANUSCRIPT)['records']}
    ordinary,modal,ordinary_source,modal_source=production_functions()
    matrix=read('work/analysis/ceremony_layout_v807_name_bounds/native_layout_matrix.json')
    fonts=read('work/analysis/ceremony_layout_v807_name_bounds/research_report.json')
    kanji=NdsImage.open('out/all_routes_combined_v803_candidate.nds').read_file('/GRP/KANJI.FNT')
    cases=[];font_refs=[]
    for index,p in enumerate(matrix['cases']):
        n=p['id']
        if n==64:continue
        row=rows[n];assert entries[n].text==compiled(row)
        values=tuple(bytes.fromhex(v) for v in p['source_values_hex'])
        result=(modal if n in (289,290,291,293,294,295) else ordinary)(prepared(arm),row,values)
        assert result['formatted_hex']==p['formatted_hex'] and result['lines']==p['lines'] and not result['findings']
        pixels=raster(arm,bytes.fromhex(result['formatted_hex']),0x01FFCE40-0x02000000,size=(228,64),instruction_limit=1000000)
        assert pixels==independent_font(arm,kanji,result['lines'])
        f=fonts['complete_font_planes'][index];assert f['case_index']==index
        path=Path(f['path']);assert sha(path.read_bytes())==f['sha256']
        with Image.open(path) as image:assert [bool(p) for p in pixels]==[p<128 for p in image.convert('L').get_flattened_data()]
        font_refs.append(f)
        cases.append(dict(id=n,source_values_hex=p['source_values_hex'],formatted_hex=result['formatted_hex'],
            lines=result['lines'],findings=[],complete_stored_template_real_parent_and_independent_full_font_verified=True))
    assert len(cases)==len(font_refs)==201 and len({c['id'] for c in cases})==51
    save(ROOT/'production_layout.json',dict(ARM9_sha256=sha(arm),COMMON_sha256=sha(common),
        manuscript_sha256=sha(MANUSCRIPT.read_bytes()),native_layouts=201,full_font_planes=201,
        cases=cases,font_references=font_refs,findings=[],
        actual_native_parent_dispatch_used_not_ID348_proxy=True,
        original_templates_copied_by_native_7336_cases_separate_proof=True,
        ordinary_effective_program_sha256=sha(ordinary_source.encode()),modal_effective_program_sha256=sha(modal_source.encode()),
        source_retained_shared64_excluded_from_production_changes=True,
        actual_gameplay_and_registered_ROM_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('201 stored-template native layouts and201 complete fonts pass for all51 production paragraphs;actual scenes remain pending.',flush=True)


if __name__=='__main__':main()
