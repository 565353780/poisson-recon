from bspline_fitting.Module.server import Server


def demo():
    port = 6004

    server = Server(port)

    server.start()
    return True
