#!/usr/bin/env bash
# Lists every member of the openpickleball organization with their activity
# in OPEN repositories over the last 90 days, and flags members with none.
#
# GOVERNANCE.md removes organization members with no activity for 90 days.
# This script only reports. It never changes membership.
#
# Run it locally as an organization owner:
#   gh auth refresh -h github.com -s read:org
#   bash scripts/membership-review.sh [days]
#
# Membership can be private, so do not paste the output into a public issue,
# pull request, or discussion.
set -euo pipefail

org="openpickleball"
days="${1:-90}"
since="$(date -u -d "-${days} days" +%Y-%m-%d)"

# The search API allows 30 requests a minute.
search_count() {
  local endpoint="$1" query="$2"
  sleep 2.5
  gh api -X GET "search/${endpoint}" -f q="${query}" --jq .total_count
}

printf 'Activity in %s since %s (%s days)\n\n' "$org" "$since" "$days"
printf '%-24s %-7s %8s %8s %8s %8s %8s %8s  %s\n' \
  member role commits prs merged issues reviews comments status

inactive=0
while IFS=$'\t' read -r login; do
  role="$(gh api "orgs/${org}/memberships/${login}" --jq .role)"
  commits="$(search_count commits "org:${org} author:${login} committer-date:>=${since}")"
  prs="$(search_count issues "org:${org} type:pr author:${login} created:>=${since}")"
  merged="$(search_count issues "org:${org} type:pr is:merged author:${login}")"
  issues="$(search_count issues "org:${org} type:issue author:${login} created:>=${since}")"
  reviews="$(search_count issues "org:${org} type:pr reviewed-by:${login} updated:>=${since}")"
  comments="$(search_count issues "org:${org} commenter:${login} updated:>=${since}")"
  status="active"
  if (( commits + prs + issues + reviews + comments == 0 )); then
    status="INACTIVE"
    inactive=$((inactive + 1))
  fi
  # merged counts all time: membership is earned with a first merged pull request.
  if (( merged == 0 )) && [[ "$role" != "admin" ]]; then
    status="${status}, no merged PR"
  fi
  printf '%-24s %-7s %8s %8s %8s %8s %8s %8s  %s\n' \
    "$login" "$role" "$commits" "$prs" "$merged" "$issues" "$reviews" "$comments" "$status"
done < <(gh api --paginate "orgs/${org}/members" --jq '.[].login')

printf '\n%s inactive member(s). "merged" is all time; other columns cover the last %s days.\n' "$inactive" "$days"
