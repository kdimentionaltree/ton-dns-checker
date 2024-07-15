# Use Node.js as the build environment
FROM node:latest as build

# Arguments to pass environment variables
ARG REACT_APP_API_URL
ARG REACT_APP_API_KEY

# Set the working directory in the container
WORKDIR /app

# Copy package.json and yarn.lock files
COPY package.json yarn.lock ./

# Install dependencies
RUN yarn install

# Copy the rest of the application source code
COPY . .

# Build the application
RUN yarn build

# Use Nginx as the server for the built application
FROM nginx:alpine

# Copy the built application files to Nginx's serve directory
COPY --from=build /app/build /usr/share/nginx/html

# Expose port 80 to the outside once the container has launched
EXPOSE 80

# Start Nginx and keep it running in the foreground
CMD ["nginx", "-g", "daemon off;"]
