import { useState,useRef } from "react";
import { ToastContainer,toast} from 'react-toastify';
import { useAuthStore } from "./hooks/store";

import HeaderSection from "./components/Header/HeaderSection";
import { Upload, Brain, SendHorizontal} from "lucide-react";
import {AtsScore,SkillsAnalysis
} from "./components/Analysis";
import { CoverLetter,ResumeContainer } from "./components/ResumeContainer";
import {  Recorder } from "./components/Recorder/Recorder";
import { optimizeResumeData,chatAgent } from "./lib/api/optimize_resume.api";




export default function App() {
  const [noTtakeAction,setNotTakeAction] = useState(true)
  const [optimizing,setIsOptimizing] = useState(false)
  const [resume, setResume] = useState('');
  const [coverLetterText, setCoverLetterText] = useState('');
  const [jD, setJd] = useState('');


  const initial_atsScore = {
  job_matching_score:0,
  keyword:0,
  skills:0,
  experience:0,
  impact:0
  }
  const [atsScore, setSAtscore] = useState(initial_atsScore);
  
  const [insightSummary,SetInsightSummary] = useState('')

  const [chat, setChat] = useState([
    { role: "ai", text: "Ask me to improve your resume" },
  ]);
  const [input, setInput] = useState("");

  
  
  

  const [resumeFile,SetResumeFile] = useState<File | null>()

  const resumeFileRef = useRef<HTMLInputElement | null>(null)
  // const [openTemplate,setOpenTemplate] = useState(false)

  const handleFileClick = () => {
  
  }

  const SendHorizontalMessage =  async () => {
    if (!input) return;
    const data = await chatAgent({
      coverLetter:coverLetterText,
      optimized_resume:resume,
      job_description:jD,
      user_query:input,
      model_api_key:model_api_key,
      model_name:model_name,
    })
    if(data){
      if (data?.type ==="resume"){
        setResume(data.resume)
        setSAtscore(data.ats_score)
        SetInsightSummary(data.insight_summary)
      }
      if (data?.type === "coverLetter"){
       setCoverLetterText(data.coverLetter)
      }
       if (data?.type === "unknown"){
       setCoverLetterText(data.coverLetter)
      }
     
      
     
     }
  };

  const {model_api_key, model_name} = useAuthStore()

  const optimizeResume = async () => {

    if (!resumeFile)return;
    if(!jD) return;
    setIsOptimizing(true)
     const data = await optimizeResumeData({
      resume:resumeFile,
      model_api_key:model_api_key,
      model_name:model_name,
      job_description:jD
     })
     
     if(data){
      setResume(data.optimizeResume)
      setCoverLetterText(data.coverLetter)
      setSAtscore(data.ats_score)
      SetInsightSummary(data.insight_summary)

      // take action like document, or chat with assistant
      setNotTakeAction(false)

      
     }
     setIsOptimizing(false)
    

   
  };

  return (
    <section className="h-auto w-full bg-gray-100 relative'
    ">

      <HeaderSection />

      <ToastContainer />

      {/* Resume template */}

      

      {/* Resume Template */}
  

      <div className="flex gap-4 p-4 flex-col md:flex-row">

        {/* LEFT */}
        <div className="h-[78rem] flex-1 flex flex-col gap-4">

         {/* resumes before and after */}
         <ResumeContainer resume={resume} takeAction={noTtakeAction}/>

         {/* resumes before and after */}

          {/* UPLOAD + JD */}
          <div className="bg-white rounded-lg border p-4 grid grid-cols-2 gap-4 border-gray-50 shadow-xl">
           <input type="file" accept=".pdf, .doc, .docx" 
           className="hidden cursor-pointer" ref={resumeFileRef}
           onChange={(e)=>{SetResumeFile(e.target.files?.[0])}}
           />

            <div className="border border-dashed rounded-lg flex flex-col items-center justify-center p-6 text-gray-500 text-sm gap-4" 
            onClick={()=>{resumeFileRef.current?.click()}}>

              <div className="flex flex-col items-center gap-2">
                <Upload size={18}/>
                <span>Upload Resume</span>
              </div>
             
               <div className=" font-semibold">
                 <p>{resumeFile?.name}</p>
              </div>
            </div>

            <div className="flex flex-col gap-2">
              <textarea
                className="border rounded-lg p-3 text-sm resize-none flex-1"
                placeholder="Paste Job Description..." value={jD}
                onChange={(e)=>{setJd(e.target.value)}}
              />

              <button disabled={optimizing}
                onClick={optimizeResume}
               
                className={`text-xs px-3 py-2 border rounded text-white  ${optimizing ? "bg-gray-500 cursor-not-allowed": "bg-gray-400 hover:bg-gray-500 cursor-pointer"}`}
              >
                {optimizing ? "optimizing resume...":"Optimize Resume"}
               
              </button>
            </div>
          </div>
        </div>

        {/* RIGHT */}
        <div className="w-full md:w-[32%] flex flex-col gap-4">

          {/* AtsScore */}
          <AtsScore score={atsScore.job_matching_score} 
          breakdown={{keywords: atsScore.keyword,skills:atsScore.skills, 
            experience:atsScore.experience,impact:atsScore.impact,
                }}/>

    
      <SkillsAnalysis insight_summary={insightSummary}/>

     

    


          {/* AtsScore */}
         

         {/* chat container */}
          <div className="h-80 bg-white border-gray-50 shadow-xl rounded-lg flex flex-col">

            <div className="p-2 border-b text-sm flex items-start justify-start gap-2">
              <Brain />
              <p> Coach Assistant</p>
            </div>

            <div className="flex-1 overflow-y-auto p-3 space-y-2 custom-scrollbar">
              {chat.map((msg, i) => (
                <div
                  key={i}
                  className={`text-sm p-2 rounded max-w-[80%] ${
                    msg.role === "user"
                      ? "bg-black text-white ml-auto"
                      : "bg-gray-100"
                  }`}
                >
                  {msg.text}
                </div>
              ))}
            </div>

            <div className="p-2 flex gap-2 border-t">
              <input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                className="flex-1 outline-0 rounded-xl px-2 py-1 text-sm shadow-2xl"
                placeholder="Chat with your resume"
              />
              <Recorder/>
              <button disabled={noTtakeAction}
                onClick={SendHorizontalMessage}
                className={`text-xs px-3 py-2 border rounded-xl text-white ${noTtakeAction ? "bg-gray-500 cursor-not-allowed": "bg-gray-400 hover:bg-gray-500 cursor-pointer"}`}
              >
                <SendHorizontal size={14} />
              </button>
            </div>
          </div>
           {/* chat container */}


        {/* cover letter container */}

           <CoverLetter coverLetter={coverLetterText} takeAction={noTtakeAction}/>

        {/* cover letter */}

        </div>
      </div>
    </section>
  );
}
