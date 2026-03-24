# Use Nginx to serve the static content
FROM nginx:alpine

# Copy everything
COPY . /usr/share/nginx/html/

# Copy minimal nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]
