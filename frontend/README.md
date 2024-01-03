# TON DNS Checker Frontend

This is the frontend part of the TON DNS Checker. Here is the guide for installation and running.

## Installation

Before starting, please ensure that Node.js is installed on your machine.

### Development Server

To start the development server locally, follow these steps:

1. **Install Dependencies**:
   ```bash
   yarn install
   ```

2. **Start the Development Server**:
   ```bash
   yarn start
   ```

3. **Access the Application**:
   Open your browser and visit [http://127.0.0.1:3090](http://127.0.0.1:3090).

   **Note**: Ensure that `API_URL` is set in `src/tools/fetchData.ts` to point to a valid api-dns backend.

### Production Build

To build the application for production, follow these steps:

1. **Build the Application**:
   ```bash
   yarn build
   ```

   This will build the application into the `build` folder.

2. **Deploy the Application**:
   You can host the `build` folder on your own web server.