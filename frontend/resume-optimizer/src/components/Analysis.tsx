import { Plus } from 'lucide-react';

type Breakdown = {
  keywords: number
  skills: number
  experience: number
  format: number
  impact: number
}

type AtsScoreProps = {
  score: number
  breakdown: Breakdown
}

export const AtsScore = ({ score, breakdown }: AtsScoreProps) => {
  return (
    <div className="bg-white border border-gray-100 shadow rounded-xl p-4 space-y-4">

      {/* Main Score */}
      <div>
        <div className="flex justify-between">
          <span className="font-medium">Job Match Score</span>
          <span className="font-bold">{score}%</span>
        </div>

        <div className="h-2 bg-gray-200 rounded mt-2">
          <div
            className="h-2 bg-black rounded"
            style={{ width: `${score}%` }}
          />
        </div>
      </div>

      {/* Breakdown */}
      <div className="text-sm space-y-1">
        <div className="flex justify-between"><span>Keywords</span><span>{breakdown.keywords}%</span></div>
        <div className="flex justify-between"><span>Skills</span><span>{breakdown.skills}%</span></div>
        <div className="flex justify-between"><span>Experience</span><span>{breakdown.experience}%</span></div>
        <div className="flex justify-between"><span>Format</span><span>{breakdown.format}%</span></div>
        <div className="flex justify-between"><span>Impact</span><span>{breakdown.impact}%</span></div>
      </div>

    </div>
  )
}




type SkillsAnalysisProps = {
  present: string[]
  missing: string[]
}

export const SkillsAnalysis = ({ present, missing }: SkillsAnalysisProps) => {
  return (
    <div className="bg-white border rounded-xl p-4 space-y-3">
      <h3 className="font-semibold">Skills Analysis</h3>

      <div className="space-y-2">
        <p className="text-xs text-gray-500">Present</p>
        <div className="flex flex-wrap gap-2">
          {present.map((s) => (
            <span key={s} className="bg-green-50 text-green-600 px-2 py-1 text-xs rounded">
              {s}
            </span>
          ))}
        </div>
      </div>

      <div className="space-y-2">
        <p className="text-xs text-gray-500">Missing</p>
        <div className="flex flex-wrap gap-2">
          {missing.map((s) => (
            <span key={s} className="bg-red-50 text-red-600 px-2 py-1 text-xs 
            rounded flex items-center justify-center gap-2 cursor-pointer">
              {s}  <Plus size={15}/>
            </span>
          ))}
        </div>
      </div>
    </div>
  )
}


