const core = require('@actions/core');

const path = core.getInput('path');


async function getKey(path) {
  try {
    
    let arrayPath = path.split("/")
    let key = ""

    for (let index = 2; index < arrayPath.length - 1; index++){
      key += `${arrayPath[index]}/`
    }

    key += 'terraform.tfstate'

    return key

  }catch (err){     
     core.setFailed(err);
  };
};

getKey(path)
  .then(
    key => setOutput(key)
  )

  async function setOutput(key) {
    
    core.setOutput("key", key);
    console.log(`output key: ${key}`)

  }