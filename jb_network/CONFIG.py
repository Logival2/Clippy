SERVER_ADDRESS = ('localhost', 1337)
BUFFER_SIZE = 1024

CREATE_LOG = False
LOGS_PATH = "./logs/"

LOG_INDIVIDUAL_CONNECTIONS = True

GREEN = "\033[32;1m"
RED = "\033[31;1m"
CYAN = "\033[36;1m"
YELLOW = "\033[33;1m"#;4m" # underline,
RESET = "\033[0m"

# TCP protocol
SEPARATOR = '\a'
EOM = '\v'

DO_SEARCH = 1
DO_NLP = 2
SEARCH_SUCCESS = 10
SEARCH_FAILED = 11
NLP_SUCCESS = 20
COMM_ERROR = 40
SERVER_ERROR = 50

# Used to check the accepted number of arguments for each command
PARAMS_NBR = {
    DO_SEARCH: range(1, 4),
    DO_NLP: [1],
}
