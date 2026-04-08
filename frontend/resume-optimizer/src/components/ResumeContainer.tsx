import React from 'react'
import ReactMarkdown from 'react-markdown'
import TemplateContainer from './Template/Container'
import { useState } from 'react'

type ResumeContainerProps = {
    resumeBefore?:string
    resumeAfter?:string
}

type CoverLetterProps = {
    coverLetter?:string
}

export const ResumeContainer:React.FC<ResumeContainerProps> = ({resumeBefore,resumeAfter}) => {

  const [openTemplate,setOpenTemplate] = useState(false)

  return (
    <>
    <TemplateContainer isOpen={openTemplate}/>
          <div className="flex-1 bg-white rounded-lg border border-gray-50 shadow-xl flex flex-col overflow-hidden relative">
             {/* EDITOR + PREVIEW */}
            <div className="flex justify-end gap-2 p-1 border-b bg-gray-50">
              <button  onClick={()=>setOpenTemplate(prev => !prev)}
              className="text-xs px-3 py-2 border rounded
               hover:bg-gray-400 bg-gray-500 text-white"
              >
                Download Resume
              </button>
            </div>

            <div className="p-3 text-gray-500 w-full flex items-start justify-between font-semibold">
              <p>Before</p>
              <p>After</p>
            </div>

            <div className="flex flex-1 overflow-hidden">

              <div className="w-1/2 p-6 overflow-y-auto prose prose-sm custom-scrollbar">
                <ReactMarkdown>{resumeBefore}</ReactMarkdown>
              </div>

              <div className="w-1/2 p-6 overflow-y-auto prose prose-sm custom-scrollbar">
                <ReactMarkdown>{resumeAfter}</ReactMarkdown>
              </div>
            </div>
          </div>
          </>
  )
}


export const CoverLetter:React.FC<CoverLetterProps> = ({coverLetter}) => {
  return (
      <div className="h-80 bg-white border-gray-50 shadow-xl rounded-lg flex flex-col">
            <div className="p-2 border-b text-sm w-full flex items-start justify-between">
              <p className="p-2">Cover Letter</p>

              <button
                className="text-xs px-3 py-2 border rounded hover:bg-gray-400 bg-gray-500 text-white"
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
