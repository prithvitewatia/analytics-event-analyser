import asyncio
import logging

from mitmproxy import options, http
from mitmproxy.tools.dump import DumpMaster
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

logging.basicConfig(filename='app.log', level=logging.DEBUG, filemode='w+')


class Counter:
    def __init__(self):
        self.num = 0

    def request(self, flow: http.HTTPFlow) -> None:
        self.num = self.num + 1
        logging.info("We've seen %d flows" % self.num)
        logging.info(flow.request)
        if log_request:
            logging.info(self.__build_curl_from_request(flow))

    def response(self, flow: http.HTTPFlow) -> None:
        if log_response:
            logging.info(self.__build_response(flow))

    def __build_curl_from_request(self, flow: http.HTTPFlow) -> str:
        request = flow.request
        base_request = f"curl -X {request.method} '{request.url}'"
        request_headers = '\n'.join([f" -H {key} : {value}" for key, value in request.headers.items()])
        request_data = ''
        if request.content:
            request_data = f" -- data '{request.content}'"

        return '\n'.join([base_request, request_headers, request_data])

    def __build_response(self, flow: http.HTTPFlow) -> str:
        response = flow.response
        response_status = f"Response status : {response.status_code}"
        response_headers = '\n'.join([key + ':' + value for key, value in response.headers.items()])
        try:
            response_data = f"{response.content.decode('utf-8')}"
        except UnicodeDecodeError:
            response_data = 'Response data could not be decoded into utf-8'
        return '\n'.join([response_status, response_headers, response_data])


async def start_proxy_server(host: str, port: int) -> None:
    opts = options.Options(listen_host=host, listen_port=port)
    server = DumpMaster(
        opts,
        with_termlog=True,
        with_dumper=False
    )
    server.addons.add(Counter())
    await server.run()


if __name__ == '__main__':
    logging.info('Started application')

    host = 'localhost'
    port = 8080
    proxy = f'{host}:{port}'
    log_request = False
    log_response = False

    chrome_options = webdriver.ChromeOptions()
    # For now, we will try to use mitmproxy certificate.
    # This is being done by
    # sudo security add-trusted-cert -d -p ssl -p basic -k /Library/Keychains/System.keychain \
    # ~/.mitmproxy/mitmproxy-ca-cert.pem
    # However, we can later use a custom CA certificate
    chrome_options.add_argument(f'--proxy-server={proxy}')
    # Options are configured to use proxy server and service is used to get manage chrome driver
    browser = webdriver.Chrome(options=chrome_options, service=ChromeService(ChromeDriverManager().install()))
    loop = asyncio.get_event_loop()
    proxy_task = loop.create_task(start_proxy_server(host=host, port=port))

    try:
        loop.run_until_complete(proxy_task)
        browser.get('https://www.google.com')
        print(browser.title)
    except KeyboardInterrupt:
        logging.info('Keyboard interrupt happened')
    finally:
        browser.quit()
        if loop.is_running():
            loop.close()
        logging.info('Shutting down application')
