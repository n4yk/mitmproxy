from mitmproxy import addons
from mitmproxy import options
from mitmproxy import master
from mitmproxy.addons import dumper, termlog, termstatus, readstdin, keepserving


class ErrorCheck:
    def __init__(self):
        self.has_errored = False

    def log(self, e):
        if e.level == "error":
            self.has_errored = True


class DumpMaster(master.Master):

    def __init__(
        self,
        options: options.Options,
        server,
        with_termlog=True,
        with_dumper=True,
    ) -> None:
        master.Master.__init__(self, options, server)
        self.errorcheck = ErrorCheck()
        if with_termlog:
            self.addons.add(termlog.TermLog(), termstatus.TermStatus())
        self.addons.add(*addons.default_addons())
        if with_dumper:
            self.addons.add(dumper.Dumper())
        self.addons.add(
            readstdin.ReadStdin(),
            keepserving.KeepServing(),
            self.errorcheck
        )
