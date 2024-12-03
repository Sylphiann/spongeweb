from django.conf import settings
from SPARQLWrapper import SPARQLWrapper, JSON


def __query(query: str):
    sparql = SPARQLWrapper(settings.GRAPH_DB_ENDPOINT)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results

def __simplify_query_result(sparql_result):
    return [
        {var: binding[var]["value"] for var in sparql_result["head"]["vars"] if var in binding}
        for binding in sparql_result["results"]["bindings"]
    ]

def search(query: str):
    query = query.lower()
    sparql_query = """
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        BASE <http://example.org/data/>
        PREFIX v: <http://example.org/vocab#>

        SELECT ?name ?type WHERE {
            ?s a ?p .
            ?p foaf:name ?type .
            {
                ?s v:hasTitle ?name .
            }
            UNION
            {
                ?s v:hasName ?name .
            }
            FILTER (isLiteral(?name) && CONTAINS(LCASE(?name), "%s"))
        }
    """ % query

    try:
        results = __query(sparql_query)
    except Exception as e:
        print(f"Error: {e}")
        results = None

    if (results is None) and (results is []):
        raise ValueError(f"Query \"{query}\": not found")
    else:
        results = __simplify_query_result(results)
        return results