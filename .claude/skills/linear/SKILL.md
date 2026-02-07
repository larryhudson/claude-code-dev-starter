# Linear GraphQL API

You can query and mutate Linear data using the `LINEAR_ACCESS_TOKEN` environment variable and `curl`.

## Search Issues

```bash
curl -s -X POST \
  -H "Authorization: $LINEAR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ issueSearch(query: \"YOUR_SEARCH\", first: 10) { nodes { identifier title state { name } assignee { name } } } }"}' \
  https://api.linear.app/graphql | jq '.data.issueSearch.nodes'
```

## Get a Specific Issue

```bash
curl -s -X POST \
  -H "Authorization: $LINEAR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ issue(id: \"ISSUE_ID\") { identifier title description state { name } assignee { name } labels { nodes { name } } comments { nodes { body user { name } createdAt } } } }"}' \
  https://api.linear.app/graphql | jq '.data.issue'
```

## List Team Issues

```bash
curl -s -X POST \
  -H "Authorization: $LINEAR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ issues(filter: { team: { key: { eq: \"TEAM_KEY\" } }, state: { type: { in: [\"started\", \"unstarted\"] } } }, first: 20) { nodes { identifier title state { name } priority assignee { name } } } }"}' \
  https://api.linear.app/graphql | jq '.data.issues.nodes'
```

## Update an Issue

```bash
curl -s -X POST \
  -H "Authorization: $LINEAR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { issueUpdate(id: \"ISSUE_ID\", input: { stateId: \"STATE_ID\" }) { success issue { identifier title state { name } } } }"}' \
  https://api.linear.app/graphql | jq '.data.issueUpdate'
```

## Add a Comment

```bash
curl -s -X POST \
  -H "Authorization: $LINEAR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { commentCreate(input: { issueId: \"ISSUE_ID\", body: \"Your comment here\" }) { success comment { id body } } }"}' \
  https://api.linear.app/graphql | jq '.data.commentCreate'
```

## Tips

- Linear uses a GraphQL API at `https://api.linear.app/graphql`.
- Issue identifiers look like `ENG-123`. Issue IDs are UUIDs.
- Use `issueSearch` with natural language queries — Linear's search is quite flexible.
- State types: `backlog`, `unstarted`, `started`, `completed`, `cancelled`.
- Priority values: 0 (none), 1 (urgent), 2 (high), 3 (medium), 4 (low).
