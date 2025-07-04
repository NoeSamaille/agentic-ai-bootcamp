# 1. Get a token (teller credentials)
TOKEN=$(curl -s -X POST http://localhost:8000/token \
         -d "username=teller" -d "password=teller123" | jq -r .access_token)

# 2. Call /accounts with the token
curl -s -H "Authorization: Bearer $TOKEN" http://localhost:8000/accounts | jq .
