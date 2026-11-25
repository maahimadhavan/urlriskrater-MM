from dataclasses import dataclass, field


@dataclass(frozen=True)
class Finding:
    check: str  #name of the check that fired
    points: int #how much risk it adds
    reason: str #human-readable explanation


@dataclass
class ParsedURL:
    raw: str
    scheme: str
    host: str           #full hostname, lowercase
    subdomain: str      #e.g. "login.verify"
    domain: str         #e.g. "paypal"
    suffix: str         #e.g. "come" or "co.uk"
    path: str 
    query: str
    has_userinfo: bool  # True if the URL contains user@ before the host

    @property
    def registered(self) -> str:
        #the registered domain, e.g. "paypall.com"
        return f"{self.domain}.{self.suffix}" if self.suffix else self.domain
    

@dataclass
class Result:
    url: str
    score: int
    level: str
    findings: list = field(default_factory=list)