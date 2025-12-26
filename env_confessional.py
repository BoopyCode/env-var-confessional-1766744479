#!/usr/bin/env python3
# ENV Var Confessional - Where your environment variables come to confess their sins
# Usage: python env_confessional.py .env

import sys
import re
from collections import defaultdict

def main():
    if len(sys.argv) < 2:
        print("Usage: python env_confessional.py <env_file>")
        sys.exit(1)
    
    env_file = sys.argv[1]
    
    try:
        with open(env_file, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"\U0001F631 Confession rejected: {env_file} not found")
        return
    
    # Track sins
    sins = defaultdict(list)
    seen_vars = {}
    line_num = 0
    
    for line in lines:
        line_num += 1
        line = line.strip()
        
        # Skip empty lines and comments
        if not line or line.startswith('#'):
            continue
        
        # Find the sinner (variable name)
        match = re.match(r'^([A-Za-z_][A-Za-z0-9_]*)=', line)
        if not match:
            sins["malformed"].append(f"Line {line_num}: Can't parse '{line[:20]}...'")
            continue
        
        var_name = match.group(1)
        
        # Check for duplicate confessions
        if var_name in seen_vars:
            sins["duplicate"].append(f"Line {line_num}: '{var_name}' already confessed at line {seen_vars[var_name]}")
        else:
            seen_vars[var_name] = line_num
        
        # Check for empty confessions
        if '=' in line and line.split('=', 1)[1].strip() == '':
            sins["empty"].append(f"Line {line_num}: '{var_name}' has nothing to confess")
    
    # Deliver the verdict
    if not sins:
        print("\U0001F64F All variables absolved! Your .env is cleaner than a monk's conscience.")
        return
    
    print(f"\U0001F4A9 CONFESSIONAL REPORT for {env_file}")
    print("=" * 50)
    
    sin_types = {
        "duplicate": "\U0001F504 DUPLICATE SINS",
        "empty": "\U0001F4A3 EMPTY CONFESSIONS",
        "malformed": "\U0001F4A5 MALFORMED PRAYERS"
    }
    
    for sin_type, title in sin_types.items():
        if sin_type in sins:
            print(f"\n{title}:")
            for sin in sins[sin_type]:
                print(f"  - {sin}")
    
    total_sins = sum(len(v) for v in sins.values())
    print(f"\n\U0001F525 TOTAL SINS: {total_sins}")
    print("\nGo forth and sin no more! (Or at least document them)")

if __name__ == "__main__":
    main()
