pipeline{
    agent any

    stages {
        stage("build"){

            steps {
                echo "build the application"

            }
        }
        stage("git pull"){
            steps {
                sh """
                cd /home/flask_project/uk_lines_disrupt
                
                git pull
                """
                
            }
            
        }
    }
}