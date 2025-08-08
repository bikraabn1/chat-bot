import React from 'react'
import { Form, Input, Button } from 'antd'
import { IoSend } from 'react-icons/io5'

const InputChat = ({onChangeInput, onSubmit, messageValue}) => {
    return (
        <div>
            <Form layout='inline' style={{ width: '100%', display: 'flex' }} onFinish={onSubmit}>
                <Form.Item style={{ flex: 1 }}>
                    <Input onChange={onChangeInput} value={messageValue}/>
                </Form.Item>
                <Form.Item>
                    <Button style={{ background: '#001529', color: "#ffffff", cursor:'pointer' }} htmlType='submit'><IoSend /></Button>
                </Form.Item>
            </Form>
        </div>
    )
}

export default InputChat