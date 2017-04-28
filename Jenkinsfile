node {
    // Set periodic trigger at 12:15 and 23:15, from Monday to Friday.
    properties([
        pipelineTriggers([cron('15 12,23 * * 1-5')]),
    ])

    dir('code') {
        stage('Checkout') {
            checkout scm
        }
    }

    dir('build') {
        stage('Build') {
            sh "export PATH=$CMAKE3_ROOT/bin:$PATH:/opt/dm_group/usr/bin && \
                export LD_LIBRARY_PATH=/opt/dm_group/usr/lib && \
                ./build/efu/build.bash"
        }

        stage('Archive') {
            archiveArtifacts artifacts: 'output.tar.gz', fingerprint: true, onlyIfSuccessful: true
        }
    }

    // Delete workspace when build is done.
    cleanWs()
}
