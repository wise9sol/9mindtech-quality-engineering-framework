Perform a full framework health check and update on the
QualiOps AI project. Do the following in order:

1. AUDIT — scan the entire project and report any Python
   syntax errors, broken imports, unregistered pytest
   markers, missing __init__.py files, and hardcoded
   credentials or URLs.

2. UPDATE — fix everything found automatically.

3. VERIFY — run py_compile on all compliance files, run
   --collect-only on all test suites, confirm counts match.

4. REPORT — summarize what was found, what was fixed, and
   what needs manual attention.

Show diffs before applying any changes.