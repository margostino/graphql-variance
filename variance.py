import sys
from concurrent.futures import ThreadPoolExecutor

from graphql import DocumentNode
from graphql import parse

OLD_INDEX = "old"
NEW_INDEX = "new"

diff = {}


def object_definitions_map(object_definitions):
    type_definitions = {}
    for definition in object_definitions:
        type_definitions[definition.name.value] = [field.name.value for field in definition.fields]
    return type_definitions


def run_in_thread_pool(tasks):
    tasks_results = {}
    with ThreadPoolExecutor() as executor:
        running_tasks = [executor.submit(task) for task in tasks]
        for running_task in running_tasks:
            index, result = running_task.result()
            tasks_results[index] = result
        return tasks_results


def read_schema(index, filename: str) -> DocumentNode:
    with open(filename, "r+") as file:
        schema = parse(file.read())
        return index, schema


if len(sys.argv) != 3:
    raise Exception("Invalid input")

old_filename = sys.argv[1]
new_filename = sys.argv[2]

data = run_in_thread_pool([
    lambda: read_schema(OLD_INDEX, old_filename),
    lambda: read_schema(NEW_INDEX, new_filename),
])

old_schema = data[OLD_INDEX]
new_schema = data[NEW_INDEX]

old_object_definitions = [definition for definition in old_schema.definitions if definition.kind == "object_type_definition"]
new_object_definitions = [definition for definition in new_schema.definitions if definition.kind == "object_type_definition"]
old_type_definitions = object_definitions_map(old_object_definitions)
new_type_definitions = object_definitions_map(new_object_definitions)

for type_def in new_type_definitions:
    if type_def not in old_type_definitions:
        diff[type_def] = new_type_definitions[type_def]
    else:
        for field in new_type_definitions[type_def]:
            if field not in old_type_definitions[type_def]:
                if type_def in diff:
                    diff[type_def].append(field)
                else:
                    diff[type_def] = [field]
