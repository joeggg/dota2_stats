"""
    Module initialisation
"""
import gevent.monkey

gevent.monkey.patch_socket()
gevent.monkey.patch_ssl()
