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
        } ORDER BY ?type ?name
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
    

def literal_details(query: str):
    sparql_query = """
        BASE <http://example.org/data>
        PREFIX v: <http://example.org/vocab#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        select ?name ?label ?result where {
            ?s a ?o ;
            ?p ?result .
            ?p rdfs:label ?label .
            {
                ?s v:hasName "%s" . 
            }
            UNION
            {
                ?s v:hasTitle "%s" . 
            }

            { ?p rdfs:label "Character name" . } UNION
            { ?p rdfs:label "URL" . } UNION
            { ?p rdfs:label "Episode title" . } UNION
            { ?p rdfs:label "Residence" . } UNION
            { ?p rdfs:label "Occupation" . } UNION
            { ?p rdfs:label "Gender" . } UNION
            { ?p rdfs:label "Classification" . } UNION
            { ?p rdfs:label "Portrayer" . } UNION
            { ?p rdfs:label "Color" . } UNION
            { ?p rdfs:label "Eye color" . } UNION
            { ?p rdfs:label "Production Code" . } UNION
            { ?p rdfs:label "Season No." . } UNION
            { ?p rdfs:label "Episode No." . } UNION
            { ?p rdfs:label "Airdate" . } UNION
            { ?p rdfs:label "U.S. premiere time (ET)" . } UNION
            { ?p rdfs:label "Copyright year" . } UNION
            { ?p rdfs:label "U.S. viewers (millions)" . } UNION
            { ?p rdfs:label "Running time" . } UNION
            { ?p rdfs:label "Writer(s)" . } UNION
            { ?p rdfs:label "Storyboard artist(s)" . } UNION
            { ?p rdfs:label "Storyboard" . } UNION
            { ?p rdfs:label "Animator(s)" . } UNION
            { ?p rdfs:label "Creative(s)" . } UNION
            { ?p rdfs:label "Guest(s)" . } UNION
            { ?p rdfs:label "Supervising" . } UNION
            { ?p rdfs:label "Line producer" . } UNION
            { ?p rdfs:label "Main" . } UNION
            { ?p rdfs:label "Supervising producer(s)" . } UNION
            { ?p rdfs:label "Technical" . } UNION
            { ?p rdfs:label "Animation supervisor" . }
        } limit 100
    """ % (query, query)
    
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
    

def character_details(query: str):
    sparql_query = """
        BASE <http://example.org/data>
        PREFIX v: <http://example.org/vocab#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        select ?name ?label ?result where {
            ?s a ?o ;
               ?p ?res .
            ?p rdfs:label ?label .
            {
                ?s v:hasName "%s" . 
            }
            UNION
            {
                ?s v:hasTitle "%s" . 
            }

            { ?p rdfs:label "Characters" . } UNION
            { ?p rdfs:label "Children" . } UNION
            { ?p rdfs:label "Parents" . } UNION
            { ?p rdfs:label "Spouse" . }

            ?res v:hasName ?result .
        } limit 100
    """ % (query, query)
    
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
    

def episode_details(query: str):
    sparql_query = """
        BASE <http://example.org/data>
        PREFIX v: <http://example.org/vocab#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        select ?name ?label ?result where {
            ?s a ?o ;
               ?p ?res .
            ?p rdfs:label ?label .
            {
                ?s v:hasName "%s" . 
            }
            UNION
            {
                ?s v:hasTitle "%s" . 
            }

            { ?p rdfs:label "First appearance" . } UNION
            { ?p rdfs:label "Latest appearance" . } UNION
            { ?p rdfs:label "Appearance" . } UNION
            { ?p rdfs:label "Sister episode(s)" . } UNION
            { ?p rdfs:label "Next Episode" . } UNION
            { ?p rdfs:label "Previous Episode" . }

            ?res v:hasTitle ?result .
        } limit 100
    """ % (query, query)
    
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