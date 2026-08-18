from dataclasses import dataclass, field

#The names here are pretty self explanatory

#Child of ProgramStates
@dataclass
class InitializationStates:
    startup_notification: bool = False

#Child of ProgramStates
@dataclass
class ApiStates:
    failed_requests: int = 0
    connection: bool = None

#Child of CheckStates
@dataclass
class FeastStates:
    mayor: bool = False
    minister: bool = False
    candidate: bool = False
    harvest_feast: bool = False

    #A small function to reset it's values
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

#The one that takes care of everything
state = ProgramStates()