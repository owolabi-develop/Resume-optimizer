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