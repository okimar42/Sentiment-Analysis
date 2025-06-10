# Stage 1: Build the app
FROM node:20-alpine AS builder

# Set working directory
WORKDIR /app

# Add package files first for better Docker layer caching
COPY package*.json ./

# Clear npm cache and install dependencies
RUN npm cache clean --force && \
    npm ci --only=production=false --no-audit --no-fund

# Copy source code
COPY . .

# Remove any .env file that might conflict
RUN rm -f .env

# Set the API URL for the build
ENV VITE_API_URL=/api

# Debug: Show the environment variable
RUN echo "VITE_API_URL is set to: $VITE_API_URL"

# Build the application
RUN npm run build

# Stage 2: Serve with a static server
FROM node:20-alpine AS production

# Set working directory
WORKDIR /app

# Install serve globally
RUN npm install -g serve

# Copy built application from builder stage
COPY --from=builder /app/dist ./dist

# Create non-root user for security
RUN addgroup -g 1001 -S nodejs && \
    adduser -S frontend -u 1001 -G nodejs

# Change ownership of app directory
RUN chown -R frontend:nodejs /app

# Switch to non-root user
USER frontend

# Expose port
EXPOSE 3000

# Start the server
CMD ["serve", "-s", "dist", "-l", "tcp://0.0.0.0:3000"] 