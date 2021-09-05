docker network create receipt-net
start "receipts_service" cmd /k "docker compose up"
start "orders_service" cmd /k "cd services/orders & docker compose up"
start "couriers_service" cmd /k "cd services/courier & docker compose up"