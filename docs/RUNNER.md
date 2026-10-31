# Where CI runs

**All jobs run on GitHub-hosted runners (`ubuntu-latest`).** This repository is public.

The estate has self-hosted runners, and the `self-hosted-runners` standard lets one repository
variable (`RUNNER_LABELS`) move every job onto them. That standard is explicit about the default
for a public repository: **cloud, always**. Pull requests from outside contributors would
otherwise execute arbitrary code on a machine we own. So:

* every `runs-on` is the literal `ubuntu-latest`; there is no `vars.RUNNER_LABELS` switch here;
* release, Pages and secret-bearing jobs would stay on cloud even if a switch were added;
* the cost of cloud minutes is zero for a public repository.

If this repository is ever made private and a local runner is wanted, adopt the standard in full
(the `fromJSON(vars.RUNNER_LABELS || '["ubuntu-latest"]')` expression in the `gates` and `build`
jobs only, ephemeral registration, `timeout-minutes` on every job) and update this file in the
same change. Do not add the variable to the workflows without it.

## Timeouts and concurrency

| Workflow | Job | `timeout-minutes` | `cancel-in-progress` |
|---|---|---|---|
| build | gates / build | 5 / 30 | true |
| secret-scan | gitleaks | 10 | true |
| pages | build / deploy | 30 / 10 | false (never cancel a deploy) |
| release | build / release | 30 / 10 | n/a (tag-driven) |

## One manual step

GitHub Pages must be switched on once by a repository admin:
**Settings → Pages → Build and deployment → Source: GitHub Actions.** `configure-pages` cannot create
the site with a workflow token; without the click the Pages workflow fails at that step.
