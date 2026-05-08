import React from 'react'
import ReactMarkdown from 'react-markdown'
import TemplateContainer from './Template/Container'
import { useRef, useState } from "react";
import { Copy, Check } from "lucide-react";
import { useReactToPrint } from "react-to-print";


type ResumeContainerProps = {
    resume?:string
    takeAction:boolean
}

type CoverLetterProps = {
    coverLetter?:string
    takeAction:boolean
}

export const ResumeContainer: React.FC<ResumeContainerProps> = ({ resume, takeAction }) => {
  const [openTemplate, setOpenTemplate] = useState(false);
  const resumeRef = useRef<HTMLDivElement>(null);

  const handleDownload = useReactToPrint({
    contentRef: resumeRef,
    documentTitle: "resume",
    pageStyle: `
      @page {
        size: A4;
        margin: 20mm;
      }

      @media print {
        body {
          font-family: Georgia, serif;
          font-size: 12px;
          line-height: 1.6;
          color: #111;
          -webkit-print-color-adjust: exact;
          print-color-adjust: exact;
        }

        h1 { font-size: 24px; font-weight: bold; margin-bottom: 8px; }
        h2 { font-size: 20px; font-weight: bold; margin-bottom: 6px; }
        h3 { font-size: 16px; font-weight: bold; margin-bottom: 4px; }

        p  { margin-bottom: 8px; }

        ul, ol { padding-left: 20px; margin-bottom: 8px; }
        li { margin-bottom: 4px; }

        strong { font-weight: bold; }
        em     { font-style: italic; }

        hr { border: none; border-top: 1px solid #ccc; margin: 12px 0; }

        h1, h2, h3 { page-break-after: avoid; }
        p, li      { page-break-inside: avoid; }
      }
    `,
  });

  return (
    <>
      <TemplateContainer isOpen={openTemplate} />
      <div className="flex-1 bg-white rounded-lg border border-gray-50 shadow-xl flex flex-col overflow-hidden relative">
        <div className="flex justify-end gap-2 p-1 border-b bg-gray-50">
          <button
            disabled={takeAction || !resume}
            onClick={() => handleDownload()}
            className={`text-xs px-3 py-2 border rounded text-white
              ${
                takeAction || !resume
                  ? "bg-gray-500 cursor-not-allowed"
                  : "bg-gray-400 hover:bg-gray-500 cursor-pointer"
              }`}
          >
            Download Resume
          </button>
        </div>

        <div className="flex flex-1 overflow-hidden">
          {/* ✅ ReactMarkdown renders markdown → HTML, react-to-print prints the HTML */}
          <div
            ref={resumeRef}
            className="w-full p-6 overflow-y-auto prose prose-sm custom-scrollbar"
          >
            <ReactMarkdown>{resume}</ReactMarkdown>
          </div>
        </div>
      </div>
    </>
  );
};


export const CoverLetter: React.FC<CoverLetterProps> = ({ coverLetter, takeAction }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    if (!coverLetter) return;

    const plain = coverLetter
      .replace(/#{1,6}\s+/g, "")
      .replace(/\*\*(.*?)\*\*/g, "$1")
      .replace(/\*(.*?)\*/g, "$1")
      .replace(/~~(.*?)~~/g, "$1")
      .replace(/`(.*?)`/g, "$1")
      .replace(/\[(.*?)\]\(.*?\)/g, "$1")
      .replace(/^[-*+]\s+/gm, "")
      .replace(/^\d+\.\s+/gm, "")
      .replace(/^>\s+/gm, "")
      .replace(/\n{2,}/g, "\n\n")
      .trim();

    await navigator.clipboard.writeText(plain);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="h-80 bg-white border-gray-50 shadow-xl rounded-lg flex flex-col">
      <div className="p-2 border-b text-sm w-full flex items-start justify-between">
        <p className="p-2">Cover Letter</p>

        <button
          onClick={handleCopy}
          disabled={takeAction || !coverLetter}
          className={`text-xs px-3 py-2 transition-colors ${
            takeAction
              ? "cursor-not-allowed text-gray-300"
              : "cursor-pointer text-gray-400 hover:text-gray-600"
          }`}
        >
          {copied ? <Check size={20} className="text-green-500" /> : <Copy size={20} />}
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-4 prose prose-sm custom-scrollbar">
        <ReactMarkdown>{coverLetter}</ReactMarkdown>
      </div>
    </div>
  );
};