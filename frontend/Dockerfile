FROM node:22-alpine AS build

WORKDIR /app

COPY package*.json ./

RUN npm ci

COPY . .

ARG VITE_USER_SERVICE_URL=/api/users
ARG VITE_STUDENT_SERVICE_URL=/api/students
ARG VITE_LECTURER_SERVICE_URL=/api/lecturers
ARG VITE_COURSE_SERVICE_URL=/api/courses
ARG VITE_ENROLLMENT_SERVICE_URL=/api/enrollments

ENV VITE_USER_SERVICE_URL=${VITE_USER_SERVICE_URL}
ENV VITE_STUDENT_SERVICE_URL=${VITE_STUDENT_SERVICE_URL}
ENV VITE_LECTURER_SERVICE_URL=${VITE_LECTURER_SERVICE_URL}
ENV VITE_COURSE_SERVICE_URL=${VITE_COURSE_SERVICE_URL}
ENV VITE_ENROLLMENT_SERVICE_URL=${VITE_ENROLLMENT_SERVICE_URL}

RUN npm run build

FROM alpine:3.23

# Alpine's own nginx package receives security patches directly,
# so apk installs the fixed build that Docker Scout checks against.
# Logs are redirected to stdout/stderr so docker logs and kubectl logs work.
RUN apk upgrade --no-cache \
    && apk add --no-cache nginx \
    && mkdir -p /run/nginx /usr/share/nginx/html \
    && ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

COPY nginx.conf /etc/nginx/http.d/default.conf

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]