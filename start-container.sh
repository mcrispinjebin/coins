# Set env vars
db_user_name='crispin'
db_pwd=''

# Host vars
db_host='db_host_ip'
db_host_ip='192.168.1.100'

source_dir=$PWD
destination_dir='/app'

if [ "$1" = restart ]
then
  docker restart wallet-system
  exit
fi


docker stop wallet-system
docker rm -f wallet-system

echo "Starting Container.."
echo "wallet-system"
docker run -d -w /app/ --env DB_USER_NAME=$db_user_name --env DB_USER_PASSWORD=$db_pwd --add-host=$db_host:$db_host_ip -v "$source_dir":$destination_dir --name wallet-system -p 8000:4982 coins-wallet:latest