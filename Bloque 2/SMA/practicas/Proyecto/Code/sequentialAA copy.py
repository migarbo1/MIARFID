import datetime
import json
import random
import time
import click
import math
import spade

random.seed(0)

auction_items= {
    "A": random.randint(10, 30),
    "B": random.randint(10, 30),
    "C": random.randint(10, 30),
    "D": random.randint(10, 30),
    "E": random.randint(10, 30),
}

EPSILON = round(1/len(list(auction_items.keys()))*0.75, 2)

class AuctionerAgent(spade.agent.Agent):

    async def setup(self):

        self.actual_items_prize = auction_items

        start_at = datetime.datetime.now() + datetime.timedelta(seconds=1)
        self.add_behaviour(self.StatusBroadcastBehaviout(period=1, start_at=start_at))
        template = spade.template.Template(metadata={"performative": "BetForObject"})
        self.add_behaviour(self.CheckOfferBehaviour(), template)
        pass

    def add_contacts(self, contact_list):
        self.contacts = [c.jid for c in contact_list if c.jid != self.jid]
        self.length = len(self.contacts)

    def random_assign(self, agents):
        assigned_items = []
        self.actual_item_assignation = {} 

        for agent in agents:
            selected_item = random.sample(list(set(auction_items.keys()) - set(assigned_items)), 1)[0]
            self.actual_item_assignation[selected_item] = str(agent.jid)
            agent.set_item(selected_item, auction_items[selected_item])
            assigned_items.append(selected_item)
        print('actual item assignation: ')
        print(self.actual_item_assignation)

    class StatusBroadcastBehaviout(spade.behaviour.PeriodicBehaviour):
        async def run(self): 
            for jid in self.agent.contacts:
                print('sending actual information:')
                print(self.agent.actual_item_assignation)
                print(self.agent.actual_items_prize)
                body = json.dumps({ "item_assignation": self.agent.actual_item_assignation, "item_price": self.agent.actual_items_prize})
                msg = spade.message.Message(to=str(jid), body=body, metadata={"performative": "Status"})
                await self.send(msg)    

    class CheckOfferBehaviour(spade.behaviour.CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=2)
            if msg:
                content = json.loads(msg.body)
                betted_item = content['desired_item']
                current_owner = self.agent.actual_item_assignation[betted_item]
                print('request from agent {} to get item {} from {}'.format(str(msg.sender), betted_item, current_owner))
                #if information still valid (no change in ownership since agent sent offer)
                if current_owner == content['owner']:
                    #change price
                    self.agent.actual_items_prize[betted_item] = content['price']
                    #change object assigned agent
                    self.agent.actual_item_assignation[content['my_item']] = content['owner']
                    self.agent.actual_item_assignation[betted_item] = str(msg.sender)

                    #notify bet's agent
                    body = json.dumps({"item": betted_item, "value": content['price']})
                    msg = spade.message.Message(to=str(msg.sender), body=body, metadata={"performative": "ObjectAssigned"})
                    await self.send(msg)

                    #notify affected agent
                    body = json.dumps({"item": content['my_item'], "value": self.agent.actual_items_prize[content['my_item']]})
                    msg = spade.message.Message(to=str(content['owner']), body=body, metadata={"performative": "ObjectAssigned"})
                    await self.send(msg)
                else:
                    print('bet rejected: out of date.')

class ClientAgent(spade.agent.Agent):

    async def setup(self):
        self.happy = False
        self.profit = 0 
        self.item = ""

        self.set_object_preference()
        
        template = spade.template.Template(metadata={"performative": "Status"})
        self.add_behaviour(self.BetForObjectBehaviour(), template)
        template = spade.template.Template(metadata={"performative": "ObjectAssigned"})
        self.add_behaviour(self.AcquireObjectBehaviour(), template)

    def add_contact(self, contact):
        self.contact = contact.jid

    def set_object_preference(self):
        self.preferences = {}
        for key in auction_items.keys():
            self.preferences[key] = random.randint(1,100)
        print('object preference for agent: ' + str(self.jid))
        print(self.preferences)

    def set_item(self, item, price):
        self.item = item
        self.profit = self.preferences[item] - price
        print('agent {} has item: {} with profit {}'.format(str(self.jid), item, self.profit))

    def get_better_item(self, actual_item_assignation, actual_item_price, best_item = ""): # best item included to retrieve second best item
        for key in actual_item_assignation.keys():
            if key != self.item and key != best_item:
                item_profit = self.preferences[key]
                item_value = actual_item_price[key]
                if item_profit - item_value > self.profit:
                    return key, item_profit, item_value
        return None, None, None

    class BetForObjectBehaviour(spade.behaviour.CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=2)
            if msg:
                content = json.loads(msg.body)
                item, profit, value = self.agent.get_better_item(dict(content['item_assignation']), dict(content['item_price']))
                if item == None:
                    self.agent.happy = True
                else:
                    print('agent {} has found better item: {}'.format(str(self.agent.jid), item))
                    sec_item, sec_profit, sec_value = self.agent.get_better_item(dict(content['item_assignation']), dict(content['item_price']), best_item = item)
                    if sec_item == None: # seccond best is actual
                        sec_item = self.agent.item
                        sec_profit = self.agent.preferences[sec_item]
                        sec_value = dict(content['item_price'])[sec_item]
                    # update item price
                    gamma = round((profit - value) - (sec_profit - sec_value) + EPSILON, 2)
                    item_new_price = value + gamma

                    body = json.dumps({"my_item": self.agent.item, "desired_item": item, "owner": dict(content['item_assignation'])[item], "price": item_new_price})
                    msg = spade.message.Message(to=str(msg.sender), body=body, metadata={"performative": "BetForObject"})
                    await self.send(msg)
    
    class AcquireObjectBehaviour(spade.behaviour.CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=2)
            if msg:
                content = json.loads(msg.body)
                self.agent.item = content['item']
                self.agent.profit = self.agent.preferences[self.agent.item] - content['value']
                print('Object assignation received by agent {}. New object {}. new profit: {}'.format(str(self.agent.jid), self.agent.item, self.agent.profit))


@click.command()
@click.option('--count', default=5, help='Number of agents.')
def main(count):

    print('auction items:')
    print(auction_items)

    auctioner = AuctionerAgent("migarbo1_push_agent_1626_{}@gtirouter.dsic.upv.es".format(1), "test")
    agents = []
    for x in range(2, count + 2):
        agents.append(ClientAgent("migarbo1_push_agent_1626_{}@gtirouter.dsic.upv.es".format(x), "test"))

    # este tiempo trata de esperar que todos los agentes estan registrados, depende de la cantidad de agentes que se lancen
    time.sleep(1)

    # se le pasa a cada agente la lista de contactos
    for ag in agents:
        ag.add_contact(auctioner)
    auctioner.add_contacts(agents)

    # se lanzan todos los agentes
    for ag in agents:
        ag.start()

    # este tiempo trata de esperar que todos los agentes estan ready, depende de la cantidad de agentes que se lancen
    time.sleep(3)

    # assign object random to the clients
    auctioner.random_assign(agents)
    
    auctioner.start()

    # este bucle imprime los valores que almacena cada agente y termina cuando todos tienen el mismo valor (consenso)
    while True:
        try:
            time.sleep(1)
            status = [ag.happy for ag in agents]
            total_profit = sum([ag.profit for ag in agents])
            print("Actual Profit: {}".format(total_profit))
            if sum(status) == len(agents):
                print("All Happy.")
                break
        except KeyboardInterrupt:
            break

    # se para a todos los agentes
    for ag in agents:
        ag.stop()


if __name__ == '__main__':
    main()
