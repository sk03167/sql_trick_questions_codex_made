"""Verify catalogue coverage, embedded executable code, fixtures and local links."""
import ast
import json
from pathlib import Path
import re

from build_pyspark_docs import solution_section, sources

ROOT = Path(__file__).resolve().parent


def main():
    questions = json.loads((ROOT / 'catalog.json').read_text())
    notes = json.loads((ROOT / 'pyspark_notes.json').read_text())
    src = sources()
    assert set(notes) == {q['id'] for q in questions}
    solutions = (ROOT / 'SOLUTIONS.md').read_text()
    question_text = (ROOT / 'QUESTIONS.md').read_text()
    guide = (ROOT / 'PYSPARK_GUIDE.md').read_text()
    assert len(re.findall(r'^### PySpark Q\d\d$', solutions, re.M)) == 50
    assert len(re.findall(r'^## Q\d\d ', solutions, re.M)) == 50
    setup_blocks = 0
    for q in questions:
        assert q['id'].lower() in src
        assert '\n\n'.join(solution_section(q)) in solutions, q['id']
        assert f'(SOLUTIONS.md#pyspark-{q["id"].lower()})' in question_text
    for helper in ['prefix', 'pack_intervals', 'reachability']:
        assert f'```python\n{src[helper]}\n```' in guide
    # Inspect each literal fixture without starting Spark; ensure it matches the declared dataset/schema.
    for code in re.findall(r'```python\n(.*?)\n```', solutions, re.S):
        tree = ast.parse(code)
        if not code.startswith('t = {}'):
            continue
        q = questions[setup_blocks]
        calls = [node for node in tree.body[1:] if isinstance(node, ast.Assign)]
        assert len(calls) == len(q['tables'])
        for assignment, table in zip(calls, q['tables']):
            assert ast.literal_eval(assignment.targets[0].slice) == table['name']
            assert ast.literal_eval(assignment.value.args[0]) == [tuple(row) for row in table['rows']]
            schema = ', '.join(name + (' long' if kind.startswith('INTEGER') else ' string') for name, kind in table['columns'])
            assert ast.literal_eval(assignment.value.args[1]) == schema
        setup_blocks += 1
    assert setup_blocks == 50
    files = [ROOT / name for name in ['README.md', 'QUESTIONS.md', 'SOLUTIONS.md', 'PYSPARK_GUIDE.md']]
    links = 0
    for path in files:
        text = path.read_text()
        for code in re.findall(r'```python\n(.*?)\n```', text, re.S):
            ast.parse(code)
        for target in re.findall(r'\]\(([^)]+)\)', re.sub(r'```.*?```', '', text, flags=re.S)):
            if '://' in target:
                continue
            filename, _, fragment = target.partition('#')
            dest = path.parent / filename if filename else path
            assert dest.exists(), (path.name, target)
            if fragment:
                slugs = {re.sub(r'[^\w\- ]', '', h.lower()).replace(' ', '-')
                         for h in re.findall(r'^#+ (.+)$', dest.read_text(), re.M)}
                assert fragment in slugs, (path.name, target)
            links += 1
    print(f'PASS: 50 PySpark sections, 50 explicit datasets, 3 helpers, Python syntax and {links} local links')


if __name__ == '__main__':
    main()
