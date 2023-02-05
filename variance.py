from graphql import parse
import sys


if len(sys.argv) != 3:
    raise Exception("Invalid input")

file_1 = sys.argv[1]
file_2 = sys.argv[2]

with open(file_1, "r+") as file1:
    schema_1 = parse(file1.read())

with open(file_2, "r+") as file2:
    schema_2 = parse(file2.read())

# document = parse("""
#     type Query {
#       me: User
#     }
#
#     type User {
#       id: ID
#       name: String
#     }
# """)

print(schema_1)