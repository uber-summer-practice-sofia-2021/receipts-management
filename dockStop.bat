docker network disconnect receipt-net couriers
docker network disconnect receipt-net orders
docker network disconnect receipt-net receipts
start "receipts_service" cmd /c "docker compose down" 
start "orders_service" cmd /c "cd services/orders & docker compose down"
start "couriers_service" cmd /c "cd services/courier & docker compose down"
docker network rm receipt-net