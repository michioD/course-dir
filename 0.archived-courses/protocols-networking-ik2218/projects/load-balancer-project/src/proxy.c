#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <poll.h>
#include "../include/balancer.h"

int current_backend = 0;

int get_next_backend(config_t *config) {
    if (config->num_backends == 0) return -1;
    
    int chosen = -1;
    int min_conns = -1;

    for (int i = 0; i < config->num_backends; i++) {
        if (!config->backends[i].is_healthy) continue;

        if (chosen == -1 || config->backends[i].active_connections < min_conns) {
            chosen = i;
            min_conns = config->backends[i].active_connections;
        }
    }
    
    return chosen;
}

void *handle_client(void *arg) {
    client_task_t *task = (client_task_t *)arg;
    int client_fd = task->client_fd;
    config_t *config = task->config;

    int backend_idx = get_next_backend(config);
    if (backend_idx < 0) {
        printf("No backends available\n");
        close(client_fd);
        free(task);
        return NULL;
    }

    backend_t *backend = &config->backends[backend_idx];
    backend->active_connections++;
    
    int backend_fd;
    struct sockaddr_in serv_addr;

    if ((backend_fd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        perror("Socket creation error");
        backend->active_connections--;
        close(client_fd);
        free(task);
        return NULL;
    }

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(backend->port);
    inet_pton(AF_INET, backend->address, &serv_addr.sin_addr);

    if (connect(backend_fd, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
        perror("Connection Failed");
        backend->active_connections--;
        close(backend_fd);
        close(client_fd);
        free(task);
        return NULL;
    }

    struct pollfd fds[2];
    fds[0].fd = client_fd;
    fds[0].events = POLLIN;
    fds[1].fd = backend_fd;
    fds[1].events = POLLIN;

    char buffer[BUFFER_SIZE];
    bool active = true;

    while (active) {
        int poll_res = poll(fds, 2, -1);
        if (poll_res < 0) {
            perror("poll error");
            break;
        }

        for (int i = 0; i < 2; i++) {
            if (fds[i].revents & POLLIN) {
                int src_fd = fds[i].fd;
                int dest_fd = (i == 0) ? backend_fd : client_fd;
                
                int n = recv(src_fd, buffer, BUFFER_SIZE, 0);
                if (n <= 0) {
                    active = false;
                    break;
                }
                send(dest_fd, buffer, n, 0);
            }
            if (fds[i].revents & (POLLERR | POLLHUP | POLLNVAL)) {
                active = false;
                break;
            }
        }
    }

    close(backend_fd);
    close(client_fd);
    backend->active_connections--;
    backend->total_requests++;
    free(task);
    return NULL;
}
