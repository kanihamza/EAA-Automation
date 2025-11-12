import sys
import yaml
import jsonschema
from pathlib import Path

def validate_yaml_file(yaml_path, schema):
    with open(yaml_path) as f:
        data = yaml.safe_load(f)
    jsonschema.validate(instance=data, schema=schema)
    print(f"✅ {yaml_path} passed schema validation.")

def main(schema_path):
    with open(schema_path) as f:
        schema = yaml.safe_load(f)

    errors = 0
    for file in Path('.').rglob('*.yaml'):
        try:
            validate_yaml_file(file, schema)
        except jsonschema.ValidationError as e:
            print(f"❌ Schema validation failed for {file}:\n{e.message}")
            errors += 1
    if errors:
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_yaml.py <schema-file>")
        sys.exit(1)
    main(sys.argv[1])
