import { useState, useEffect } from 'react'
import useWebsocket, { ReadyState } from 'react-use-websocket'
import { useChatStore } from '../store/use-chat-store'

export const useChatSocket = () => {
    const { setChat, updateChat } = useChatStore()
    const socketURL = import.meta.env.VITE_WS_URL
    const [currentMessageId, setCurrentMessageId] = useState(null)
    const { sendMessage, lastMessage, readyState } = useWebsocket(socketURL)

    useEffect(() => {
        if (lastMessage !== null) {
            const data = JSON.parse(lastMessage.data)

            if (data.type === "content") {
                if(!currentMessageId){
                    const newId = self.crypto.randomUUID()
                    setCurrentMessageId(newId)
                    setChat({
                        id: newId,
                        text: data.data,
                        isMine: false
                    })
                }else{
                    updateChat(currentMessageId, (prev) => ({
                        ...prev,
                        text: prev.text + data.data
                    }))
                }
            }

            if (data.type === "end") {
                if(currentMessageId){
                    setCurrentMessageId(null)
                }
            }
            return
        }
    }, [lastMessage])

    const connectionStatus = {
        [ReadyState.CONNECTING]: 'Connecting',
        [ReadyState.OPEN]: 'Open',
        [ReadyState.CLOSING]: 'Closing',
        [ReadyState.CLOSED]: 'Closed',
        [ReadyState.UNINSTANTIATED]: 'Uninstantiated',
    }[readyState]

    return { sendMessage, lastMessage, readyState, connectionStatus }
}
