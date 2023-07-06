#define _XOPEN_SOURCE 700

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <stdbool.h>
#include <fcntl.h>
#include <sys/wait.h>
#include <signal.h>

#define MAX_IN 1024
#define MAX_TOKEN 512

int lfgs = 0, lbgp = -1;
int status = 0;
bool foreground_mode = false;
bool taking_input = true;

struct sigaction SIGINT_action = {0}, SIGTSTP_action = {0};

void init();

void handle_SIGTSTP(int);

void handle_SIGINT(int);

bool is_numeric(const char *s);

void child_exit();

void do_cd(char **args);

void do_exit(char **args);

void do_status(char **args);

void loop();

char **parse(char *line);

void run(char **args);


void str_replace(char *target, const char *needle, const char *replacement) {
    char buffer[1024] = {0};
    char *insert_point = &buffer[0];
    const char *tmp = target;
    size_t needle_len = strlen(needle);
    size_t repl_len = strlen(replacement);

    while (1) {
        const char *p = strstr(tmp, needle);

        // walked past last occurrence of needle; copy remaining part
        if (p == NULL) {
            strcpy(insert_point, tmp);
            break;
        }

        // copy part before needle
        memcpy(insert_point, tmp, p - tmp);
        insert_point += p - tmp;

        // copy replacement string
        memcpy(insert_point, replacement, repl_len);
        insert_point += repl_len;

        // adjust pointers, move on
        tmp = p + needle_len;
    }

    // write altered string back to target
    strcpy(target, buffer);
}

int main() {
    init();
    loop();
    return 0;
}

void init() {
    signal(SIGCHLD, child_exit); // handle child exit of background process.

    SIGINT_action.sa_handler = handle_SIGINT;
    sigfillset(&SIGINT_action.sa_mask);
    SIGINT_action.sa_flags = 0;

    SIGTSTP_action.sa_handler = handle_SIGTSTP;
    sigfillset(&SIGTSTP_action.sa_mask);
    SIGTSTP_action.sa_flags = 0;

    sigaction(SIGINT, &SIGINT_action, NULL);
    sigaction(SIGTSTP, &SIGTSTP_action, NULL);
}

char **parse(char *line) {
    int pid = getpid();
    char *spid = malloc(sizeof(100));
    char *fgpid = malloc(sizeof(100));
    char *bgpid = malloc(sizeof(100));

    sprintf(spid, "%d", pid);
    sprintf(fgpid, "%d", lfgs);
    if (lbgp != -1)
        sprintf(bgpid, "%d", lbgp);
    else {
//        free(bgpid);
        bgpid = "";
    }
    for (int i = 0; i < strlen(line); i++) {
        if (line[i] == '#') {
            line[i] = '\0';
            break;
        }
    }
    str_replace(line, "$$", spid);
    str_replace(line, "$?", fgpid);
    str_replace(line, "$!", bgpid);
    char *path = malloc(1024);
    strcpy(path, getenv("HOME"));
    strcat(path, "/");
    str_replace(line, "~/", path);
//    free(path);

    str_replace(line, " \'", "\'"); // hacky way to make strings works, sets next delimit to '

//    free(spid);
//    free(fgpid);
//    if(strcmp(bgpid, "") != 0)
//    free(bgpid);

    char **tokens = malloc(MAX_TOKEN * sizeof(char *));
    char *token;

    int n = strlen(line);
    line[n] = ' ';
    line[n + 1] = '\0';
    char delimit[] = " \t\r\n\v\f\'";
    char *temp = malloc(n + 2);
    strcpy(temp, line);
    token = strtok(line, delimit);
    int index = 0;
    while (token != NULL) {
        int s_index = token - line;

//        printf("%s %d %c\n", token, s_index, *(temp + s_index + strlen(token)));

        bool in_string = false;
        if(s_index + strlen(token) < n) {
            if (*(temp + s_index + strlen(token)) == '\'') {
                // check if we have a ending ' in string.
                for(int k = s_index + strlen(token) + 1; k < n; k ++)
                    if(temp[k] == '\'') {
                        in_string = true;
                        break;
                    }
            }
        }
        tokens[index++] = token;
        token = strtok(NULL, in_string ? "\'" : delimit);
    }
    tokens[index] = NULL;
    return tokens;
}

void loop() {
    while (1) {
        taking_input = true;
        char *line = malloc(MAX_IN);
        size_t n;


        // check if any background child process exited.
        pid_t pid = waitpid(-1, &status, WNOHANG);
        if (pid != 0 && pid != -1) {
            printf("Background child %d exited with the status %d\n", pid, status);
        }

        fprintf(stdout, getenv("PS1"));
        fflush(stdout);

        *line = '\0';
        getline(&line, &n, stdin);
        taking_input = false;
        char **tokens = parse(line);
        run(tokens);

        free(line);
        free(tokens);
    }
}

