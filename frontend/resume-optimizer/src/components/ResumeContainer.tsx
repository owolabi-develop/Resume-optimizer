import React from 'react'
import ReactMarkdown from 'react-markdown'
import TemplateContainer from './Template/Container'
import { useState } from 'react'

type ResumeContainerProps = {
    resume?:string
    takeAction:boolean
}

type CoverLetterProps = {
    coverLetter?:string
    takeAction:boolean
}

export const ResumeContainer:React.FC<ResumeContainerProps> = ({resume,takeAction}) => {

  const [openTemplate,setOpenTemplate] = useState(false)

  return (
    <>
    <TemplateContainer isOpen={openTemplate}/>
          <div className="flex-1 bg-white rounded-lg border border-gray-50 shadow-xl flex flex-col overflow-hidden relative">
             {/* EDITOR + PREVIEW */}
            <div className="flex justify-end gap-2 p-1 border-b bg-gray-50">
              <button disabled={takeAction} onClick={()=>setOpenTemplate(prev => !prev)}
              className={`text-xs px-3 py-2 border rounded text-white  
                ${takeAction ? "bg-gray-500 cursor-not-allowed": "bg-gray-400 hover:bg-gray-500 cursor-pointer"} `}
              >
                Download Resume
              </button>
            </div>

            <div className="flex flex-1 overflow-hidden">

              <div className="w-full p-6 overflow-y-auto prose prose-sm custom-scrollbar">
                <ReactMarkdown >{resume}</ReactMarkdown>
              </div>
            </div>
          </div>
          </>
  )
}


export const CoverLetter:React.FC<CoverLetterProps> = ({coverLetter,takeAction}) => {
  return (
      <div className="h-80 bg-white border-gray-50 shadow-xl rounded-lg flex flex-col">
            <div className="p-2 border-b text-sm w-full flex items-start justify-between">
              <p className="p-2">Cover Letter</p>

              <button disabled={takeAction}
                className={`text-xs px-3 py-2 border rounded text-white  ${takeAction ? "bg-gray-500 cursor-not-allowed": "bg-gray-400 hover:bg-gray-500 cursor-pointer"}`}
              >
                Download Cover Letter
              </button>
            </div>

            <div className="flex-1 overflow-y-auto p-4 prose prose-sm custom-scrollbar">
              <ReactMarkdown>{coverLetter}</ReactMarkdown>
            </div>
          </div>
  )
}
