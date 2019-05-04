import datetime
from .Data import Data
from .cart import Cart
from .models import Type
from .models import Order
from .forms import UserForm
from .models import product
from .models import feedback
from .models import OrderItem
from .forms import FeedbackForm
from .models import needforvideo
from django.conf import settings
from django.views.generic import View
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login
from django.shortcuts import render,get_object_or_404, get_list_or_404,redirect
from rest_framework.views import APIView
from rest_framework.response import Response


#Index
def index(request):
    needforvideos=needforvideo.objects.filter(title='beauty')
    feedbacks=feedback.objects.order_by('-id')
    if request.method == 'POST':
        form=FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
    forma=FeedbackForm()
    popular=product.objects.order_by('price')[:4]
    latest=product.objects.order_by('-created_date')[:4]
    products=product.objects.all()[:4]
    context={
        "video":needforvideos,
        "feedback":feedbacks,
        'form': forma,
        "pop":popular,
        'last':latest,
        'prods':products
    }
    return render(request, 'blog/index.html',context )


#Mail
def mail(request):
    name=request.GET.get('author')
    number=request.GET.get('number')
    idea=request.GET.get('idea')
    msg = render_to_string('mails/idea_mail.html', {'name':name,'number':number,'idea': idea})
    send_mail('Идеи от клиента', msg, settings.EMAIL_HOST_USER ,['qwertyasdfgzxcvpoiu@mail.ru'], )
    prod=get_object_or_404(product,id=4)
    return render(request, 'blog/product-detail.html', {"prod":prod } )

#All products
def products(request,type,order):
    products=[]
    if type=="tort":
        if order=="chip":
            products=get_list_or_404(product.objects.order_by('price'),type=1)
        else:
            products=get_list_or_404(product.objects.order_by('-price'),type=1)
    elif type=="pirog":
        if order=="chip":
            products=get_list_or_404(product.objects.order_by('price'),type=5)
        else:
            products=get_list_or_404(product.objects.order_by('-price'),type=5)
    elif type=="konfeta":
        if order=="chip":
            products=get_list_or_404(product.objects.order_by('price'),type=3)
        else:
            products=get_list_or_404(product.objects.order_by('-price'),type=3)
    elif type=="desert":
        if order=="chip":
            products=get_list_or_404(product.objects.order_by('price'),type=2)
        else:
            products=get_list_or_404(product.objects.order_by('-price'),type=2)
    elif type=="domash":
        if order=="chip":
            products=get_list_or_404(product.objects.order_by('price'),type=4)
        else:
            products=get_list_or_404(product.objects.order_by('-price'),type=4)
    elif type=="all":
        if order=="chip":
            products=product.objects.order_by('price')
        else:
            products=product.objects.order_by('-price')
    return render(request, 'blog/products.html', {"prods":products, "type":type} )

#Product details
def detail(request,prod_id):
    prod=get_object_or_404(product,id=prod_id)
    return render(request, 'blog/product-detail.html', {"prod":prod, } )

#Cart
def cart(request):
    cart=Cart(request)
    if(request.POST):
        prod_id=request.POST.get('id')
        prod2=get_object_or_404(product,id=prod_id)
        cart.add(prod2)
    sum=cart.get_total_price()
    cart=request.session.get('cart',{})
    return render(request, 'blog/cart.html', {"list":cart,"sum":sum} )


#Delete
def delete(request):
    cart=Cart(request)
    to_del=request.GET.get('delObj')
    prod=get_object_or_404(product,id=to_del)
    cart.remove(prod)
    sum=cart.get_total_price()
    cart=request.session.get('cart',{})
    return render(request, 'blog/cart.html', {"list":cart,"sum":sum,} )


#Change
def change(request):
    cart=Cart(request)
    to_change=request.POST.get('to_change')
    quantity=int(request.POST.get('quantity'))
    prod=product.objects.filter(id=to_change)
    prod=prod[0]
    cart.add(prod,quantity,True)
    sum=cart.get_total_price()
    cart=request.session.get('cart',{})
    return render(request, 'blog/cart.html', {"list":cart,"sum":sum,} )


