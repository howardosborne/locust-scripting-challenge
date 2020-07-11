import gevent
from locust.env import Environment
from locust.stats import stats_printer
from locust.log import setup_logging
from locust import SequentialTaskSet, task, constant, HttpUser
from flask import request
import random, string, re, json
from lxml import html, etree

class TestTaskSet(SequentialTaskSet):

    @task
    def start(self):
        self.token_re = re.compile('.+<input type="hidden" id="token" name="token" value="(\w+)">.+')
        with self.client.get("/",catch_response=True) as response:
            search_result = self.token_re.search(response.text)
            if search_result:
                self.token = search_result.group(1)
            else:
                response.failure("could not find token")
                self.environment.runner.quit()

    @task
    def verify_correlation(self):
        self.username = ''.join(random.choices(string.ascii_lowercase, k=5))
        with self.client.get(f"/api/verify_correlation?username={self.username}&token={self.token}", name="/api/verify_correlation",catch_response=True) as response:
            json_response = json.loads(response.text)
            self.item_id = json_response["item_id"]
    @task
    def parse_json(self):
        payload = '{"item_id":"' + self.item_id + '"}'
        headers = {"Content-Type": "application/json"}
        with self.client.post("/api/parse_json",payload, headers=headers ,catch_response=True) as response:
            self.encoded_text = response.text

    @task
    def extract_html(self):
        with self.client.get(f"/api/urlencoded/{self.encoded_text}", name="/api/urlencoded" ,catch_response=True) as response:
            #get the smallest item
            tree = html.fromstring(response.text)
            items = tree.xpath("//li/text()")
            self.lowest_item = sorted(items)[0]

    @task
    def custom_cookie(self):
        with self.client.get(f"/api/html_extract/{self.lowest_item}", name="/api/html_extract",catch_response=True) as response:
            cookie_list = response.text.split("=")
            if len(cookie_list) == 2:
                self.custom_cookie = cookie_list[1]
            else:
                response.failure("could not get the cookie")
                self.environment.runner.quit()

    @task
    def custom_header(self):
        cookies = dict(custom_cookie=self.custom_cookie)
        with self.client.get(f"/api/cookie",cookies=cookies,catch_response=True) as response:
            self.custom_header = response.text

    @task
    def final_step(self):
        headers = dict(custom_header=self.custom_header)
        with self.client.get(f"/api/header",headers=headers,catch_response=True) as response:
            if not f"Well done {self.username}" in response.text:
                response.failure(f"fell at final hurdle: {response.text}")
                self.environment.runner.quit()

class TakeTest(HttpUser):
    wait_time = constant(1)
    host = "http://localhost:5000"
    tasks = [TestTaskSet]

#set up logging
setup_logging("INFO", None)


# setup Environment and Runner
env = Environment(user_classes=[TakeTest])

#create a local runner
env.create_local_runner()
env.create_web_ui("127.0.0.1", 8089)

# start a greenlet that periodically outputs the current stats
#gevent.spawn(stats_printer(env.stats))

# start the test
env.runner.start(50, hatch_rate=1)

gevent.spawn_later(120, lambda: env.runner.quit())

# wait for the greenlets
env.runner.greenlet.join()

# stop the web server for good measures
env.web_ui.stop()