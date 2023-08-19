import elasticsearch
import pandas
import pprint
import dataclasses

from elasticsearch import helpers
from typing import Iterable, Any

from utils.timeit import timeit

@dataclasses.dataclass
class IndexerConfig:
    es_host: str
    es_port: int
    source_csv: str

def get_elasticsearch(host: str, port: int) -> elasticsearch.Elasticsearch:
    return elasticsearch.Elasticsearch([
        {
            "host": host,
            "port": port,
            "scheme": "http"
        }
    ])

def generate_records(source_csv: str) -> Iterable[dict[str, Any]]:
    df = pandas.read_excel(source_csv)
    for record in df.to_dict(orient='records'):
        yield {
            "_op_type": "index",
            "_index": "raw_index_001",
            "_source": record
        }

# @timeit(fmt_msg="Data indexed suceesfully in {}s")
def main(config: IndexerConfig) -> list[tuple[bool, dict[str, Any]]]:
    es = get_elasticsearch(config.es_host, config.es_port)
    return [
        result
        for result in helpers.streaming_bulk(
            client=es, 
            actions=generate_records(config.source_csv), 
            max_chunk_bytes=1000
        )
    ]

if __name__ == "__main__":
    print("Started indexing")
    config = IndexerConfig(
        es_host="localhost", 
        es_port=9200, 
        source_csv="/Users/nishantjain/Development/SmartNeev/smart-neev-data/data/property_details.xlsx"
    )
    result = main(config)
    print(f"Summary: {pprint.pformat(result, indent=2)}")