properties([
  disableConcurrentBuilds(),
  pipelineTriggers([
    cron('11 1 * * *'),
    [
      $class: 'jenkins.triggers.ReverseBuildTrigger',
      upstreamProjects: "ess-dmsc/event-formation-unit/master,ess-dmsc/forwarder/master,ess-dmsc/kafka-to-nexus/master",
      threshold: hudson.model.Result.SUCCESS
    ]
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
    credentialsId: 'dmsc-gitlab-username-with-token',
    usernameVariable: 'USERNAME',
    passwordVariable: 'PASSWORD'
  )]) {
    stage("Clone dm-ansible") {
      sh '''
        set +x
        ./jenkins/clone-repo \
          http://git.esss.dk/dm_group/dm-ansible.git \
          $USERNAME \
          $PASSWORD
      '''
    }  // stage
  }  // withCredentials

  stage('Uninstall') {
    withCredentials([
      string(
        credentialsId: 'dm-ansible-vault-password-file-path',
        variable: 'VAULT_PASSWORD_FILE_PATH'
      )
    ]) {
      sh '''
        cd dm-ansible
        ansible-playbook \
          --inventory=inventories/ci/integration-test-deployment \
          --vault-password-file=$VAULT_PASSWORD_FILE_PATH \
          utils/uninstall_efu.yml
        ansible-playbook \
          --inventory=inventories/ci/integration-test-deployment \
          --vault-password-file=$VAULT_PASSWORD_FILE_PATH \
          utils/uninstall_forwarder.yml
        ansible-playbook \
          --inventory=inventories/ci/integration-test-deployment \
          --vault-password-file=$VAULT_PASSWORD_FILE_PATH \
          utils/uninstall_kafka_to_nexus.yml
        ansible-playbook \
          --inventory=inventories/ci/integration-test-deployment \
          --vault-password-file=$VAULT_PASSWORD_FILE_PATH \
          utils/uninstall_kafka_and_clean_all.yml
        ansible-playbook \
          --inventory=inventories/ci/integration-test-deployment \
          --vault-password-file=$VAULT_PASSWORD_FILE_PATH \
          utils/uninstall_zookeeper_and_clean_all.yml
        ansible-playbook \
          --inventory=inventories/ci/integration-test-deployment \
          --vault-password-file=$VAULT_PASSWORD_FILE_PATH \
          utils/uninstall_conan.yml
      '''
    }  // withCredentials
  }  // stage

  stage('Deploy') {
    withCredentials([
      string(
        credentialsId: 'dm-ansible-vault-password-file-path',
        variable: 'VAULT_PASSWORD_FILE_PATH'
      )
    ]) {
      sh '''
        cd dm-ansible
        ansible-playbook \
          --inventory=inventories/ci/integration-test-deployment \
          --vault-password-file=$VAULT_PASSWORD_FILE_PATH \
          site.yml
      '''
    }  // withCredentials
  }  // stage

  try {
    stage('Run tests') {
      withCredentials([
        string(
          credentialsId: 'dm-ansible-vault-password-file-path',
          variable: 'VAULT_PASSWORD_FILE_PATH'
        )
      ]) {
        sh '''
          cd dm-ansible
          cp ../ansible/*.yml .
          ansible-playbook \
            --inventory=inventories/ci/integration-test-services \
            --inventory=inventories/ci/integration-test-deployment \
            --extra-vars="integration_test_result_dir=\$(pwd)/test-results" \
            --vault-password-file=$VAULT_PASSWORD_FILE_PATH \
            run_test.yml
        '''
      }  // withCredentials
    }  // stage
  } finally {
    stage('Archive') {
      archiveArtifacts 'dm-ansible/test-results/*.log,dm-ansible/test-results/*.nxs'
    }
  }
}  // node
