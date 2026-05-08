import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface authState {
    model_api_key: string;
    model_name: string;
    setApiKey:(model_api_key: string) => void
    setModelName:(model_name: string) => void
}


export const useAuthStore = create<authState>()(
     persist(
        (set)=>({
            model_api_key:'',
            model_name:'gemini-2.5-flash',
            setApiKey: (model_api_key)=>set(()=>({model_api_key:model_api_key})),
            setModelName:(model_name)=> set(()=>({model_name:model_name}))
        }),
        {name:'auth-storage'}


     ),
)



interface ChatMessage {
  text: string;
  role: "ai" | "user";
}

interface ChatStore {
  chats: ChatMessage[];
  _hasHydrated: boolean;
  setHasHydrated: (val: boolean) => void;
  addChat: (message: ChatMessage) => void;
  initialChat: (message: ChatMessage) => void;
  clearChats: () => void;
}

export const useChatResponse = create<ChatStore>()(
  persist(
    (set) => ({
      chats: [],
      _hasHydrated: false,

      setHasHydrated: (val) => set({ _hasHydrated: val }),
      addChat: (message) =>
        set((state) => {
          const last = state.chats[state.chats.length - 1];
          if (last?.text === message.text && last?.role === message.role) {
            return state; // same reference = no re-render
          }
          return { chats: [...state.chats, message] };
        }),

      initialChat: (message) =>
        set((state) => {
          if (
            state.chats.length === 1 &&
            state.chats[0].text === message.text &&
            state.chats[0].role === message.role
          ) {
            return state;
          }
          return { chats: [message] };
        }),

      clearChats: () =>
        set((state) => {
          if (state.chats.length === 0) return state;
          return { chats: [] };
        }),
    }),
    {
      name: "chat-response",
      partialize: (state) => ({ chats: state.chats }), 
      onRehydrateStorage: () => (state) => {
        state?.setHasHydrated(true); 
      },
    }
  )
);