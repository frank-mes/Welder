from dataclasses import dataclass, asdict

@dataclass
class WelderEntity:
    name: str = ""
    gender: str = ""
    id_card: str = ""
    stamp_code: str = ""
    workshop: str = ""
    team: str = ""
    cert_large: str = ""
    cert_small: str = ""

    def to_dict(self):
        return asdict(self)
