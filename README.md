# Docker Projects Manager
Python CLI app to manage all **Docker Compose** projects on a server.

It requires:
- a normal user used to run the script, added in the `docker` group
- Docker Compose installed as a [CLI plugin](https://docs.docker.com/compose/cli-command/#install-on-linux)

# Download
You don't need to install Python or any dependency. It's available as a standalone Linux executable, available as an artifact from the latest [GitHub Actions execution](https://github.com/simonesestito/server-manager/actions)

# Usage
It can run both in interactive and batch mode.

If an action and all it's parameters are provided from the command itself, and also Git can clone the repo without user interaction, it'll run without propting inputs.
Otherwise, a beautiful menu is displayed to make a selection.

**Note**: the delete command, because of its destructive nature, always prompts for confirmation. You can pipe it with `yes` if you are sure.

```
project-manager <ACTION> <args...>

Actions:
- add [GIT_URL] [PROJECT_NAME]
  Add a new project
- update [PROJECT_NAME]
  Update a project, pulling latest Docker images and files from Git repository
- test [PROJECT_NAME]
  Perform a series of tests on a project (e.g.: it's reachable via the domain name, it's listening, ...)
- delete [PROJECT_NAME]
  Delete a project, its images and, optionally, its volumes
```

## Example usage
<a href="https://asciinema.org/a/476861">
  <img src="https://asciinema.org/a/476861.svg" alt="Asciinema recording" width="700" />
</a>

# Limitations
Since building the full Docker image from sources it's heavy and not ideal on the deployment server, it only copies ```docker-compose.yml``` file from the git repository. Because of that, you need to build your images locally from source (e.g.: on your workstation) and then [pull them to a Registry](https://docs.docker.com/docker-hub/) (like Docker Hub).

# See also
Do you need a script to do an initial server setup? Check out [this server setup script](https://gist.github.com/simonesestito/a15d11ca544e04865118b86834624084)

# License
    Copyright 2022 Simone Sestito
    This file is part of "Docker Projects Manager".

    "Docker Projects Manager" is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    "Docker Projects Manager" is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with "Docker Projects Manager".  If not, see <http://www.gnu.org/licenses/>.


