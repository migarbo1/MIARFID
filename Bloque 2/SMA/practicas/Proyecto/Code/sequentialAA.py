import datetime
import json
import random
import time
import click
import numpy as np
import spade

random.seed(0)

talla = 0
auction_items = []
EPSILON = 0

iters = 0
req_count = 0
ood_req_count = 0

comprobation_in_progress = False

class AuctionerAgent(spade.agent.Agent):

    async def setup(self):

        self.actual_items_prize = auction_items

        start_at = datetime.datetime.now() + datetime.timedelta(seconds=1)
        self.add_behaviour(self.StatusBroadcastBehaviout(period=2, start_at=start_at))
        template = spade.template.Template(metadata={"performative": "BetForObject"})
        self.add_behaviour(self.CheckOfferBehaviour(), template)
        pass

    def add_contacts(self, contact_list):
        self.contacts = [c.jid for c in contact_list if c.jid != self.jid]
        self.length = len(self.contacts)

    def random_assign(self, agents):
        copy = agents
        random.shuffle(copy)

        self.actual_item_assignation = []

        for agent in copy:
            self.actual_item_assignation.append(str(agent.jid))
            agent.set_item(len(self.actual_item_assignation)-1, auction_items[len(self.actual_item_assignation)-1])

        print('actual item assignation: ')
        print(self.actual_item_assignation)

    class StatusBroadcastBehaviout(spade.behaviour.PeriodicBehaviour):
        async def run(self): 
            global iters
            iters += 1
            for jid in self.agent.contacts:
                print('sending actual information:')
                print(self.agent.actual_item_assignation)
                print(self.agent.actual_items_prize)
                body = json.dumps({ "item_assignation": self.agent.actual_item_assignation, "item_price": self.agent.actual_items_prize})
                msg = spade.message.Message(to=str(jid), body=body, metadata={"performative": "Status"})
                await self.send(msg)    

    class CheckOfferBehaviour(spade.behaviour.CyclicBehaviour):
        async def run(self):
            global comprobation_in_progress, req_count, ood_req_count
            msg = await self.receive(timeout=1)
            if msg and not comprobation_in_progress:
                req_count += 1
                comprobation_in_progress = True

                content = json.loads(msg.body)
                betted_item = content['desired_item']
                current_owner = self.agent.actual_item_assignation[betted_item]
                print('request from agent {} to get item {} from {}'.format(str(msg.sender), betted_item, current_owner))
                #if information still valid (no change in ownership since agent sent offer)
                    
                if current_owner == content['owner'] and self.agent.actual_item_assignation[content['buyer_item']] == str(msg.sender):
                    #change price
                    payed_price = self.agent.actual_items_prize[betted_item] 
                    self.agent.actual_items_prize[betted_item] = content['price']
                    #change object assigned agent
                    self.agent.actual_item_assignation[content['buyer_item']] = content['owner']
                    self.agent.actual_item_assignation[betted_item] = str(msg.sender)

                    #notify bet's agent
                    body = json.dumps({"item": betted_item, "value": payed_price, "happy": True})
                    msg = spade.message.Message(to=str(msg.sender), body=body, metadata={"performative": "ObjectAssigned"})
                    await self.send(msg)

                    #notify affected agent
                    body = json.dumps({"item": content['buyer_item'], "value": self.agent.actual_items_prize[content['buyer_item']], 'happy': False})
                    msg = spade.message.Message(to=str(content['owner']), body=body, metadata={"performative": "ObjectAssigned"})
                    await self.send(msg)

                    print('actual item assignation: ')
                    print(self.agent.actual_item_assignation)
                else:
                    ood_req_count += 1
                    print('bet rejected: out of date.')
                comprobation_in_progress = False

