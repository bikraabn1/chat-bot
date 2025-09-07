import React, { useCallback, useState } from 'react'
import ChatCanvas from '../../components/chat-page/ChatCanvas'
import InputChat from '../../components/chat-page/InputChat'
import { Flex } from 'antd'
import { useChatSocket } from '../../hooks/use-chat-sockets'
import { useChatStore } from '../../store/use-chat-store'

const ChatPage = () => {
    const [message, setMessage] = useState('')
    const { sendMessage, connectionStatus } = useChatSocket()
    const { chats } = useChatStore()

    const handleSubmit = () => {
        if (!message.trim()) return 
        
        sendMessage(message)
        setMessage('')
    }

    const onChangeInput = useCallback((e) => {
        setMessage(e.target.value)
    }, [])

    const handleKeyPress = useCallback((e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault()
            handleSubmit()
        }
    }, [handleSubmit])

    return (
        <div style={{ height: "100%" }}>
            <Flex
                vertical={true}
                style={{ height: "100%" }}
            >
                
                <ChatCanvas history={chats}/>
                <InputChat 
                    onChangeInput={onChangeInput} 
                    onSubmit={handleSubmit}
                    onKeyPress={handleKeyPress}
                    messageValue={message}
                    disabled={connectionStatus === 'Closed'}
                />
            </Flex>
        </div>
    )
}

export default ChatPage