import httpx
import json
import time

print("Sending init...")
r = httpx.post('http://127.0.0.1:8080/api/agent/init', json={'persona': {'name': 'Ada', 'domain': 'AI Security'}})
print('INIT:', r.json())
agent_id = r.json()['agentId']

print("Sleeping 5 seconds to let worker run...")
time.sleep(5)

print("Fetching feed...")
feed = httpx.get(f'http://127.0.0.1:8080/api/agent/feed?agentId={agent_id}')
print('FEED:', json.dumps(feed.json(), indent=2))
