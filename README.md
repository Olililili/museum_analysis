## 1. Git clone museum_analysis repository
`git clone https://github.com/Olililili/museum_analysis.git`

## 2. cd into the cloned repository, for example:
`cd /Users/yixunli/GitProjects`

## 3. build the Docker image
`docker build -t museum_analysis .`

### If the above command throw error message: "ERROR [internal] load metadata for docker.io/library/python:3", run it with sudo
`sudo docker build -t museum_analysis .`

## 4. deploy the Docker container and run museum_analysis
`docker run -p 4000:80 museum_analysis`

