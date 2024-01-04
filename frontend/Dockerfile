FROM --platform=linux/amd64 node:16-alpine as build
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY . ./
RUN npm install
RUN npm run build

FROM --platform=linux/amd64 nginx:stable
RUN apt-get update && apt-get install -y nginx-extras
RUN apt-get install libnginx-mod-http-headers-more-filter
RUN rm /etc/nginx/sites-enabled/default
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx/default.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
