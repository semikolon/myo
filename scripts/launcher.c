// MyoBridge launcher: the app bundle's main executable.
// It starts the Python bridge as a CHILD (never exec), so macOS treats MyoBridge.app
// as the responsible process: the Bluetooth prompt names MyoBridge, and the grant
// belongs to this app rather than to the Python interpreter.
// Build: scripts/build_app.sh. Arguments pass through to the bridge.
#include <signal.h>
#include <spawn.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>

extern char **environ;
static pid_t child = 0;

static void forward(int sig) {
    if (child > 0) kill(child, sig);
}

int main(int argc, char *argv[]) {
    const char *python = PYTHON_PATH;  // set by the build script
    char **args = calloc((size_t)argc + 4, sizeof(char *));
    if (!args) return 1;
    args[0] = (char *)python;
    args[1] = "-m";
    args[2] = "myo_bridge.bridge";
    for (int i = 1; i < argc; i++) args[i + 2] = argv[i];

    signal(SIGTERM, forward);
    signal(SIGINT, forward);
    signal(SIGHUP, forward);

    int rc = posix_spawn(&child, python, NULL, NULL, args, environ);
    if (rc != 0) {
        fprintf(stderr, "MyoBridge: cannot start %s: %s\n", python, strerror(rc));
        return 1;
    }
    int status = 0;
    while (waitpid(child, &status, 0) < 0) {
    }
    return WIFEXITED(status) ? WEXITSTATUS(status) : 1;
}
