def healthcheck(register):
    '''
    healthcheck function to interate through the list of servers and update their status
    '''
    for host in register:
        for server in register[host]:
            server.healthcheck_and_update_status()
    return register