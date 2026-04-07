

type ResumeVersionProps = {
    resumeVersions?:string[]
}

const ResumeVersion = ({resumeVersions}: ResumeVersionProps) => {
  return (
    <div className="h-48 bg-white border-gray-50 shadow-xl rounded-lg p-3 flex flex-col">
            <div className="text-sm mb-2">Versions</div>
            <div className="flex-1 overflow-y-auto text-xs space-y-1 custom-scrollbar">
              {resumeVersions?.map((v, i) => (
                <div key={i}>{v}</div>
              ))}
            </div>
          </div>
  )
}

export default ResumeVersion