#Import Biblioteca do Flask
from flask import Flask, request, redirect

#Import Biblioteca do OpenID Connect
from oic.oic import Client
from oic.utils.authn.client import CLIENT_AUTHN_METHOD


'''
               OPENID CONNECT

+--------+                                   +--------+
|        |                                   |        |
|        |---------(1) AuthN Request-------->|        |
|        |                                   |        |
|        |  +--------+                       |        |
|        |  |        |                       |        |
|        |  |  End-  |<--(2) AuthN & AuthZ-->|        |
|        |  |  User  |                       |        |
|   RP   |  |        |                       |   OP   |
|        |  +--------+                       |        |
|        |                                   |        |
|        |<--------(3) AuthN Response--------|        |
|        |                                   |        |
|        |---------(4) UserInfo Request----->|        |
|        |                                   |        |
|        |<--------(5) UserInfo Response-----|        |
|        |                                   |        |
+--------+                                   +--------+

RP -> Aplicação cliente que requisita a autenticação e informações do usuário final para o Provedor OpenID.

OP -> Servidor de autorização que é capaz de autenticar o usuário e fornercer informações sobre o usuário final.

(1) O RP (Client) envia uma requisição para o OpenID Provider (OP) [WSO2 Identity Server].
(2) O OP [WSO2 Identity Server] autentica o usuário final e obtem autorização.
(3) O OP responde com um ID Token e geralmente com um Access Token.
(4) O RP pode enviar requisições com o Access Token para o OP para solicitar informações do usuário final.
(5) O OP retornar com informações do usuário para o RP.

Para mais informações sobre Opend ID Connect: https://openid.net/specs/openid-connect-core-1_0.html


-> Biblioteca usada do Open ID: https://pyoidc.readthedocs.io/en/latest/

-> Este código demonstra como construir um RP usando a biblioteca pyoidc, que é certificada pela fundação OpenID.

'''



#Criar objeto cliente
client = Client(client_authn_method=CLIENT_AUTHN_METHOD)


app = Flask(__name__)



# Desativando a verificação de certificado SSL
# É desativado a verificação SSL, pois o WSO2 IS que estamos usando de exemplo não tem um certificado válido
# Mais informações: https://stackoverflow.com/questions/15445981/how-do-i-disable-the-security-certificate-check-in-python-requests

import warnings
import contextlib

import requests
from urllib3.exceptions import InsecureRequestWarning


old_merge_environment_settings = requests.Session.merge_environment_settings

@contextlib.contextmanager
def no_ssl_verification():
    opened_adapters = set()

    def merge_environment_settings(self, url, proxies, stream, verify, cert):
        # Verification happens only once per connection so we need to close
        # all the opened adapters once we're done. Otherwise, the effects of
        # verify=False persist beyond the end of this context manager.
        opened_adapters.add(self.get_adapter(url))

        settings = old_merge_environment_settings(self, url, proxies, stream, verify, cert)
        settings['verify'] = False

        return settings

    requests.Session.merge_environment_settings = merge_environment_settings

    try:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', InsecureRequestWarning)
            yield
    finally:
        requests.Session.merge_environment_settings = old_merge_environment_settings

        for adapter in opened_adapters:
            try:
                adapter.close()
            except:
                pass



#Registrando o Cliente (RP)

from oic.oic.message import ProviderConfigurationResponse

# Informações padrões sobre os end-points do Provedor OpenID (OP - WSO2 IS)
op_info = ProviderConfigurationResponse( 
    version="1.0", 
    issuer= "https://wso2.dcc.ufmg.br:9443/",
    authorization_endpoint="https://wso2.dcc.ufmg.br:9443/oauth2/authorize",
    token_endpoint="https://wso2.dcc.ufmg.br:9443/oauth2/token",
    jwks_uri= "https://wso2.dcc.ufmg.br:9443/oauth2/jwks",
    userinfo_endpoint= "https://wso2.dcc.ufmg.br:9443/oauth2/userinfo",
    revocation_endpoint= "https://wso2.dcc.ufmg.br:9443/oauth2/revoke",
    introspection_endpoint= "https://wso2.dcc.ufmg.br:9443/oauth2/introspect",
    end_session_endpoint= "https://wso2.dcc.ufmg.br:9443/oidc/logout"
    )

client.handle_provider_config(op_info, op_info['issuer'])


from oic.oic.message import RegistrationResponse

# Client ID e Client Secret são geradas pelo Provedor OpenID (OP - WSO2 IS)
info = {"client_id": "HRtE9bHFDqTRTVj5YXE84PLB8B4a", 
        "client_secret": "IIy6Mwf29RrhuHGAAHm14v7Ei00a"
        }


client_reg = RegistrationResponse(**info)

client.store_registration_info(client_reg)



# Após realizar o registro do cliente, é possível solicitar que o OP autentique usuários e obtenha informações sobre eles.
# O Fluxo de Autenticação Utilizado é Authorization Code Grant, definido pela RFC 6749 do OAuth 2.0
# Para mais informações sobre o fluxo de autenticação: https://tools.ietf.org/html/rfc6749#section-4.1

# Nesta etapa, ao fim é gerado a URL a qual o usuário deve ser direcionado para realizar o Login.

from oic import rndstr
from oic.utils.http_util import Redirect


state = rndstr()
nonce = rndstr()

args = {
    "client_id": client.client_id,
    "response_type": ['code'], # Determina o fluxo de autorização OAuth 2.0 que será utilizado
    "scope": ["openid email"], #Por padrão é inserido 'openid', mas também pode ser inserido informações a qual deseja ter do usuário, como exemplo, email.
    "nonce": nonce, #É um valor de string usado para associar uma sessão de cliente a um token de ID e para mitigar ataques de repetição
    "redirect_uri": ['http://localhost:5000/callback'], #URL que o Provedor OpenID deve retornar após autenticação ser realizada
    "state": state #É utilizado para controlar as respostas às solicitações pendentes
}

auth_req = client.construct_AuthorizationRequest(request_args=args)
login_url = auth_req.request(client.authorization_endpoint)




@app.route("/")
def main():
    return "Hello Word"


@app.route("/login", methods=['GET'])
def login():
    return login_url
        

#Rota que trata informações retornadas pela provedor OpenID (OP - WSO2 IS)
@app.route("/callback")
def callback():

    from oic.oic.message import AuthorizationResponse
   
    # If you're in a WSGI environment
    # Coleta as informações da URL que foram retornadas pelo Provedor OpenID (OP - WSO2 IS)
    response = request.query_string
  

    response = response.decode('ascii')
   
    
    aresp = client.parse_response(AuthorizationResponse, info=response, sformat="urlencoded")
    
   
    code = aresp["code"]
    assert aresp["state"] == state   #Verifica se o state enviado na solicitação de autenticação é o mesmo retornado pelo Provedor Open ID (OP - WSO2 IS)

  
    with no_ssl_verification():
        
        # Utiliza o Code Grant Type retornado pelo OP para solicitar ao OP o Access Token e ID Token
        args = {
        "code": aresp["code"]
        }
        resp = client.do_access_token_request(state=aresp["state"],
                                            request_args=args,
                                            authn_method="client_secret_basic")

    # Printa as informações sobre a autenticação realizada.
    # Informações como: Access Token, ID Token, Token Type, entre outras.
    print(resp)


    if(resp["access_token"]!= ""):
        return redirect("http://localhost:3000/Autenticado")
    
    else:
        return "ERRO DE AUTENTICAÇÃO"



app.run(debug=True)