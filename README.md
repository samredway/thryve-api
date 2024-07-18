# thryve-api

## deploy

To deploy you need to build the image and push it to ECR as such:

    aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin 453530752230.dkr.ecr.eu-west-1.amazonaws.com
    docker build --platform linux/amd64 -t thryve-api .
    docker tag thryve-api:latest 453530752230.dkr.ecr.eu-west-1.amazonaws.com/thryve-api:latest
    docker push 453530752230.dkr.ecr.eu-west-1.amazonaws.com/thryve-api:latest
