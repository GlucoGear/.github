import subprocess
import json
import os
import shutil
import sys


def readPackage(nodeEnv):
    jsonFile = open('./package.json')
    jsonData = json.load(jsonFile)

    nodeBuild = None
    test = True
    mainFile = ""

    if f'build:{nodeEnv}' in jsonData['scripts']:
        print(f"using cmd build:{nodeEnv}")
        nodeBuild = f'build:{nodeEnv}'
    elif 'build' in jsonData['scripts']:
        print(f"using cmd build")
        nodeBuild = 'build'

    if 'main' in jsonData:
        mainFile = jsonData['main']

    if 'test' not in jsonData['scripts']:
        test = False

    return nodeBuild, mainFile, test

def createDist(mainFile):
    print("mkdir dist")
    if not os.path.exists("dist"):
        os.makedirs("dist")

    print("copying files...")
    shutil.copyfile(mainFile, f'./dist/{mainFile}')
    shutil.copyfile("package.json", './dist/package.json')
    shutil.copyfile("package-lock.json", './dist/package-lock.json')

    if sys.argv[1] != "lambda":
        shutil.copytree("./node_modules", './dist/node_modules')

    pass

def useYarn():
    return os.path.exists(".yarnrc")

def main(build, mainFile, runTest):
    try:

        package = "npm"

        if build != None:
            if useYarn():
                print("Installing yarn")
                subprocess.run(["npm", "install", "-g", "yarn"])
                subprocess.run(["npm", "install", "-g", "env-cmd"])
                print("Yarn version")
                subprocess.run(["yarn", "--version"])
                package = "yarn"
                        
            print(f"build NODE_ENV: {nodeEnv}")

            print(f"running {package} install")
            subprocess.run([package, "install"])
            print(f"running {package} {build}")
            subprocess.run([package, "run", build])

            if runTest:
                subprocess.run([package, "test"])

        else:
            print("create dist folder")
            createDist(mainFile)        

    except Exception as e:
        print(f"ERROR: {e}")

    pass

if __name__ == '__main__':
    nodeEnv = os.getenv("NODE_ENV")
    print("Looking for Build script")    
    buildNode, mainFile, runTest = readPackage(nodeEnv)
    print(f"Find build script: {buildNode}")
    main(buildNode, mainFile, runTest)