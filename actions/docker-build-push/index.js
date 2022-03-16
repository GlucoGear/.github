'use strict';

const core = require('@actions/core');
const aws = require('aws-sdk');
const exec = require('child_process').exec;

const environment = core.getInput('environment').toUpperCase();
const imageTag = process.env.GITHUB_SHA.substring(0, 8)
var registryName = core.getInput('registry').replace("$env", environment).toLowerCase();
const usePrd = core.getInput('usePrd')
if (!usePrd) {
    let envIndex = registryName.lastIndexOf(environment.toLowerCase());
    registryName = registryName.substring(0, envIndex - 1)
}
const image = `${registryName}:${imageTag}`;

async function dockerBuild(){
    console.log(`Running docker build, image: ${image}`);
    return new Promise( (resolve, reject) => {
        exec(`docker build . --file ${process.env.GITHUB_WORKSPACE}/Dockerfile --tag ${image}`, (error, stdout, stderr) => {
        if (error){             
            console.error(`Error build: ${error}`)
        }               
        resolve(stdout);
    });
        
    });

}

async function dockerLogin(){    
    aws.config.update({region: 'us-east-1'})

    let accountId = {"HML":"309688920665", "DEV":"309688920665", "PRD":"527674370273", "ORG":"271959017503"};

    var params = {
        registryIds: [
            accountId[environment]
        ]
      };

    let ecr = new aws.ECR();

    ecr.getAuthorizationToken(params, function(err, data) {
        if (err) { 
            core.setFailed(`get auth token failed: ${err}`); 
            throw err;
        }

        let authToken = Buffer.from(data.authorizationData[0].authorizationToken, 'base64').toString('ascii').replace("AWS:", "");
        let endPoint = data.authorizationData[0].proxyEndpoint.replace("https://", "");

        console.log(`Getting login of ecr: ${endPoint}`);
        exec(`docker login -u AWS -p ${authToken} ${endPoint}`, (error, stdout, stderr) => {
            if (error){ 
                console.error(`Error login: ${error}`)
            }            
            console.log(`Response Login: ${stdout}`)

            let imageECR = `${endPoint}/${registryName}`

            Promise.all([dockerTag(imageECR, imageTag), dockerTag(imageECR, "latest")]).then(values => dockerPush(imageECR));

        });

    });

}

async function dockerTag(imageECR, imageTAG){   

    return new Promise( (resolve) => {

        let imageECRTag = `${imageECR}:${imageTAG}`
        console.log(`docker tag ${image} ${imageECRTag}`);

        exec(`docker tag ${image} ${imageECRTag}`, (error, stdout, stderr) => {

            if (error){             
                console.error(`Error at docker tag: ${error}`);
            }

            resolve(stdout)

        })

    })    

}

async function dockerPush(imageEcr){
    
    console.log(`docker push ${imageEcr}`);
        exec(`docker push ${imageEcr}`, (error, stdout, stderr) => {
            if (error){ 
                console.error(`Error push: ${error}`)
            } 
            
            console.log(`Response push: ${stdout}`)

        });
        exec(`docker push ${imageEcr}:${imageTag}`, (error, stdout, stderr) => {
            if (error){ 
                console.error(`Error push: ${error}`)
            } 
            
            console.log(`Response push: ${stdout}`)

        });

    let imageECRTag = `${imageEcr}:${imageTag}`

    core.setOutput("image", imageECRTag);    

}

try{
    let result = dockerBuild();
    result.then(response => {
        console.log(`Response Build: ${response}`)
        dockerLogin();
    })    

} catch(e){
    console.error(e) 
}