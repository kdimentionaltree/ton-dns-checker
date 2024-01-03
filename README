# DHTChecker API Documentation

DHTChecker is an API built with FastAPI, designed to check the status of DHT nodes and resolve related information.

## API Documentation

### 1. Get DHT Nodes Information

- **Endpoint:** `/dhts`
- **Method:** `GET`
- **Description:** Returns the status information of the current DHT nodes.
- **Response Model:** `List[DhtNodeModel]`

### 2. Resolve ADNL Address

- **Endpoint:** `/resolve`
- **Method:** `GET`
- **Parameters:** 
  - `adnl`: String representing the ADNL address
- **Description:** Resolves the specified ADNL address.
- **Response Model:** `List[DhtResolveModel]`

### 3. Get Liteserver Information

- **Endpoint:** `/liteservers`
- **Method:** `GET`
- **Description:** Returns information about the current Liteserver nodes.
- **Response Model:** `List[LiteserverModel]`

### 4. Liteserver Domain Resolution

- **Endpoint:** `/ls_resolve`
- **Method:** `GET`
- **Parameters:** 
  - `domain`: Domain name to resolve
  - `category`: Category of resolution (e.g., 'site' or 'wallet')
- **Description:** Resolves the Liteserver address for a specified domain.
- **Response Model:** `List[LiteserverResolveModel]`

### 5. Health Check

- **Endpoint:** `/healthcheck`
- **Method:** `GET`
- **Description:** Checks the health status of the API service.
