import sys

def wait_net_service(server, port, timeout=None):
    """ Wait for network service to appear 
        @param timeout: in seconds, if None or 0 wait forever
        @return: True of False, if timeout is None may return only True or
                 throw unhandled network exception
    """
    import socket
    import errno
    from time import sleep

    s = socket.socket()
    if timeout:
        from time import time as now
        # time module is needed to calc timeout shared between two exceptions
        end = now() + timeout
    
    attempt = 0

    while True:
        try:
            if attempt == 3:
                return True;

            attempt = attempt + 1

            if timeout:
                next_timeout = end - now()
                if next_timeout < 0:
                    return False
                else:
            	    s.settimeout(next_timeout)
            
            s.connect((server, port))
        
        except socket.timeout, err:
            # this exception occurs only if timeout is set
            if timeout:
                return False
      
        except socket.error, err:
            # catch timeout exception from underlying network library
            # this one is different from socket.timeout
            sleep(1)
        else:
            s.close()
            return True

if __name__ == '__main__':
    port = 9999
    if len(sys.argv) == 2:
        try:
            port = int(sys.argv[1])
        except:
            port = 9999
    wait_net_service("127.0.0.1", port)
