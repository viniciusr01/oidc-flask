## OpenID Connect com Flask

<br>

### OPENID CONNECT 


<p align="center">
  <img src="https://github.com/viniciusr01/oidc-flask/blob/master/Fluxo%20OpenID%20Connect.png" />
</p>


RP -> Aplicação cliente que requisita a autenticação e informações do usuário final para o Provedor OpenID.

OP -> Servidor de autorização que é capaz de autenticar o usuário e fornercer informações sobre o usuário final.

<ol>
<li> O RP (Client) envia uma requisição para o OpenID Provider (OP) [WSO2 Identity Server].</li>
<li> O OP [WSO2 Identity Server] autentica o usuário final e obtem autorização.</li>
<li> O OP responde com um ID Token e geralmente com um Access Token.</li>
<li> O RP pode enviar requisições com o Access Token para o OP para solicitar informações do usuário final.</li>
<li> O OP retornar com informações do usuário para o RP.</li>
</ol>

Para mais informações sobre Opend ID Connect: https://openid.net/specs/openid-connect-core-1_0.html


- Biblioteca usada do Open ID: https://pyoidc.readthedocs.io/en/latest/

- Este código demonstra como construir um RP usando a biblioteca pyoidc, que é uma biblioteca certificada pela Fundação OpenID.

<br>
<br>

### Como executar

  - Na pasta front-end execute o comando abaixo, para instalar as bibliotecas
  > npm install
  <br>
  
  - Após intalada as bibliotecas, execute o comando abaixo, para startar o front-end
  > npm start
  <br>
  
  - Na pasta back-end execute os seguinte comandos:
  > . venv/bin/activate <br>
  > flask run
  




