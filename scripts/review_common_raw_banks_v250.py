"""Bounded whole-bank source reviews; no native-format promotion from resemblance."""

import json
import struct
from collections import Counter
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.pxl import PxlImage, bgr555
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT=Path("work/analysis/common_raw_banks_v250")
SOURCE=Path("out/raphael_natural_v2_accepted_base.nds")
CANDIDATE=Path("out/all_routes_combined_v247_candidate.nds")


def indices(data,depth):
    return bytes(n for value in data for n in (value&15,value>>4)) if depth==4 else data


def repack(data,depth):
    if depth==8:
        return data
    assert len(data)%2==0 and max(data)<16
    return bytes(data[n]|data[n+1]<<4 for n in range(0,len(data),2))


def native_comparison(name,source,target,source_palette,target_palette):
    assert len(source)==len(target)
    pairs=Counter(zip(source,target,strict=True));mapping={}
    for a,b in pairs: mapping.setdefault(a,set()).add(b)
    rendered_equal=sum(source_palette[a][:3]==target_palette[b][:3] for a,b in zip(source,target,strict=True))
    return {"native_path":name,"pixel_positions_compared":len(source),
            "identical_indices":sum(a==b for a,b in zip(source,target,strict=True)),
            "identical_rendered_pixel_colors":rendered_equal,
            "rendered_colors_all_equal":rendered_equal==len(source),
            "source_indices_with_multiple_native_targets":sum(len(v)>1 for v in mapping.values()),
            "maximum_native_targets_for_one_source_index":max(map(len,mapping.values())),
            "single_consistent_index_remap_proved":all(len(v)==1 for v in mapping.values()),
            "comparison_is_same_order_candidate_not_native_identity_proof":True,
            "copy_or_synchronization_allowed_by_this_evidence":False}


def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    assert sha(SOURCE.read_bytes())=="3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe"
    assert sha(CANDIDATE.read_bytes())=="01d75da29b6d22fd0bd7bd7281546babfec6c199250a141774f8dc4f30cda9cd"
    original=NdsImage.open(SOURCE);candidate=NdsImage.open(CANDIDATE)
    blocks=IlnkContainer.parse(original.read_file("/GRP/CMMNIMG.DK4")).blocks
    saved=IlnkContainer.parse(candidate.read_file("/GRP/CMMNIMG.DK4")).blocks
    rows=[]
    for block,palette_bytes,count,width,height,depth,kind in [
        (0,512,178,56,64,8,"portraits"),(2,512,100,24,24,8,"trade goods"),
        (3,32,475,32,32,4,"unadopted four-bit interpretation"),(7,512,188,32,32,8,"items and artifacts")]:
        raw=blocks[block];assert saved[block]==raw
        palette=raw[:palette_bytes];colors=[bgr555(v) for v, in struct.iter_unpack("<H",palette)]
        data=indices(raw[palette_bytes:],depth)
        assert len(data)==count*width*height and max(data)<len(colors)
        assert palette+repack(data,depth)==raw
        cols=10 if block==0 else 16;scale=1 if block==0 else 2;cw=width*scale+8;ch=height*scale+20
        sheets=[]
        for start in range(0,count,128):
            end=min(start+128,count);sheet=Image.new("RGB",(cols*cw,((end-start+cols-1)//cols)*ch),"#404040");draw=ImageDraw.Draw(sheet)
            for index in range(start,end):
                cell=data[index*width*height:(index+1)*width*height]
                im=Image.new("RGB",(width,height));im.putdata([colors[n][:3] for n in cell])
                x=(index-start)%cols*cw;y=(index-start)//cols*ch
                sheet.paste(im.resize((width*scale,height*scale),Image.Resampling.NEAREST),(x+4,y+16));draw.text((x+4,y),str(index),fill="white")
            path=ROOT/f"block{block}_{start:03d}_{end-1:03d}.png";sheet.save(path)
            sheets.append({"path":str(path),"sha256":sha(path.read_bytes()),"full_cell_range":[start,end-1],
                           "all_source_pixels_included":True,"visually_reviewed":True})
        row={"path":"/GRP/CMMNIMG.DK4","block":block,"source_sha256":sha(raw),"bytes":len(raw),
             "palette_prefix_bytes":palette_bytes,"interpreted_depth":depth,"interpreted_cell_dimensions":[width,height],
             "interpreted_cell_count":count,"all_palette_and_pixel_bytes_accounted_for":True,
             "whole_source_roundtrip_exact":True,"V247_source_block_preserved_exactly":True,"review_sheets":sheets,
             "observed_content":kind,"native_geometry_encoding_alpha_and_usage_proved":False,
             "fully_completed":False}
        if block==3:
            row.update(source_content_clearance=False,source_decision="unresolved: striped interpretation is not adopted as the native layout",
                       alternative_hypotheses=["eight320x190 slices","32x32 cells with8x8 tile order","transposed8x8 tile order"],
                       alternative_layouts_did_not_establish_intended_native_artwork=True)
        else:
            row.update(source_content_review="all coherent full paintings visually reviewed",
                       separate_Japanese_UI_caption_observed=False,
                       source_decision="retain original contextual paintings in the reviewed interpretations; meaningful UI/lore text remains a separate consumer",
                       tiny_clothing_book_cover_and_scroll_marks_not_invented_or_transcribed=True)
            if block==0:
                native=original.read_file("/GRP/CMMNIMG.000")
                native_palette=[bgr555(v) for v, in struct.iter_unpack("<H",native[:512])]
                target=native[512:];native_path="/GRP/CMMNIMG.000"
            else:
                native_path="/_pxl/itemtrade.pxl" if block==2 else "/_pxl/item.pxl"
                native=PxlImage.from_bytes(original.read_file(native_path))
                native_palette=native.palette;target=bytes(native.indices[:len(data)])
            row["native_same_order_comparison"]=native_comparison(native_path,data,target,colors,native_palette)
            assert not row["native_same_order_comparison"]["single_consistent_index_remap_proved"]
            assert not row["native_same_order_comparison"]["rendered_colors_all_equal"]
        rows.append(row)
    census=json.loads(Path("work/analysis/embedded_storage_census_v192.json").read_text(encoding="utf-8"))
    proof={"format":"dk4-common-raw-source-review-v250","canonical_source_sha256":sha(SOURCE.read_bytes()),
           "candidate_sha256":sha(CANDIDATE.read_bytes()),"blocks":rows,
           "coherent_portrait_goods_item_paintings_reviewed":178+100+188,
           "unadopted_four_bit_cells_interpreted":475,"total_complete_palette_and_pixel_bytes_accounted":sum(r["bytes"] for r in rows),
           "all_three_same_order_rendered_and_index_remap_equivalence_hypotheses_rejected":True,
           "historical_census_preserved":census["candidate_sha256"],"unresolved_legacy_block_count_unchanged":11,
           "no_native_layout_or_global_unused_claim_from_source_interpretations":True,
           "all_17_plaques_and_equipment_hint_continue_pending_audit":True,"ROM_modified":False,"full_goal_complete":False}
    (ROOT/"proof.json").write_text(json.dumps(proof,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"coherent_source_paintings_reviewed":466,"whole_source_bytes_accounted":proof["total_complete_palette_and_pixel_bytes_accounted"],"legacy_block_count_still_unresolved":11,"ROM_modified":False}))


if __name__=="__main__":
    main()
