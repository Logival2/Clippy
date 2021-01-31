import json

from NetworkManager import NetworkManager
from utils import Response, Logger
from CONFIG import *

class Manager(object):
    def __init__(self):
        self.logger = Logger()
        self.clients = {}
        self.network_manager = NetworkManager(self.clients, self.logger)
        self.logger.log("Init done, server started", GREEN)

    def start(self):
        while 42:
            self.network_manager.do_turn()
            for client_id, client_object in self.clients.items():
                if not client_object.todo:
                    continue
                result = self.handle_msg(client_object.todo)  # Returns a Response object
                client_object.result = result
                client_object.todo = None

    def handle_msg(self, msg):
        try:
            task_code = int(msg[0])
        except ValueError:
            return Response(COMM_ERROR, ["Invalid task code: {}".format(msg[0])])
        if task_code not in PARAMS_NBR:
            return Response(COMM_ERROR, ["Invalid task code: {}".format(msg[0])])
        if len(msg) == 1:
            return Response(COMM_ERROR, ["Invalid message, no parameters"])
        if msg[1] != SEPARATOR:
            return Response(
                COMM_ERROR,
                ["Malformed message, wrong separator: {}".format(msg[1])]
            )
        if msg[-1] != EOM:
            return Response(
                COMM_ERROR,
                ["Malformed message, wrong End Of Message byte: {}".format(msg[-1])]
            )
        params = msg[2:-1].split(SEPARATOR)
        # print(params)
        if len(params) not in PARAMS_NBR[task_code]:
            return Response(
                COMM_ERROR,
                ["Error: invalid number of parameters: {}\n{}".format(len(params), params)]
            )
        if task_code == DO_SEARCH:
            return self.handle_search(params)
        elif task_code == DO_NLP:
            return self.handle_nlp(params)

    def handle_search(self, params):
        result = self.search_engine.search(params[0])
        # print(result[1])
        if result[0]:  # Successful search
            return self.handle_headers_creation(result[1], params)
        else:  # Return string suggestion and words suggestions
            return Response(SEARCH_FAILED, result[1])

    def handle_headers_creation(self, result, params):
        if len(params) > 1:
            try:
                num_results = int(params[1])
            except ValueError:
                return Response(COMM_ERROR, ["Invalid numresult parameter: {}".format(params[1])])
        else:
            num_results = DEFAULT_RESULTS_PER_PAGE
        if len(params) > 2:
            try:
                num_page = int(params[2])
            except ValueError:
                return Response(COMM_ERROR, ["Invalid numpage parameter: {}".format(params[2])])
        else:
            num_page = DEFAULT_PAGE_IDX
        start_result_idx = num_page * (num_results + 1)
        end_result_idx = start_result_idx + num_results
        results_nbr = len(result)
        if end_result_idx > results_nbr:
            end_result_idx = results_nbr
            start_result_idx = end_result_idx - num_results
            if start_result_idx < 0:
                start_result_idx = 0
        page_nbr = results_nbr // num_results
        if results_nbr % num_results != 0:
            page_nbr += 1
        print("start header idx: {}, end header idx: {}".format(start_result_idx, end_result_idx))
        res_headers = {}
        for article_path in result[start_result_idx:end_result_idx]:
            pmcid, data = self.nlp_agent.get_header(article_path)
            res_headers[pmcid] = data
        return Response(SEARCH_SUCCESS, [page_nbr, results_nbr, json.dumps(res_headers)])

    def handle_nlp(self, params):
        html = self.nlp_agent.get_html("{}{}.txt".format(ARTICLES_PATH, params[0]))
        if html:
            return Response(NLP_SUCCESS, [html])
        return Response(SERVER_ERROR, ["Server error, article not found: " + params[0]])


if __name__ == '__main__':
    try:
        manager = Manager()
    except OSError:
        print("{}Init failed, TCP address already in use, change TCP port{}".format(RED, RESET))
    else:
        manager.start()
