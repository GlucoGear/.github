#!/usr/bin/env python3

import os
from jinja2 import Template
from jinja2 import Environment, FileSystemLoader
import json
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('-rd', '--rootDir', help="- root dir.", required=True)
parser.add_argument('-t', '--taskName', help="- task name of deployment.", required=True)
parser.add_argument('-n', '--namespace', help="- namespace to deploy.", required=True, choices=['dev', 'hml', 'prd'])
parser.add_argument('-i', '--image', help="- image of container of pod.", required=True)
parser.add_argument('-r', '--replicas', help="- number of replicas of pod, default: 1.", nargs='?', type=int, default=1, const=1)
parser.add_argument('-v', '--version', help="- version of configmap, default: 1.", nargs='?', type=int, default=1, const=1)
parser.add_argument('-p', '--port', help="- port of pod and target port of service, default: 80.", nargs='?', type=int, default=80, const=80)
parser.add_argument('-cl', '--cpuLimit', help="- limit of cpu of pod, default: 300m.", nargs='?', default='300m', const='0.5')
parser.add_argument('-ml', '--memLimit', help="- limit of memory of pod, default: 256Mi.", nargs='?', default='256Mi', const='256Mi')
parser.add_argument('-cr', '--cpuRequest', help="- request of cpu of pod, default: 0.01.", nargs='?', default='0.01', const='0.01')
parser.add_argument('-mrq', '--memRequest', help="- request of memory of pod, default: 10Mi.", nargs='?', default='10Mi', const='10Mi')
parser.add_argument('-mr', '--minReplicas', help="- min of replicas of hpa, default: 1.", nargs='?', type=int, default=1, const=1)
parser.add_argument('-xr', '--maxReplicas', help="- max of replicas of hpa, default: 5.", nargs='?', type=int, default=2, const=2)
parser.add_argument('-ac', '--avgCpu', help="- average cpu of hpa, default: 70%.", nargs='?', type=int, default=70, const=70)
parser.add_argument('-am', '--avgMem', help="- average memory of hpa, default: 60%.", nargs='?', type=int, default=60, const=60)
parser.add_argument('-c', '--configs', help="- configs of configmap (must be a json), default: '{/}'.", nargs='?', type=json.loads, default=dict(), const=dict())

args = parser.parse_args()

class Manifest:

    def __init__(self, taskName, namespace, configs, replicas, version, port, cpuLimit, memLimit, cpuRequest, memRequest, minReplicas, maxReplicas, avgCpu, avgMem, image):

        self.taskName = taskName
        self.namespace = namespace
        self.configs = configs
        self.replicas = replicas
        self.version = version
        self.port = port
        self.cpuLimit = cpuLimit
        self.memLimit = memLimit
        self.cpuRequest = cpuRequest
        self.memRequest = memRequest
        self.minReplicas = minReplicas
        self.maxReplicas = maxReplicas
        self.avgCpu = avgCpu
        self.avgMem = avgMem        
        self.image = image

    def getTaskName(self):
        return self.taskName

    def getNamespace(self):
        return self.namespace    
    
    def getConfigs(self):
        return self.configs    
    
    def getReplicas(self):
        return self.replicas    
    
    def getVersion(self):
        return self.version    
    
    def getPort(self):
        return self.port    
    
    def getCpuLimit(self):
        return self.cpuLimit    
    
    def getMemLimit(self):
        return self.memLimit    

    def getCpuRequest(self):
        return self.cpuRequest
    
    def getMemRequest(self):
        return self.memRequest
    
    def getMinReplicas(self):
        return self.minReplicas    

    def getMaxReplicas(self):
        return self.maxReplicas    

    def getAvgCpu(self):
        return self.avgCpu    

    def getAvgMem(self):
        return self.avgMem    

    def getPath(self):
        self.path = f'{self.taskName}/{self.namespace}'
        if self.namespace == 'prd':
            self.path = f'{self.taskName}'
        return self.path    
    
    def getImage(self):
        return self.image    

manifest = Manifest(args.taskName, args.namespace, args.configs, args.replicas, args.version, args.port, args.cpuLimit, args.memLimit, args.cpuRequest, args.memRequest, args.minReplicas, args.maxReplicas, args.avgCpu, args.avgMem, args.image)

dirManifest = None

if os.path.isdir(f'{args.rootDir}/kubernetes'):
    dirManifest = f'{args.rootDir}/kubernetes'
elif os.path.isdir(f'{args.rootDir}/k8s'):
    dirManifest = f'{args.rootDir}/k8s'

if dirManifest is None:
    sys.exit("Directory of manifests not found, default directories: ./k8s or ./kubernetes")

allFiles = os.listdir(dirManifest)
yamlFiles = list()

for anyFile in allFiles:
    if anyFile.endswith('.yaml'):
        yamlFiles.append(anyFile)
    elif anyFile.endswith('.yml'):
        yamlFiles.append(anyFile)

if len(yamlFiles) <= 0:
    sys.exit(f"Any yaml/yml file founded inside {dirManifest}")

file_loader = FileSystemLoader(dirManifest)
env = Environment(loader=file_loader)

renderedDir = f'{args.rootDir}/k8sRendered'

if not os.path.exists(renderedDir):
    os.makedirs(renderedDir)

yamlFilesRendered = list()

for yamlFile in yamlFiles:
    template = env.get_template(yamlFile)
    output = template.render(man=manifest)
    yamlFilesRendered.append(f'{renderedDir}/{yamlFile}')

    with open(f'{renderedDir}/{yamlFile}', 'w') as renderedYaml:
        renderedYaml.write(output)

    detail = '-' * 110
    print(f'Yaml Output: {yamlFile} {detail}\n')
    print(f'{output}\n\n')

for yamlRendered in yamlFilesRendered:
    os.system(f'kubectl apply -f {yamlRendered}')