class ClientAgent(spade.agent.Agent):

    async def setup(self):
        self.happy = False
        self.net_value = 0 
        self.profit = -1
        self.item = -1

        self.set_object_preference()
        
        template = spade.template.Template(metadata={"performative": "Status"})
        self.add_behaviour(self.BetForObjectBehaviour(), template)
        template = spade.template.Template(metadata={"performative": "ObjectAssigned"})
        self.add_behaviour(self.AcquireObjectBehaviour(), template)

    def add_contact(self, contact):
        self.contact = contact.jid

    def set_object_preference(self):
        self.preferences = [random.randint(65, 99) for _ in range(len(auction_items))]

        print('object preference for agent: ' + str(self.jid))
        print(self.preferences)

    def set_item(self, item, price):
        self.item = item
        self.profit = self.preferences[item]
        self.net_value = self.preferences[item] - price
        print('agent {} has item: {} with profit {}'.format(str(self.jid), item, self.net_value))

    def check_auction(self, actual_item_price):

        np_pref = np.array(self.preferences)
        np_item_price = np.array(actual_item_price)

        net_values = np.subtract(np_pref, np_item_price) - EPSILON
        best_item = np.argmax(net_values)

        if np.max(net_values) > self.net_value:
            copy = list(net_values[0:best_item]) + list(net_values[best_item+1:]) if best_item < len(net_values) else net_values[0:best_item]
            sec_best = np.argmax(copy)
            return best_item, sec_best
        else:
            return None, None

    class BetForObjectBehaviour(spade.behaviour.CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=1)
            if msg:
                content = json.loads(msg.body)
                best_item, sec_best_item = self.agent.check_auction(list(content['item_price']))

                #item, profit, value = self.agent.get_better_item(dict(content['item_assignation']), dict(content['item_price']))
                if best_item == None:
                    self.agent.happy = True
                else:
                    print('agent {} has found better item: {}'.format(str(self.agent.jid), best_item))

                    # update item price
                    best_net_value = self.agent.preferences[best_item] - list(content['item_price'])[best_item]
                    sec_best_net_value = self.agent.preferences[sec_best_item] - list(content['item_price'])[sec_best_item]
                    gamma = round(best_net_value - sec_best_net_value + EPSILON, 2)
                    item_new_price = list(content['item_price'])[best_item] + gamma

                    body = json.dumps({"buyer_item": self.agent.item, "desired_item": int(best_item), "owner": list(content['item_assignation'])[best_item], "price": item_new_price})
                    msg = spade.message.Message(to=str(msg.sender), body=body, metadata={"performative": "BetForObject"})
                    await self.send(msg)
    
    class AcquireObjectBehaviour(spade.behaviour.CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=1)
            if msg:
                content = json.loads(msg.body)
                self.agent.set_item(content['item'], content['value'])
                self.agent.happy = content['happy']
                print('Object assignation received by agent {}. New object {}. new profit: {}'.format(str(self.agent.jid), self.agent.item, self.agent.net_value))


@click.command()
@click.option('--count', default=5, help='Number of agents.')
def main(count):

    global talla, auction_items, EPSILON, iters, req_count, ood_req_count

    talla = count
    auction_items = [random.randint(10,30) for _ in range(talla)]
    EPSILON = round(1/len(list(auction_items))*0.95, 2)

    print('auction items:')
    print(auction_items)

    auctioner = AuctionerAgent("migarbo1_push_agent_1626_{}@gtirouter.dsic.upv.es".format(1), "test")
    agents = []
    for x in range(2, count + 2):
        agents.append(ClientAgent("migarbo1_push_agent_1626_{}@gtirouter.dsic.upv.es".format(x), "test"))

    # este tiempo trata de esperar que todos los agentes estan registrados, depende de la cantidad de agentes que se lancen
    time.sleep(15)

    # se le pasa a cada agente la lista de contactos
    for ag in agents:
        ag.add_contact(auctioner)
    auctioner.add_contacts(agents)

    # se lanzan todos los agentes
    for ag in agents:
        ag.start()

    # este tiempo trata de esperar que todos los agentes estan ready, depende de la cantidad de agentes que se lancen
    time.sleep(20)

    # assign object random to the clients
    auctioner.random_assign(agents)
    
    auctioner.start()

    profit_ev = []

    # este bucle imprime los valores que almacena cada agente y termina cuando todos tienen el mismo valor (consenso)
    while True:
        try:
            time.sleep(1)
            status = [ag.happy for ag in agents]
            total_profit = sum([ag.profit for ag in agents])
            profit_ev.append(total_profit)
            print("Actual Profit: {}".format(total_profit))
            if sum(status) == len(agents):
                for ag in agents:
                    print('agent {} has item: {} with profit {}'.format(str(ag.jid), ag.item, ag.net_value))
                print("All Happy.")
                break
        except KeyboardInterrupt:
            break

    # se para a todos los agentes
    for ag in agents:
        ag.stop()

    results = {
        'n_iter' : iters,
        'n_req' : req_count,
        'n_req_ood' : ood_req_count,
        'profit evo' : profit_ev
    }

    a = json.dumps(results)

    # open file for writing, "w" 
    f = open("3_res{}.json".format(talla),"w")

    # write json object to file
    f.write(a)

    # close file
    f.close()

if __name__ == '__main__':
    main()
