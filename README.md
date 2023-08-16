# Airport-API-Service

Airport API service - system for tracking flights from airports across the whole globe. 

Supports:
- JWT Authentication
- Swagger Documentation
- PostgreSQL
- Docker

### Database Table

![Alt Text](https://github.com/leetwinoff/Airport-API-Service/raw/develop/images/database%20table.png)


#### Admin possibilities:
- Create/Update/Delete airplane crew positions
- Create/Update/Delete crew, assign crew position
- Create/Update/Delete airplane types
- Create/Update/Delete airplanes with assigned crew
- Create/Update/Delete airports
- Create/Update/Delete routes with source and destination airports
- Create/Update/Delete flight with certain routes and airplane

#### User possibilities:
- Create/Update/Delete ticket with order for certain flight


## Installation

1. Clone link from GitHub repository [airport-API](https://github.com/leetwinoff/Airport-API-Service.git)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Create .env file and update fields like in .env.sample 

3. Build docker container 
```bash
docker build -t airport_api . 
```

4. Run Docker container 
```bash
docker compose up
```

5. Create superuser
```bash
docker exec -it <container_name> bash
```

