###NEEDS TO BE FIXES

start cmd /k docker compose up
timeout 3
start cmd /k cd services/courier
docker compose up
timeout 3
start cmd /k cd services/orders
docker compose up