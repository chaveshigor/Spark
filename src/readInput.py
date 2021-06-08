from capacitance import Capacitor
from resistence import Resistor
from indutance import Indutance
from source import Source
import json


def readInputElements(path, dt):

    def readInputFile(path):

        inputFile = open(path, 'r')
        return json.loads(inputFile.read())


    inputElements = readInputFile(path)
    elements = []

    for element in inputElements:

        if inputElements[element]['type'] == 'V':
            if inputElements[element]['typeOf'] == 'CC':
                nodes = inputElements[element]['nodes']
                vm = float(inputElements[element]['params']['vm'])
                Zin = float(inputElements[element]['params']['Zin'])
                src = Source(nodes, 'CC', [vm, Zin], dt)
                elements.append(src)

            elif inputElements[element]['typeOf'] == 'CA':
                nodes = inputElements[element]['nodes']
                vm = float(inputElements[element]['params']['vm'])
                Zin = float(inputElements[element]['params']['Zin'])
                f = float(inputElements[element]['params']['f'])
                phase = float(inputElements[element]['params']['phase'])

                src = Source(nodes, 'CA', [vm, Zin, f, phase], dt)
                elements.append(src)

        elif inputElements[element]['type'] == 'C':
            nodes = inputElements[element]['nodes']
            C = float(inputElements[element]['C'])
            v0 = float(inputElements[element]['v0'])
            i0 = float(inputElements[element]['i0'])

            cap = Capacitor(nodes, C, v0, i0, dt)
            elements.append(cap)

        elif inputElements[element]['type'] == 'L':
            nodes = inputElements[element]['nodes']
            L = float(inputElements[element]['L'])
            v0 = float(inputElements[element]['v0'])
            i0 = float(inputElements[element]['i0'])

            ind = Indutance(nodes, L, v0, i0, dt)
            elements.append(ind)

        elif inputElements[element]['type'] == 'R':
            nodes = inputElements[element]['nodes']
            R = float(inputElements[element]['R'])

            res = Resistor(nodes, R)
            elements.append(res)

    return elements

