echo "Data dumping...."

echo "USE Master;" > ./init_db/3_migration_data.sql
docker exec -it christa-db-1 mysqldump -u root -proot_password -t Master drafts >> ./init_db/3_migration_data.sql

echo "Down docker containers...."

docker-compose down --volumes

echo "Deleting existing database files...."

rm -r ./maria_data/*

echo "Restarting docker containers...."

docker-compose up -d

echo "Migration is completed."

