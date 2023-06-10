#!/usr/bin/env python3

from ariadne import QueryType, graphql_sync, make_executable_schema, load_schema_from_path
from ariadne.explorer import ExplorerGraphiQL
from flask import Flask, jsonify, request
from resolvers import hello_resolver

type_defs = load_schema_from_path("schema.graphql")

query = QueryType()
query.set_field("hello", hello_resolver.resolve_hello)

schema = make_executable_schema(type_defs, [query])

app = Flask(__name__)

# Retrieve HTML for the GraphiQL.
# If explorer implements logic dependant on current request,
# change the html(None) call to the html(request)
# and move this line to the graphql_explorer function.
explorer_html = ExplorerGraphiQL().html(None)

@app.route("/graphql", methods=["GET"])
def graphql_explorer():
  # On GET request serve the GraphQL explorer.
  # You don't have to provide the explorer if you don't want to
  # but keep on mind this will not prohibit clients from
  # exploring your API using desktop GraphQL explorer app.
  return explorer_html, 200

@app.route("/graphql", methods=["POST"])
def graphql_server():
  # GraphQL queries are always sent as POST
  data = request.get_json()

  # Note: Passing the request to the context is optional.
  # In Flask, the current request is always accessible as flask.request
  success, result = graphql_sync(
    schema,
    data,
    context_value={"request": request},
    debug=app.debug
  )

  status_code = 200 if success else 400
  return jsonify(result), status_code

if __name__ == "__main__":
  app.run(debug=True)

