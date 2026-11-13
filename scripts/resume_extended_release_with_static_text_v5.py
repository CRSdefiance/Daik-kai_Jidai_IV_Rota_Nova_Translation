"""Expose the callable original static_text stage to the registered chain."""
from scripts.registered_canonical_extension_resume_v5 import run_driver

def main():
    run_driver('static_text',__file__)

if __name__=='__main__':main()
