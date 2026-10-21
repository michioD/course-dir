#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <signal.h>
#include <pthread.h>
#include "../include/balancer.h"

int server_fd;

void handle_sigint(int sig) {
    (void)sig; // Fix unused parameter warning
    printf("\nShutting down server...\n");
    close(server_fd);
    exit(0);
}

int start_server(int port) {
    struct sockaddr_in address;
    int opt = 1;
    // what is opt?
    // what is fd?
    // what is AF_INET 
    // what is SOCK_STREAM?
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        perror("socket failed");
        exit(EXIT_FAILURE);
    }
    // what is &opt
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt))) {
        perror("setsockopt");
        exit(EXIT_FAILURE);
    }
    // waht is sin_famiyl?
    // what is sin_addr?
    // what is INADDR_ANY?
    // what is htons?
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(port);

    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) {
        perror("bind failed");
        exit(EXIT_FAILURE);
    }

    if (listen(server_fd, 3) < 0) {
        perror("listen");
        exit(EXIT_FAILURE);
    }

    printf("Load balancer listening on port %d\n", port);
    return server_fd;
}

void *dashboard_loop(void *arg) {
    config_t *config = (config_t *)arg;
    while (1) {
        print_dashboard(config);
        sleep(1);
    }
    return NULL;
}

void print_dashboard(config_t *config) {
    printf("\033[H\033[J"); // Clear screen
    printf("C-LOAD-BALANCER Dashboard\n");
    printf("----------------------------------------------------------------------\n");
    printf("%-20s %-10s %-10s %-10s\n", "Backend", "Status", "Active", "Total");
    printf("----------------------------------------------------------------------\n");
    for (int i = 0; i < config->num_backends; i++) {
        backend_t *backend = &config->backends[i];
        printf("%-20s %-10s %-10d %-10d\n", 
               backend->address, 
               backend->is_healthy ? "UP" : "DOWN", 
               backend->active_connections,
               backend->total_requests);
    }
    printf("----------------------------------------------------------------------\n");
    printf("Listening on port: %d\n", config->listen_port);
}

int main(int argc, char const *argv[]) {
    (void)argc; (void)argv;
    signal(SIGINT, handle_sigint);

    config_t config = {
        .listen_port = 8080,
        .num_backends = 2,
        .backends = {
            {"127.0.0.1", 8081, true, 0, 0},
            {"127.0.0.1", 8082, true, 0, 0}
        }
    };

    pthread_t health_thread, dashboard_thread;
    pthread_create(&health_thread, NULL, health_check_loop, &config);
    pthread_create(&dashboard_thread, NULL, dashboard_loop, &config);

    int listen_fd = start_server(config.listen_port);

    while (1) {
        struct sockaddr_in client_addr;
        socklen_t addrlen = sizeof(client_addr);
        int client_fd = accept(listen_fd, (struct sockaddr *)&client_addr, &addrlen);
        
        if (client_fd < 0) {
            perror("accept");
            continue;
        }
        // what is client_task_t?
        client_task_t *task = malloc(sizeof(client_task_t));
        task->client_fd = client_fd;
        task->config = &config;

        pthread_t client_thread;
        if (pthread_create(&client_thread, NULL, handle_client, task) != 0) {
            perror("Failed to create client thread");
            close(client_fd);
            free(task);
        } else {
            pthread_detach(client_thread);
        }
    }

    return 0;
}
