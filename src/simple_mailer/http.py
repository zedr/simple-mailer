from dataclasses import dataclass


@dataclass
class Location:
    hostname: str
    path: str

    @property
    def https_url(self):
        return f"https://{self.hostname}{self.path}"