#Buy
def buy(request):
    cart=Cart(request)
    sum=cart.get_total_price()
    cart=request.session.get('cart',{})
    if not request.user.is_authenticated:
        message='sign in'
        return render(request, 'blog/cart.html', {"list":cart,"sum":sum,'error':message} )
    else:
        my_order=Order(user=request.user)
        my_order.save()
        total_sum=0
        for key,Product in cart.items():
            prod=get_object_or_404(product,id=Product['id'])
            new_item=OrderItem(prod=prod,quantity=Product['quantity'],order=my_order)
            new_item.save()
        number=request.GET.get('number')
        msg = render_to_string('mails/Buy_mail.html', {'name':request.user.username,'number':number,"list":cart,"sum":sum})
        send_mail('Заказ от клиента', msg, settings.EMAIL_HOST_USER ,['qwertyasdfgzxcvpoiu@mail.ru'] )
        to_clean=Cart(request)
        to_clean.clear()
        return render(request, 'blog/order.html', {"list":cart,"sum":sum} )

#Search
def search(request):
    query=request.GET.get('search')
    if query:
        template='blog/products.html'
        type=Type.objects.filter(name__icontains=query)
        if not type:
            products = product.objects.filter(title__icontains=query)
        else:
            type=type[0]
            products = product.objects.filter(type=type.id)
        context={"prods":products,"type":'all'}
    else:
        template='blog/index.html'
        needforvideos=needforvideo.objects.filter(title='main slider')
        feedbacks=feedback.objects.all()
        forma=FeedbackForm()
        context={"video":needforvideos,"feedback":feedbacks,'form': forma}
    return render(request, template,context )

#Registration
class UserFormView(View):
    form_class=UserForm
    template_name = "registration/register.html"

    #display blank form
    def get(self,request):
        form = self.form_class(None)
        return render(request,self.template_name,{'form':form})


    #process form data
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            #dont save
            user=form.save(commit=False)

            #cleaned(normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()#save

            #Returns user object if all ok
            user=authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("index")
        return render(request,self.template_name,{'form':form})


#Profile
def profile(request):
    orders=Order.objects.all()
    ids=[]
    dict={}
    items=[]
    for order in orders:
        if( order.user==request.user) :
            ids.append(order.id)
    for id in ids:
        items=OrderItem.objects.filter(order=id)
        dict[id]=items
    all_time_sum=0
    order_sum=[]
    sum=0
    if items:
        for order in dict.values():
            for item in order:
                sum+=item.get_sum()
            order_sum.append(sum)
            all_time_sum+=sum
            sum=0
    context={'orders':dict.values(),'all_sum':all_time_sum,"orders_sum":order_sum}
    return render(request, 'blog/profile.html', context )




#AdminPage
def admin(request):
    return render(request, 'blog/admin.html')

#AdminData
class ChartData(APIView):
    authentication_classes = []
    permission_classes = []


    def get(self, request):
        myData=Data()
        if(request.GET):
            start_time=datetime.datetime.strptime(request.GET.get('start'), "%Y-%m-%d")

            end_time=datetime.datetime.strptime(request.GET.get('end'), "%Y-%m-%d")
        else:
            start_time=datetime.datetime.strptime('2019-04-27T19:00:00.999Z', "%Y-%m-%dT%H:%M:%S.%fZ")
            end_time = datetime.datetime.now()
        myData.set_dates(start_time,end_time)
        labels= myData.get_dates_labels()
        defaultData=[]
        defaultData.append(myData.get_all_orders())
        defaultData.append(myData.get_all_products())
        data={
            "labels1":labels,
            "labels2":defaultData[1][1],
            "default1":defaultData[0],
            "default2":defaultData[1][0]
        }
        return Response(data)
