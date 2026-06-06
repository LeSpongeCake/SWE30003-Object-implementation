import hashlib
from abc import ABC, abstractmethod


class Account(ABC):
    _registry: dict[str, type] = {}

    def __init__(self, id: int, name: str, username: str, password: str):
        self.id = id
        self.name = name
        self.username = username
        self.password = password

    def check_password(self, password):
        return (
            hashlib.sha256(password.encode()).hexdigest()
            == self.password
        )

    @classmethod
    def register(cls, role: str):
        def decorator(subclass):
            Account._registry[role] = subclass
            return subclass
        return decorator

    @property
    @abstractmethod
    def role(self) -> str:
        pass

    @property
    def is_persistent(self) -> bool:
        return True

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "password": self.password,
            "role": self.role,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Account":
        subclass = cls._registry.get(data["role"])
        if subclass is None:
            raise ValueError(f"Unknown role: {data['role']}")
        return subclass(int(data["id"]), data["name"], data["username"], data["password"])


@Account.register("customer")
class CustomerAccount(Account):
    @property
    def role(self) -> str:
        return "customer"


@Account.register("admin")
class AdminAccount(Account):
    @property
    def role(self) -> str:
        return "admin"
    

class GuestAccount(Account):
    def __init__(self):
        super().__init__(0, "Guest", "", "")

    @property
    def role(self) -> str:
        return "guest"

    @property
    def is_persistent(self) -> bool:
        return False