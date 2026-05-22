stage('semgrep-scan') {
  steps {
    sh '''
      docker pull semgrep/semgrep:1.157.0

      CONTAINER_NAME="semgrep-main-${BUILD_NUMBER}"

      echo "Starting Semgrep full scan on main branch..."
      echo "Container name: $CONTAINER_NAME"

      (
        while true; do
          docker stats --no-stream \
            --format "Semgrep memory: {{.MemUsage}} | CPU: {{.CPUPerc}}" \
            "$CONTAINER_NAME" 2>/dev/null || true
          sleep 5
        done
      ) &
      STATS_PID=$!

      docker run --name "$CONTAINER_NAME" --rm \
        --memory=8g \
        --memory-swap=8g \
        -e SEMGREP_APP_TOKEN="$SEMGREP_APP_TOKEN" \
        -e SEMGREP_REPO_NAME="$SEMGREP_REPO_NAME" \
        -v "$(pwd):$(pwd)" --workdir "$(pwd)" \
        --entrypoint /bin/sh \
        semgrep/semgrep:1.157.0 \
        -lc '
          apk add --no-cache openjdk17-jdk maven

          echo "Java version:"
          java -version

          echo "Maven version:"
          mvn -version

          semgrep ci --supply-chain --allow-local-builds --x-mem-policy=aggressive
        '

      SCAN_EXIT_CODE=$?

      kill $STATS_PID 2>/dev/null || true

      exit $SCAN_EXIT_CODE
    '''
  }
}
