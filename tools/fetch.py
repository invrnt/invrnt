#!/usr/bin/env python3
"""Snapshot the public GitHub data the surface scenes imitate. Python standard library only.

Reads a token from GITHUB_TOKEN or GH_TOKEN and writes tools/data/github.json.
The build never needs the network; it only reads this snapshot.
"""

from datetime import datetime, timezone
from json import dumps, loads
from os import environ
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
TARGET = Path(__file__).parent / "data" / "github.json"
LOGIN = "invrnt"

QUERY = """
query($login:String!,$from:DateTime!,$to:DateTime!){
  user(login:$login){
    year:contributionsCollection{
      contributionCalendar{totalContributions weeks{contributionDays{date weekday contributionCount contributionLevel}}}
    }
    month:contributionsCollection(from:$from,to:$to){
      restrictedContributionsCount
      commitContributionsByRepository(maxRepositories:4){repository{nameWithOwner} contributions{totalCount}}
      repositoryContributions(first:3){totalCount nodes{occurredAt repository{nameWithOwner primaryLanguage{name color}}}}
      pullRequestContributionsByRepository(maxRepositories:2){repository{nameWithOwner}
        contributions(first:2){totalCount nodes{occurredAt pullRequest{title merged state}}}}
    }
  }
  bento:repository(owner:"invrnt",name:"bento"){
    defaultBranchRef{target{...on Commit{messageHeadline committedDate history{totalCount}}}}
    object(expression:"HEAD:"){...on Tree{entries{name type}}}
  }
}"""


def fetch():
    token = environ.get("GITHUB_TOKEN") or environ.get("GH_TOKEN")
    if not token:
        raise SystemExit("Set GITHUB_TOKEN or GH_TOKEN.")
    now = datetime.now(timezone.utc)
    start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    variables = {"login": LOGIN, "from": start.isoformat(), "to": now.isoformat()}
    request = Request("https://api.github.com/graphql", dumps({"query": QUERY, "variables": variables}).encode(),
                      {"Authorization": f"bearer {token}", "Content-Type": "application/json"})
    with urlopen(request, timeout=30) as response:
        payload = loads(response.read())
    if payload.get("errors"):
        raise SystemExit(dumps(payload["errors"], indent=2))
    data = payload["data"]
    calendar = data["user"]["year"]["contributionCalendar"]
    month = data["user"]["month"]
    levels = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2, "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}
    commit = data["bento"]["defaultBranchRef"]["target"]
    snapshot = {
        "generated": now.strftime("%Y-%m-%d"),
        "month": now.strftime("%B"),
        "year": now.year,
        "total": calendar["totalContributions"],
        "weeks": [[[d["date"], d["contributionCount"], levels[d["contributionLevel"]]] for d in week["contributionDays"]]
                  for week in calendar["weeks"]],
        "private": month["restrictedContributionsCount"],
        "commits": [[r["repository"]["nameWithOwner"], r["contributions"]["totalCount"]]
                    for r in month["commitContributionsByRepository"]],
        "created": [[n["repository"]["nameWithOwner"], (n["repository"]["primaryLanguage"] or {}).get("name", ""),
                     (n["repository"]["primaryLanguage"] or {}).get("color", ""), n["occurredAt"][:10]]
                    for n in month["repositoryContributions"]["nodes"]],
        "pulls": [[r["repository"]["nameWithOwner"], [[n["pullRequest"]["title"], n["pullRequest"]["merged"],
                   n["pullRequest"]["state"], n["occurredAt"][:10]] for n in r["contributions"]["nodes"]]]
                  for r in month["pullRequestContributionsByRepository"]],
        "bento": {"message": commit["messageHeadline"], "date": commit["committedDate"][:10],
                  "commits": commit["history"]["totalCount"],
                  "entries": [[e["name"], e["type"]] for e in data["bento"]["object"]["entries"]]},
    }
    TARGET.parent.mkdir(exist_ok=True)
    TARGET.write_text(dumps(snapshot, separators=(",", ":")) + "\n")
    print(f"{TARGET.relative_to(ROOT)}  {snapshot['total']:,} contributions, {len(snapshot['weeks'])} weeks")


if __name__ == "__main__":
    fetch()
