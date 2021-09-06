docker network create receipt-net
python pathGenerate.py
start "receipts_service" cmd /c "docker compose up"
start "orders_service" cmd /c "cd services/orders & docker compose up"
start "couriers_service" cmd /c "cd services/courier & docker compose up"