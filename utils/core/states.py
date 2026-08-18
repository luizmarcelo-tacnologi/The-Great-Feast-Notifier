from dataclasses import dataclass, field

#Child of ProgramStates
@dataclass
class InitializationStates:
    startup_notification: bool = False

#Child of ProgramStates
@dataclass
class ApiStates:
    failed_api_requests: int = 0

#Child of CheckStates
@dataclass
class FeastStates:
    mayor: bool = False
    minister: bool = False
    candidate: bool = False
    harvest_feast: bool = False

    def reset(self):
        self.mayor = False
        self.minister = False
        self.candidate = False
        self.harvest_feast = False

#Child of ProgramStates
@dataclass
class CheckStates:
    feast: FeastStates = field(default_factory=FeastStates)

#The Father
@dataclass
class ProgramStates:
    init: InitializationStates = field(default_factory=InitializationStates)
    api: ApiStates = field(default_factory=ApiStates)
    checks: CheckStates = field(default_factory=CheckStates)

state = ProgramStates()