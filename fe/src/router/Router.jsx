import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import ChatPage from '../page/chat-page/ChatPage'
import Login from '../page/login/Login'
import ProtectedRoute from './ProtectedRoute'
import React from 'react'
import MainLayout from '../layout/MainLayout'

const Router = () => {
    const router = createBrowserRouter([
        {
            path: '/login',
            element: <Login />
        },
        {
            path: '/',
            element: <ProtectedRoute>
                        <MainLayout />
                     </ProtectedRoute>,
            children: [
                {
                    path: "/",
                    element: <ChatPage />
                }
            ]
        }
    ])

    return <RouterProvider router={router} />
}

export default Router