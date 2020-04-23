from django.shortcuts import render
from django.http import HttpResponse

from ecom.models import *
from math import ceil
from django.views.decorators.csrf import csrf_exempt
from ecom.paytm import checksum
MERCHANT_KEY = 'npI_h5KJ6!BxemZ4'

# Create your views here.

def index(request):



    #params={ 'no_of_slides':nslides , 'range': range(nslides) , 'product':products}
    #allprods=[[products , range(1,nslides) , nslides ],
              #  [products , range(1,nslides) , nslides]]

    allprods = []
    catprods = product.objects.values('category' ,'id')
    cats = {item ['category'] for item in catprods}

    for cat in cats:
        prod = product.objects.filter(category=cat)
        n=len(prod)
        nslides = n//4 + ceil((n/4)-(n//4))

        allprods.append([prod , range( 1, nslides ) , nslides ])

    params={'allprods':allprods}
    return render(request,'ecom/index.html', params)

def about(request):

    return render(request,'ecom/about.html')

def contact(request):
    #thank = False
    if request.method=="POST":
       # print(request)
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        phone=request.POST.get('phone','')
        desc=request.POST.get('desc','')
        #print(name , email , phone , desc)
        contact = contact(name=name, email=email , phone=phone , desc=desc)
        contact.save()
    #thank = True


    return render(request,'ecom/contact.html' )

def tracker(request):
    return render(request,'ecom/tracker.html')

def search(request):
    return render(request,'ecom/search.html')

def productview(request, myid):
    #fetching product using id
    produ = product.objects.filter(id=myid)


    return render(request,'ecom/prodview.html', {'produ':produ[0]})

def checkout(request):
    if request.method=="POST":
       # print(request)
        items_json=request.POST.get('itemsJson','')
        name=request.POST.get('name','')
        amount=request.POST.get('amount','')
        email=request.POST.get('email','')
        address=request.POST.get('address1','') + " "+ request.POST.get('address2','')
        state=request.POST.get('state','')
        city=request.POST.get('city','')
        zip_code=request.POST.get('zip_code','')
        phone_number=request.POST.get('phone_number','')


        #print(name , email , phone , desc)
        order = Orders(items_json=items_json, name=name, amount=amount, email=email , address=address, city=city, state=state, zip_code=zip_code, phone_number=phone_number )
        order.save()
        thank=True
        id=order.order_id
        #return render(request,'ecom/checkout.html' , {'thank':thank  , 'id':id})
        #request paytm to transfer amount to your account after paytm by user
        param_dict = {
            'MID':'AhagdK84355164141885',
            'ORDER_ID':str(order.order_id),
            'TXN_AMOUNT':str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID':'Retail',
            'WEBSITE':'DEFAULT',
            'CHANNEL_ID':'WEB',
	        'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest/',

        }
        param_dict['CHECKSUMHASH'] = checksum.generate_checksum(param_dict,MERCHANT_KEY)
        return render(request,'ecom/paytm.html', {'param_dict': param_dict})



    return render(request,'ecom/checkout.html')
@csrf_exempt
def handlerequest(request):
    #paytm will post request c
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i=='CHECKSUMHASH':
            checksum=form[i]

    #verify = checksum.verify_checksum(response_dict, MERCHANT_KEY)
    verify = checksum.verify_checksum(paytmParams, "MERCHANT_KEY", checksum)
    if verify:
        if response_dict['RESPCODE'] =='01':
            print("Order Successsful")
        else:
            print("Order was not Successsful because " + response_dict['RESPMSG'])

    return  render(request,"ecom/paymentstatus.html" , {'response':response_dict })
