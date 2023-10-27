import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import SearchResults from './views/SearchResults';
import ProductView from './views/ProductView';
import reportWebVitals from './reportWebVitals';
import {
  createBrowserRouter,
  RouterProvider,
}
from "react-router-dom";
import {
  Provider,
  KeepAlive,
} from 'react-keep-alive';
import KeepAliveProvider from "react-keep-alive/es/components/Provider";


const router = createBrowserRouter([
  {
    path: "/",
    element: <App/>,
  },
  {
    path: "/search",
    element: <SearchResults/>,
  },
  {
    path: "/products",
    element: <ProductView/>,
  },
]);


const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  // <React.StrictMode>
    <RouterProvider router={router}>
        <App/>
    </RouterProvider>

  // </React.StrictMode>
);


// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
