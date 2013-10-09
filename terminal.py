import datetime
import unittest
# uncomment this for dynamic middle of the month
# from calendar import monthrange

card_types = ['Monthly','Value','TransitEmployee']

swipe_cost = 5.00
weekend_modifier = 0.75

# ------------- date handling
today = datetime.date.today()
## in the event they decide to change it from after the 15th, to the dynamic middle of the month
#  --get the number of days in current month
# range = monthrange(today.year,today.month)
#  --find out if pro-rated day of the month
# if range/2 > today.day:
#     pro_rated = False
# else:
#     pro_rated = True

today = datetime.date.today()

def determine_monthly_pro_rate(date=None):
    if date.day > 15:
        pro_rated = 0.50
    else:
        pro_rated = 1.00
    return pro_rated

user_archetype_data = {
        1: {
            'type': 'student',
            'fee_modifier': 0.50,
        },
        2: {
            'type': 'elderly',
            'fee_modifier': 0.50,
        },
        3: {
            'type': 'transit_worker',
            'fee_modifier': 0.00,
        },
        4: {
            'type': 'adult',
            'fee_modifier': 1.00,
        }
    }

class Person():
    def __init__(self,type):
        self.user_type = user_archetype_data[type]
    
    def buy_card(self,card_type,value=None,date=None):
        monthly_cost = 50
        pro_rate_modifier = 0.50
        if card_type == 'TransitEmployee':
            cost = 0
        elif card_type == 'Monthly':
            if self.user_type['type'] == 'adult':
                if date:
                    the_date = date
                else:
                    the_date = today
                pro_rate = determine_monthly_pro_rate(the_date)
                cost = monthly_cost*pro_rate_modifier
            else:
                cost = monthly_cost*self.user_type['fee_modifier']
        elif card_type == 'Value':
            if value:
                cost = value
            else:
                cost = None
                print 'please enter value'
        self.card_type = card_type
        self.type = self.user_type['type']
        self.card_value = value
        self.cost = cost
    
    def swipe_card(self,date=None):
        if self.card_type:
            print "Before Value - {}".format(self.card_value)
            if self.card_type == 'Monthly':
                print 'Card swiped. Please board now'
            elif self.card_type == 'Value':
                if date:
                    the_date = date
                else:
                    the_date = today
                # checck if the date falls on a weekend. 0-4 is Mon-Fri, 5/6: Sat/Sun
                if the_date.weekday() < 5:
                    if self.type == 'elderly' or self.type == 'student':
                        self.card_value = self.card_value-(swipe_cost*self.user_type['fee_modifier'])
                    else:
                        self.card_value = self.card_value-swipe_cost
                else:
                    self.card_value = self.card_value-(swipe_cost*weekend_modifier)
            elif self.card_type == 'TransitEmployee':
                print 'Welcome, transit employee. Enjoy your free ride.'
            print "After Value - {}".format(self.card_value)
        else:
            print 'sorry, there is no card for this person. please create one.'
    
    def check_balance(self):
        if self.card_type == 'Value':
            print "Your Balance is: {}".format(self.card_value)
        elif self.card_type == 'Monthly':
            print 'Your card does not have a balance. You may use it until the end of the month'
        elif self.card_type == 'TransitEmployee':
            print 'You ride for free!'

class TestPersonFunctions(unittest.TestCase):
    def setUp(self):
        # person who buys a monthly today
        self.steve = Person(1)
        self.steve.buy_card('Monthly')
        # person who buys a monthly on October 22
        self.mark = Person(4)
        self.mark.buy_card('Monthly',None,datetime.date(2013,10,22))
        # transit worker who gets a pass
        self.jim = Person(3)
        self.jim.buy_card('TransitEmployee')
        # elderly person who buys a value pass
        self.eric = Person(2)
        self.eric.buy_card('Value',200)
    
    def test_buy_card(self):
        # makes sure that the costs are correct.
        self.assertEqual(self.steve.cost,25)
        self.assertEqual(self.mark.cost,25)
        self.assertEqual(self.jim.cost,0)
        self.assertEqual(self.eric.cost,200)
    
    def test_swipe_card(self):
        self.weekender = Person(2)
        self.weekender.buy_card('Value',200)
        
        self.steve.swipe_card()
        self.mark.swipe_card()
        self.jim.swipe_card()
        self.eric.swipe_card(datetime.date(2013,10,8))
        self.weekender.swipe_card(datetime.date(2013,10,20))
        
        # these 3 don't have to do anything but check that there is a card
        self.assertEqual(self.steve.card_type,'Monthly')
        self.assertEqual(self.mark.card_type,'Monthly')
        self.assertEqual(self.jim.card_type,'TransitEmployee')
        
        # these check the amount taken from the account based day of the week.
        self.assertEqual(self.eric.card_value,200-2.50)
        self.assertEqual(self.weekender.card_value,200-3.75)
        
    def test_check_balance(self):
        # runs the check balance. should print out his current balance
        self.eric.check_balance()
        
        # based on the setUp value of 200, his balance should still be 200
        self.assertEqual(self.eric.card_value,200)
        