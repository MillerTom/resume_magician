import json

a = '''```json
{
  "file_name": "Thomas Miller PYTHON base",
  "confidence": 0.95
}
```'''
b = a.replace('json', '').replace('`', '')
print(b)
print(json.loads(b))