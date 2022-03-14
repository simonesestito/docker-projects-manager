from dataclasses import dataclass
import os

from config import DEFAULT_TOP_DOMAIN_NAME, METADATA_JSON_FILE, NGINX_CONFS_DIR, NGINX_ENABLED_DIR, WORK_DIR


@dataclass
class Project:
    name: str
    git_url: str
    port: int
    last_commit: str

    @property
    def dir_path(self) -> str:
        return os.path.join(WORK_DIR, self.name)

    @property
    def spec_file_path(self) -> str:
        return os.path.join(self.dir_path, METADATA_JSON_FILE)

    @property
    def domain_name(self) -> str:
        return self.name if '.' in self.name else f'{self.name}.{DEFAULT_TOP_DOMAIN_NAME}'

    @property
    def nginx_file(self) -> str:
        return os.path.join(NGINX_CONFS_DIR, f'{self.name}.conf')

    @property
    def nginx_link(self) -> str:
        return os.path.join(NGINX_ENABLED_DIR, f'{self.name}.conf')

    @property
    def env_file(self) -> str:
        return os.path.join(self.dir_path, '.env')