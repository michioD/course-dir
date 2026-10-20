#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <pthread.h>
#include "../include/balancer.h"

void *health_check_loop(void *arg) {
    config_t *config = (config_t *)arg;
    while (1) {
        for (int i = 0; i < config->num_backends; i++) {
            backend_t *backend = &config->backends[i];
            
            int sockfd = socket(AF_INET, SOCK_STREAM, 0);
            if (sockfd < 0) continue;

            struct timeval tv;
            tv.tv_sec = 1;
            tv.tv_usec = 0;
            setsockopt(sockfd, SOL_SOCKET, SO_RCVTIMEO, (const char*)&tv, sizeof tv);
            setsockopt(sockfd, SOL_SOCKET, SO_SNDTIMEO, (const char*)&tv, sizeof tv);

            struct sockaddr_in serv_addr;
            serv_addr.sin_family = AF_INET;
            serv_addr.sin_port = htons(backend->port);
            inet_pton(AF_INET, backend->address, &serv_addr.sin_addr);

            if (connect(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) == 0) {
                if (!backend->is_healthy) {
                    printf("Backend %s:%d is now UP\n", backend->address, backend->port);
                }
                backend->is_healthy = true;
            } else {
                if (backend->is_healthy) {
                    printf("Backend %s:%d is now DOWN\n", backend->address, backend->port);
                }
                backend->is_healthy = false;
            }
            close(sockfd);
        }
        sleep(5);
    }
    return NULL;
}
