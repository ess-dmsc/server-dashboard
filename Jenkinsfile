@Library('ecdc-pipeline')
import ecdcpipeline.ContainerBuildNode
import ecdcpipeline.PipelineBuilder
import ecdcpipeline.DeploymentTrigger

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
    dt = new DeploymentTrigger(this, 'server-dashboard-deployment')
    dt.deploy(version)
  }

  // Delete workspace when build is done
  cleanWs()
}
