import React, { Component} from "react";
import "../css/App.css";

class App extends Component{
  render(){
    return(
      <div className="App">
        <div className="row mt-2">
          <div className="col-md-12 noselect">
              Para: <span className="disabled-color">Manuel Bernal</span>
          </div>
        </div>
        <hr/>
        <div className="row mt-2">
          <div className="col-md-12 noselect">
              Asunto: <span className="disabled-color">Buenas noticias</span>
          </div>
        </div>
        <hr/>

        <div className="row mt-2">
          <div className="col-md-12 noselect disabled-color">
              Hola Ricardo,<br></br><br></br>
              Estoy probando esta nueva app para generar firmas automáticas de correo<br></br><br></br>
              Saludos, <br></br><br></br>
              Ricardo
          </div>
        </div>
      </div>
    );
  }
}

export default App;
