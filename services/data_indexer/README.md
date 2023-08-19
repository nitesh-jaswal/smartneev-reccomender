# Data Indexer

Indexes data expected to be a `.xlsx` format currently. Can be easily configured to support formats like csv later but currently not supported

## Running

1. Start colima with `colima start`
2. Bring container up with `docker compose up`. Run this from the dir which has the `docker-compose.yml` file
3. Run the `indexer` or `query_client` as per your requirement  

# Troubleshooting

## Running Elastic Search 
1. `colima` increase `vm.max_map_count` to avoid OOM issues  

```sh
colima ssh
sudo sysctl -w vm.max_map_count=262144
exit
```

2. If you get OS error in ES logs, stop colima and restart with `colima start -a x86_64`. Make sure to reset the `vm_memory_map` because teh setting is not currently persistent
3. If you see JVM errors in the logs, try deleting the container and re-upping it by

```sh
docker compose down -v
docker compose up
```