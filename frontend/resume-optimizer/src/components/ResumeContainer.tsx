import React from 'react'
import ReactMarkdown from 'react-markdown'
type ResumeContainerProps = {
    resume?:string
}

type CoverLetterProps = {
    coverLetter?:string
}

export const ResumeContainer:React.FC<ResumeContainerProps> = ({resume}) => {
  return (
    <div className='max-h-96  overflow-y-auto p-2 custom-scrollbar border-b border-b-mauve-950 '> 
    <ReactMarkdown>{resume}</ReactMarkdown>
    </div>
  )
}


export const CoverLetter:React.FC<CoverLetterProps> = ({coverLetter}) => {
  return (
    <div className='max-h-96 border-b border-b-mauve-950 overflow-y-auto p-2 custom-scrollbar'> <ReactMarkdown>{coverLetter}</ReactMarkdown></div>
  )
}
