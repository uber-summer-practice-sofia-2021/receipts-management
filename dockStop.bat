docker network disconnect receipt-net couriers
docker network disconnect receipt-net orders
docker network disconnect receipt-net receipts
start "receipts_service_kill" cmd /c "docker compose down" 
start "orders_service_kill" cmd /c "cd services/orders & docker compose down"
start "couriers_service_kill" cmd /c "cd services/courier & docker compose down"
docker network rm receipt-net
docker rmi courier_server
docker rmi orders_server
docker rmi receipts-management_server