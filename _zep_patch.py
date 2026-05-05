#!/usr/bin/env python3
"""Re-apply Zep context patch after Hermes updates.

This script patches prompt_builder.py and run_agent.py to:
1. Auto-load Zep Cloud context at every session start
2. Inject ZEP_MEMORY_GUIDANCE into the system prompt

Run after each `hermes update` that might overwrite these files.

Usage:
    python3 ~/.hermes/scripts/zep_patch.py
"""

import os
import re

HERMES_HOME = os.path.expanduser("~/.hermes/hermes-agent")

def patch_file(filepath, replacements):
    """Apply find-replace patches to a file. Returns True if any patch was applied."""
    if not os.path.exists(filepath):
        print(f"  NOT FOUND: {filepath}")
        return False
    
    with open(filepath, "r") as f:
        content = f.read()
    
    original = content
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new, 1)
            print(f"  ✓ Patched: {os.path.basename(filepath)}")
        else:
            print(f"  ✗ Pattern not found in {os.path.basename(filepath)}")
    
    if content != original:
        with open(filepath, "w") as f:
            f.write(content)
        return True
    return False


def main():
    print("=== Zep Context Patch ===")
    
    # Patch 1: prompt_builder.py - Add import + ZEP_MEMORY_GUIDANCE + load function
    prompt_builder = os.path.join(HERMES_HOME, "agent", "prompt_builder.py")
    
    replacements_pb = [
        # Add subprocess import
        ('import threading\nfrom collections import OrderedDict\nfrom pathlib import Path',
         'import subprocess\nimport threading\nfrom collections import OrderedDict\nfrom pathlib import Path'),
    ]
    patch_file(prompt_builder, replacements_pb)
    
    # Patch 2: run_agent.py - Add ZEP_MEMORY_GUIDANCE import + injection
    run_agent = os.path.join(HERMES_HOME, "run_agent.py")
    
    replacements_ra = [
        ("SESSION_SEARCH_GUIDANCE, SKILLS_GUIDANCE,", "SESSION_SEARCH_GUIDANCE, SKILLS_GUIDANCE, ZEP_MEMORY_GUIDANCE,"),
    ]
    patch_file(run_agent, replacements_ra)
    
    print("\nDone! Restart Hermes for changes to take effect (/reset).")


if __name__ == "__main__":
    main()
