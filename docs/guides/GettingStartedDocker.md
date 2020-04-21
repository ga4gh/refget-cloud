# Getting Started - Docker Container Setup

## Installation

As a prerequisite, Docker must be installed on your system.

The refget web server can be run via Docker container. The repository of versioned docker images is available on Docker Hub at [ga4gh/refget-cloud](https://hub.docker.com/repository/docker/ga4gh/refget-cloud)

Execute the following command to pull a specific version of the Docker image (in this case, version 0.3.0):
```
docker pull ga4gh/refget-cloud:0.3.0
```

## Usage

To spin up a server through a docker container, use the `docker run` command. Be sure to publish the port the service is running on to the host 
```
docker run -p 8888:8888 ga4gh/refget-cloud:0.3.0
```

Running the service like this is not necessarily very useful, as the server is configured with all default parameters. This means it will run on the default port (8888), and only serve reference sequences from the AWS INSDC public dataset.

To configure the service with custom properties (e.g. port, data source, etc.), you may pass specific **environment variables** to the docker container. For example, to change the port the server runs on inside the container, you would execute:
```
docker run -p 80:80 --env SERVER_PORT=80 ga4gh/refget-cloud:0.3.0
```

Click [here](../other/RefgetServerProperties.md) to view allowed environment variable names and their uses. 
