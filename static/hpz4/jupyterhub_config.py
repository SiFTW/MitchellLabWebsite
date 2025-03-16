from jupyter_client.localinterfaces import public_ips
# Configuration file for Jupyter Hub
c.JupyterHub.cookie_secret = bytes.fromhex('3A0C1158179FCECC560148B19F37D94BB5226852AD37610EAF91B76B06A874C8')
c = get_config()

# spawn with Docker
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'

c.DockerSpawner.start_timeout=600

# Spawn containers from this image
c.DockerSpawner.image = 'simon/jupytersingleuser:latest'
c.DockerSpawner.extra_create_kwargs = {'user': 'jovyan'}
c.DockerSpawner.environment = {
  'GRANT_SUDO': '1',
  'UID': '0', # workaround https://github.com/jupyter/docker-stacks/pull/420
}
# c.JupyterHub.base_url='/jupyterhub'
# JupyterHub requires a single-user instance of the Notebook server, so we
# default to using the `start-singleuser.sh` script included in the
# jupyter/docker-stacks *-notebook images as the Docker run command when
# spawning containers.  Optionally, you can overridethe Docker run command
# using the DOCKER_SPAWN_CMD environment variable.

c.Spawner.cmd=['/usr/local/bin/jupyterhub-singleuser']
c.DockerSpawner.extra_create_kwargs.update({ 'command': "start-singleuser.sh --SingleUserNotebookApp.default_url=/lab" })


#import netifaces
#docker0 = netifaces.ifaddresses('eth0')
#docker0_ipv4 = '139.184.170.218' #docker0[netifaces.AF_INET][0]
#docker0_ipv4 = '139.184.171.6'
#c.JupyterHub.hub_ip = '139.184.171.6' #'0.0.0.0' #docker0_ipv4['addr']
# Connect containers to this Docker network
network_name = 'jupyterhub_network'
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = network_name
# Pass the network name as argument to spawned containers
c.DockerSpawner.extra_host_config = { 'network_mode': network_name }



# Explicitly set notebook directory because we'll be mounting a host volume to
# it.  Most jupyter/docker-stacks *-notebook images run the Notebook server as
# user `jovyan`, and set the notebook directory to `/home/jovyan/work`.
# We follow the same convention.
notebook_dir = '/home/user/jovyan'
# notebook_dir = '/home/jovyan/work'
c.DockerSpawner.notebook_dir = notebook_dir
# Mount the real user's Docker volume on the host to the notebook user's
# notebook directory in the container
c.DockerSpawner.volumes = { 'jupyterhub-user-{username}': notebook_dir,'jupyterhub-shared': {"bind": '/home/user/jovyan/shared', "mode": "rw"}}
# volume_driver is no longer a keyword argument to create_container()
# c.DockerSpawner.extra_create_kwargs.update({ 'volume_driver': 'local' })
# Remove containers once they are stopped
c.DockerSpawner.remove_containers = False
# For debugging arguments passed to spawned containers
c.DockerSpawner.debug = True
c.NotebookApp.allow_origin = '*' #allow all origins
c.NotebookApp.ip = '0.0.0.0' # listen on all IPs 
# The docker instances need access to the Hub, so the default loopback port doesn't work:
from jupyter_client.localinterfaces import public_ips

ip = public_ips()[0]
c.JupyterHub.hub_ip = '0.0.0.0'
#c.JupyterHub.proxy_api_ip = ip
#c.JupyterHub.proxy_api_port=9090
#c.JupyterHub.hub_connect_ip=ip
# IP Configurations
c.JupyterHub.port = 8111
#c.JupyterHub.proxy_api_ip=ip
#c.JupyterHub.port = 8111
c.DockerSpawner.hub_ip_connect = ip
#c.JupyterHub.hub_connect_port = 9091
#c.DockerSpawner.hub_connect_ip = ip
# OAuth with GitLab
import os

c.LocalAuthenticator.create_system_users=True
#c.JupyterHub.authenticator_class = 'oauthenticator.gitlab.GitLabOAuthenticator'

#os.environ['OAUTH_CALLBACK_URL'] = 'http://10.101.14.13:8000/hub/oauth_callback'
#os.environ['GITLAB_CLIENT_ID'] = 'd89d76ef002100f217f4a7c1fc73011ca4d9eee7bb5ff8ce3e9532ba7721e29e'
#os.environ['GITLAB_CLIENT_SECRET'] = '05075caea4f3cb63a0cebc5d65e446df4dfc9598932cf3ddc751deb8eee5baf3'

#c.GitLabOAuthenticator.oauth_callback_url = os.environ['OAUTH_CALLBACK_URL']
#c.GitlabOAuthenticator.client_id = os.environ['GITLAB_CLIENT_ID']
#c.GitlabOAuthenticator.client_secret = os.environ['GITLAB_CLIENT_SECRET']


c.Authenticator.whitelist = whitelist = set()
c.Authenticator.admin_users = admin = set()

here = os.path.dirname(__file__)
with open(os.path.join(os.path.dirname(__file__), 'userlist')) as f:
    for line in f:
        if not line:
            continue
        parts = line.split()
        name = parts[0]
        whitelist.add(name)
        if len(parts) > 1 and parts[1] == 'admin':
            admin.add(name)
