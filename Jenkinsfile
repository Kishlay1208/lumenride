pipeline {
  agent any

  environment {
    IMAGE = "lumenride-svc:1"
    CONTAINER_NAME = "lumenride-svc"
    HOST_PORT = "12056"
    CONTAINER_PORT = "5000"
  }

  stages {
    stage('Pre-check Docker') {
      steps {
        script {
          def rc = sh(script: 'docker info > /dev/null 2>&1 || echo FAIL', returnStdout: true).trim()
          if (rc == 'FAIL') {
            error("Docker is not available on the agent. Ensure Docker is installed and the Jenkins user can access it (e.g. mount /var/run/docker.sock).")
          } else {
            echo "Docker appears available."
            sh 'docker version'
          }
        }
      }
    }

    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build Image') {
      steps {
        sh """
          echo "Building Docker image ${IMAGE} ..."
          docker build -t ${IMAGE} .
        """
      }
    }

    stage('Stop previous container (if any)') {
      steps {
        sh """
          if docker ps -a --format '{{.Names}}' | grep -w ${CONTAINER_NAME} > /dev/null 2>&1; then
            echo "Stopping and removing existing container ${CONTAINER_NAME} ..."
            docker rm -f ${CONTAINER_NAME} || true
          else
            echo "No existing container named ${CONTAINER_NAME}."
          fi
        """
      }
    }

    stage('Run container') {
      steps {
        sh """
          echo "Starting container ${CONTAINER_NAME} mapping host port ${HOST_PORT} -> container port ${CONTAINER_PORT} ..."
          docker run -d --name ${CONTAINER_NAME} -p ${HOST_PORT}:${CONTAINER_PORT} ${IMAGE}
