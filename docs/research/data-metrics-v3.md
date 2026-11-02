# Public data metrics, schema 3

The profile adds three different views rather than repeating contribution totals. Every value derives from the saved public input. Collection finishes before rendering, and rendering finishes before output files are written. A source failure retains the previous publication.

## Activity mix

`calendar_kinds` contains exactly `commits`, `issues`, `pull_requests`, `reviews` and `repositories`. These partition the same records as `calendar_days`, from 1 July 2026 through the collection's UTC date. Their sums must match. Commits sum GitHub's `commitCount`; the other kinds count contribution records. These are GitHub qualifying contribution records, not every Git object or every hour worked.

The collector reuses its existing paginated contribution traversal. Private repositories and restricted contributions are removed before a record identity or count is retained. Public issue, PR and review IDs identify records; a commit contribution is identified by repository ID and occurrence timestamp. Repository creations use repository ID. Repeated public records abort collection rather than inflate totals. The contribution's `resourcePath` is not a unique identity; GitHub returns the same overview path for separate contributions.

## Merged patch footprint

`change_footprint(records)` returns `prs`, `additions`, `deletions` and `file_changes` for `MERGED` upstream PRs only, across all time. Inputs are GraphQL `PullRequest.additions`, `deletions` and `changedFiles`. These are current PR patch statistics, summed over merged PRs, including all coauthors and generated code. File changes count a file again in each PR. The total is neither distinct files nor personal lines of code, effort, quality or impact.

The upstream search covers authored public PRs outside both owned namespaces, `jerome-queck` and `Jerome-Group`. The collector verifies public visibility, author, repository owner, identity, state and timestamps. Pagination must advance, reported result counts must remain stable, duplicate PR IDs fail, and results above GitHub's complete 1,000-result search bound fail. Missing, negative or boolean patch statistics fail rather than become zero.

## Open proposal age

`open_pr_ages(records, observed_to)` returns `repo`, `number`, `url` and integer `days` for `OPEN` upstream PRs. Age is the number of completed 24-hour periods between PR creation and the saved observation endpoint. Timezone-aware timestamps determine UTC elapsed time. The wall clock at rendering is never consulted. Creation must precede the latest update, which must not exceed observation. Merged or closed timestamps on an open PR fail.

Age describes time since opening. It does not establish that a proposal awaits review, that maintainers have taken no action, or how much work it required. Each row links its actual PR number.

## Snapshot compatibility

Schema 3 requires all five activity kinds and all three patch fields. Schema 2 snapshots cannot supply them and are rejected explicitly. Missing sources are unavailable input, not measured zero. A valid empty public result remains zero. The native Markdown contains all kind totals, patch totals and definitions, each open age, complete PR titles and source links, and both observation endpoints.

The publication payload remains the existing 15 filenames. No workflow copy step is added. The compositor can consume the new saved fields and pure helpers without a new API query.

## Retained public observation

`tests/fixtures/public-metrics-v3.json` retains the complete upstream PR result and calendar partition observed on 2 November 2026, from 13:54:48 to 13:57:04 UTC. The July-to-November calendar partitions into 1,650 commit contributions, 1,346 issues, 1,314 pull requests, 11 reviews and 15 repository creations, totaling 4,336. The upstream result has 18 PRs across three repositories: six merged, eleven open and one closed without merge. Merged patch totals are 753 additions, 264 deletions and 96 file changes. Open ages are one proposal at two completed days, nine at one day and one at zero days. These are retained observations, not continuously current facts.
