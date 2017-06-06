import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "minedash.settings") # noqa
import django
django.setup() # noqa
from django.conf import settings
from django.utils import timezone
from metrics.models import MetricSample

import psutil
from mcstatus import MinecraftServer
from socket import error as socket_error


try:
    server = MinecraftServer(settings.MINECRAFT_SERVER_URL)
    status = server.status()
    players = status.players.online
except (socket_error, AttributeError):
    players = 0

cpu = psutil.cpu_percent(interval=5)
memory = psutil.virtual_memory().percent

disk_root = getattr(settings, 'MINECRAFT_DISK_ROOT', '/')
disk = psutil.disk_usage(disk_root).percent

now = timezone.now()

data = []
data.append({
    "name": 'cpu', "volume": cpu,
    "unit": 'percentage', 'timestamp': str(now)
})

data.append({
    "name": 'memory', "volume": memory,
    "unit": 'percentage', 'timestamp': str(now)
})

data.append({
    "name": 'disk', "volume": disk,
    "unit": 'percentage', 'timestamp': str(now)
})

data.append({
    "name": 'players', "volume": players,
    "unit": 'count', 'timestamp': str(now)
})

for metric in data:
    m = MetricSample(**metric)
    m.save()
