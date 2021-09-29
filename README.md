![deployment](https://github.com/xncbf/resize-instagram/workflows/deployment%20to%20master/badge.svg)

# resize-instagram

resize for instagram photo without cropping online

[![resize instagram](https://github.com/xncbf/resize-instagram/blob/master/static/resize-instagram.png)](https://resiz.io/)

# Usage:sunglasses:

 1. Upload images
 2. Select option
 3. Click download
 4. Enjoy!:clap::clap::clap:


# Output

>  It is expressed on a gray background to help understanding, but in fact it is expressed in white.

| original |      1:1      |  4:5  |  5:4  |
|----------|:-------------:|------:|------:|
| ![origin](https://github.com/xncbf/resize-instagram/blob/master/static/origin.png) |  ![origin](https://github.com/xncbf/resize-instagram/blob/master/static/1x1.png) | ![origin](https://github.com/xncbf/resize-instagram/blob/master/static/4x5.png) | ![origin](https://github.com/xncbf/resize-instagram/blob/master/static/5x4.png) |


# deployment

docker-compose build prod
docker push {ecr}:latest
update digest on `serverless.yaml`
sls deploy

# Contribute

Please submit a PR for better functionality
