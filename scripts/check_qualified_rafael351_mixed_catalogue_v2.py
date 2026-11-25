"""Check every one ofthe341 stored ordinary/style bodies through the original catalogue."""
from scripts.check_qualified_rafael_mixed_catalogue_v1 import source as previous,TEMPLATE
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    'len(rows)==len(items)==243':'len(rows)==len(items)==341',
    'all243_ordinary_andphysical_style_bodies_checked':'all341_ordinary_andphysical_style_bodies_checked',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-complete-full-buffer-catalogue-new341-bodies','exec'),globals())
