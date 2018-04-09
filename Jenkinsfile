properties([
  disableConcurrentBuilds(),
  pipelineTriggers([
    [$class: 'PeriodicFolderTrigger', interval: '1d'],
    [$class: 'jenkins.triggers.ReverseBuildTrigger', upstreamProjects: "ess-dmsc/event-formation-unit/master", threshold: hudson.model.Result.SUCCESS],
    [$class: 'jenkins.triggers.ReverseBuildTrigger', upstreamProjects: "ess-dmsc/forward-epics-to-kafka/essiip-deployment", threshold: hudson.model.Result.SUCCESS],
    [$class: 'jenkins.triggers.ReverseBuildTrigger', upstreamProjects: "ess-dmsc/kafka-to-nexus/essiip-deployment", threshold: hudson.model.Result.SUCCESS]
  ])
])


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
          ${PASSWORD}
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
      cp ../ansible/*.yml . &&
      ansible-playbook \
        --inventory=inventories/dmsc/integration-test/deployment \
        run_test.yml
    """
  }
}  // node
