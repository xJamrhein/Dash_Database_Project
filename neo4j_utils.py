from neo4j import GraphDatabase

def db_connect():
    db = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"), database="academicworld")
    return db


def get_publication_count(name):
    try:
        db = db_connect()
    except:
        print("neo4j connection unsuccessful")
        return 3
    else:
        print("neo4j connection Successful")

    print(name)
    neo4j_query = "MATCH (f:FACULTY {name: $name})-[pub:PUBLISH]->(p:PUBLICATION) RETURN count(p) as count"
    with db.session() as session:
        print("Executing query: " + neo4j_query)
        data = session.run(neo4j_query, name=name)
        processed_data = data.single()
        count = processed_data["count"]
        print("Data: " + str(data))
        print("Processed Data: " + str(processed_data))
        print("Publication Count: " + str(count))
    db.close()
    return processed_data


