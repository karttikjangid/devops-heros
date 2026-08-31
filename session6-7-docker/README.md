# Docker Homework - Hello World Applications

I used podman instead of docker since I have experience working with it, and on Mac the podman VM is lighter compared to Docker Desktop. The commands for both are the same, so it makes no difference.

Thanks for understanding, Mam!

## Node App (`node-app`)

```
$ podman build -t node-app .
STEP 1/7: FROM node:24-alpine
STEP 2/7: WORKDIR /app
STEP 3/7: COPY package*.json ./
STEP 4/7: RUN npm install
added 68 packages, and audited 69 packages in 17s
found 0 vulnerabilities
STEP 5/7: COPY . .
STEP 6/7: EXPOSE 3000
STEP 7/7: CMD ["npm", "start"]
COMMIT node-app
Successfully tagged localhost/node-app:latest
```

## Python App (`python-app`)

Built with FastAPI, served using uvicorn.

```
$ podman build -t python-app .
STEP 1/7: FROM python:3.11-slim
STEP 2/7: WORKDIR /app
STEP 3/7: COPY requirements.txt .
STEP 4/7: RUN pip install -r requirements.txt
Successfully installed fastapi-0.141.1 uvicorn-0.52.4 ...
STEP 5/7: COPY app.py .
STEP 6/7: EXPOSE 8000
STEP 7/7: CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
COMMIT python-app
Successfully tagged localhost/python-app:latest
```


## Java App (`java-app`)

Built with Java's built-in `HttpServer` (no extra framework needed).

```
$ podman build -t java-app .
STEP 1/6: FROM eclipse-temurin:21-jdk-alpine
STEP 2/6: WORKDIR /app
STEP 3/6: COPY App.java .
STEP 4/6: RUN javac App.java
STEP 5/6: EXPOSE 8080
STEP 6/6: CMD ["java", "App"]
COMMIT java-app
Successfully tagged localhost/java-app:latest
```

## Apache App (`Apache-app`)

Static `index.html` served by the official Apache httpd image.

```
$ podman build -t apache-app .
STEP 1/4: FROM httpd:latest
STEP 2/4: COPY index.html /usr/local/apache2/htdocs/index.html
STEP 3/4: EXPOSE 80
STEP 4/4: CMD ["httpd-foreground"]
COMMIT apache-app
Successfully tagged localhost/apache-app:latest
```


## React App (`React-app`)

Built with Vite, using a multi-stage Dockerfile: stage 1 builds the React app with Node, stage 2 serves the built static files with Nginx.

```
$ podman build -t react-app .
[1/2] STEP 1/6: FROM node:24-alpine AS build
[1/2] STEP 4/6: RUN npm install
[1/2] STEP 6/6: RUN npm run build
vite v5.4.21 building for production...
✓ 30 modules transformed.
✓ built in 299ms
[2/2] STEP 1/4: FROM nginx:latest
[2/2] STEP 2/4: COPY --from=build /app/dist /usr/share/nginx/html
[2/2] STEP 4/4: CMD ["nginx", "-g", "daemon off;"]
COMMIT react-app
Successfully tagged localhost/react-app:latest
```
