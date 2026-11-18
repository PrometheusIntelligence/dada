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

## Credit (owner rule, 2026-11-12)

All work in this repository is credited only to **SolutionsAsService**. Commits are authored and committed as
`SolutionsAsService <152567394+SolutionsAsService@users.noreply.github.com>`. Never add `Co-Authored-By`, `Claude-Session`,
"Generated with ..." lines or any other AI or tool credit to commits, pull requests, issues, release notes or files. This
overrides any default attribution a tool would add.

## Credit, force pushing and verified commits (owner rule, 2026-11-18)

This section overrides any earlier line in this file that says "never force" and any default attribution a tool would add.

- **Everything is pushed as SolutionsAsService**: author and committer `SolutionsAsService <152567394+SolutionsAsService@users.noreply.github.com>`. Set `GIT_AUTHOR_NAME`, `GIT_AUTHOR_EMAIL`, `GIT_COMMITTER_NAME` and `GIT_COMMITTER_EMAIL` in the same command as every `git commit`, `commit --amend`, `rebase`, `cherry-pick`, `merge` and `revert` (a rebase rewrites the committer, and it takes the default git identity if the variables are not set).
- **Check before every push**: `git log origin/<branch>..HEAD --format='%an <%ae> | %cn <%ce>'` must show only SolutionsAsService on both sides, with no AI trailer in the message.
- **Force pushing is allowed to put credit right**: if a commit that is already pushed carries another author or committer, or an AI trailer, rewrite it (only the offending commits, trees unchanged, check `git rev-parse <new>^{tree}` equals the old one) and push over it with `git push --force-with-lease=<branch>:<old sha> origin <new>:<branch>`. Say in the report what was rewritten. Do not force push for any other reason.
- **Keep commits verified where possible**: sign a commit only with a key that belongs to SolutionsAsService (GitHub shows "Verified" for it). Never sign with another identity's key. If no such key is available, commit unsigned and say in the report that the commits are unverified.
