from django.conf import settings
from SPARQLWrapper import SPARQLWrapper, JSON

from json import dumps
from collections import defaultdict
import requests
from bs4 import BeautifulSoup


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
        BASE <http://proyeksemweb.org/data/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX v: <http://proyeksemweb.org/vocab#>

        SELECT ?name ?type WHERE {
            ?s a ?p .
            ?p rdfs:label ?type .
            {
                ?s v:hasTitle ?name .
            }
            UNION
            {
                ?s v:hasName ?name .
            }
            FILTER (isLiteral(?name) && CONTAINS(LCASE(?name), %s))
        } ORDER BY ?type ?name
    """ % dumps(query)

    try:
        results = __query(sparql_query)
    except Exception as e:
        print(f"Error: {e}")
        results = None

    if (results is None) or (results is []):
        raise ValueError(f"Query \"{query}\": not found")
    else:
        results = __simplify_query_result(results)
        return results


def literal_details(query: str):
    sparql_query = """
        BASE <http://proyeksemweb.org/data/>
        PREFIX v: <http://proyeksemweb.org/vocab#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        select ?name ?label ?result where {
            ?s a ?o ;
            ?p ?result .
            ?p rdfs:label ?label .
            {
                ?s v:hasName %s . 
            }
            UNION
            {
                ?s v:hasTitle %s . 
            }

            { ?p rdfs:label "Name" . } UNION
            { ?p rdfs:label "Wiki URL" . } UNION
            { ?p rdfs:label "Title" . } UNION
            { ?p rdfs:label "Residence" . } UNION
            { ?p rdfs:label "Occupation" . } UNION
            { ?p rdfs:label "Gender" . } UNION
            { ?p rdfs:label "Classification" . } UNION
            { ?p rdfs:label "Color" . } UNION
            { ?p rdfs:label "Eye color" . } UNION
            { ?p rdfs:label "Production Code" . } UNION
            { ?p rdfs:label "Season No." . } UNION
            { ?p rdfs:label "Episode No." . } UNION
            { ?p rdfs:label "Airdate" . } UNION
            { ?p rdfs:label "U.S. premiere time (ET)" . } UNION
            { ?p rdfs:label "Copyright year" . } UNION
            { ?p rdfs:label "U.S. viewers (millions)" . } UNION
            { ?p rdfs:label "Running time" . }
        } ORDER BY ?label
    """ % (dumps(query), dumps(query))
    
    try:
        results = __query(sparql_query)
    except Exception as e:
        print(f"Error: {e}")
        results = None

    if (results is None) or (results is []):
        raise ValueError(f"Query \"{query}\": not found")
    else:
        results = __simplify_query_result(results)
        return results


def character_details(query: str):
    sparql_query = """
        BASE <http://proyeksemweb.org/data/>
        PREFIX v: <http://proyeksemweb.org/vocab#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        select ?name ?label ?result where {
            ?s a ?o ;
               ?p ?res .
            ?p rdfs:label ?label .
            {
                ?s v:hasName %s . 
            }
            UNION
            {
                ?s v:hasTitle %s . 
            }

            { ?p rdfs:label "Character" . } UNION
            { ?p rdfs:label "Children" . } UNION
            { ?p rdfs:label "Parents" . } UNION
            { ?p rdfs:label "Spouse" . }

            ?res v:hasName ?result .
        } ORDER BY ?label
    """ % (dumps(query), dumps(query))

    try:
        results = __query(sparql_query)
    except Exception as e:
        print(f"Error: {e}")
        results = None

    if (results is None) or (results is []):
        raise ValueError(f"Query \"{query}\": not found")
    else:
        results = __simplify_query_result(results)
        return results


def character_details_portrayer(query: str):
    sparql_query = """
        BASE <http://proyeksemweb.org/data/>
        PREFIX v: <http://proyeksemweb.org/vocab#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

        SELECT DISTINCT ?charName ?properti ?portrayerName ?explanation ?episodeTitle WHERE {
        ?s a <Character>.
        ?s rdfs:label %s.
        ?s rdfs:label ?charName .
        ?s v:hasPortrayer ?bNode.
        ?bNode v:portrayedBy ?human.
        ?human rdfs:label ?portrayerName.
        
        OPTIONAL { ?bNode v:hasExplanation ?explanation. }
        OPTIONAL { ?bNode v:inEpisode ?episode. ?episode rdfs:label ?episodeTitle. }
        
        BIND ("Portrayer" as ?properti)
        }
        ORDER BY DESC(?portrayerName)
    """ % (
        dumps(query)
    )

    try:
        results = __query(sparql_query)
    except Exception as e:
        print(f"Error: {e}")
        results = None

    if (results is None) or (results is []):
        raise ValueError(f'Query "{query}": not found')
    else:
        results = __simplify_query_result(results)
        results = group_character_details(results)
        return results


def episode_details(query: str):
    sparql_query = """
        BASE <http://proyeksemweb.org/data/>
        PREFIX v: <http://proyeksemweb.org/vocab#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        select ?name ?label ?result where {
            ?s a ?o ;
               ?p ?res .
            ?p rdfs:label ?label .
            {
                ?s v:hasName %s . 
            }
            UNION
            {
                ?s v:hasTitle %s . 
            }

            { ?p rdfs:label "First appearance" . } UNION
            { ?p rdfs:label "Latest appearance" . } UNION
            { ?p rdfs:label "Appearance" . } UNION
            { ?p rdfs:label "Sister episode" . } UNION
            { ?p rdfs:label "Next episode" . } UNION
            { ?p rdfs:label "Previous episode" . }

            ?res v:hasTitle ?result .
        } ORDER BY ?label
    """ % (dumps(query), dumps(query))

    try:
        results = __query(sparql_query)
    except Exception as e:
        print(f"Error: {e}")
        results = None

    if (results is None) or (results is []):
        raise ValueError(f"Query \"{query}\": not found")
    else:
        results = __simplify_query_result(results)
        return results


def group_character_details(data):
    grouped_data = defaultdict(
        lambda: {
            "portrayerName": None,
            "explanation": None,
            "episodes": set(),
        }
    )
    for item in data:
        char_name = item["charName"]
        portrayer_name = item["portrayerName"]
        explanation = item.get("explanation", None)
        episode_title = item.get("episodeTitle", None)
        if grouped_data[char_name]["portrayerName"] is None:
            grouped_data[char_name]["portrayerName"] = portrayer_name
        if grouped_data[char_name]["explanation"] is None and explanation:
            grouped_data[char_name]["explanation"] = explanation
        if episode_title:
            grouped_data[char_name]["episodes"].add(episode_title)
    results = []
    for char_name, details in grouped_data.items():
        results.append(
            {
                "charName": char_name,
                "portrayerName": details["portrayerName"],
                "explanation": details["explanation"],
                "episodes": sorted(
                    details["episodes"]
                ),
            }
        )
    return results

def episode_casting(query: str):
    sparql_query = """
        BASE <http://proyeksemweb.org/data/>
        PREFIX v: <http://proyeksemweb.org/vocab#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?roleName ?name ?explanation WHERE {
            ?episode a <Episode> ;
                    v:generalInfo ?roleNode .
            ?episode rdfs:label %s .
            ?roleNode a <EpisodeRole> ;
                    ?roleType ?roleValue .
            ?roleType rdfs:label ?roleName .
            ?roleValue rdfs:label ?name .
            OPTIONAL { ?roleNode v:hasRole ?explanation . }
            FILTER(?roleType IN (
                v:hasWriters,
                v:hasStoryboardArtists,
                v:hasStoryboard,
                v:hasAnimators,
                v:hasCreatives,
                v:hasGuests,
                v:hasSupervisor,
                v:hasLineProducer,
                v:hasMain,
                v:hasSupervisingProducers,
                v:hasTechnicals,
                v:hasAnimationSupervisor
            ))
        }
    """ % (
        dumps(query)
    )

    try:
        results = __query(sparql_query)
    except Exception as e:
        print(f"Error: {e}")
        results = None

    if (results is None) or (results is []):
        raise ValueError(f'Query "{query}": not found')
    else:
        results = __simplify_query_result(results)
        return results

def char_to_episode(query : str):
    sparql_query = """
        BASE <http://proyeksemweb.org/data/>
        PREFIX v: <http://proyeksemweb.org/vocab#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT DISTINCT ?episodeTitle WHERE {
            ?episode a <Episode> ;
                    v:hasCharacter ?character ;
                    rdfs:label ?episodeTitle .
            ?character rdfs:label %s .
        }
        ORDER BY ?episodeTitle
    """ % (
        dumps(query)
    )

    try:
        results = __query(sparql_query)
    except Exception as e:
        print(f"Error: {e}")
        results = None

    if (results is None) or (results is []):
        raise ValueError(f'Query "{query}": not found')
    else:
        results = __simplify_query_result(results)
        return results

def get_image_external(query : str):
    try:
        response = requests.get(query)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        infobox = soup.find("aside", class_="portable-infobox")
        if not infobox:
            return None
        image_tag = infobox.find(
            "img", src=lambda x: x and "static.wikia.nocookie.net" in x
        )
        if image_tag:
            return image_tag["src"]
        else:
            return None
    except Exception as e:
        return None

def get_data_wikidata(query : str):
    endpoint_url = "https://query.wikidata.org/sparql"
    sparql_query = """
        SELECT DISTINCT ?person ?personLabel ?birthDate ?genderLabel ?nationalityLabel ?occupationLabel ?languageLabel ?placeOfBirthLabel ?educatedAtLabel WHERE {
            ?person ?label %s@en.
            OPTIONAL { ?person wdt:P569 ?birthDate. }
            OPTIONAL { ?person wdt:P27 ?nationality. }
            OPTIONAL { ?person wdt:P21 ?gender. }
            OPTIONAL { ?person wdt:P106 ?occupation. }
            OPTIONAL { ?person wdt:P103 ?language. }
            OPTIONAL { ?person wdt:P19 ?placeOfBirth. }
            OPTIONAL { ?person wdt:P69 ?educatedAt. }
            SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
        }
    """ % (
        dumps(query)
    )
    try:
        sparql = SPARQLWrapper(endpoint_url)
        sparql.setQuery(sparql_query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
    except Exception as e:
        print(f"Error: {e}")
        results = None
    if (results is None) or (results is []):
        raise ValueError(f'Query "{query}": not found')
    else:
        results = __simplify_query_result(results)
        aggregated_data = defaultdict(set)
        for row in results:
            for key, value in row.items():
                if (key.endswith("Label") and key != "personLabel"):
                    aggregated_data[key].add(value)
        final_data_1 = {key: ", ".join(values) for key, values in aggregated_data.items()}
        key_mapping = {
            "genderLabel": "Gender",
            "nationalityLabel": "Nationality",
            "occupationLabel": "Occupations",
            "languageLabel": "Language",
            "placeOfBirthLabel": "Place of Birth",
            "educatedAtLabel": "Educated At"
        }
        final_data = {key_mapping.get(key, key): value for key, value in final_data_1.items()}
        return final_data