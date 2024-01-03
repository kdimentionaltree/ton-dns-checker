# TON DNS Checker

TON DNS Checker is a robust application designed to provide DNS checking capabilities within the TON (Telegram Open Network) blockchain environment. It leverages Redis for caching and includes a front-end interface for easy interaction.

## Features

- **DHT Node Status Checking**: Fetches and displays the status of Distributed Hash Table (DHT) nodes.
- **ADNL Address Resolution**: Allows the resolution of Abstract Data Network Layer (ADNL) addresses.
- **Liteserver Information Retrieval**: Retrieves and displays information about liteservers.
- **Domain Resolution for Liteservers**: Resolves domains for liteservers, crucial for navigating and interacting within the TON network.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Docker and Docker Compose installed on your system.
- Basic understanding of Docker, FastAPI, and Redis.

### Installation and Running the Application

1. **Clone the Repository**

   ```sh
   git clone https://github.com/your-repository/TON-DNS-Checker.git
   ```

2. **Navigate to the Project Directory**

   ```sh
   cd TON-DNS-Checker
   ```

3. **Start the Services**

   Use Docker Compose to build and start the services defined in the `docker-compose.yml` file.

   ```sh
   docker-compose up --build
   ```

   This command builds the images for the services (if not already built) and starts the services. Specifically, it sets up the following:

   - A Redis caching service.
   - A DNS checker service that runs on port 8090.
   - A front-end service accessible on port 3090.

4. **Verify the Services**

   Once the services are up and running, you can navigate to `http://localhost:8090/healthcheck` to check the health of the DNS checker service and `http://localhost:3090` to access the front-end interface.

## Usage

- Access the front-end interface at `http://localhost:8090/docs`.
- The interface will interact with the DNS checker backend to perform functionalities like DHT node status checking, ADNL address resolution, and more.