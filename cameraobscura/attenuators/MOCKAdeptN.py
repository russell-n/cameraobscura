class MockAdeptN(object):
    def __init__(self):
        print "creating MOCK AdeptN"

    def setAttenuation(self, what, AP="not necessary"):
        return "OK! Attenuation set to " + str(what)

    def getAttenuation(self, AP="not necessary"):
        return 0

    def getAttenMax(self, AP="not necessary"):
        return 20
