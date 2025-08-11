import React from 'react'
import { Flex, Card, Form, Input, Button, Divider } from 'antd'
import { useNavigate } from 'react-router-dom'
import { BsGoogle } from 'react-icons/bs'
import { useAuth } from '../../hooks/use-auth'

const Login = () => {
    const navigate = useNavigate()
    const { handleLoginWithGoogle, handleLoginWithJWT } = useAuth()

    const onFinish = async (value) => {
        try {
            const success = await handleLoginWithJWT(value.username, value.password);
            if (!success) {
                console.error('Login gagal, periksa kembali username dan password.');
                return
            }

            navigate('/', { replace: true })

        } catch (error) {
            console.error('Terjadi kesalahan saat mencoba login:', error);
        }
    }

    return (
        <Flex justify='center' align='center' style={{ height: '100vh', width: '100vw' }}>
            <Card title="Login" style={{ width: 400 }}>
                <Form style={{ width: '100%' }} onFinish={onFinish}>
                    <Flex justify='center' align='center' vertical gap={15}>
                        <Form.Item label="Username" name="username" layout='vertical' style={{ width: '100%' }}>
                            <Input />
                        </Form.Item>
                        <Form.Item label="Password" name="password" layout='vertical' style={{ width: '100%' }}>
                            <Input.Password />
                        </Form.Item>

                        <Button variant='solid' color='primary' htmlType='submit' style={{ width: '100%', marginTop: 30 }}>Login</Button>

                        <Divider style={{ color: '#888888' }}>or</Divider>

                        <Button variant='solid' color='primary' icon={<BsGoogle />} style={{ width: '100%' }} onClick={handleLoginWithGoogle}>Login With Google</Button>
                    </Flex>
                </Form>
            </Card>
        </Flex>
    )
}

export default Login