docker network create receipt-net
start "receipts_service" cmd /c "docker compose up -f docker-compose-windows.yml"
start "orders_service" cmd /c "cd services/orders & docker compose up"
start "couriers_service" cmd /c "cd services/courier & docker compose up"
