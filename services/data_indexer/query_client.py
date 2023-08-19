import dataclasses
import elasticsearch
import pprint
import sys

from elasticsearch import helpers
from typing import Any

from utils.timeit import timeit

@dataclasses.dataclass
class QueryClientConfig:
    es_host: str
    es_port: int
    index_name:  str

def get_elasticsearch(host: str, port: int) -> elasticsearch.Elasticsearch:
    return elasticsearch.Elasticsearch([
        {
            "host": host,
            "port": port,
            "scheme": "http"
        }
    ])

class ESQueryClient:
    def __init__(self, client: elasticsearch.Elasticsearch, index_name: str):
        self.client = client
        self.index_name = index_name

    def search(self, search_term: str) -> dict[str, Any]:
        response = self.client.search(index=self.index_name, body={
            "query": {
                "match": {
                    "field_name": search_term
                }
            }
        })
        return response

@timeit(fmt_msg="Data indexed suceesfully in {}s")
def main(config: QueryClientConfig, search_term: str) -> list[tuple[bool, dict[str, Any]]]:
    search_client = ESQueryClient(
        client=get_elasticsearch(config.es_host, config.es_port),
        index_name=config.index_name
    )
    return search_client.search(search_term)

if __name__ == "__main__":
    config = QueryClientConfig(
        es_host="localhost", 
        es_port=9200, 
        index_name="raw_index_001",
    )
    search_term = input("Enter search term: ")
    result = main(config, search_term)
    print(f"Summary: {pprint.pformat(result, indent=2)}")