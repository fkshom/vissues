from pprint import pprint
import gitlab
import json

gl = gitlab.Gitlab.from_config('home', ['./gl.cfg'])
gl.auth()

class DumpEncoder(json.JSONEncoder):
  def default(self, obj):
    pprint(obj)
    pprint(obj.__class__.__name__)
    if obj.__class__.__name__ == 'Gitlab':
      return ""
    if hasattr(obj, '__dict__'):
      return obj.__dict__
    else:
      return json.JSONEncoder.default(self, obj)

projects = gl.projects.list(all=True)
project_ids = []
# projects = [gl.projects.get(project_id) for project_id in project_ids]

allissues = []
for idx, project in enumerate(projects, start=1):
  pprint(project)
  print(f'fetch issues Project: {project.id} ({idx}/{len(projects)}) ')
  issues = project.issues.list(all=True)
  allissues.extend(issues)

pprint(allissues)
print('write issues.json')
with open('issues.json', 'w') as f:
  allissues_for_json = []
  if len(allissues) != 0:
    allissues_for_json = [issue.attributes for issue in allissues]
    

  f.write("issues = ")
  json.dump(allissues_for_json, f, indent=2)


alllinks_for_json = []

for idx, issue in enumerate(allissues, start=1):
  print(f'fetch links Project: {issue.project_id} Issue: {issue.iid} ({idx}/{len(allissues)}) ')

  links = []
  try:
    links = issue.links.list(all=True)
  except gitlab.exceptions.GitlabListError:
    print(1)

  if len(links) != 0:
    alllinks_for_json.append({
      'project_id': issue.project_id,
      'id': issue.id,
      'iid': issue.iid,
      # 'links': links.__dict__['_attrs']
      'links': links.attributes
    })

print('write relations.json')
with open('relations.json', 'w') as f:
  f.write("relations = ")
  json.dump(alllinks_for_json, f, indent=2)
