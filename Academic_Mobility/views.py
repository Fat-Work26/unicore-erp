from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import AcademicMobilityOrder

# ================================================================
@login_required(login_url='login')
def newOrder(request):
    return render(request,'Academic_Mobility/newOrder.html')
   
    #  order = AcademicMobilityOrder.objects.filter(user = request.user)
    #  if (order.count()>0):
          
        #  return render(request,'Academic_Mobility/Orderstage.html',{'order':order})
        
    #  else:
    #     if request.method=='POST':
        
    #         if(request.user.profile.TYPE=='Enseignants'):
                
    #                 form = StageCreationForm(request.POST,request.FILES)

    #         elif(request.user.profile.TYPE=='Personnels Administratifs Techniques et de Soutien'):
    #                 form = StageCreationForm1(request.POST,request.FILES)
    #         elif(request.user.profile.TYPE=='Doct'):
    #                 form = StageCreationForm2(request.POST,request.FILES)        

    #         if form.is_valid():
    #                 instance = form.save(commit = False)
    #                 user = request.user
    #                 instance.user = user
    #                 instance.save()
    #                 messages.success(request,'تم ارسال طلبكم،  في انتظار رد المسؤول عليها  ',extra_tags = 'alert alert-success alert-dismissible show')
    #                 return redirect('newOrder')
            
    #     dataset = dict()
       
    #     if(request.user.profile.TYPE=='Enseignants'):
    #         form = StageCreationForm()
    #     elif(request.user.profile.TYPE=='Personnels Administratifs Techniques et de Soutien'):
    #         form = StageCreationForm1()
    #     elif(request.user.profile.TYPE=='Doct'):
    #         form = StageCreationForm2()    
                
    #     dataset['form'] = form
    #     dataset['title'] = 'طلب تربص '
    #     return render(request,'Academic_Mobility/newOrder.html',dataset)

# ================================================================