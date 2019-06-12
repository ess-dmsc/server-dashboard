properties([
  disableConcurrentBuilds(),
  pipelineTriggers([[
    $class: 'jenkins.triggers.ReverseBuildTrigger',
    upstreamProjects: "ess-dmsc/event-formation-unit/debug_integration_test,ess-dmsc/forward-epics-to-kafka/master,ess-dmsc/kafka-to-nexus/master",
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
    withCredentials([
      file(
        credentialsId: 'dm-ansible-vault-password-file',
        variable: 'VAULT_PASSWORD_FILE'
      )
    ]) {
      sh """
        cd dm-ansible
        ansible-playbook \
          --inventory=inventories/ci \
          --vault-password-file=${VAULT_PASSWORD_FILE} \
          uninstall_efu.yml
        ansible-playbook \
          --inventory=inventories/ci \
          --vault-password-file=${VAULT_PASSWORD_FILE} \
          uninstall_forward_epics_to_kafka.yml
        ansible-playbook \
          --inventory=inventories/ci \
          --vault-password-file=${VAULT_PASSWORD_FILE} \
          uninstall_kafka_to_nexus.yml
        ansible-playbook \
          --inventory=inventories/ci \
          --vault-password-file=${VAULT_PASSWORD_FILE} \
          uninstall_kafka_and_clean_all.yml
        ansible-playbook \
          --inventory=inventories/ci \
          --vault-password-file=${VAULT_PASSWORD_FILE} \
          uninstall_zookeeper_and_clean_all.yml
      """
    }  // withCredentials
  }  // stage

  stage('Deploy') {
    withCredentials([
      file(
        credentialsId: 'dm-ansible-vault-password-file',
        variable: 'VAULT_PASSWORD_FILE'
      )
    ]) {
      sh """
        cd dm-ansible
        ansible-playbook \
          --inventory=inventories/ci/integration-test-deployment \
          --vault-password-file=${VAULT_PASSWORD_FILE} \
          site.yml
      """
    }  // withCredentials
  }  // stage

  try {
    stage('Run tests') {
      withCredentials([
        file(
          credentialsId: 'dm-ansible-vault-password-file',
          variable: 'VAULT_PASSWORD_FILE'
        )
      ]) {
        sh """
          cd dm-ansible
          cp ../ansible/*.yml .
          ansible-playbook \
            --inventory=inventories/ci \
            --extra-vars="integration_test_result_dir=\$(pwd)/test-results" \
            --vault-password-file=${VAULT_PASSWORD_FILE} \
            run_test.yml
        """
      }  // withCredentials
    }  // stage
  } finally {
    stage('Archive') {
      archiveArtifacts 'dm-ansible/test-results/*.log'
    }
  }
}  // node