void run(char **args) {
    if (args[0] == NULL) return;

    bool infile_redirection = false;
    bool outfile_redirection = false;
    bool is_bg = false;

    char *infile, *outfile;

    int size = 0;
    while (args[size] != NULL) size++;

    if (strcmp(args[0], "cd") == 0) {
        do_cd(args);
        return;
    } else if (strcmp(args[0], "exit") == 0) {
        do_exit(args);
        return;
    } else if (strcmp(args[0], "status") == 0) {
        do_status(args);
        return;
    }
    // infile outfile can be
    bool is_prev_ok = false;
    for (int i = size - 1; i >= 0; i--) {
        if (i == size - 1 && strcmp(args[i], "&") == 0) {
            is_bg = true;
            args[size - 1] = NULL;
            is_prev_ok = false;
        } else if (strcmp(args[i], "<") == 0 && is_prev_ok) {
            is_prev_ok = false;
            infile_redirection = true;
            infile = args[i + 1];
            args[i] = NULL;
        } else if (strcmp(args[i], ">") == 0 && is_prev_ok) {
            is_prev_ok = false;
            outfile_redirection = true;
            outfile = args[i + 1];
            args[i] = NULL;
        } else if (is_prev_ok) {
            // two args means now we can't have any redirection.
            break;
        } else {
            is_prev_ok = true;
        }
    }


    pid_t cpid = fork();

    switch (cpid) {
        case 0:
            signal(SIGCHLD, NULL); // handle child exit of background process.
            SIGINT_action.sa_handler = SIG_DFL;
            sigaction(SIGINT, &SIGINT_action, NULL);
            // input/output redirection.
            if (infile_redirection) {
                int currfd = open(infile, O_RDONLY, 0640);
                if (currfd == -1) {
                    fprintf(stderr, "cannot open %s for input", infile);
                    exit(1);
                }
                int dest = dup2(currfd, 0);
                if (dest == -1) {
                    perror("can't redirect stdin to infile");
                    exit(1);
                }
            }
            if (outfile_redirection) {
                int currfd = open(outfile, O_WRONLY | O_CREAT | O_TRUNC, 0640);
                if (currfd == -1) {
                    fprintf(stderr, "cannot open %s for input", outfile);
                    exit(2);
                }
                int dest = dup2(currfd, 1);
                if (dest == -1) {
                    perror("can't redirect stdout to outfile");
                    exit(2);
                }
            }
            // execute the command.
            if (execvp(args[0], args) == -1) {
                perror(args[0]);
                fflush(stderr);
                fflush(stdout);
                exit(1);
            }
            break;
        case -1:
            perror("fork() failed");
            exit(1);
            break;
        default:
            if (is_bg && !foreground_mode) {
                lbgp = cpid;
                printf("Background process id: %d\n", cpid);
                fflush(stdout);
            } else {
                pid_t p = waitpid(cpid, &status, 0);
                if (p != -1) {
                    if (WIFSTOPPED(status) && WSTOPSIG(status) == SIGSTOP) {
                        printf("Child process %d stopped. Continuing.\n", cpid);
                        if (kill(cpid, SIGCONT) == -1) {
                            perror("kill");
                            exit(EXIT_FAILURE);
                        }
                        lbgp = cpid;
                        return;
                    }
                    if (WIFEXITED(status)) {
                        lfgs = WEXITSTATUS(status);
                    }
                    if (WIFSIGNALED(status)) {
                        lfgs = 128 + WTERMSIG(status);
                    }
                }
            }
    }
}

void handle_SIGINT(int signo) {
    (void) (signo);
    if (taking_input) {
        exit(1);
    }
    return;
}

void handle_SIGTSTP(int signo) {
    (void) (signo);
    // enable fg mode
    if (foreground_mode) {
        printf("Exiting foreground only mode.\n");
        fflush(stdout);
        // disable fg mode
    } else {
        printf("Entering foreground only mode. '&' will be ignored.");
        fflush(stdout);
    }
    foreground_mode = !foreground_mode;
}

void do_cd(char **args) {
    char path[1024];
    getcwd(path, sizeof path);

    if (args[1] == NULL) {
        chdir(getenv("HOME"));
    } else {
        strcat(path, "/");
        strcat(path, args[1]);
        chdir(path);
    }

    getcwd(path, sizeof path);
}

void do_exit(char **args) {
    printf("\nexit\n");
    int ex_status = lfgs;
    if (args[1] != NULL && args[2] != NULL) {
        perror("More than 2 argument to exit.");
        return;
    }
    if (args[1] != NULL) {
        if (!is_numeric(args[1])) {
            perror("exit status must be numeric");
            return;
        }
        ex_status = atoi(args[1]);
    }

    exit(ex_status);
}

bool is_numeric(const char *s) {
    while (*s) {
        if (*s < '0' || *s > '9')
            return false;
        ++s;
    }
    return true;
}

void child_exit() {
    int wstat;
    pid_t pid;

    while (true) {
        pid = wait3(&wstat, WNOHANG, (struct rusage *) NULL);
        if (pid != 0 && pid != -1) {
            if (WIFSIGNALED(pid))
                printf("Child process %d done. Signaled: %d.\n", pid, WTERMSIG(pid));
            else
                printf("Child process %d done. Exit status: %d.\n", pid, wstat);
        } else
            return;
    }
}

void do_status(char **args) {
    if (WIFSIGNALED(status)) {
        printf("exited with signal %d\n", WTERMSIG(status));
        fflush(stdout);
    } else {
        printf("exited with status %d\n", WEXITSTATUS(status));
        fflush(stdout);
    }
}
