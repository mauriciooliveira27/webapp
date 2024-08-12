from django.shortcuts import render,redirect
from django.views import View
from .service_controller import start_pm2_process,stop_pm2_process,status_pm2_process, test_read_temp
from .models import RegistroPlaca, RegistroCordoes,Servicos
from django.contrib import messages
from .commandSQL import registro_cordao, update_canal_sensor,update_cod_placa,registrar_canal_sensor,cadastrar_cordao_manual
from django.views.generic import ListView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from .forms import PlacaForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect,JsonResponse
from django.urls import reverse
import re
import httpx

class ConfigurePlacaView(View):

    template_name = 'configure_placa.html'
    

    def get(self, request):
        
        #print(self.cordao_sensor.cordao_fisico)
        return render(request, self.template_name)
   
    
    def post(self, request):

        nome                =   str(request.POST['nome_placa'])
        cod_placa           =   int(request.POST['cod_placa'])
        ip_placa            =   str(request.POST['ip_placa'])
        #numero_cordao = int(request.POST['cordao'])    
        self.cordao_sensor  =   RegistroCordoes.objects.last()
    
        if isinstance(cod_placa,int) and isinstance(ip_placa, str):
            if RegistroPlaca.objects.filter(ip=ip_placa).exists() or RegistroPlaca.objects.filter(nome=nome).exists() :
                messages.success(request, 'Placa ja existe.')

            else:
                placa           = RegistroPlaca(ip  =   ip_placa, nome  =   nome,cod_placa  =   cod_placa)
                placa.save()
                placa_obj       = RegistroPlaca.objects.filter(ip=ip_placa).first()
                #id_placa = placa_obj.id
                
                
                messages.success(request,'Salvo com sucesso.')

        return redirect('sensor_config_form')


class ListPlacaView(ListView):

    models              =   RegistroPlaca
    template_name       =   'home.html'
    queryset            =   RegistroPlaca.objects.all()
    context_object_name =   'placas'

class UpdatePlacaView(UpdateView):
    model           =   RegistroPlaca
    template_name   =   'update_placa.html'
    fields          =   ( 'id','nome','cod_placa','ip')
    success_url     =   reverse_lazy('home')

    def post(self,request,pk):

        placa               =   self.get_object()
        placa.cod_placa     =   request.POST['cod_placa']
        placa.nome          =   request.POST['nome']
        placa.ip            =   request.POST['ip']
        

        cod_placa = request.POST['cod_placa']
        id_placa = request.POST['id']
        
        update_cod_placa(cod_placa,id_placa)
        placa.save()
        return redirect(self.success_url)

class DeletePlacaView(DeleteView):
    model           =   RegistroPlaca
    template_name   =   'warning_delete.html'
    success_url     =   reverse_lazy('home')




class UpdateCordoesView(UpdateView):

    def get(self, request):
        context = {
            'cordoes' : RegistroCordoes.objects.filter()
        }

        return render(request, 'update_cordoes.html', context) 
    

    def post(self, request):

        canal_sensor    =   request.POST.getlist('cordao_fisico')
        sensor          =   request.POST.getlist('sensor')
        canal           =   request.POST.getlist('canal')
        
            
        update_canal_sensor(canal_sensor,canal,sensor)
        return redirect('update-cordoes')


class ListCordoesView(ListView):
    models              =   RegistroCordoes
    template_name       =   'list_cordoes.html'
    queryset            =   RegistroCordoes.objects.all()
    context_object_name =   'cordoes'


class DeleteCordaoView(DeleteView):
    model               =   RegistroCordoes
    template_name       =   'warning_delete.html'
    success_url         =   reverse_lazy('update-cordoes')




class SensorConfigView(View):
    template_name = 'sensor_config_form.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
    
            canais          =   int(request.POST['numCanais'])
            lista_canal     =   [i for i in range(1, canais + 1)]
            lista_sensor    =   []

            for canal in lista_canal:
                s = int(request.POST[f'sensores_canal_{canal}'])
                lista_sensor.append(s)
          
           
            lista_sensores              =   [[i for i in range(1, n + 1)] for n in lista_sensor]
            ultimo_registro_cordao      =   RegistroCordoes.objects.last()
            ultima_placa                =   RegistroPlaca.objects.last()
            ultimo_registro             =   RegistroCordoes.objects.filter(cod_placa = ultima_placa.cod_placa).last()

            if ultimo_registro is None:
                ultimo_sensor   =   0
                ultimo_canal    =   0
            
            else:
                ultimo_sensor   =   ultimo_registro.sensor_placa
                ultimo_canal    =   ultimo_registro.canal_placa
            placa = RegistroPlaca.objects.last()
            
           
            registro_cordao(ultimo_registro_cordao,placa.cod_placa,placa.id,lista_sensores)
            
         
            registrar_canal_sensor(ultimo_sensor,ultimo_canal,lista_sensores)
            
            return redirect ('home')
    


class CreateCordaoView(CreateView):
    template_name = 'cadastrar_cordoes.html'
    def get(self, request):

        

        return render(request,self.template_name)
    
    def post(self,request):

        cod_placa = request.POST.getlist('cod_placa[]')
        ip_placa = request.POST.getlist('id_placa[]')
        cordao_fisico = request.POST.getlist('cordao-fisico[]')
        canal = request.POST.getlist('canal[]')
        sensor = request.POST.getlist('sensor[]')

        cadastrar_cordao_manual(cod_placa,ip_placa,cordao_fisico, canal,sensor)
        return render(request, self.template_name)



class ServicosView(View):

    template_name = 'servicos.html'

    def get(self, request):
        servicos = Servicos.objects.all()
        context = {'servicos':servicos}
        return render(request, self.template_name,context)
    
    def post(self, request):
        nome_servico = request.POST.get('nome_servico')

        result = start_pm2_process(nome_servico)
        print(result)
       
        return redirect('servico-start')

  

class ServicosStopView(View):

    template_name = 'servicos.html'
    
    def post(self, request):
        nome_servico = request.POST.get('nome_servico')
       
        stop_pm2_process(nome_servico)
       
        return redirect('servico-start')




class ServicosStatusView(View):

    template_name = 'servico_status.html'

    def get(self,request):
        status = request.GET.get('status')

        online = re.search(r'\bonline\b', status)
        stopped = re.search(r'\bstopped\b', status)        

        if online:
            status_service = online.group(0)
            return render(request, self.template_name, {'result': status_service})
        
        elif stopped:
            status_service = stopped.group(0)
            return render(request, self.template_name, {'result': status_service})
        
        else:
            return render(request, self.template_name, {'result': 'Serviço não iniciado.'})

            
        

    def post(self,request):
        nome_servico = request.POST.get('nome_servico')
        result = status_pm2_process(nome_servico)
        print(result)
        redirect_url = reverse('servico-status') + '?status=' + result

        # Redirecionando com parâmetros de consulta
        return HttpResponseRedirect(redirect_url)
    

class AsyncClassView(View):

    async def get(self, request, *args, **kwargs):

        temperature_data = await test_read_temp()
        return JsonResponse({'Temperature':temperature_data})

