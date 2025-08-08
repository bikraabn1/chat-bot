import { create } from 'zustand'

export const useChatStore = create((set) => ({
    order: 0,
    chats: [],
    
    setChat: (newChat) => set((state) => ({
        chats: [
            ...state.chats,
            { ...newChat, order: state.order++ }
        ]
    })),
    updateChat: (id, updater) => set((state) => ({
        chats: state.chats.map(chat =>
            chat.id === id
                ? updater(chat)
                : chat
        )
    }))
}))
