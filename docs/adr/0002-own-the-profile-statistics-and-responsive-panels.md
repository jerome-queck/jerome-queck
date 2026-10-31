# ADR-0002: Own the profile statistics and responsive panels

Accepted 1 November 2026. Issue #12. Supersedes ADR-0001 only for the upstream repository card and published file list.

The Owner rejected the first graphical redesign. Its diagram repeated project membership,
and the upstream card reported somebody else's repository totals. A personal profile benefits
more from an original composition and precisely scoped authored contribution evidence.

Remove the GitHub Readme Stats card and its Action dependency. Standard-library Python now
produces desktop and mobile counter layouts from the same tuple and timestamp. The daily
workflow still publishes one complete generated snapshot after every generation step succeeds.
The five current payloads are counters.svg, counters-mobile.svg, calendar.svg, activity.svg and
README.md. Remove the legacy openclaw.svg file on the next successful publication.

Use GitHub's supported picture/source markup to select the mobile counter and mathematical
figure. Native text and links retain all meaning. Dynamic data stays on profile-data; authored
copy and figures stay on main. Existing privacy filters, pagination boundaries, metric
semantics, schedule, failure preservation and no-force-push rules remain unchanged.
