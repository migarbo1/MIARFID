from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction, Action
from rasa_sdk.events import SlotSet
import pandas as pd
import numpy as np
import smtplib
import random
import ssl
import os
import re

class ResetSlots(Action):

    def name(self):
        return  "reset"
    
    async def run(self, dispatcher, tracker, domain):
        return [
            SlotSet("year", None),
            SlotSet("selling_price", None),
            SlotSet("km_driven_prev_owner", None),
            SlotSet("fuel", None),
            SlotSet("transmission", None),
            SlotSet("km_driven_per_day", None),
            SlotSet("has_garage", None),
            SlotSet("yearly_income", None),
            SlotSet("constant_payments", None),
            SlotSet("user_email", None),
            SlotSet("selected_car", None)
        ]
    
class ComputeBestFuelType(Action):

    def name(self):
        return "compute_best_fuel_type"
    
    async def run(self, dispatcher, tracker, domain):

        has_garage = tracker.get_slot('has_garage') == 'yes'
        km_driven_per_day = int(tracker.get_slot('km_driven_per_day'))

        if has_garage and float(km_driven_per_day) < 100:
            dispatcher.utter_message(text=f'Since you have a garage and your daily mileage is not really high, you can go for an Electric car.')
            return []
        
        gas_price = 1.6 #€/L
        diese_price = 1.495 #€/L

        gas_avg_consumption = 7.5 #L/100km
        diesel_avg_consumption = 5.5 #L/100km

        database = pd.read_csv(f'{os.getcwd()}/actions/Database.csv')

        diesel_car_avg_price = np.mean(database.loc[database['fuel'] == 'Diesel']['selling_price']) * 0.011
        petrol_car_avg_price = np.mean(database.loc[database['fuel'] == 'Petrol']['selling_price']) * 0.011
        
        diesel_overprice = diesel_car_avg_price - petrol_car_avg_price
        diesel_savings_per_km = (gas_price * gas_avg_consumption - diese_price * diesel_avg_consumption)/100 # €/1km

        years_til_benefit = diesel_overprice/(km_driven_per_day*365*diesel_savings_per_km)

        if years_til_benefit > 10: #petrol
            dispatcher.utter_message(text=f'On average, Diesel cars cost {diesel_overprice:.2f}€ more, although them consume less and this fuel is cheaper. \nGiven the actual fuel price, you will get the return of investment in {years_til_benefit:.0f} years. That\'s more than the recommended value (10). \nSo i suggest you to get a Petrol car.')
            return []
        else: #diesel
            dispatcher.utter_message(text=f'On average, Diesel cars cost {diesel_overprice:.2f}€ more, although them consume less and this fuel is cheaper. \nGiven the actual fuel price, you will get the return of investment in {years_til_benefit:.0f} years. That\'s less than the recommended value (10). \nSo i suggest you to get a Diesel car.')
            return []
        
class SendByEmail(Action):

    def name(self):
        return "send_by_email"
    
    async def run(self, dispatcher, tracker, domain):
        selected_car = tracker.get_slot('selected_car')
        user_email = tracker.get_slot('user_email')

        try:
            server = smtplib.SMTP("mail.gmx.com", 587)
            server.starttls(context=ssl.create_default_context())
            server.login('carbot@gmx.es', 'iamabotXDXD')
            from_email = 'carbot@gmx.es'
            to_emails = [user_email]
            body = selected_car
            headers = f"From: {from_email}\r\n"
            headers += f"To: {', '.join(to_emails)}\r\n"
            headers += f"Subject: Retrieved car!\r\n"
            email_message = headers + "\r\n" + body
            server.sendmail(from_email, to_emails, email_message)

        except Exception as e:
            print(e)

        finally:
            server.quit()
            dispatcher.utter_message(text=f'Email sent to {user_email}. You should receive it in any minute')


        return []
    

class ComputeBestMaxPrice(Action):

    def name(self):
        return "compute_best_max_price"
    
    async def run(self, dispatcher, tracker, domain):
        yearly_income = tracker.get_slot('yearly_income')
        constant_payments = tracker.get_slot('constant_payments')

        monthly_payment = yearly_income/12
        monthly_remains = monthly_payment - constant_payments

        car_monthly_spent = monthly_remains/3

        car_total_value = car_monthly_spent * 12 * 7
        dispatcher.utter_message(text=f'Based on your current financial conditions, you should not spend more than {car_monthly_spent:.2f}€ each month in the car. \nSo to completelly pay it in 7 years, you have a maximum price of {car_total_value:.2f}')

        return []
    
