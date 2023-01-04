import socket
import pickle
import slowAlg as GA
generation = None
population_size = 10

class Slave():
    def __init__(self):
        self.name = f'Slave P : %10'

    def ListenMessage(self,tcpServer):
        global generation
        while True:
            data = tcpServer.recv(100000)
            if data is None : continue
            convertedData = pickle.loads(data)
            #print(f"\nreceived data: {convertedData}")
            generation.population = convertedData
            evolved = generation.evolve(10)
            self.SendMessage(tcpServer,evolved)

    def SendMessage(self,tcpServer,dataToSend = None):
        if dataToSend is None : return
        convertedData = pickle.dumps(dataToSend)
        tcpServer.send(convertedData)

    def start(self):
        host = 'localhost'
        port = 6001

        tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpServer.connect((host, port))
        self.ListenMessage(tcpServer)

if __name__ == '__main__':
    generation = GA.evolution(population_size)
    c1 = Slave()
    c1.start()
