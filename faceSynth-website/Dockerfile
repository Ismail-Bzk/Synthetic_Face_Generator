# Build stage
FROM node:18-alpine AS builder

WORKDIR /app

# Copy files
COPY package*.json ./
COPY tsconfig.json ./
COPY tailwind.config.ts ./
COPY postcss.config.js ./
COPY next.config.js ./
COPY app/ ./app/
COPY public/ ./public/

# Install dependencies
RUN npm ci

# Build Next.js
RUN npm run build

# Production stage
FROM node:18-alpine

WORKDIR /app

# Copy from builder
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package*.json ./

# Expose port
EXPOSE 3000

# Start app
CMD ["npm", "start"]
