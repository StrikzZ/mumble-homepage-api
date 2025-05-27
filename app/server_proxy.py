import Ice
import atexit
import os
import threading
import MumbleServer as Murmur
import signal
import sys

ICE_HOST = os.getenv("ICE_HOST", "localhost")
ICE_PORT = int(os.getenv("ICE_PORT", 6502))
ICE_ENDPOINT = f"Meta:tcp -h {ICE_HOST} -p {ICE_PORT}"

ICE_SECRET_READ = os.getenv("ICE_SECRET_READ", "")

_lock = threading.Lock()
_communicator = None
_server = None

def _cleanup_ice():
    global _communicator, _server
    try:
        if _communicator:
            try:
                _communicator.destroy()
                print("Ice communicator destroyed")
            except Exception:
                pass
        _communicator = None
        _server = None
    except Exception:
        pass

def cleanup_and_exit(signum, frame):
    print("Cleanup due to Signal!")
    _cleanup_ice()
    exit(0)

def build_ice_communicator():
    props = Ice.createProperties(sys.argv)
    props.setProperty("Ice.ImplicitContext", "Shared")
    props.setProperty("Ice.Override.Timeout", "200")
    props.setProperty("Ice.MessageSizeMax", "4096")
    initdata = Ice.InitializationData()
    initdata.properties = props
    comm = Ice.initialize(initdata)
    if ICE_SECRET_READ:
        comm.getImplicitContext().put("secret", ICE_SECRET_READ)
    return comm

def get_server_proxy():
    global _communicator, _server
    with _lock:
        if _server:
            try:
                _server.getConf("registerName")
                return _server
            except Exception:
                _cleanup_ice()

        comm = None
        comm_promoted = False  # Tracks weather temp comm was promoted to cache 
        try:
            comm = build_ice_communicator()
            meta = Murmur.MetaPrx.checkedCast(
                comm.stringToProxy(ICE_ENDPOINT)
            )
            servers = meta.getBootedServers()
            if not servers:
                raise RuntimeError("No running servers found")
            identity = servers[0].ice_getIdentity()
            identity_str = f"{identity.category}/{identity.name}"
            simple_proxy_str = f"{identity_str}:tcp -h {ICE_HOST} -p {ICE_PORT}"
            server = Murmur.ServerPrx.checkedCast(
                comm.stringToProxy(simple_proxy_str)
            )
            if not server:
                raise RuntimeError("ServerPrx cast failed")
            _communicator = comm
            _server = server
            comm_promoted = True  # Tracks that comm was promoted to global cache
            return _server
        except Exception as e:
            print("EXCEPTION in get_server_proxy:", type(e), repr(e))
            raise RuntimeError("Mumble Server unreachable")
        finally:
            # Destroy when comm doesnt exist and was not promoted 
            if comm is not None and not comm_promoted:
                try:
                    comm.destroy()
                except Exception:
                    pass
                
signal.signal(signal.SIGTERM, cleanup_and_exit)
signal.signal(signal.SIGINT, cleanup_and_exit)
atexit.register(_cleanup_ice)