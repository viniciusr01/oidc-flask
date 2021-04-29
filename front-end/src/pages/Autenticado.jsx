import React from 'react';
import axios from 'axios';



//Função de Logout
function logout() {
    console.log("To na função de logout!") 
    }




class Logado extends React.Component{
  
    
    
    render (){
             
    
           
        return (
            <div className="Logado-header">
                <h2>Autenticação Realizada!</h2>
                <br></br>

                <button
                            className="button-logout"
                             onClick = {logout}
                            >
                                Logout
                            </button>
                <br></br>


                <div >
                
                </div>
            </div>


        )


    }




}




export default Logado;