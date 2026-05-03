import ReactMarkdown from 'react-markdown'

type Breakdown = {
  keywords: number
  skills: number
  experience: number
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
        <div className="flex justify-between"><span>Impact</span><span>{breakdown.impact}%</span></div>
      </div>

    </div>
  )
}




type InsightSummary = {
  insight_summary:string
}

export const SkillsAnalysis = ({ insight_summary}: InsightSummary) => {
  return (
    <div className="bg-white border rounded-xl p-4 space-y-3">
      <h3 className="font-semibold">Insight Summary</h3>

      <div className="text-base h-80 flex-1 overflow-y-auto p-4 prose prose-sm custom-scrollbar">
        <ReactMarkdown>{insight_summary}</ReactMarkdown>
      </div>

      
    </div>
  )
}


