from django.conf import settings
from .models import Type
from .models import Order
from .models import product
from .models import OrderItem
import datetime



class Data(object):
    def __init__(self):
        self.orders = Order.objects.all()
        self.products=product.objects.all()
        self.start_date = []
        self.end_date = []

    def set_dates(self,startDate,endDate):
        self.start_date=startDate
        self.end_date=endDate

    def get_all_orders(self):
        elapsed=self.end_date-self.start_date
        data=[]
        if(elapsed<=datetime.timedelta(days=31)):
            for i in range (elapsed.days+1):
                date=self.start_date+datetime.timedelta(days=i)
                orders=Order.objects.filter(order_date__day=str(date.day))
                orders=orders.filter(order_date__month=str(date.month))
                orders=orders.filter(order_date__year=str(date.year))
                sum=0
                for order in orders:
                    sum+=order.get_sum()
                data.append(sum)
        elif(elapsed<datetime.timedelta(days= 366)):
            for i in range (0,elapsed.days+30,30):
                date=self.start_date+datetime.timedelta(days=i)
                orders=Order.objects.filter(order_date__month=str(date.month))
                orders=orders.filter(order_date__year=str(date.year))
                sum=0
                for order in orders:
                    sum+=order.get_sum()
                data.append(sum)
        else:
            for i in range (0,elapsed.days+365,365):
                date=self.start_date+datetime.timedelta(days=i)
                orders=Order.objects.filter(order_date__year=str(date.year))
                sum=0
                for order in orders:
                    sum+=order.get_sum()
                data.append(sum)
        return data

    def get_dates_labels(self):
        elapsed=self.end_date-self.start_date
        labels=[]
        months=['Январь','Февраль','Март','Апрель','Май','Июнь','Июль','Август','Сентябрь','Октябрь','Ноябрь','Декабрь']
        if(elapsed<=datetime.timedelta(days=31)):
            for i in range (elapsed.days+1):
                day=self.start_date+datetime.timedelta(days=i)
                s=str(day.day)+"."+str(day.month)
                labels.append(day.day)
        elif(elapsed<datetime.timedelta(days= 366)):
            for i in range (0,elapsed.days,30):
                date=self.start_date+datetime.timedelta(days=i)
                labels.append(months[date.month-1])
        else:
            for i in range (0,elapsed.days+365,365):
                date=self.start_date+datetime.timedelta(days=i)
                labels.append(date.year)

        return labels


    def get_all_products(self):
        elapsed=self.end_date-self.start_date
        data={}
        items=[]
        if(elapsed <= datetime.timedelta(days=31)):
            orders=Order.objects.filter(order_date__month=str(self.start_date.month))
            orders=orders.filter(order_date__year=str(self.start_date.year))
        elif(elapsed < datetime.timedelta(days= 366)):
            orders=Order.objects.filter(order_date__year=str(self.start_date.year))
        else:
            orders = Order.objects.all()

        for order in orders:
            orderitems=OrderItem.objects.filter(order=order.id)
            for item in orderitems:
                items.append(item)
        for item in items:
            id=int(item.prod.id)
            if(id in data):
                data[id]+=item.quantity
            else:
                data[id]=item.quantity
        returning_data=[]
        nameslist=[]
        for key in data:
            prod = product.objects.filter(id=key)
            nameslist.append(prod[0].title)
            returning_data.append(data[key])
        return [returning_data,nameslist]





