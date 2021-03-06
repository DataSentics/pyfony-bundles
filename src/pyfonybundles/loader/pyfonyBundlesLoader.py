from typing import List
from injecta.module import attributeLoader
from pyfonybundles.Bundle import Bundle
from pyfonybundles.loader import entryPointsReader, pyprojectReader

def getEntryPoints():
    entryPoints = entryPointsReader.getByKey('pyfony.bundle')

    for entryPoint in entryPoints:
        _checkName(entryPoint.name, entryPoint.value)

    return entryPoints

def loadBundles() -> List[Bundle]:
    return [entryPoint.load()() for entryPoint in getEntryPoints()]

def loadBundlesWithCurrent() -> List[Bundle]:
    bundles = loadBundles()

    rawConfig = pyprojectReader.read(pyprojectReader.getPath())

    if not _entryPointDefined(rawConfig):
        raise Exception('Missing entry point [tool.poetry.plugins."pyfony.bundle"] in pyproject.toml')

    bundle = _loadDirectly(rawConfig)()
    bundles.append(bundle)

    return bundles

def _entryPointDefined(rawConfig):
    return (
        'tool' in rawConfig
        and 'poetry' in rawConfig['tool']
        and 'plugins' in rawConfig['tool']['poetry']
        and 'pyfony.bundle' in rawConfig['tool']['poetry']['plugins']
    )

def _loadDirectly(rawConfig):
    entryPoints = rawConfig['tool']['poetry']['plugins']['pyfony.bundle']

    for name, val in entryPoints.items():
        _checkName(name, val)

    return attributeLoader.loadFromString(entryPoints['create'])

def _checkName(name: str, value):
    if name != 'create':
        raise Exception(f'Unexpected entry point name "{name}" for {value}')
