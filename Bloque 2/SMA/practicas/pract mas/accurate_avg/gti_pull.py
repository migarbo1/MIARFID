import datetime
import json
import random
import time
import click
import math
import spade

random.seed(0)
ADD_VALUE_MODE='' #max or avg

class PullAgent(spade.agent.Agent):

    async def setup(self):
        self.value = random.randint(1, 1000)
        self.avg_dict = {self.jid[0]: self.value}

        start_at = datetime.datetime.now() + datetime.timedelta(seconds=1)
        self.add_behaviour(self.PullBehaviour(period=2, start_at=start_at))
        template = spade.template.Template(metadata={"performative": "PULL"})
        self.add_behaviour(self.RecvBehaviour(), template)
        template = spade.template.Template(metadata={"performative": "REPLY"})
        self.add_behaviour(self.ReplyBehaviour(), template)


    def add_value(self, value, sender_avg_dict):
        global ADD_VALUE_MODE
        # seleccion del valor adecuado entre el propio y el nuevo
        if ADD_VALUE_MODE == "max":
            self.value = max(self.value, value)
        if ADD_VALUE_MODE == "avg":
            new_contacts = list(set(sender_avg_dict.keys()).difference(self.avg_dict.keys()))
            for id in new_contacts:
                self.avg_dict[id] = sender_avg_dict[id]
            self.value = round(sum(self.avg_dict.values())/len(self.avg_dict.keys()),2)


    def add_contacts(self, contact_list):
        self.contacts = [c.jid for c in contact_list if c.jid != self.jid]
        self.length = len(self.contacts)

    # comportamiento encargado de enviar el mensaje push
    class PullBehaviour(spade.behaviour.PeriodicBehaviour):
        async def run(self):
            global NUM_NEIGHBOURS
            # el numero de amigos está fijado a 1, se puede modificar
            k=NUM_NEIGHBOURS

            random_contacts = random.sample(self.agent.contacts, k)
            
            # se envia el mensaje con el dato a los k amigos seleccionados
            for jid in random_contacts:
                body = json.dumps({ "timestamp": time.time()})
                msg = spade.message.Message(to=str(jid), body=body, metadata={"performative": "PULL"})
                await self.send(msg)

    # comportamiento encargado de gestionar la llegada de un mensaje push
    class RecvBehaviour(spade.behaviour.CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=2)
            if msg:
                body = json.dumps({"value": self.agent.value, "avg_dict":self.agent.avg_dict, "timestamp": time.time()})
                msg = spade.message.Message(to=str(msg.sender), body=body, metadata={"performative": "REPLY"})
                await self.send(msg)
            
    class ReplyBehaviour(spade.behaviour.CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=2)
            if msg:
                body = json.loads(msg.body)
                # llamamos al método encargado de decidir si actualiza el dato o no
                self.agent.add_value(body["value"], body["avg_dict"])


@click.command()
@click.option('--count', default=10, help='Number of agents.')
@click.option('--mode', default='max', help='mode to update value, avg or max')
@click.option('--k', default=1, help='number of neighbous for each agent')
def main(count, mode, k):
    global ADD_VALUE_MODE, NUM_NEIGHBOURS

    NUM_NEIGHBOURS = k
    ADD_VALUE_MODE = mode
    agents = []
    for x in range(1, count + 1):
        # nos guardamos la lista de agentes para poder visualizar el estado del proceso gossiping
        # el servidor está fijado a gtirouter.dsic.upv.es, si se tiene un serviodor XMPP en local, se puede sustituir por localhost
        agents.append(PullAgent("migarbo1_push_agent_1626_{}@gtirouter.dsic.upv.es".format(x), "test"))

    # este tiempo trata de esperar que todos los agentes estan registrados, depende de la cantidad de agentes que se lancen
    time.sleep(3)

    # se le pasa a cada agente la lista de contactos
    for ag in agents:
        ag.add_contacts(agents)
        ag.value = 0

    # se lanzan todos los agentes
    for ag in agents:
        ag.start()

    # este tiempo trata de esperar que todos los agentes estan ready, depende de la cantidad de agentes que se lancen
    time.sleep(4)
    
    # este bucle imprime los valores que almacena cada agente y termina cuando todos tienen el mismo valor (consenso)
    while True:
        try:
            time.sleep(1)
            status = [ag.value for ag in agents]
            print("STATUS: {}".format(status))
            if len(set(status)) <= 1:
                print("Gossip done.")
                break
        except KeyboardInterrupt:
            break

    # se para a todos los agentes
    for ag in agents:
        ag.stop()


if __name__ == '__main__':
    main()
