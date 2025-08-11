import React, { useEffect, useState } from 'react'
import { Navigate } from 'react-router-dom'
import { Flex, Spin } from 'antd'
import axios from 'axios'

const ProtectedRoute = ({ children }) => {
    const [loading, setLoading] = useState(true)
    const [isAuth, setIsAuth] = useState(false)

    useEffect(() => {
        axios
            .get(
                `${import.meta.env.VITE_BASE_URL}/auth/verify-token`,
                {
                    withCredentials: true
                }
            )
            .then(() => setIsAuth(true))
            .catch(() => setIsAuth(false))
            .finally(() => setLoading(false))
    }, [])

    if (loading) {
        return (
            <div style={{ width: '100vw', height: '100vh' }}>
                <Flex>
                    <Spin />
                </Flex>
            </div>
        )
    }

    if(!isAuth){
        return <Navigate to="/login" replace/>
    }

    return children
}

export default ProtectedRoute