docker network disconnect receipt-net couriers
docker network disconnect receipt-net orders
docker network disconnect receipt-net receipts
docker network rm receipt-net
start "receipts_service_kill" cmd /c "docker compose down --rmi local" 
start "orders_service_kill" cmd /c "cd services/orders & docker compose down --rmi local"
start "couriers_service_kill" cmd /c "cd services/courier & docker compose down --rmi local"