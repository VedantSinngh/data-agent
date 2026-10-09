export default function Dashboard() {
  return (
    <div className="flex flex-col gap-12">
      <header className="max-w-3xl space-y-4">
        <h1 className="text-5xl md:text-7xl font-sans tracking-tighter-2 text-ink">Data quality, <br className="hidden md:block"/> grounded in evidence.</h1>
        <p className="text-lg text-body font-sans leading-relaxed">
          Upload your sales dataset. DataTrust automatically profiles the schema, detects duplicates and nulls, and uses retrieval-augmented generation against your policies to propose safe corrections.
        </p>
        <div className="pt-4 flex gap-4">
          <button className="btn-primary">Upload Dataset</button>
          <button className="btn-outline">View Sample Report</button>
        </div>
      </header>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-12 border-t border-hairline">
        
        <div className="card space-y-4">
          <div className="label-mono flex justify-between">
            <span>Finding DQ-001</span>
            <span className="text-red-400">High</span>
          </div>
          <h3 className="text-2xl text-ink tracking-tight-1">Duplicate transactions</h3>
          <p className="text-sm text-body-mid leading-relaxed">
            Potentially inflated sales totals. Verify duplicates using the transaction ID and documented uniqueness rules. 
          </p>
          <div className="pt-2">
            <button className="btn-outline w-full text-center">Review records</button>
          </div>
        </div>

        <div className="card space-y-4">
          <div className="label-mono flex justify-between">
            <span>Finding DQ-002</span>
            <span className="text-orange-400">Medium</span>
          </div>
          <h3 className="text-2xl text-ink tracking-tight-1">Inconsistent categories</h3>
          <p className="text-sm text-body-mid leading-relaxed">
            Category variants may split reporting totals. Normalize them only when a verified mapping exists according to category rules.
          </p>
          <div className="pt-2">
            <button className="btn-outline w-full text-center">Map categories</button>
          </div>
        </div>

      </div>
    </div>
  )
}
