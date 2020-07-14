# Scripting Challenge
A challenge to help learn how to write a performance test script

This project is designed to help learn how to write performance test scripts. The focus in on writing scripts for [locust.io](https://locust.io) but it could be used to learn about scripting with any tool.

It runs on [Flask](https://flask.palletsprojects.com/en/1.1.x/quickstart/), which is the same python-based technology used for the Locust web interface.

## Getting Started
Familiarise yourself with what you are going to script by looking at the instance running on [Heroku](https://locust-scripting-challenge.herokuapp.com/). Please don't run high volume tests against it. It is there for you to work out how to script and run short low-volume tests (no more than 50 users).

If you do want to run a high volume test or just want to run your own instance, start the app locally (gunicorn locust-scripting-challenge:app).


You will be walked through what your script needs to do.

Suggestion: use the network tab of your browser's developer tools or use a protocol analyser like [Fiddler](https://www.telerik.com/fiddler) to understand what your script needs to do.

If you get completely stuck, have a look at the example script in the [examples](./examples) folder.

## Contribute
Contributions and feedback are very welcome. Raise an issue or PR if you have a suggestion or would like to help...