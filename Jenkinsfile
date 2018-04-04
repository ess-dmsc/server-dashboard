// Set periodic trigger at 12:15 and 23:15, from Monday to Friday.
// properties([
//   pipelineTriggers([cron('15 10,21 * * 1-5')]),
// ])

def failure_function(exception_obj, failureMessage) {
    def toEmails = [[$class: 'DevelopersRecipientProvider']]
    emailext body: '${DEFAULT_CONTENT}\n\"' + failureMessage + '\"\n\nCheck console output at $BUILD_URL to view the results.', recipientProviders: toEmails, subject: '${DEFAULT_SUBJECT}'
    throw exception_obj
}

node('integration-test') {
  // Delete workspace when build is done.
  cleanWs()

  stage("Checkout") {
    checkout scm
  }  // stage

  withCredentials([usernamePassword(
    credentialsId: 'dm_jenkins_gitlab_token',
    usernameVariable: 'USERNAME',
    passwordVariable: 'PASSWORD'
  )]) {
    stage("Clone dm-ansible") {
      sh """
        set +x
        ./jenkins/clone-repo \
          http://git.esss.dk/dm_group/dm-ansible.git \
          ${USERNAME} \
          ${PASSWORD} && \
        cd dm-ansible && \
        git checkout integration_test_refactoring
      """
    }  // stage
  }  // withCredentials

  stage('Deploy') {
    sh """
      cd dm-ansible &&
      ansible-playbook \
        --inventory=inventories/dmsc/integration-test/deployment \
        site.yml
    """
  }  // stage

  stage('Run tests') {
    sh """
      cd dm-ansible &&
      ansible-playbook \
        --inventory=inventories/dmsc/integration-test/deployment \
        ../ansible/run_test.yml
    """
  }
}  // node
