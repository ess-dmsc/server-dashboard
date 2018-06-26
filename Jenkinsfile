properties([
  disableConcurrentBuilds(),
  pipelineTriggers([[
    $class: 'jenkins.triggers.ReverseBuildTrigger',
    upstreamProjects: "ess-dmsc/event-formation-unit/master,ess-dmsc/forward-epics-to-kafka/master,ess-dmsc/kafka-to-nexus/master",
    threshold: hudson.model.Result.SUCCESS
  ]])
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

  stage('Uninstall') {
    sh """
      cd dm-ansible &&
      ansible-playbook \
        --inventory=inventories/dmsc/integration-test \
        uninstall_efu.yml && \
      ansible-playbook \
        --inventory=inventories/dmsc/integration-test \
        uninstall_forward_epics_to_kafka.yml &&
      ansible-playbook \
        --inventory=inventories/dmsc/integration-test \
        uninstall_kafka_to_nexus.yml
    """
  }  // stage

  stage('Deploy') {
    sh """
      cd dm-ansible &&
      ansible-playbook \
        --inventory=inventories/dmsc/integration-test/deployment \
        site.yml
    """
  }  // stage

  try {
    stage('Run tests') {
      sh """
        cd dm-ansible &&
        cp ../ansible/*.yml . &&
        ansible-playbook \
          --inventory=inventories/dmsc/integration-test \
          --extra-vars="integration_test_result_dir=\$(pwd)/test-results" \
          run_test.yml
      """
    }
  } finally {
    stage('Archive') {
      archiveArtifacts 'dm-ansible/test-results/*.log'
    }
  }
}  // node
