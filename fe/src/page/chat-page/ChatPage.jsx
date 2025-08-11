import React, { useCallback, useState } from 'react'
import { Flex } from 'antd'
import ChatCanvas from '../../components/chat-page/ChatCanvas'
import InputChat from '../../components/chat-page/InputChat'
import { useChatSocket } from '../../hooks/use-chat-sockets'
import { useChatStore } from '../../store/use-chat-store'

const ChatPage = () => {
    const [message, setMessage] = useState('')
    const { sendMessage } = useChatSocket()
    const { chats, setChat } = useChatStore()

    const handleSubmit = () => {
        sendMessage(message)
        setChat({
            id: self.crypto.randomUUID(),
            text: message,
            isMine: true
        })
        setMessage('')
    }

    const onChangeInput = useCallback((e) => {
        setMessage(e.target.value)
    },[])

    return (
        <div style={{ height: "100%" }}>
            <Flex
                vertical={true}
                style={{ height: "100%" }}
            >
                <ChatCanvas history={chats}/>
                <InputChat onChangeInput={onChangeInput} onSubmit={handleSubmit} messageValue={message}/>
            </Flex>
        </div>
    )
}

export default ChatPage