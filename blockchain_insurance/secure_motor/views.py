from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Client
from web3 import Web3
from solcx import compile_standard
import json, os
import bcrypt

#compile contract
cwd = os.path.dirname(__file__)
static = os.path.join(cwd, 'static')
compiled = os.path.join(static, 'compiled_code.json')
file_path = os.path.join(static, 'insurance.sol')
data_file = open(file_path, 'r')
data = data_file.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"Insurance.sol": {"content": data}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            },
        },
    },
    solc_version="0.8.22"
)
with open(compiled, 'w') as file:
    json.dump(compiled_sol, file)

#get bytecode
bytecode = compiled_sol["contracts"]["Insurance.sol"]["MotorInsurance"]["evm"]["bytecode"]["object"]
#get abi
abi = compiled_sol["contracts"]["Insurance.sol"]["MotorInsurance"]["abi"]

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chain_id = 5777
my_address = "0xD16c999b4069a8D6de8F2da720D93A57cBBD9659"
private_key = "0x4cb2d59008b7df8922300e7b38c3fed9f2e4fae9bfd59aeae15b141fce659e27"

Insurance = w3.eth.contract(abi=abi, bytecode=bytecode)
print(Insurance)
# Create your views here.
# Home page
def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

# Login
def login(request):
    template = loader.get_template('login.html')
    context ={}
    if request.method == "POST":
        email = request.POST.get("email")
        if Client.objects.filter(email=email).exists():
            passString = request.POST.get("password")
            password = bytes(passString, 'utf-8')
            client = Client.objects.all().get(email=email)
            dbPass = client.password
            dbPassByte = bytes(dbPass, 'utf-8')
            if bcrypt.checkpw(password, dbPassByte):
                print("Password correct")
                request.session['email'] = client.email
                return redirect('dashboard')
            else:
                print("Password incorrect")
        else:
            print("User doesn't exist")
    return HttpResponse(template.render(context, request))

# Register
def register(request):
    template = loader.get_template('register.html')
    context = {}
    client = Client()
    salt = bcrypt.gensalt()
    if request.method == "POST":
        first_name = request.POST.get("fName")
        last_name = request.POST.get("lName")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        confPassword = request.POST.get("confirmPassword")
        if password == confPassword:
            passbyte = bytes(password, 'utf-8')
            print(passbyte)
            hashPassByte = bcrypt.hashpw(passbyte, salt)
            hashPass = hashPassByte.decode('utf-8')
            client.first_name = first_name
            client.last_name = last_name
            client.email = email
            client.phone = phone
            client.password = hashPass
            client.save()
            print("User registered!")
            return redirect('login')
        else: 
            print("Passwords do not match")
    return HttpResponse(template.render(context, request))

def dashboard(request):
    template = loader.get_template('dashboard.html')
    if request.session.has_key('email'):
        email = request.session['email']
        client = Client.objects.all().get(email=email)
        context = {
            "email": email,
            "fName": client.first_name,
            "lName": client.last_name
        }
        return HttpResponse(template.render(context, request))
    else:
        return redirect('login')

def policies(request):
    template = loader.get_template('policies.html')
    if request.session.has_key('email'):
        email = request.session['email']
        client = Client.objects.all().get(email=email)
        context = {
            "email": email,
            "fName": client.first_name,
            "lName": client.last_name
        }
        return HttpResponse(template.render(context, request))
    else:
        return redirect('login')

def fileclaim(request):
    template = loader.get_template('fileclaim.html')
    if request.session.has_key('email'):
        email = request.session['email']
        client = Client.objects.all().get(email=email)
        context = {
            "email": email,
            "fName": client.first_name,
            "lName": client.last_name
        }
        return HttpResponse(template.render(context, request))
    else:
        return redirect('login')

def myclaims(request):
    template = loader.get_template('myclaims.html')
    if request.session.has_key('email'):
        email = request.session['email']
        client = Client.objects.all().get(email=email)
        context = {
            "email": email,
            "fName": client.first_name,
            "lName": client.last_name
        }
        return HttpResponse(template.render(context, request))
    else:
        return redirect('login')

def support(request):
    template = loader.get_template('support.html')
    if request.session.has_key('email'):
        email = request.session['email']
        client = Client.objects.all().get(email=email)
        context = {
            "email": email,
            "fName": client.first_name,
            "lName": client.last_name
        }
        return HttpResponse(template.render(context, request))
    else:
        return redirect('login')

def logout(request):
    try:
        del request.session['email']
    except:
        pass
    return redirect('login')

def terms(request):
    template = loader.get_template('terms.html')
    context = {

    }
    return HttpResponse(template.render(context, request))

def applyPolicy(request):
    template = loader.get_template('applyPolicy.html')
    if request.session.has_key('email'):
        email = request.session['email']
        client = Client.objects.all().get(email=email)
        context = {
            "email": email,
            "fName": client.first_name,
            "lName": client.last_name
        }
        if request.method == "POST":
            first_name = request.POST.get("fName")
            last_name = request.POST.get("lName")
            licenseNo = request.POST.get("licenseNo")
            pType = request.POST.get("pType")
            use = request.POST.get("use")
            registration = request.POST.get("registration")
            print(use)
            nonce = w3.eth.get_transaction_count(my_address)
            print(nonce)
        return HttpResponse(template.render(context, request))
    else:
        return redirect('login')


