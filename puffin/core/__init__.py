from . import config
from . import db
from . import mail
from . import queue
from . import security
from . import applications
from . import machine
from . import compose
from . import network
from . import docker
from . import stats
from . import analytics
from . import db_tables


def init():
    config.init()
    db.init()
    queue.init()
    mail.init()
    security.init()
    applications.init()
    machine.init()
    compose.init()
    network.init()
    docker.init()
    stats.init()
    analytics.init()
    db_tables.init()