class Query(Action):

    def name(self):
        return "query"
    
    async def run(self, dispatcher, tracker, domain):
        
        database = pd.read_csv(f'{os.getcwd()}/actions/Database.csv')

        if tracker.get_slot('year') and tracker.get_slot('selling_price') and tracker.get_slot('km_driven_prev_owner') and tracker.get_slot('fuel') and tracker.get_slot('transmission'):

            year = float(tracker.get_slot('year'))
            selling_price = float(tracker.get_slot('selling_price'))
            km_driven_prev_owner = float(tracker.get_slot('km_driven_prev_owner'))
            fuel = tracker.get_slot('fuel')
            transmission = tracker.get_slot('transmission')

            query_res = database.loc[database['fuel'] == fuel]
            query_res = query_res.loc[query_res['transmission'] == transmission]
            
            if len(query_res) == 0:# reset parameters and try again
                dispatcher.utter_message(text=f'I don\'t have any car with the given combination of fuel and transmission types, please reset the parameters and try again.')
                return []
            
            query_res = query_res.loc[query_res['km_driven'] <= km_driven_prev_owner]
            if len(query_res) == 0:# reset parameters and try again
                dispatcher.utter_message(text=f'Sadly there\'s no car with less than the specified miles. Please increase the number and try again.')
                return []
            
            query_res = query_res.loc[query_res['year'] >= year]
            if len(query_res) == 0:# reset parameters and try again
                dispatcher.utter_message(text=f'There are no cars fabricated after {year} that meet your conditions, please change them and try again.')
                return []
            
            final_query_res = query_res.loc[query_res['selling_price'] <= selling_price/0.011]
            if len(final_query_res) == 0:# reset parameters and try again
                dispatcher.utter_message(text=f'Before applying the price limit, I had {len(query_res)} cars for you. But none meet your price limitations. If you like increase it and try again.')
                return []

            selected_car = self.to_string(final_query_res.sample())
            tracker.slots['selected_car'] = selected_car

            dispatcher.utter_message(text=f'Here\'s the perfect car that I have for you on my database: \n{selected_car}')
        else:
            dispatcher.utter_message(text=f'TO get a car first you have to specify the required parameters')
        return []
    
    def to_string(self, car):
        car = car.iloc[0]
        return f"It\'s a {car['year']}, {car['name']} with {car['fuel']} fuel, {car['transmission']} transmission that is on sale at {float(car['selling_price'])*0.011:.2f} €."
    

class ValidateInfoFuelTypeForm(FormValidationAction):
    def name(self):
        return "validate_info_fuel_type_form"

    def validate_km_driven_per_day(self, value, dispatcher, tracker, domain):

        if int(value) <= 0:
            dispatcher.utter_message(response="utter_incorrect_km_driven_per_day")
            return {"km_driven_per_day": None}
        else:
            return {"km_driven_per_day": value}
        

class ValidateInfoIncomeForm(FormValidationAction):
    def name(self):
        return "validate_info_income_form"

    def validate_yearly_income(self, value, dispatcher, tracker, domain):

        if int(value) <= 0:
            dispatcher.utter_message(response="utter_positive_amount")
            return {"yearly_income": None}
        else:
            return {"yearly_income": value}
        
    def validate_constant_payments(self, value, dispatcher, tracker, domain):

        if int(value) < 0:
            dispatcher.utter_message(response="utter_positive_amount")
            return {"constant_payments": None}
        else:
            return {"constant_payments": value}

class ValidateInfoCarForm(FormValidationAction):
    def name(self):
        return "validate_info_car_form"

    def validate_year(self, value, dispatcher, tracker, domain):

        if int(value) < 1992 or int(value) > 2020:
            dispatcher.utter_message(response="utter_incorrect_year")
            return {"year": None}
        else:
            return {"year": value}
        
    def validate_selling_price(self, value, dispatcher, tracker, domain):

        if int(value) <= 0:
            dispatcher.utter_message(response="utter_incorrect_selling_price")
            return {"selling_price": None}
        else:
            return {"selling_price": value}
    
    def validate_km_driven_prev_owner(self, value, dispatcher, tracker, domain):

        if int(value) < 0:
            dispatcher.utter_message(response="utter_incorrect_km_driven_prev_owner")
            return {"km_driven_prev_owner": None}
        else:
            return {"km_driven_prev_owner": value}
        
    def validate_fuel(self, value, dispatcher, tracker, domain):

        if value not in ['Electric', 'Petrol', 'Diesel']:
            dispatcher.utter_message(response="utter_incorrect_fuel")
            return {"fuel": None}
        else:
            return {"fuel": value}
        
    def validate_transmission(self, value, dispatcher, tracker, domain):

        if value not in ['Manual', 'Automatic']:
            dispatcher.utter_message(response="utter_transmission")
            return {"transmission": None}
        else:
            return {"transmission": value}
