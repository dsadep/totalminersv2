P.S. Deploy:
```bash
sudo docker compose up -d db
# We need to do this, cause migrations are broken
psql -U dbuser -h localhost -p 5432 totalminersdb < init_schema.sql
sudo docker compose up -d
```
