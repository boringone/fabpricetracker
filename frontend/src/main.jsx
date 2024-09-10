import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import CardDetail from './CardDetail.jsx'
import './index.css'
import { createBrowserRouter, RouterProvider, Link } from 'react-router-dom'

const router = createBrowserRouter([
    {path: '/:pageNumb?',
    element: <App />,
    errorElement: <div>404 Not Found
                <Link to="/">Home</Link>
            </div>,
    },
    {path: '/cardData/:printingId',
    element: <CardDetail/>},


])

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <RouterProvider router={router}/>
  </React.StrictMode>,
)
