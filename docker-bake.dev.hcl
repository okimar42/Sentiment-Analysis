variable "DOCKER_REGISTRY" {
  default = ""
}

variable "DOCKER_ORG" {
  default = "sentiment-analysis"
}

variable "DOCKER_TAG" {
  default = "dev"
}

variable "USE_GPU" {
  default = "true"
}

variable "NO_LOCAL_LLM" {
  default = "0"
}

# If NO_LOCAL_LLM=1 or USE_GPU=false, use Dockerfile.cpu for backend; otherwise use Dockerfile
# This logic is handled by setting the dockerfile path dynamically below

group "default" {
  targets = ["frontend", "backend", "nginx"]
}

target "frontend" {
  context = "./frontend"
  dockerfile = "Dockerfile"
  tags = ["${DOCKER_REGISTRY}${DOCKER_ORG}/frontend:${DOCKER_TAG}"]
  platforms = ["linux/amd64"]
  cache-from = ["type=registry,ref=${DOCKER_REGISTRY}${DOCKER_ORG}/frontend:dev-cache"]
  cache-to = ["type=registry,ref=${DOCKER_REGISTRY}${DOCKER_ORG}/frontend:dev-cache,mode=max"]
  target = "development"
}

target "backend" {
  context = "./backend"
  dockerfile = "${NO_LOCAL_LLM}" == "1" || "${USE_GPU}" == "false" ? "Dockerfile.cpu" : "Dockerfile"
  tags = ["${DOCKER_REGISTRY}${DOCKER_ORG}/backend:${DOCKER_TAG}"]
  platforms = ["linux/amd64"]
  cache-from = ["type=registry,ref=${DOCKER_REGISTRY}${DOCKER_ORG}/backend:dev-cache"]
  cache-to = ["type=registry,ref=${DOCKER_REGISTRY}${DOCKER_ORG}/backend:dev-cache,mode=max"]
  target = "development"
  args = {
    USE_GPU = "${USE_GPU}"
    NO_LOCAL_LLM = "${NO_LOCAL_LLM}"
  }
}

target "nginx" {
  context = "./nginx"
  dockerfile = "Dockerfile"
  tags = ["${DOCKER_REGISTRY}${DOCKER_ORG}/nginx:${DOCKER_TAG}"]
  platforms = ["linux/amd64"]
  cache-from = ["type=registry,ref=${DOCKER_REGISTRY}${DOCKER_ORG}/nginx:dev-cache"]
  cache-to = ["type=registry,ref=${DOCKER_REGISTRY}${DOCKER_ORG}/nginx:dev-cache,mode=max"]
  target = "development"
} 