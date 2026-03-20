from dataclasses import dataclass, asdict

@dataclass
class WelderEntity:
    """焊工实体类：严格对应数据库字段"""
    id: str = ""
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
