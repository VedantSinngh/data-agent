"use client"

import { useState } from 'react'

export default function Dashboard() {
  const [loading, setLoading] = useState(false)
  const [report, setReport] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)

  const handleInvestigate = async () => {
    setLoading(true)
    setError(null)
    try {
      // In a real app, the dataset_id would be dynamic based on the uploaded file.
      // For this MVP, we use our mocked "sales_defects" dataset ID.
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'
      
      const response = await fetch(`${apiUrl}/datasets/sales_defects/investigate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          dataset_id: "sales_defects",
          question: "Investigate the quality of this dataset, identify the most important problems, explain their business impact, and recommend how I should fix them."
        })
      })

      if (!response.ok) throw new Error('Failed to fetch report from API')
      
      const data = await response.json()
      setReport(data)
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex flex-col gap-12">
      <header className="max-w-3xl space-y-4">
        <h1 className="text-5xl md:text-7xl font-sans tracking-tighter-2 text-ink">Data quality, <br className="hidden md:block"/> grounded in evidence.</h1>
        <p className="text-lg text-body font-sans leading-relaxed">
          Upload your sales dataset. DataTrust automatically profiles the schema, detects duplicates and nulls, and uses retrieval-augmented generation against your policies to propose safe corrections.
        </p>
        <div className="pt-4 flex gap-4">
          <button className="btn-primary" onClick={handleInvestigate} disabled={loading}>
            {loading ? 'Analyzing Dataset...' : 'Run Investigation (Demo)'}
          </button>
        </div>
        {error && <p className="text-red-400 text-sm">{error}</p>}
      </header>
      
      {/* Show dynamic report if it exists, otherwise show empty state/placeholder */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-12 border-t border-hairline">
        
        {report ? (
          report.findings.map((finding: any, idx: number) => (
            <div key={idx} className="card space-y-4">
              <div className="label-mono flex justify-between">
                <span>{finding.finding_id}</span>
                <span className={finding.severity === 'high' ? 'text-red-400' : 'text-orange-400'}>
                  {finding.severity.toUpperCase()}
                </span>
              </div>
              <h3 className="text-2xl text-ink tracking-tight-1">{finding.explanation.split('.')[0]}</h3>
              <p className="text-sm text-body-mid leading-relaxed">
                {finding.business_impact}
              </p>
              <div className="pt-4 space-y-2">
                <p className="text-xs text-body uppercase tracking-widest">Recommended Action:</p>
                <p className="text-sm text-ink">{finding.recommended_action}</p>
              </div>
            </div>
          ))
        ) : (
          <div className="col-span-1 md:col-span-2 text-center py-12 border border-hairline border-dashed rounded-lg">
            <p className="text-body-mid">Click "Run Investigation" to analyze the sample dataset against the Hugging Face API.</p>
          </div>
        )}

      </div>
    </div>
  )
}
