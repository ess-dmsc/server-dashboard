@Library('ecdc-pipeline')
import ecdcpipeline.ContainerBuildNode
import ecdcpipeline.PipelineBuilder

containerBuildNodes = [
  'centos7': ContainerBuildNode.getDefaultContainerBuildNode('centos7-gcc11')
]

pipelineBuilder = new PipelineBuilder(this, containerBuildNodes)
pipelineBuilder.activateEmailFailureNotifications()

builders = pipelineBuilder.createBuilders { container ->
  pipelineBuilder.stage("${container.key}: Checkout") {
    dir(pipelineBuilder.project) {
      scmVars = checkout scm
    }
    container.copyTo(pipelineBuilder.project, pipelineBuilder.project)
  }  // stage

  pipelineBuilder.stage("${container.key}: Test") {
    container.sh "/usr/bin/true"
  }  // stage
}  // createBuilders

def deploy(commit) {
  withCredentials([string(
    credentialsId: 'ess-gitlab-server-dashboard-deployment-url',
    variable: 'TRIGGER_URL'
  )]) {
    withCredentials([string(
      credentialsId: 'ess-gitlab-server-dashboard-deployment-token',
      variable: 'TRIGGER_TOKEN'
    )]) {
      sh """
        set +x
        curl -X POST \
          --fail \
          -F token='${TRIGGER_TOKEN}' \
          -F ref=main \
          -F 'variables[COMMIT]=$commit' \
          ${TRIGGER_URL} \
          2>&1 > /dev/null
      """
    }  // TOKEN
  }  // URL
}

node {
  dir("${pipelineBuilder.project}") {
    scmVars = checkout scm
  }

  try {
    parallel builders
  } catch (e) {
    throw e
  }
  
  stage("Deploy") {
    deploy(scmVars.GIT_COMMIT)
  }

  // Delete workspace when build is done
  cleanWs()
}
