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
        set((state) => ({
          chats: [...state.chats, message],
        })),

      initialChat: (message) =>
        set((state) => {
          // only set if chats is empty (fresh session)
          if (state.chats.length === 0) {
            return { chats: [message] };
          }
          return state;
        }),

      clearChats: () => set({ chats: [] }),
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



interface JDState {
    job_description: string;
    setJD:(job_description: string) => void
}


export const useJDStore = create<JDState>()(
     persist(
        (set)=>({
            job_description:'',
            setJD: (job_description)=>set(()=>({job_description:job_description})),    
        }),
        {name:'JD-store'}
     ),
)
