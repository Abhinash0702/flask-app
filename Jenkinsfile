
pipeline {
  agent {
    docker {
      image 'python:3.11-slim'      // use 'python:3.11-alpine' if you prefer Alpine
      args  '-u'                    // unbuffered output for clearer logs
    }
  }

  options {
    timestamps()
    disableConcurrentBuilds()
    timeout(time: 20, unit: 'MINUTES')
  }

  environment {
    PIP_DISABLE_PIP_VERSION_CHECK = '1'
    PIP_NO_CACHE_DIR = '1'
    SKIP_DB = '1'                   // used by your tests to skip DB
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Setup Python Env') {
      steps {
        dir('app') {
          sh '''
            set -e
            python --version
            python -m venv venv
            . venv/bin/activate
            pip install --upgrade pip
            if [ -f requirements.txt ]; then
              pip install -r requirements.txt
            else
              pip install Flask mysql-connector-python
            fi
            pip install pytest
          '''
        }
      }
    }

    stage('Run Tests (skip DB)') {
      steps {
        dir('app') {
          sh '''
            set -e
            . venv/bin/activate
            pytest --maxfail=1 --disable-warnings -q
          '''
        }
      }
    }
  }

  post {
    success {
      echo '✅ Python code validated successfully (DB skipped in CI).'
    }
    failure {
      echo '❌ Validation failed. Check the stage logs above.'
    }
    always {
      cleanWs()
    }
  }
}
