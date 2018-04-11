from logging import getLogger, StreamHandler
from structlog import configure, stdlib, processors


log = getLogger("tornado")
log.addHandler(StreamHandler())

processors = [stdlib.filter_by_level,
              stdlib.add_log_level,
              stdlib.PositionalArgumentsFormatter(),
              processors.StackInfoRenderer(),
              processors.format_exc_info,
              processors.UnicodeDecoder()]

configure(context_class=dict, logger_factory=stdlib.LoggerFactory(),
          wrapper_class=stdlib.BoundLogger, cache_logger_on_first_use=True)
