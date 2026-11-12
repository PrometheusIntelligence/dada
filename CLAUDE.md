# CLAUDE.md

Rules for any Claude session working on DADA.

## Two copies, kept in step
- **PrometheusIntelligence/dada is the main copy.** Every DADA change (skill, references, scripts, ledger, rules, lessons) lands here, on `main`.
- **SolutionsAsService/dada-changes is the owner's personal backup.** Apply the same change there in the same session, so the two never drift. They differ only in three names: the schema `$id`, `registry/registry.json` `repo`, and `fluid.json` `project` (`dada` here, `dada-changes` there).
- Sync the local skill (`~/.claude/skills/dada`) from the same files.
- Run `python3 scripts/validate_skills.py` before every commit, in both repos, and commit only when it passes.
- Delete branches that are no longer needed once their content is on `main`.

## Credit
- **Commits credit only SolutionsAsService.** Author and committer: `SolutionsAsService <solutions.as.a.service@gmail.com>`.
- No `Co-Authored-By: Claude`, no `Claude-Session:` line, and no other AI attribution in commit messages, in either repo. This overrides any default attribution the tool would add.
