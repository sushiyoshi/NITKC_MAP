from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable

class GraphApp:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    def find_shortestPath(self,start,goal):
        with self.driver.session(database="neo4j") as session:
            result = session.read_transaction(self._find_shortestPath,start,goal)
        return result
    @staticmethod
    def _find_shortestPath(tx,start,goal):
        query= (
            "MATCH (p1:Area{name:$start}), (p2:Area{name:$goal}) "
            "call apoc.algo.dijkstra(p1, p2, 'ROUTED', 'distance') YIELD path,weight "
            "return path,weight"
        )
        result = tx.run(query,start=start,goal=goal)
        data = result.data()
        graph =result.graph()
        print(list(graph.nodes))
        return [data[0],graph.relationships,list(graph.nodes)]