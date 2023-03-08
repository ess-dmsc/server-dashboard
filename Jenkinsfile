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
    container.sh "/usr/bin/false"
  }  // stage
}  // createBuilders

node {
  dir("${pipelineBuilder.project}") {
    scmVars = checkout scm
  }

  try {
    parallel builders
    echo "Failed?"
  } catch (e) {
    throw e
  }

  // Delete workspace when build is done
  cleanWs()
}
