
pipeline {
  agent any

  options {
    timestamps()
    disableConcurrentBuilds()
    timeout(time: 20, unit: 'MINUTES')
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
            python3 -m venv venv
            . venv/bin/activate
            python --version
            pip install --upgrade pip
            # Install your app dependencies
            if [ -f requirements.txt ]; then
              pip install -r requirements.txt
            else
              pip install Flask mysql-connector-python
            fi
            # Install test tool
            pip install pytest
          '''
        }
      }
    }

    stage('Run Tests (skip DB)') {
      environment {
        SKIP_DB = '1'   // your Flask app should use this to bypass MySQL init
      }
      steps {
        dir('app') {
          sh '''
            . venv/bin/activate
            pytest --maxfail=1 --disable-warnings -q
            # If you prefer a specific file:
            # pytest tests/test.py --maxfail=1 --disable-warnings -q
          '''
        }
      }
      // If you later add JUnit XML, you can publish it like:
      // post { always { junit 'app/tests/test-results.xml' } }
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
