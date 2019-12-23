## Dockerfile References: https://docs.docker.com/engine/reference/builder/
#
## Start from the latest golang base image
#FROM golang:latest
#
## Set the Current Working Directory inside the container
#WORKDIR /app
#
## Copy go mod and sum files
#COPY go.mod go.sum ./
#
## Download all dependencies. Dependencies will be cached if the go.mod and go.sum files are not changed
#RUN go mod download
#
## Copy the source from the current directory to the Working Directory inside the container
#COPY . .
#
## Build the Go app
#RUN go build -o main .
#
## Run the binary program produced by `go install`
#CMD ["./main"]


FROM alpine:3.9
RUN apk add bind-tools
RUN  apk update && \
     apk add libc6-compat && \
     apk add ca-certificates

COPY ./pdex-data-collector /
COPY ./run.sh /

RUN chmod +x /pdex-data-collector
RUN chmod +x /run.sh

CMD ["/bin/sh", "./run.sh"]