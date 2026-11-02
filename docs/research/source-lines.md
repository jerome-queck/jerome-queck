# Source lines in selected public projects

GitHub language bytes describe file sizes. They cannot establish a line count: line length, comments, blank lines, encoding and language syntax differ. The profile therefore counts the actual public sources at each selected repository's recorded default-branch commit. It does not estimate a byte-to-line conversion.

## Counter and provenance

The collector uses [cloc 2.10](https://github.com/AlDanial/cloc/releases/tag/v2.10), a Perl program that counts physical code, comment and blank lines by language. The [official source](https://raw.githubusercontent.com/AlDanial/cloc/eb5cef64db2b2d4380f501568cc584b7cab4ba50/cloc) is pinned to commit `eb5cef64db2b2d4380f501568cc584b7cab4ba50` and SHA-256 `bf59272455172108072a0a106379f7509fd4349bdcfd85203bac038ccd286d83`. The tag resolves to that commit through GitHub's tag-ref API. The collector verifies the downloaded script before Perl runs it; the script remains in a temporary cache outside the repository. No global installation is required.

Each archive URL names a recorded 40-character commit SHA from the public repository metadata. Downloads use unauthenticated GitHub codeload URLs, so repository credentials cannot grant access to private sources. The collector accepts only the nine catalogue identities. An unavailable archive aborts collection.

Archives are data only. Extraction rejects absolute paths, traversal, duplicate paths, multiple roots and special files. Links are skipped. Bounds are 150 MiB compressed, 600 MiB expanded and 100,000 archive members per repository. Each network read has a 45-second timeout and the download checks a 90-second elapsed bound between reads. A counter process has a 90-second total timeout. Repository code is never run.

## What the number includes

The `code` count is cloc's physical code-line classification, including plain text, markup and configuration where cloc recognizes them. It includes every author at the recorded commit. It is neither Jerome's authored lines nor expertise, effort or code quality.

Rules are recorded in the snapshot with a SHA-256 manifest. Dependency/build directories are excluded by exact directory basename. `--no-autogen` excludes cloc's known generated filenames; it does not identify every generated file or match GitHub Linguist. Duplicate file contents count separately (`--skip-uniqueness`). Cloc's config file is disabled, and per-filter timeouts are disabled so they cannot silently discard slow files; the whole counter still has a hard process timeout.

Binary and unrecognized formats contribute no classified lines. `archive_files - classified files` is recorded as `uncounted_files`; it combines these formats with excluded files rather than pretending to distinguish them. Skipped links are separate. A successful cloc run emits `{}` when nothing is recognized; only that complete, successful output is accepted as an empty classification. Missing output, malformed JSON, mismatched sums, unexpected counter versions, counter errors and timeouts fail collection.

## Snapshot and display

Schema 4 adds `source_lines`: counter identity, rules, repository commit/archive provenance, per-repository language counts and exact aggregates. Every language has integer `files`, `code`, `comment` and `blank` counts. Repository totals and aggregate totals must agree. Schema 3 lacks this required source and is refused by the new renderer.

The visible ranking shows at most ten languages by descending code lines, with language name as the tie-breaker. A separate Other count sums remaining code lines. The native snapshot and generated README retain every language, exact counts, source commits and limitations. Comments, blanks and classified file totals come from the same counter pass.

Rendering consumes the saved snapshot and performs no tool or archive downloads. Collection and rendering must both complete before the generator writes any output. The fifteen published payload filenames and Git publication boundary are unchanged.

## Verification

`tests/test_source_lines.py` runs the pinned Perl counter on Python and JavaScript fixtures with known code, comments, blanks and duplicated contents. It checks dependency exclusion and a valid unrecognized-file empty result. Other cases reject unsafe archives, unselected repositories, inconsistent provenance, invalid numeric values, incomplete reports, malformed JSON, counter failures and process timeouts. Snapshot tests exercise native completeness, deterministic fifteen-file rendering and retention of existing output on failed input.
