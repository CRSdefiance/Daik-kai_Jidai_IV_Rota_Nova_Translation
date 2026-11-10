"""Read each distinct observed lower-screen plane once; retain all original captures."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

original=Path('scripts/make_editorial_capture_sheets.py')
source=checked_text(original.read_text(encoding='utf-8'),{
    '        pictures=[]':'        pictures=[];coverage=[];seen={}',
    '            pictures.append((frame,filename,picture))':
    """            lower=sha(picture.crop((0,192,256,384)).tobytes())
            entry=dict(frame=frame,path=str(filename),PNG_sha256=sha(filename.read_bytes()),lower_RGB_sha256=lower)
            if lower in seen:
                entry['exact_lower_screen_reuse_of_frame']=seen[lower]
                coverage.append(entry);continue
            seen[lower]=frame;coverage.append(entry)
            pictures.append((frame,filename,picture))""",
    '            selected_images=[dict(frame=frame,path=str(filename),sha256=sha(filename.read_bytes()))':
        '            all_lower_screen_capture_coverage=coverage,duplicate_lower_planes_reused=len(coverage)-len(pictures),selected_images=[dict(frame=frame,path=str(filename),sha256=sha(filename.read_bytes()))',
    '        direct_review_pending=True,new_credit=0,producer_sha256=sha(Path(__file__).read_bytes())))':
        '        direct_review_pending=True,only_exact_same_run_lower_RGB_duplicates_reused=True,new_credit=0,producer_sha256=sha(Path(__file__).read_bytes())))',
})
exec(compile(source,__file__+'::distinct-observed-planes','exec'),globals())
