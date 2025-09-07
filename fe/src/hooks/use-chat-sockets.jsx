import { useState, useEffect, useRef } from 'react';
import { useChatStore } from '../store/use-chat-store';
import io from 'socket.io-client';

export const useChatSocket = () => {
    const { setChat, updateChat } = useChatStore();
    const socketURL = import.meta.env.VITE_BACKEND_URL;
    const [socket, setSocket] = useState(null);
    const currentMessageIdRef = useRef(null);

    useEffect(() => {
        const newSocket = io(socketURL);
        setSocket(newSocket);

        newSocket.on('connect', () => {
            console.log('Connected to server');
        });

        newSocket.on('disconnect', () => {
            console.log('Disconnected from server');
        });

        newSocket.on('stream_chunk', (data) => {
            console.log('Stream chunk:', data);
            
            if (!currentMessageIdRef.current) {
                const newId = self.crypto.randomUUID();
                currentMessageIdRef.current = newId;
                setChat({
                    id: newId,
                    text: data.data,
                    isMine: false,
                });
            } else {
                updateChat(currentMessageIdRef.current, (prev) => ({
                    ...prev,
                    text: prev.text + data.data,
                }));
            }
        });

        newSocket.on('stream_end', (data) => {
            console.log('Stream ended:', data);
            currentMessageIdRef.current = null;
        });

        newSocket.on('error', (error) => {
            console.error('Socket error:', error);
            currentMessageIdRef.current = null;
        });

        return () => {
            currentMessageIdRef.current = null;
            newSocket.disconnect();
        };
    }, [socketURL, setChat, updateChat]);

    const sendMessage = (message) => {
        if (socket && socket.connected) {
            currentMessageIdRef.current = null;
            
            const userMessageId = self.crypto.randomUUID();
            setChat({
                id: userMessageId,
                text: message,
                isMine: true,
            });

            socket.emit('user_prompt', { message });
        } else {
            console.error('Socket not connected');
        }
    };

    const connectionStatus = socket?.connected ? 'Open' : 'Closed';

    return { sendMessage, connectionStatus };
};