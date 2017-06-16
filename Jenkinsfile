// Set periodic trigger at 12:15 and 23:15, from Monday to Friday.
properties([
    pipelineTriggers([cron('15 10,21 * * 1-5')]),
])

def failure_function(exception_obj, failureMessage) {
    def toEmails = [[$class: 'DevelopersRecipientProvider']]
    emailext body: '${DEFAULT_CONTENT}\n\"' + failureMessage + '\"\n\nCheck console output at $BUILD_URL to view the results.', recipientProviders: toEmails, subject: '${DEFAULT_SUBJECT}'
    throw exception_obj
}

node('kafka-client') {
    // Delete workspace when build is done.
    cleanWs()

    dir('code') {
        try {
            stage('Checkout') {
                checkout scm
            }
        } catch (e) {
            failure_function(e, 'Checkout failed')
        }
    }

    dir('build') {
        try {
            stage('Build') {
                sh "export PATH=$CMAKE3_ROOT/bin:$PATH:/opt/dm_group/usr/bin && \
                    export LD_LIBRARY_PATH=/opt/dm_group/usr/lib && \
                    ../code/efu/build.bash"
            }
        } catch (e) {
            failure_function(e, 'Build failed')
        }    
    }

    dir('code') {
        try {
            stage('Stash') {
                stash includes: 'ansible/', name: 'ansible'
            }
        } catch (e) {
            failure_function(e, 'Stash failed')
        }
    }
}

// This currently uses the artifact from the integration-test job.
node('integration-test') {
    dir('code') {
        try {
            stage('Unstash') {
                unstash 'ansible'
            }
        } catch (e) {
            failure_function(e, 'Unstash failed')
        }
        
        try {
            stage('Deploy') {
                sh "ansible-playbook -i ansible/hosts ansible/site.yml"
            }
        } catch (e) {
            failure_function(e, 'Deploy failed')
        }
        
        try {
            stage('Test') {
                sh "ansible-playbook -i ansible/hosts ansible/run_test.yml"
            }
        } catch (e) {
            failure_function(e, 'Test failed')
        }
    }
}
