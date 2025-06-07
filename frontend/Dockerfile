# Stage 1: Build the app
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
# Remove any .env file that might conflict
RUN rm -f .env
# Set the API URL for the build (after copying files)
# Force the environment variable
ENV VITE_API_URL=/api
# Debug: Show the environment variable
RUN echo "VITE_API_URL is set to: $VITE_API_URL"
RUN npm run build

# Stage 2: Serve with a static server
FROM node:20-alpine
WORKDIR /app
RUN npm install -g serve
COPY --from=builder /app/dist ./dist
EXPOSE 3000
CMD ["serve", "-s", "dist", "-l", "tcp://0.0.0.0:3000"] 