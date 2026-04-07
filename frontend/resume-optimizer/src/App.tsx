import React, { useState,useRef } from "react";

import HeaderSection from "./components/Header/HeaderSection";
import { Upload, Brain, SendHorizontal} from "lucide-react";
import { sampleResume } from "./components/samples";
import {AtsScore,SkillsAnalysis
} from "./components/Analysis";
import { CoverLetter,ResumeContainer } from "./components/ResumeContainer";
import ResumeVersion from "./components/ResumeVersion";
import {  Recorder } from "./components/Recorder/Recorder";
import { SettingsModals } from "./components/modals";



export default function App() {
  const [resume, setResume] = useState(sampleResume);
  const [coverLetterText, setCoverLetterText] = useState(
    "# Cover Letter\nYour generated cover letter appears here..."
  );
  
  const [skillsAnalysis,SetskillsAnalysis] = useState(
    {present:["Python", "FastAPI", "SQL"],missing:["Docker", "AWS", "Kubernetes"]})

  const [chat, setChat] = useState([
    { role: "ai", text: "Ask me to improve your resume" },
  ]);
  const [input, setInput] = useState("");
  const [score, setScore] = useState(72);
   const [jD, setJd] = useState('');
  const [versions, setVersions] = useState(["Initial version"]);

  const [resumeFile,SetResumeFile] = useState<File | null>()

  const resumeFileRef = useRef<HTMLInputElement | null>(null)

  const handleFileClick = () => {
  
  }

  const SendHorizontalMessage = () => {
    if (!input) return;

  };

  const optimizeResume = () => {
   
  };

  return (
    <section className="h-auto w-full bg-gray-100">
      <HeaderSection />
  

      <div className="flex gap-4 p-4 flex-col md:flex-row">

        {/* LEFT */}
        <div className="h-[80rem] flex-1 flex flex-col gap-4">

         {/* resumes before and after */}
         <ResumeContainer resumeBefore={resume} resumeAfter={resume}/>

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

              <button
                onClick={optimizeResume}
                className="text-xs px-3 py-2 border rounded hover:bg-gray-400 bg-gray-500 text-white"
              >
                Optimize Resume
              </button>
            </div>
          </div>
        </div>

        {/* RIGHT */}
        <div className="w-full md:w-[32%] flex flex-col gap-4">

          {/* AtsScore */}
          <AtsScore score={score} 
          breakdown={{keywords: 
            78,skills: 80, experience: 85,format: 90,impact: 75,
                }}/>

    
      <SkillsAnalysis present={skillsAnalysis?.present} missing={skillsAnalysis?.missing}
      />

     

    


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
              <button
                onClick={SendHorizontalMessage}
                className="text-xs px-3 py-2 border rounded-xl hover:bg-gray-400 bg-gray-500 text-white"
              >
                <SendHorizontal size={14} />
              </button>
            </div>
          </div>
           {/* chat container */}


        {/* cover letter container */}

           <CoverLetter coverLetter={coverLetterText}/>

        {/* cover letter */}



        {/* resume version */}

        <ResumeVersion resumeVersions={versions}/>

        {/* resume version */}

        </div>
      </div>
    </section>
  );
}
