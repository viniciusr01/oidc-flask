import React from 'react';
import './App.css';
import { BrowserRouter, Route, Switch} from 'react-router-dom'
import Home from './pages/Home'
import Logado from './pages/Autenticado'




const Routes = () => {
    return (
        <BrowserRouter>
            <Switch>
    
                <Route exact path ="/" component={Home}/>
    
                <Route path ="/Autenticado" component={Logado}/> 

    
            </Switch>
        </BrowserRouter>
    );
    };
    
export default Routes;
