
// import React from "react";
// import ReactDOM from "react-dom";
// import App from "./js/App.js";
// import Dashboard from "./js/Dashboard.js";
// import Login from "./js/Login.js";
// //ReactDOM.render(<Login />, document.getElementById("root"));
//
//
// ReactDOM.render(<Login />, document.getElementById("root"));

import React from "react";
import ReactDOM from "react-dom";
import Login from "./js/Login.js";
import Dashboard from "./js/Dashboard.js";
import Chart from "./js/Chart.js";
import { BrowserRouter, Route, Link } from "react-router-dom";


ReactDOM.render((
  <BrowserRouter>
    <div>
      <Route path="/" exact component={Login} />
      <Route path="/map/" exact component={Dashboard} />
      <Route path="/chart/" component={Chart} />
    </div>
  </BrowserRouter>
), document.getElementById('root'))
