"""Keep all repaired caption planes and report the two invalid ASCII baselines."""
from scripts import check_rafael_two_choice_display_v2 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous.source, {
    "args.out.mkdir(parents=True);planes=[];pictures=[]":
        "args.out.mkdir(parents=True);planes=[];pictures=[];corrupt_baselines=[]",
    "            for style in [1,15]:":
        """            if not label.isascii():
                assert version['version']=='current-padded-English'
                assert rows[index]['block']==178 and rows[index]['source_command_offset']==356
                assert label.strip()==('産es','札ecline')[index]
                corrupt_baselines.append(dict(index=index,exact_current_provider_text=label,
                    reason='The English caption pixel validator takes ASCII; the exact current mixed-glyph text was checked at the provider.'))
                continue
            for style in [1,15]:""",
    "    sheet=Image.new('RGB',(900,240),'#263238');draw=ImageDraw.Draw(sheet)":
        """    assert len(corrupt_baselines)==(2 if rows[0]['block']==178 else 0)
    assert len(planes)==8-2*len(corrupt_baselines)
    sheet=Image.new('RGB',(900,60*len(pictures)),'#263238');draw=ImageDraw.Draw(sheet)""",
    'complete_English_caption_style_planes=len(planes),compiler_negatives_rejected=negatives,':
        'complete_English_caption_style_planes=len(planes),omitted_corrupt_baseline_ASCII_planes=corrupt_baselines,compiler_negatives_rejected=negatives,',
})
exec(compile(source, __file__+'::same-typed-caption-checks-with-disclosed-baseline-exception', 'exec'), globals())
