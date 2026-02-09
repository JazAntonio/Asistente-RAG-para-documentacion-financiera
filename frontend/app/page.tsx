'use client'

import { useState } from 'react'

interface QueryResponse {
    answer: string
    sources: Array<{
        content: string
        metadata: {
            document_id: string
            title?: string
        }
    }>
    error?: string
}

export default function Home() {
    const [query, setQuery] = useState('')
    const [response, setResponse] = useState<QueryResponse | null>(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()

        if (!query.trim()) {
            setError('Por favor ingresa una pregunta')
            return
        }

        setLoading(true)
        setError(null)
        setResponse(null)

        try {
            const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080'
            console.log('Using API URL:', apiUrl) // Debug log
            const res = await fetch(`${apiUrl}/api/query`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query }),
            })

            if (!res.ok) {
                throw new Error(`Error: ${res.status} ${res.statusText}`)
            }

            const data = await res.json()
            setResponse(data)
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Error al procesar la consulta')
        } finally {
            setLoading(false)
        }
    }

    return (
        <main className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 p-8">
            <div className="max-w-4xl mx-auto">
                {/* Header */}
                <div className="text-center mb-12">
                    <h1 className="text-5xl font-bold text-white mb-4">
                        Asistente Financiero RAG
                    </h1>
                    <p className="text-blue-200 text-lg">
                        Consulta documentación financiera con inteligencia artificial
                    </p>
                </div>

                {/* Query Form */}
                <div className="bg-white/10 backdrop-blur-lg rounded-2xl shadow-2xl p-8 mb-8 border border-white/20">
                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div>
                            <label htmlFor="query" className="block text-white font-medium mb-2">
                                Tu pregunta
                            </label>
                            <textarea
                                id="query"
                                value={query}
                                onChange={(e) => setQuery(e.target.value)}
                                placeholder="Ejemplo: ¿Cuáles son los requisitos de capital para instituciones financieras?"
                                className="w-full px-4 py-3 rounded-lg bg-white/90 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 min-h-[120px] resize-y"
                                disabled={loading}
                            />
                        </div>
                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-xl"
                        >
                            {loading ? (
                                <span className="flex items-center justify-center">
                                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                    </svg>
                                    Procesando...
                                </span>
                            ) : (
                                'Consultar'
                            )}
                        </button>
                    </form>
                </div>

                {/* Error Display */}
                {error && (
                    <div className="bg-red-500/20 backdrop-blur-lg border border-red-500/50 rounded-lg p-4 mb-8">
                        <p className="text-red-200 font-medium">⚠️ {error}</p>
                    </div>
                )}

                {/* Response Display */}
                {response && (
                    <div className="bg-white/10 backdrop-blur-lg rounded-2xl shadow-2xl p-8 border border-white/20">
                        <h2 className="text-2xl font-bold text-white mb-4">Respuesta</h2>
                        <div className="bg-white/90 rounded-lg p-6 mb-6">
                            <p className="text-gray-900 leading-relaxed whitespace-pre-wrap">
                                {response.answer}
                            </p>
                        </div>

                        {/* Sources */}
                        {response.sources && response.sources.length > 0 && (
                            <div>
                                <h3 className="text-xl font-semibold text-white mb-3">
                                    Fuentes consultadas ({response.sources.length})
                                </h3>
                                <div className="space-y-3">
                                    {response.sources.map((source, idx) => (
                                        <div
                                            key={idx}
                                            className="bg-white/80 rounded-lg p-4 border-l-4 border-blue-500"
                                        >
                                            <p className="text-sm text-gray-700 mb-2">
                                                {source.content.substring(0, 200)}
                                                {source.content.length > 200 ? '...' : ''}
                                            </p>
                                            {source.metadata.title && (
                                                <p className="text-xs text-gray-500 font-medium">
                                                    📄 {source.metadata.title}
                                                </p>
                                            )}
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}
                    </div>
                )}

                {/* Footer */}
                <div className="text-center mt-12">
                    <p className="text-blue-200/60 text-sm">
                        Powered by RAG • Next.js • Go • Python • Pinecone
                    </p>
                </div>
            </div>
        </main>
    )
}
