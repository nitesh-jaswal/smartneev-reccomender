import dataclasses
import elasticsearch
import pandas
import pprint

from elasticsearch import helpers
from typing import Iterable, Any

from utils.timeit import timeit

@dataclasses.dataclass
class IndexerConfig:
    es_host: str
    es_port: int
    index_name:  str
    source_file: str

def get_elasticsearch(host: str, port: int) -> elasticsearch.Elasticsearch:
    return elasticsearch.Elasticsearch([
        {
            "host": host,
            "port": port,
            "scheme": "http"
        }
    ])

def generate_records(source_file: str, index_name: str) -> Iterable[dict[str, Any]]:
    df = pandas.read_excel(source_file)
    for record in df.to_dict(orient='records'):
        yield {
            "_op_type": "index",
            "_index": index_name,
            "_source": record
        }

@timeit(fmt_msg="Data indexed suceesfully in {}s")
def main(config: IndexerConfig) -> list[tuple[bool, dict[str, Any]]]:
    return [
        result
        for result in helpers.streaming_bulk(
            client=get_elasticsearch(config.es_host, config.es_port), 
            actions=generate_records(config.source_file, config.index_name), 
            max_chunk_bytes=1000
        )
    ]

if __name__ == "__main__":
    print("Started indexing")
    config = IndexerConfig(
        es_host="localhost", 
        es_port=9200, 
        index_name="raw_index_001",
        source_file="~/Documents/dummy.xlsx",
    )
    result = main(config)
    print(f"Summary: {pprint.pformat(result, indent=2)}")
