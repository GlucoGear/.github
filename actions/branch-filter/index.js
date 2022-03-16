'use strict';

const core = require('@actions/core');

const environment = core.getInput('environment');
let branch = core.getInput('branch');
branch = branch.slice(branch.search(branch.split("/")[2]))

const branchMap = {
    master: "PRD",
    main: "PRD",
    homolog: "HML",
    develop: "HML",
    default: function(){
        branch = branch.split('/')[0]
        if(branchMap[branch]){
            core.setOutput("environment", branchMap[branch]);
            core.setOutput("environmentLowercase", branchMap[branch].toLowerCase());
        }else{
            core.setFailed("Sem branch padrão - (master|main|develop|homolog).* - ou, sem input de environment");
        }        
    }
}

if(branchMap[branch]){
    core.setOutput("environment", branchMap[branch]);
    core.setOutput("environmentLowercase", branchMap[branch].toLowerCase());
}else{
    if(environment){
        core.setOutput("environment", environment.toUpperCase());
        core.setOutput("environmentLowercase", environment.toLowerCase());
    }else{
        branchMap["default"]()
    }
}
