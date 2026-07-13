#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
gh api graphql -f query='
{ user(login:"Ryandovalle"){
    followers{ totalCount } following{ totalCount }
    repositories(isFork:false, ownerAffiliations:OWNER){ totalCount }
    contributionsCollection{
      contributionCalendar{
        totalContributions
        weeks{ contributionDays{ contributionCount date } }
      }
    }
} }' > assets/data.json
echo "wrote assets/data.json"
