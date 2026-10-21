#ifndef BALANCER_H
#define BALANCER_H

#include <netinet/in.h>
#include <stdbool.h>

#define MAX_BACKENDS 10
#define BUFFER_SIZE 8192

typedef struct {
    char *address;
    int port;
    bool is_healthy;
    int active_connections;
    int total_requests;
} backend_t;

typedef struct {
    int listen_port;
    backend_t backends[MAX_BACKENDS];
    int num_backends;
} config_t;

typedef struct {
    int client_fd;
    config_t *config;
} client_task_t;

// Function prototypes
int start_server(int port);
void *handle_client(void *arg);
int get_next_backend(config_t *config);
void *health_check_loop(void *arg);
void print_dashboard(config_t *config);

#endif // BALANCER_H
