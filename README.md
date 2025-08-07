# thryve-api

Thryve Api is a backend, data only application that serves personal financial data from plaid in a format that can be consumed by a seperate client applicaiton.

I was playing with this idea of creating a personal finances app for which I did a small MVP of which this is part and some user testing / marketing.

Eventually I abonded the idea and have moved this to my public repo as a simple example of some backend Python code I have written.

Since I have written this I have gained some extra years working with fast api daily for various microservices and have changed my approach a littel in some cases. Overall however I do think this is an example of fairly well structured statically typed Python - which is how I like to write it.

You will note that as a quick MVP / POC this probably has a few TODOs scattered may have less than ideal test coverage and has almost no IAC. In short this is not a production app and was never meant to be. Just a fun side project!

## Run the tests

You can tinker with the code by getting the DB running:

    docker compose up

Then:

    pytest .

## Run it locally

To get the api up get the database running as shown above then do:

    fastapi run
