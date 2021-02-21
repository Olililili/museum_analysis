## To build the Docker image
`docker build -t museum_analysi .`

## If the above command throw error message: "ERROR [internal] load metadata for docker.io/library/python:3", run it with sudo
`sudo docker build -t museum_analysi .`

## To deploy the Docker container and run museum_analysis
`docker run -p 4000:80 museum_analysis`

