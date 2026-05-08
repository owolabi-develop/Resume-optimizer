import { toast } from 'react-toastify';
interface ResumeProps {
    resume:File;
    model_api_key: string;
    model_name:string;
    job_description:string;
}


export async function optimizeResumeData({resume,model_api_key,model_name,job_description}: ResumeProps){
    try{
    const formdata = new FormData()
    formdata.append("resume",resume)
    formdata.append("model_api_key",model_api_key)
    formdata.append("model_name",model_name)
    formdata.append("job_description",job_description)
    const response  = await fetch("http://127.0.0.1:8000/resume/optimize/api/",{
        method:"POST",
        body:formdata,
        headers: {
          accept: "application/json",
        },
    })
    if(!response.ok){
         const errorData = await response.json();
        toast(errorData.detail)
      
         return null


    }
    const data = await response.json();
    return data
} catch (error){
    console.error(error)
}
}

interface ChatAgentProps {
    coverLetter: string;
    optimized_resume: string;
    job_description:string;
    user_query: string;
    model_name: string;
    model_api_key: string;
}

export async function chatAgent({coverLetter,optimized_resume,job_description,user_query,model_name,model_api_key}: ChatAgentProps){
            try{
                // const formdata = new FormData()
                const docData = {
                    coverLetter:coverLetter,
                    optimized_resume: optimized_resume,
                    job_description:job_description,
                    user_query:user_query,
                    model_name: model_name,
                    model_api_key:model_api_key
                }
               const response  = await fetch("http://127.0.0.1:8000/resume/chat/agent/",{
                    method:"POST",
                    body:JSON.stringify(docData),
                    headers: {'Content-Type': 'application/json'}
                })
                if(!response.ok){
                const errorData = await response.json();
                toast(errorData.detail)

                return null


                }
                const data = await response.json();
                return data



                }catch (error){
                    console.error(error)
                }
    }
        