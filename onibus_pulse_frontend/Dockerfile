FROM node:22-alpine AS build

WORKDIR /app

# Copy package.json and lock file first to leverage Docker cache
COPY package*.json ./
RUN npm install

# Copy all source files and build
COPY . .
RUN npm run build

# --- Stage 2: Serve the static assets with Nginx ---
FROM nginx:stable-alpine

# Copy built assets to Nginx html folder
COPY --from=build /app/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# The default Nginx configuration works for most simple SPAs, 
# but we might need a custom one if we have complex routing later.

CMD ["nginx", "-g", "daemon off;"]
