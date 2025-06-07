variable "DOCKER_REGISTRY" {
  default = ""
}

variable "DOCKER_ORG" {
  default = "sentiment-analysis"
}

variable "DOCKER_TAG" {
  default = "latest"
}

group "default" {
  targets = ["frontend", "backend", "nginx"]
}

target "frontend" {
  context = "./frontend"
  dockerfile = "Dockerfile.dev"
  tags = ["${DOCKER_REGISTRY}${DOCKER_ORG}/frontend:${DOCKER_TAG}"]
  platforms = ["linux/amd64"]
  cache-from = ["type=registry,ref=${DOCKER_REGISTRY}${DOCKER_ORG}/frontend:buildcache"]
  cache-to = ["type=registry,ref=${DOCKER_REGISTRY}${DOCKER_ORG}/frontend:buildcache,mode=max"]
}

target "backend" {
  context = "./backend"
  dockerfile = "Dockerfile"
  tags = ["${DOCKER_REGISTRY}${DOCKER_ORG}/backend:${DOCKER_TAG}"]
  platforms = ["linux/amd64"]
  cache-from = ["type=registry,ref=${DOCKER_REGISTRY}${DOCKER_ORG}/backend:buildcache"]
  cache-to = ["type=registry,ref=${DOCKER_REGISTRY}${DOCKER_ORG}/backend:buildcache,mode=max"]
}

target "nginx" {
  context = "./nginx"
  dockerfile = "Dockerfile"
  tags = ["${DOCKER_REGISTRY}${DOCKER_ORG}/nginx:${DOCKER_TAG}"]
  platforms = ["linux/amd64"]
  cache-from = ["type=registry,ref=${DOCKER_REGISTRY}${DOCKER_ORG}/nginx:buildcache"]
  cache-to = ["type=registry,ref=${DOCKER_REGISTRY}${DOCKER_ORG}/nginx:buildcache,mode=max"]
} 