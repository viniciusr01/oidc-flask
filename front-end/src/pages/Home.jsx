import React from 'react';
import logos from "./Logo Lemonade.png";
import axios from 'axios';



//Função que recebe a url de login e abre a URL.
function login () {


    axios
    .get('/login')
    .then(url_login => {
      console.log(url_login.data);
      
      window.location.href = url_login.data //Abre no browser a URL de login recebida.
    })
    

  }
  



  class Home extends React.Component {

    
    render (){  
    return (
      
        <div >
          
          <header className="App-header">
    
            <img src={logos} className="logos" alt="Logo do Lemonade"></img>
            <h4> Protótipo em Flask - OpenID Connect</h4>
            <div className="circulo">
            </div>
              <button
              className = "button-login"
              onClick = {login}
              >
                Login
             </button>
          </header>
          
        </div>
      );
    }


  };

export default Home;