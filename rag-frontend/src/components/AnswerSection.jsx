function AnswerSection({ result }) {
  if (!result) {
    return (
      <div className="card empty-answer">
        <h2>Answer</h2>
        <p className="muted">
          Ask a question to generate a grounded answer with citations.
        </p>
      </div>
    );
  }

  if (result.error) {
    return (
      <div className="card error-card">
        <h2>Answer</h2>
        <p>{result.error}</p>
      </div>
    );
  }

  return (
    <div className="card answer-card">
      <div className="card-header">
        <div>
          <h2>Answer</h2>
          <p>Generated using retrieved document context.</p>
        </div>
      </div>

      {result.rewritten_question && (
        <div className="mini-card">
          <h3>Rewritten Question</h3>
          <p>{result.rewritten_question}</p>
        </div>
      )}

      <div className="mini-card">
        <h3>Cited Answer</h3>
        <pre className="answer-text">{result.cited_answer || result.answer}</pre>
      </div>

      <div className="mini-card">
        <h3>Sources</h3>

        {result.sources?.length > 0 ? (
          <div className="source-list">
            {result.sources.map((src, index) => (
              <div className="source-item" key={index}>
                <span className="source-badge">{src.label || `S${index + 1}`}</span>
                <span>{src.source}</span>
                <span className="chunk-badge">Chunk {src.chunk_index}</span>
              </div>
            ))}
          </div>
        ) : (
          <p className="muted">No sources returned.</p>
        )}
      </div>
    </div>
  );
}

export default AnswerSection;