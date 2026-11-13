"""Append direct reviews for the final remaining exchanges and two clause refinements."""
import argparse
from scripts.meaning_maria328_clean_v1 import ROOT
from scripts.record_maria328_visual_review_v1 import journal

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--blocks',type=int,nargs='*',default=[])
    ap.add_argument('--clause-refinements',action='store_true');args=ap.parse_args()
    out=ROOT/'visual_reviews_v1';assert out.exists()
    for block in args.blocks:journal(block,ROOT/'selected_review_sheets_v2',out)
    if args.clause_refinements:
        journal(88,ROOT/'native_final_v2',out)
        journal(77,ROOT/'telescope_native_v1',out)

if __name__=='__main__':main()
